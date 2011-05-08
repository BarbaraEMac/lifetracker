from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users

from SendQueries import SendQueriesHandler
from Data import NewDataPointHandler
from Data import NewQueryHandler
from Data import EditQueryHandler
from Data import GetQueriesHandler
from Data import GetDataPointsHandler
from ui.manage_queries import ManageQueriesHandler
from ui.manage_data import ManageDataHandler

from model import User, Query, DataPoint
from incoming_mail import EmailResponseHandler

class HomeHandler(webapp.RequestHandler):
  def get(self):
    google_user = users.get_current_user()
    if google_user == None:
      self.redirect(users.create_login_url(self.request.uri))
    else:
      if User.get_by_google_user(google_user) == None:
        db_user = User(google_user = google_user, 
          first_name='', 
          last_name='', 
          email=google_user.email()
        )

        db_user.put()

      logout_url = users.create_logout_url(self.request.uri)
      self.response.out.write("Lifetracker. It's gonna be a thing. " + "<a href='" + logout_url + "'>Logout</a>")

appRoute = webapp.WSGIApplication( [
  ('/', HomeHandler),
  ('/sendQueries', SendQueriesHandler),
  ('/data/newPoint', NewDataPointHandler),
  ('/data/newQuery', NewQueryHandler),
  ('/data/editQuery', EditQueryHandler),
  ('/data/queries', GetQueriesHandler),
  ('/data/points', GetDataPointsHandler),
  ('/queries', ManageQueriesHandler),
  ('/data', ManageDataHandler),
  EmailResponseHandler.mapping(),
], debug=True)

def main():
  run_wsgi_app(appRoute)

if __name__ == '__main__':
  main()
