import logging

from google.appengine.ext import webapp
from google.appengine.api import memcache

from datetime import datetime

from django.utils import simplejson as json
from analytics.analytics import analyze_query_data

from ui.analyze import AnalyzeDataHandler

from model import Query, DataPoint

class AnalyticsRefreshHandler(webapp.RequestHandler):
  def get(self):
    start = datetime.now().strftime('%s')

    queries = Query.all().fetch(1000)

    for query in queries:
      lytics = analyze_query_data(query)

      mck_analytics_json = str(query.key()) + '.analytics-json'
      mck_analytics_json_last_update = str(query.key()) + '.analytics-json-last-update'

      analytics_json = json.dumps(lytics)

      memcache.set(
        key=mck_analytics_json,
        value=analytics_json,
      )

      memcache.set(
        key=mck_analytics_json_last_update,
        value=datetime.now().strftime('%s'),        
      )

      # update metric_last_update

      mck_metric_last_update = str(query.key()) + '.last-update'
      metric_last_update = memcache.get(mck_metric_last_update)
    
      if metric_last_update == None:
        memcache.set(
          key=mck_metric_last_update,
          value=datetime.now(),
        )
      else:
        memcache.set(
          key=mck_metric_last_update,
          value=metric_last_update,
        )      


      logging.info("Refreshed analytics for metric: " + str(query.key()))

    end = datetime.now().strftime('%s')

    logging.info('Analytics refresh started: ' + start)
    logging.info('Analytics refresh ended: ' + end)


