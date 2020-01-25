import redis
from flask import current_app
from lib.py.core.config import Config
# from lib.py.core.singleton import Singleton
from lib.py.core.traces import println


class RedisSession:
    """
    Maybe it's better to create a new connection every time?
    # metaclass=Singleton
    """

    def __init__(self):
        config = Config()["database"]["redis"]
        println(config)
        self.r = redis.Redis(host=config["host"],
                             port=config["port"],
                             db=config["db"],
                             password=config["password"])
        try:
            self.r.ping()
        except redis.ConnectionError:
            pass

    def _scoped_key(self, key):
        scope = current_app.bearer()
        println(scope)
        println(key)
        return str(scope) + ":" + str(key)

    def _get(self, key):
        return self.r.get(self._scoped_key(key))

    def _set(self, key, value):
        return self.r.get(self._scoped_key(key), value)

    @property
    def USER_INFO(self):
        res = self._get("USER_INFO")
        println(res)

        if res is None:
            from lib.py.auth.facebook import FacebookAuthAPI
            fb_api = FacebookAuthAPI(bearer=current_app.bearer())
            user_info = fb_api.get_user_info()
            self._set("USER_INFO", user_info)
            res = user_info
        println(res)
        return res

    @USER_INFO.setter
    def USER_INFO(self, value):
        self._set("USER_INFO", value)
