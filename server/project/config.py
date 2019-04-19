# flask config file

import os
from datetime import timedelta

SECRET_KEY=os.urandom(24)
PERMANENT_SESSION_LIFETIME=timedelta(days=7)
DATABASE='instance/db.sqlite3'
DEBUG=True
PHOTODIR='static/'