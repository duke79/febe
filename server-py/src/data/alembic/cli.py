"""
Ref: https://stackoverflow.com/a/35211383/973425
"""

import alembic.config

from ...core.paths import ActiveDir, alembic_path
from ..common import db_uri
from ..common.base import db_session
from ..tables import *  # DO NOT REMOVE | Redundant import kept on purpose


class AlembicCLI:
    def init_db(self):
        session = db_session()  # This line creates the tables
        pass

    def upgrade(self):
        with ActiveDir(alembic_path):
            alembicArgs = [
                '--raiseerr',
                '-x', 'dbPath=' + db_uri,
                'upgrade', 'head',
            ]
            alembic.config.main(argv=alembicArgs)

    def migrate(self, revision_name="new revision"):
        with ActiveDir(alembic_path):
            alembicArgs = [
                '--raiseerr',
                '-x', 'dbPath=' + db_uri,
                "revision", "--autogenerate", "-m", revision_name
            ]
            alembic.config.main(argv=alembicArgs)

    def print_db_uri(self):
        print(db_uri[10:])
