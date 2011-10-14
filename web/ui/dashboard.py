from google.appengine.ext import webapp
from google.appengine.api import users

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
    metric_html = \
    """<div id='metric-%(query_id)s' class='metric'>
      <input type='hidden' id='metric-%(query_id)s-type' value='%(format)s'/>
      <div class='metric-name-container'>
        <h3 id='metric-%(query_id)s-name' class='metric-name'>%(name)s</h3>
        <input type='text' value='%(name)s' id='edit-name-%(query_id)s' class='edit-field edit-name'/>
      </div>
      <div class='metric-snapshot'>
        <p class='overview-metric'>Current: %(current_value)s</p>
        <p class='overview-metric'>%(overview)s</p> 
        <p class='edit-field'>
          <input type='hidden' id='freq-minutes-%(query_id)s' value='%(freq_minutes)s'/>
          Frequency: <select id='edit-frequency-%(query_id)s' class='edit-field edit-frequency'>
          <option id='freq-1440'>Every Day</option>           
          <option id='freq-360'>Every 6 Hours</option>           
          <option id='freq-180'>Every 3 Hours</option>           
          <option id='freq-60'>Every Hour</option>           
          <option id='freq-1'>Every Minute</option>         
        </select>
      </p>
      </div>
      <div class='metric-options'>
        <a id='analyze-%(query_id)s' class='analyze-button' href='#'>Analyze</a>
        <a id='edit-%(query_id)s' class='query-edit-button' href='#'>Edit</a>
        <a id='submit-%(query_id)s' class='query-edit-submit-button' href='#'>Submit</a>
        <a id='delete-%(query_id)s' class='query-delete-button' href='#'>Delete</a>
        <a id='confirm-delete-%(query_id)s' class='query-delete-confirm-button' href='#'>Really?</a>
      </div>
      <div id='edit-format-container-%(query_id)s' class='edit-field edit-format-container'>
        <p>Format</p>
        <form id='edit-format-%(query_id)s' class='edit-format'>
        <p>
          Text <input type='radio' name='format' class='format-text' value='text'/>
          Number <input type='radio' name='format' class='format-number' value='number'/>
          Time <input type='radio' name='format' class='format-time' value='time'/>
        </p>
        </form>
      </div>
      <div id='edit-text-container-%(query_id)s' class='edit-field edit-text-container'>
        <p>Query Text:</p>
        <input id='edit-text-%(query_id)s' class='edit-field edit-text' type='text' value='%(text)s'/>
      </div>
      <div id='analytics-container-%(query_id)s' class='analytics-container'>
        <div id='numeric-analytics-container-%(query_id)s' class='numeric-analytics'>
          <img class='analytics-loading' src='images/loading.gif'/>
          <table id='analytics-%(query_id)s' class='analytics-table'></table>
          <p>
            <a href='analyze?query_id=%(query_id)s' id='analytics-more-%(query_id)s' class='more-analytics-button'>More</a>
          </p>
        </div>
        <div id='chart-%(query_id)s' class='chart'>
          <img class='chart-loading' src='images/loading.gif'/>
        </div>
      </div>
    </div>
"""

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




