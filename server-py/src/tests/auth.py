import datetime

from sqlalchemy.exc import IntegrityError

from lib.py.core.config import Config


class TestFacebook:
    def user(self):
        """
        token source: https://developers.facebook.com/tools/explorer
        :return:
        """
        with Config() as config:
            from lib.py.auth.facebook import FacebookAuthAPI
            token = config["tests"]["fb_token"]
            auth_api = FacebookAuthAPI(bearer=token)
            try:
                identity = auth_api.create()
                assert identity.json_data["id"] == config["tests"]["fb_id"]
            except IntegrityError as e:
                identity = auth_api.sync_to_db()
                updated_at = identity.updated_at
                now = datetime.datetime.now(datetime.timezone.utc)
                assert now.timestamp() - updated_at.timestamp() < 30000
            except FileNotFoundError as e:
                print("Token has expired.\nGet a new token from: https://developers.facebook.com/tools/explorer")
                token = input("Enter token:")
                config["tests"]["fb_token"] = token
                print("Now try again!")
                assert False
