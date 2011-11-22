import logging

from google.appengine.ext import webapp
from google.appengine.api import memcache

from datetime import datetime

from model import Query, DataPoint

class MemcacheRefreshHandler(webapp.RequestHandler):
  def get(self):
    start = datetime.now()
    
    queries = Query.all().fetch(1000)

    self.refresh_datapoints(queries)
    self.refresh_most_recent_dp(queries)

    end = datetime.now()

    logging.info("Memcache refresh started: " + start.strftime('%s'))
    logging.info("Memcache refresh ended: " + end.strftime('%s'))

  def refresh_datapoints(self, queries):
    # weird thing here.
    # if DataPoint.get_by_query cache-misses, we are actually refreshing
    # this twice in a row. If it cache-hits, we only refresh it once (which
    # is what we want)

    # maybe this should be inside model.py, but I don't think an extra
    # few memcache puts every day are going to kill us right now.

    # for each metric
    #   get all datapoints in json
    #   put into memcache
    for query in queries:
      datapoints = DataPoint.get_by_query(query)
      json_dps =  DataPoint.JsonFromArray(datapoints)

      mck_metric_datapoints = str(query.key()) + '.datapoints'
      mck_metric_datapoints_last_update = str(query.key()) + '.datapoints-last-update'

      memcache.set(
        key=mck_metric_datapoints,
        value=json_dps,
      )

      memcache.set(
        key=mck_metric_datapoints_last_update,
        value=datetime.now().strftime('%s'),
      )
    
      logging.info("Refreshed datapoints for metric: " + str(query.key()))

  def refresh_most_recent_dp(self, queries):
    for query in queries:
      most_recent_dp = DataPoint.get_by_query_most_recent(query)
      
      mck_most_recent_dp = str(query.key()) + '.most-recent-dp'
      mck_most_recent_dp_update = str(query.key()) + 'most-recent-dp-update'

      memcache.set(
        key=mck_most_recent_dp,
        value=most_recent_dp,
      )

      memcache.set(
        key=mck_most_recent_dp_update,  
        value=datetime.now().strftime('%s'),
      )

      logging.info('Updated Most Recent Datapoint for metric: ' + str(query.key()))
