import getpass
import os
import socket
from os.path import expanduser


def config_defaults():
    defaults = dict()

    home_config = os.path.join(expanduser("~"), "vilokanlabs")
    sqlite_path = os.path.join(home_config, os.path.normpath("sqlite.db"))
    py_home = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    alembic_home = os.path.normpath(os.path.join(py_home, "data/alembic"))

    defaults["home"] = home_config
    defaults["devas"] = {
        "home": py_home,  # absolute path to src/VilokanLabs
        "version": "0.0.1"
    }
    defaults["server"] = {
        "host": "0.0.0.0",
        "port": "5555",
        "secret_key": "k:P@[Q@zGY;rP>S!Nb72K5gMg2POJ!-@oM1xC.Va%xsRBv-(NXt}rhg!(9Jo6N6"
    }

    host_ip = "localhost"
    if "HOST_IP" in os.environ:
        host_ip = os.environ["HOST_IP"]
    defaults["database"] = {
        "alembic_path": alembic_home,
        "active": "postgres",
        "sqlite": {
            "path": sqlite_path
        },
        "mysql": {
            "db": "dummy_db",
            "user": "dummy_user",
            "host": "localhost",
            "password": "dummy_password"
        },
        "postgres": {
            "db": "vilokanlabs",
            "user": "vilokanlabs",
            "host": host_ip,
            "password": "mintfresh",
            "port": "5432",
            "email": "vilokanlabs@gmail.com"
        },
        "redis": {
            "host": host_ip,
            "port": "6379",
            "password": "mintfresh",
            "db": 0
        }
    }
    defaults["debug"] = True
    defaults["stacktrace"] = False
    defaults["slackbot"] = {
        "access_token": "your oAuth access token here",
        "user_token": "your bot user access token here",
        "authorized_user_ids": ["UA75M023Z"]
    }
    defaults["ml"] = {
        "dir": os.path.join(defaults["home"], "ml")
    }
    defaults["auth"] = {
        "facebook": {
            "app_id": "504466700388776",
            "app_name": "Vilokan Labs"
        }
    }
    defaults["tests"] = {
        "fb_token": "fb auth token here",
        "fb_id": "10220672111821443"
    }

    try:
        os.makedirs(defaults["ml"]["dir"])
    except FileExistsError:
        pass

    return defaults
