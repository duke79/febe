import os
import sys
from lib.py.core.traces import print_exception_traces

from lib.py.data.alembic.cli import AlembicCLI
from lib.py.data.tables import *  # DO NOT REMOVE | Redundant import kept on purpose

alembic_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "alembic")

try:
    alembic = AlembicCLI()
    if len(sys.argv) > 1:
        if "init" == sys.argv[1]:
            alembic.init_db()
        elif "migrate" == sys.argv[1]:
            alembic.migrate(alembic_path=alembic_path)
        elif "upgrade" == sys.argv[1]:
            alembic.upgrade(alembic_path=alembic_path)
    else:
        alembic.print_db_uri()
except Exception as e:
    print_exception_traces(e)
