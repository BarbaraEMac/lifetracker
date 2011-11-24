from google.appengine.api import logservice

import logging

logservice.AUTOFLUSH_ENABLED = False
logging.info("Analytics Refresh Backend Started")
logservice.flush()
