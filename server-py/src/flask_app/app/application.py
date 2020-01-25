import logging

from flask import Flask
from ...core.config import Config
from ...core.traces import println


class Application(Flask):
    def __init__(self, *args, **kwargs):
        Flask.__init__(self, *args, **kwargs)

    def configure(self):
        # Configuration
        ## Set the secret key to some random bytes. Keep this really secret!
        try:
            self.config['SECRET_KEY'] = Config()["server"]["secret_key"]
        except KeyError as e:
            pass

        self.debug = Config()["debug"]

    def bearer(self):
        from flask import request
        bearer = request.headers.get('bearer')
        println(bearer)
        if bearer is None:
            raise FileNotFoundError
        return bearer

    def enable_CORS(self):
        # Cross Origin
        from flask_cors import CORS
        CORS(self)

    def init_debug_toolbar(self):
        # Debug
        from flask_debugtoolbar import DebugToolbarExtension

        toolbar = DebugToolbarExtension(self)
        toolbar.init_app(self)

    def init_sentry(self):
        # Sentry (error reporting)
        # https://sentry.io/organizations/vilokan-labs/issues/?project=1766096
        import sentry_sdk
        from sentry_sdk.integrations.flask import FlaskIntegration
        from sentry_sdk.integrations.redis import RedisIntegration
        from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
        from sentry_sdk.integrations.logging import LoggingIntegration

        logging_integration = LoggingIntegration(
            level=logging.INFO,  # Capture info and above as breadcrumbs
            event_level=logging.ERROR  # Send errors as events
        )

        sentry_sdk.init(
            dsn="https://c8f88d7866e442d3927ccd924b7b9ecf@sentry.io/1766096",
            integrations=[FlaskIntegration(),
                          RedisIntegration(),
                          SqlalchemyIntegration(),
                          logging_integration]
        )

    def upgrade_db(self):
        # SQLAlchemy
        from ...data.alembic.cli import AlembicCLI

        alembic = AlembicCLI()
        alembic.upgrade()
