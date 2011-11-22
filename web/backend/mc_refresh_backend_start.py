from google.appengine.api import logservice

import logging

logservice.AUTOFLUSH_ENABLED = False
logging.info("Memcache Refresh Backend Started")
logservice.flush()
