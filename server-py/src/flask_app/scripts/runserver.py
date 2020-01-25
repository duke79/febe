import sys
sys.path.append("..") # Adds higher directory to python modules path.

# from waitress import serve
import logging

from gevent import pywsgi, monkey
from geventwebsocket.handler import WebSocketHandler

from ...core.config import Config
from multiprocessing import freeze_support, Process

import os

from ...flask_app.app import app

logging.basicConfig(level=logging.WARNING)  # This has to be called, for unknown reasons
logging.getLogger().setLevel(logging.NOTSET)  # INFO only works once basicConfig is set

icons_directory = os.path.dirname(__file__)
icons_directory = os.path.join(icons_directory, "app\\static\\images")
fav_icon = os.path.join(icons_directory, "favicon.ico")


def server_url():
    config = Config()
    host = config["server"]["host"]
    port = config["server"]["port"]
    # url = "http://{0}:{1}".format("localhost", "5555")
    url = "http://{0}:{1}".format("localhost", port)
    return url


def start_server():
    config = Config()
    # config.commit()

    freeze_support()

    host = config["server"]["host"]
    port = config["server"]["port"]
    url = "http://" + host + ":" + port
    port = int(port)
    debug_mode = config["debug"]
    config_home = Config()["home"]

    # system("explorer {0}".format(config_home))  # Open config home (optional)
    print("Configurations at: " + config_home)
    # webbrowser.open(url)  # Open site in default browser (optional)

    print("App running on " + url)
    # 1 bare flask
    # use_reloader | https://stackoverflow.com/a/9476701/973425
    # app.run(host, port, threaded=True, debug=debug_mode, use_reloader=False)
    # 2 waitress
    # serve(app, host=host, port=port)
    # 3 gevent
    server = pywsgi.WSGIServer((host, port), app, handler_class=WebSocketHandler)
    server.serve_forever()


if __name__ == '__main__':
    # monkey.patch_all()  # blocking calls become non-blocking calls | https://stackoverflow.com/a/14552642/973425
    config = Config()
    debug_mode = config["debug"]
    start_server()
