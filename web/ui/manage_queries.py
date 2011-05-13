from google.appengine.ext import webapp
from google.appengine.api import users

from model import User, Query, DataPoint

class ManageQueriesHandler(webapp.RequestHandler):
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

      # display all the user's queries
      # add a new query
      # edit queries 
      
      html_file = open("ui/html/manage_queries.html")
      html = html_file.read()

      # generate the query table
      html = html % {'queries': self.generate_query_table(user), 'logout_url': logout_url, 'user_email': user.email}

      self.response.out.write(html)

  def query_to_table_row(self, query):
    row = "<tr id='%(query_id)s'>\
      <td class='name-cell'><p id='name-%(query_id)s'>%(name)s</p>\
      <input id='edit-name-%(query_id)s' value='%(name)s' class='query-edit-field'/>\
      </td>\
      <td class='text-cell'><p id='text-%(query_id)s'>%(text)s</p>\
      <input id='edit-text-%(query_id)s' class='query-edit-field' value='%(text)s'/>\
      </td>\
      <td class='frequency-cell'><p id='frequency-%(query_id)s'>%(frequency)s</p>\
      <input id='edit-frequency-%(query_id)s' class='query-edit-field' value='%(frequency)s'/>\
      </td>\
      <td class='format-cell'>%(format)s</td>\
      <td class='timestamp-cell'>%(lastsentat)s</td>\
      <td class='action-cell'>\
      <a class='query-edit-button' id='edit-%(query_id)s' href='#'>Edit</a>\
      <a class='query-edit-submit-button' id='submit-%(query_id)s' href='#'>Submit</a>\
      <a class='query-delete-button' id='delete-%(query_id)s' href='#'>Delete</a>\
      <a class='query-delete-confirm-button' id='confirm-delete-%(query_id)s' href='#'>Really?</a>\
      </td>\
      </tr>"
    queryData = {'query_id': query.key(), 'name': query.name, 'text': query.text, 'format': query.format, 'frequency': query.frequency, 'lastsentat': query.lastSentAt}

    return row % queryData

  def generate_query_table(self, user):
    queries = Query.get_by_user(user)

    html = ''

    for query in queries:
      html += self.query_to_table_row(query)

    return html




