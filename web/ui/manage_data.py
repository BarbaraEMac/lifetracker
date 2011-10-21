from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.api import memcache

from model import User, Query, DataPoint
from lthandler import LoggedInPageHandler
from constants import whitelist

from datetime import datetime

class ManageDataHandler(LoggedInPageHandler):
  def get(self):
    user = self.get_user()
    if not user:
      return
    
    params = {
      'user_email': user.email, 
      'data': self.generate_data_view(user)
    }

    self.register_css(['manage_data.css'])
    self.register_js(['manage_data.js'])

    html = self.render_page('ui/html/manage_data.html', params)

    self.response.out.write(html)

  def generate_data_view(self, user):
    # get all the queries

    queries = Query.get_by_user(user)
    html = ''
    # for each query
    #   append query_to_data(query)
    for query in queries:
      html += self.query_to_data(query)
    
    return html

  def query_to_data(self, query):
    # keys
    mck_metric_last_updated = str(query.key()) + '.last-updated'
    mck_data_last_updated = str(query.key()) + '.data-last-updated'
    mck_data = str(query.key()) + '.data'

    # values
    metric_last_updated = memcache.get(mck_metric_last_updated)
    data_last_updated = memcache.get(mck_data_last_updated)
    data = memcache.get(mck_data)
 
    # cache miss condition
    if not (data is not None and metric_last_updated is not None and data_last_updated is not None and int(metric_last_updated) < int(data_last_updated)):

      # cache miss thingy
      data = self.query_data_from_db(query)

      # update the relevant keys
      memcache.set(
        key=mck_data,
        value=data,
        time=86400
      )

      memcache.set(
        key=mck_data_last_updated,
        value=datetime.now().strftime('%s'),
        time=86400
      )

      if metric_last_updated is None:
        memcache.set(
          key=mck_metric_last_updated,
          value=datetime.now().strftime('%s'),
          time=86400
        )

    return data 

  def query_data_from_db(self, query):
    query_template = open('ui/html/metric_data.html').read()

    rows =  ''
    # get all datapoints associated with the query
    datapoints = DataPoint.get_by_query(query)
    # for each datapoint from the query
    #   append data_point_to_row(dp)
    for dp in datapoints:
      rows += self.data_point_to_row(dp)
  
    params =  {
      'rows': rows, 
      'name': query.name, 
      'query_id': query.key()
    }

    return query_template % params

  def data_point_to_row(self, dp):
    row_template = """<tr id='delete-row-%(dp_id)s'><td>%(date)s</td><td>%(text)s</td><td><a id='delete-%(dp_id)s' class='dp-delete-button' href='#'>Delete</a></td></tr>"""

    # format a datapoint into a table row
    return row_template % {'date': dp.timestamp, 'text': dp.text, 'dp_id': dp.key()}

