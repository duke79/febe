import requests

from lib.py.core.config import Config
from lib.py.core.input import parse_args
from lib.py.core.traces import print_exception_traces

from lib.py.cli.run import FireCLI


def tfire(args):
    return FireCLI().run_and_return_json(args, caller="py.test")


class Client:
    def __init__(self, host="http://localhost", port="5555"):
        self._host = host
        self._port = port

    def fire(self, *args, **kwargs):
        """Run fire commands on server"""

        with Config() as config:
            token = config["tests"]["fb_token"]
            args_str = parse_args(*args, **kwargs)

            url = "{host}:{port}/fire".format_map({
                "host": self._host,
                "port": self._port
            })
            payload = "{\n \"cmd\" : \"%s\"\n}" % args_str
            headers = {
                'content-type': "application/json",
                'cache-control': "no-cache",
                "bearer": token
            }

            response = requests.request("POST", url, data=payload, headers=headers)

            if 403 == response.status_code:
                print("Token has expired.\nGet a new token from: https://developers.facebook.com/tools/explorer")
                token = input("Enter token:")
                config["tests"]["fb_token"] = token
                print("Now try again!")

            return response.text, response.status_code

    def rest(self, *args, **kwargs):
        url = "{host}:{port}".format_map({
            "host": self._host,
            "port": self._port
        })
        payload = "{}"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
        }

        response = requests.request("POST", url, data=payload, headers=headers)
        return response.text

    def load(self, *args, workers=10, **kwargs):
        """

        :param args:
        :param workers: Number of requests to make
        :param kwargs:
        :return:
        """
        import time
        start_time = time.time()
        try:
            # https://stackoverflow.com/a/14299004/973425
            from multiprocessing.pool import ThreadPool
            from multiprocessing import cpu_count
            # https://stackoverflow.com/a/25098521/973425
            nbr_workers = cpu_count() * 2
            print("no. of workers: %s" % nbr_workers)
            pool = ThreadPool(processes=nbr_workers)

            args_list = tuple()
            args_str = parse_args(*args, **kwargs)
            for arg in str(args_str).split(" "):
                args_list += (arg,)
            # print(args_list)

            # async_result = pool.apply_async(self.fire, args=args_list)
            args_over_and_over = []
            for i in range(workers):
                args_over_and_over.append(args_list)

            # print(args_over_and_over)

            async_results = pool.starmap(self.fire, args_over_and_over)

            for async_result in async_results:
                # print(async_result)
                pass

        except Exception as e:
            print_exception_traces(e)

        end_time = time.time()
        total_time = end_time - start_time
        print("executed in %s seconds" % str(total_time))
        print("average time: %s seconds per request" % str(total_time / workers))
