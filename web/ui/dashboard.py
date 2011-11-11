from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.api import memcache

from django.utils import simplejson as json
from datetime import datetime

from model import User, Query, DataPoint, TemplateMetric

from analytics.analytics import overview
from constants import whitelist

from lthandler import LoggedInPageHandler

import logging

class DashboardHandler(LoggedInPageHandler):
  def get(self):
    user = self.get_user()
    if not user:
      return

    # generate the query table
    params = {
      'queries': self.generate_query_table(user), 
      'user_email': user.email, 
      'template_metrics': TemplateMetric.json_list(),
    }
    
    self.register_css([
      'dashboard.css',
      'popup.css', 
      'new_metric_autocomplete.css',
    ])

    self.register_js([
      'https://www.google.com/jsapi',
      'google_charts.js',
      'dashboard.js',
    ])

    html = self.render_page('ui/html/dashboard.html', params)

    self.response.out.write(html)

  def query_to_table_row(self, query):
    metric_html = open('ui/html/metric.html').read()

    current_value = ''
    try:
      current_value = DataPoint.get_by_query_most_recent(query)[0].text
    except IndexError:
      current_value = 'None'

    metric_overview = self.get_overview(query)

    metric_data = {
      'query_id': query.key(), 
      'name': query.name, 
      'text': query.text, 
      'format': query.format, 
      'frequency': self.frequency_minutes_to_text(query.frequency),
      'lastsentat': query.lastSentAt,
      'freq_minutes': query.frequency,
      'current_value': current_value,
      'overview': metric_overview,
      'ask_when': json.dumps(query.ask_when),
    }

    return metric_html % metric_data


  def get_overview(self, query):
    # key names
    mck_metric_overview = str(query.key()) + '.overview'
    mck_overview_last_update = str(query.key()) + '.overview-last-update'
    mck_metric_last_update = str(query.key()) + '.last-update'

    #key values
    metric_overview = memcache.get(mck_metric_overview)
    overview_last_update = memcache.get(mck_overview_last_update)
    metric_last_update = memcache.get(mck_metric_last_update)

    # cache miss condition
    if not (metric_overview is not None and overview_last_update is not None and metric_last_update is not None and int(metric_last_update) < int(overview_last_update)):

      #cache miss, so calculate the overview
      metric_overview = overview(query)

      # update the relevant keys
      memcache.set(
        key=mck_metric_overview,
        value=metric_overview,
      )

      memcache.set(
        key=mck_overview_last_update,
        value=datetime.now().strftime('%s'),
      )

      if metric_last_update is None:
        memcache.set(
          key=mck_metric_last_update,
          value=datetime.now().strftime('%s'),
        )


    return metric_overview
 
  # not presently in use, but will be again soon
  def frequency_minutes_to_text(self, mins):
    freq_text = ''

    if mins < 60: 
      freq_text = 'Every %s minutes' % (mins)
    elif mins < 1440:
      hours = mins // 60
      if hours == 1:
        freq_text = 'Every hour'
      else:
        freq_text = 'Every %s hours' % (hours)
    else:
      days = mins // 1440
      if days == 1:
        freq_text = 'Every day'
      else:
        freq_text = 'Every %s days' % (days)

    return freq_text

  def generate_query_table(self, user):
    queries = Query.get_by_user(user)

    html = ''

    for query in queries:
      html += self.query_to_table_row(query)

    return html




