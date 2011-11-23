from google.appengine.api import logservice

import logging

logservice.AUTOFLUSH_ENABLED = False
logging.info("Query Agent Backend Started")
logservice.flush()
