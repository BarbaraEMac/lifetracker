from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.api import users

from model import User, Query, DataPoint

from constants import whitelist

class ExportDataHandler(webapp.RequestHandler):
  def get(self):
    google_user = users.get_current_user()
    if google_user == None:
      self.redirect(users.create_login_url(self.request.uri))
    elif not google_user.email() in whitelist:
      self.redirect(users.create_logout_url(self.request.uri))
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

      html_file = open("ui/html/export_data.html")
      html = html_file.read()

      query_id = self.request.get('query_id', None)
     
      query = db.get(query_id)
 
      # generate the query table
      html = html % {'logout_url': logout_url, 'user_email': user.email, 'query_id': query_id, 'query_name': query.name}

      self.response.out.write(html)


