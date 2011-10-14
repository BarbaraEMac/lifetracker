from google.appengine.ext import webapp
from google.appengine.api import users

from django.utils import simplejson as json

from analytics.analytics import analyze_query_data
from analytics.text_analytics import common_word_frequencies
from model import User, Query, DataPoint
from lthandler import LTHandler, LoggedInPageHandler
from constants import whitelist

import logging

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

    analytics = analyze_query_data(query)

    self.response.out.write(json.dumps(analytics))

class AnalyzeDataHandler(LoggedInPageHandler):
  def get(self):
    user = self.get_user()
    if not user:
      return
      
    query_id = self.request.get('query_id')
    query = Query.get_by_id(query_id)

    analytics = analyze_query_data(query)
    analytics_html = self.generate_analysis_view(analytics)

    params = {
      'analytics_rows': analytics_html, 
      'user_email': user.email, 
      'query_name': query.name,
    }

    html = self.render_page('ui/html/analyze.html', params)

    self.response.out.write(html)

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
