#!/usr/bin/env python

import sys

from app import app as application
from app.core import Core

sys.path.append('/var/www/apache-flask')
application.core = Core('config/apache.cfg')
application.core.setup()