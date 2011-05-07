from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users

from SendQueries import SendQueriesHandler
from Data import NewDataPointHandler
from Data import NewQueryHandler
from Data import GetQueriesHandler
from Data import GetDataPointsHandler

from model import User, Query, DataPoint

class HomeHandler(webapp.RequestHandler):
  def get(self):
    google_user = users.get_current_user()
    if not google_user:
      self.redirect(users.create_login_url(self.request.uri))

    db_user = User(google_user = google_user, 
      first_name='', 
      last_name='', 
      email=google_user.email()
    )

    db_user.put()

    self.response.out.write("Lifetracker. It's gonna be a thing.")

appRoute = webapp.WSGIApplication( [
  ('/', HomeHandler),
  ('/sendQueries', SendQueriesHandler),
  ('/data/newPoint', NewDataPointHandler),
  ('/data/newQuery', NewQueryHandler),
  ('/data/queries', GetQueriesHandler),
  ('/data/points', GetDataPointsHandler),
], debug=True)

def main():
  run_wsgi_app(appRoute)

if __name__ == '__main__':
  main()
