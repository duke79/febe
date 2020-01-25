import json

import requests
from urllib.parse import parse_qs

# def user_info():
#     import facebook
#     graph = facebook.GraphAPI(access_token=self._access_token, version="2.12")
#     info = graph.get_connections(id="me", connection_name="")
#     return info
from sqlalchemy.orm.exc import NoResultFound

from lib.py.core.traces import println
from lib.py.data.tables.user import User


class FacebookAuthAPI:
    """
    Ref: https://facebook-sdk.readthedocs.io/en/latest/api.html
    """

    def __init__(self, bearer):
        self.FACEBOOK_GRAPH_URL = "https://graph.facebook.com/"
        self.API_VERSION = "v4.0"
        self._bearer = bearer
        self._session = requests.Session()

    def request(self, args=None, post_args=None, files=None, method=None):
        """
        Generic interface for Facebook Graph API. No magic here!
        Ref: https://developers.facebook.com/docs/graph-api/reference/
        Tool: https://developers.facebook.com/tools/explorer/?method=GET&path=me%2F%3Ffields%3Demail&version=v4.0
        user id example: 1495258009
        :param args:
        :return:
        """
        if args is None:
            args = dict()
        if post_args is not None:
            method = "POST"

        if post_args and "access_token" not in post_args:
            post_args["access_token"] = self._bearer
        elif "access_token" not in args:
            args["access_token"] = self._bearer

        try:
            response = self._session.request(
                method or "GET",
                self.FACEBOOK_GRAPH_URL + self.API_VERSION + "/me",
                params=args,
                data=post_args,
                files=files
            )
        except requests.HTTPError as e:
            response = json.loads(e.read())
            raise FileNotFoundError(response)

        headers = response.headers
        if "json" in headers["content-type"]:
            result = response.json()
        elif "image/" in headers["content-type"]:
            mimetype = headers["content-type"]
            result = {
                "data": response.content,
                "mime-type": mimetype,
                "url": response.url,
            }
        elif "access_token" in parse_qs(response.text):
            query_str = parse_qs(response.text)
            if "access_token" in query_str:
                result = {"access_token": query_str["access_token"][0]}
                if "expires" in query_str:
                    result["expires"] = query_str["expires"][0]
            else:
                raise FileNotFoundError(response.json())
        else:
            raise FileNotFoundError("Maintype was not text, image, or querystring")

        if result and isinstance(result, dict) and result.get("error"):
            raise FileNotFoundError(result)
        return [result]

    def get_user_info(self):
        args = {"fields": "id,email,first_name,last_name,picture"}
        res = self.request(args=args)
        return res

    def sync_to_db(self):
        user_info = self.get_user_info()[0]

        # SYnc
        from lib.py.data.tables.oauth_identity import OAuthIdentity
        identity = OAuthIdentity()
        identity = identity.find(platform_id=user_info["id"], platform="facebook")
        identity.update(platform_id=user_info["id"], platform="facebook", json_data=user_info)

        # Return current record
        identity = OAuthIdentity()
        identity = identity.find(platform_id=user_info["id"], platform="facebook")
        return identity

    def create(self):
        user_info = self.get_user_info()[0]
        println(user_info)
        from lib.py.data.tables.oauth_identity import OAuthIdentity
        identity = OAuthIdentity()

        user = User()
        try:
            user = user.find(email=user_info["email"])
        except NoResultFound as e:
            print(user_info)
            user = user.create(first_name=user_info["first_name"],
                               last_name=user_info["last_name"],
                               email=user_info["email"],
                               picture=user_info["picture"]["data"]["url"])

        identity = identity.create(user_id=user.id,
                                   platform_id=user_info["id"],
                                   platform="facebook",
                                   json_data=user_info)
        return identity
