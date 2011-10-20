from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.api import memcache

from django.utils import simplejson as json
from datetime import datetime

from analytics.analytics import analyze_query_data
from analytics.text_analytics import common_word_frequencies
from model import User, Query, DataPoint
from lthandler import LTHandler, LoggedInPageHandler
from constants import whitelist

class TextMetricWordFrequencies(LTHandler):
  def get(self):
    user = self.get_user()
    if not user:
      return
      
    query_id = self.request.get('query_id')
    query = Query.get_by_id(query_id)
   
    datapoints = DataPoint.get_by_query(query)
    
    frequencies = common_word_frequencies(datapoints)

    self.response.out.write('[' + json.dumps(frequencies) + ']')
    

class AnalyzeDataJSONHandler(LTHandler):
  def get(self):
    user = self.get_user()
    if not user:
      return
      
    query_id = self.request.get('query_id')
    query = Query.get_by_id(query_id)

    analytics_json = self.get_analytics(query)

    self.response.out.write(analytics_json)

  def get_analytics(self, query):
    # key names
    mck_analytics_json = str(query.key()) + '.analytics-json'
    mck_analytics_json_last_update = str(query.key()) + '.analytics-json-last-update'
    mck_metric_last_update = str(query.key()) + '.last-update'


    # key values
    metric_last_update = memcache.get(mck_metric_last_update)
    analytics_json_last_update = memcache.get(mck_analytics_json_last_update)
    analytics_json = memcache.get(mck_analytics_json)


    # cache miss condition
    if not (analytics_json is not None and metric_last_update is not None and analytics_json_last_update is not None and int(metric_last_update) < int(analytics_json_last_update)):
     
      # cache miss, so calculate the analytics
      analytics_json = json.dumps(analyze_query_data(query))

      # update the relevant keys
      memcache.set( 
        key=mck_analytics_json, 
        value=analytics_json, 
        time=86400
      )
   
      memcache.set(
        key=mck_analytics_json_last_update, 
        value=datetime.now().strftime('%s'), 
        time=86400
      )

      # must have fallen out of memcache
      if metric_last_update is None: 
        memcache.set(
          key=mck_metric_last_update,
          value=datetime.now().strftime('%s'),
          time=86400
        )

    return analytics_json



class AnalyzeDataHandler(LoggedInPageHandler):
  def get(self):
    user = self.get_user()
    if not user:
      return
      
    query_id = self.request.get('query_id')
    query = Query.get_by_id(query_id)

    analytics_html = self.get_analytics(query)

    params = {
      'analytics_rows': analytics_html, 
      'user_email': user.email, 
      'query_name': query.name,
    }

    html = self.render_page('ui/html/analyze.html', params)

    self.response.out.write(html)

  def get_analytics(self, query):
    # key names
    mck_analytics = str(query.key()) + '.analytics-html'
    mck_analytics_last_update = str(query.key()) + '.analytics-last-update'
    mck_metric_last_update = str(query.key()) + '.last-update'

    # values
    metric_last_update = memcache.get(mck_metric_last_update)
    analytics_last_update = memcache.get(mck_analytics_last_update)
    analytics_html = memcache.get(mck_analytics)

    # cache miss condition 
    if not (analytics_html is not None and metric_last_update is not None and analytics_last_update is not None and int(metric_last_update) < int(analytics_last_update)):
     
      # cache miss, so calculate the analytics
      analytics = analyze_query_data(query)
      analytics_html = self.generate_analysis_view(analytics)

      # update the relevant keys
      memcache.set(
        key=mck_analytics, 
        value=analytics_html, 
        time=86400
      )

      memcache.set(
        key=mck_analytics_last_update, 
        value=datetime.now().strftime('%s'), 
        time=86400
      )

      # must have fallen out of memcache
      if metric_last_update is None: 
        memcache.set(
          key=mck_metric_last_update,
          value=datetime.now().strftime('%s'),
          time=86400
        )

    return analytics_html 

  #def stat_to_row(self, analytic):
  def stat_to_row(self, name, value):
    #return "<tr><td>%(name)s</td><td>%(value)s</td></tr>" % {'name': analytic['name'], 'value': analytic['value']}
    return "<tr><td>%(name)s</td><td>%(value)s</td></tr>" % {'name': name, 'value': value}

  def generate_analysis_view(self, analytics):
    html = ''
    # we could make analytics a simple map
    # then we could do:
    # for key, value in analytics
    #   ...
    """for analytic in analytics:
      html += self.stat_to_row(analytic)"""
    for (name, value) in analytics:
      html += self.stat_to_row(name, value)
    return html
