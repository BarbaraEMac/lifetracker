from google.appengine.ext import webapp
from google.appengine.api import users

from model import User, Query, DataPoint
from lthandler import LTHandler
from constants import whitelist

class ManageDataHandler(LTHandler):
  def get(self):
    user = self.get_user()
    if not user:
      return
    
    logout_url = users.create_logout_url(self.request.uri)

    html_file = open("ui/html/manage_data.html")
    html = html_file.read()

    # generate the query table
    html = html % {'logout_url': logout_url, 'user_email': user.email, 'data': self.generate_data_view(user)}

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
    query_template = """<div class="lt-query">
      <h2>%(name)s</h2>
      <table class='lt-data-table'>
        <thead>
          <td class='date-cell'>Date</td>
          <td class='text-cell'>Response</td>
          <td>Delete</td>
        <thead>
        %(rows)s
        <tr class='input-row' id='input-row-%(query_id)s'>
          <td class='date-cell'>Now</td>
          <td class='text-cell'><input type='text' value='value'/></td>
          <td><a class='new-entry-submit-button' id='new-entry-submit-button-%(query_id)s' href='#'>Submit</a></td>
        </tr>
      </table>
      <p class='new-entry'><a class='new-entry-button' id='new-entry-button-%(query_id)s' href="#">New entry</a> <a class='import-data-button' href='import?query_id=%(query_id)s'>Import Data</a> <a class='export-data-button' href='export?query_id=%(query_id)s'>Export Data</a> <a href='analyze?query_id=%(query_id)s'>Analyze</a></p>
    </div>"""

    rows =  ''
    # get all datapoints associated with the query
    datapoints = DataPoint.get_by_query(query)
    # for each datapoint from the query
    #   append data_point_to_row(dp)
    for dp in datapoints:
      rows += self.data_point_to_row(dp)
   
    return query_template % {'rows': rows, 'name': query.name, 'query_id': query.key()}

  def data_point_to_row(self, dp):
    row_template = """<tr id='delete-row-%(dp_id)s'><td>%(date)s</td><td>%(text)s</td><td><a id='delete-%(dp_id)s' class='dp-delete-button' href='#'>Delete</a></td></tr>"""

    # format a datapoint into a table row
    return row_template % {'date': dp.timestamp, 'text': dp.text, 'dp_id': dp.key()}

