from google.appengine.ext import webapp
from google.appengine.api import users
from django.utils import simplejson as json

from model import User, Query, DataPoint, TemplateMetric

from analytics.analytics import overview
from constants import whitelist

from lthandler import LoggedInPageHandler


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

    metric_overview = overview(query)

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




