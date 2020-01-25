# Check which python implementation is being used
import platform

from ...core.traces import println
from .application import Application

println(platform.python_implementation())

app = Application(__name__)
app.configure()
app.enable_CORS()
app.upgrade_db()
app.init_debug_toolbar()
app.init_sentry()

# Views
from .views import *
