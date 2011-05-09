from google.appengine.ext import webapp
from google.appengine.api import users

from model import User, Query, DataPoint

class ManageDataHandler(webapp.RequestHandler):
  def get(self):
    google_user = users.get_current_user()
    if google_user == None:
      self.redirect(users.create_login_url(self.request.uri))
    else:
      user = User.get_by_google_user(google_user)
      if user == None:
        user = User(google_user = google_user, 
          first_name='', 
          last_name='', 
          email=google_user.email()
        )

        user.put()
      
      logout_url = users.create_logout_url(self.request.uri)

      html_file = open("ui/data.html")
      html = html_file.read()

      # generate the query table
      html = html % {'logout_url': logout_url, 'user_email': user.email, 'data': self.GenerateDataView(user)}

      self.response.out.write(html)

  def GenerateDataView(self, user):
    # get all the queries

    queries = Query.get_by_user(user)
    html = ''
    # for each query
    #   append QueryToData(query)
    for query in queries:
      html += self.QueryToData(query)
    
    return html

  def QueryToData(self, query):
    query_template = """<div class="lt-query">
      <h2>%(name)s</h2>
      <table class='lt-data-table'>
        <thead>
          <td class='date-cell'>Date</td>
          <td class='text-cell'>Response</td>
        <thead>
        %(rows)s
        <tr class='input-row' id='input-row-%(query_id)s'>
          <td class='date-cell'>Now</td>
          <td class='text-cell'><input type='text' value='value'/></td>
        </tr>
      </table>
      <p class='new-entry'><a class='new-entry-button' id='new-entry-button-%(query_id)s' href="#">New entry</a> <a class='new-entry-submit-button' id='new-entry-submit-button-%(query_id)s' href='#'>Submit</a> <a class='import-data-button' href='import?query_id=%(query_id)s'>Import Data</a></p>
    </div>"""

    rows =  ''
    # get all datapoints associated with the query
    datapoints = DataPoint.get_by_query(query)
    # for each datapoint from the query
    #   append DataPointToRow(dp)
    for dp in datapoints:
      rows += self.DataPointToRow(dp)
   
    return query_template % {'rows': rows, 'name': query.name, 'query_id': query.key()}

  def DataPointToRow(self, dp):
    row_template = """<tr><td>%(date)s</td><td>%(text)s</tr>"""

    # format a datapoint into a table row
    return row_template % {'date': dp.timestamp, 'text': dp.text}

