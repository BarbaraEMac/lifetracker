from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users

from SendQueries import SendQueriesHandler
from Data import NewDataPointHandler
from Data import NewQueryHandler
from Data import EditQueryHandler
from Data import DeleteQueryHandler
from Data import GetQueriesHandler
from Data import GetDataPointsHandler
from Data import ImportCSVHandler
from ui.manage_queries import ManageQueriesHandler
from ui.manage_data import ManageDataHandler
from ui.analyze import AnalyzeDataHandler
from ui.account import AccountHandler
from sms import ReceiveSMSHandler
from update_account import UpdateAccountHandler

from model import User, Query, DataPoint
from incoming_mail import EmailResponseHandler
from ui.import_data import ImportDataHandler

class HomeHandler(webapp.RequestHandler):
  def get(self):
      html_file = open("ui/home.html")
      html = html_file.read()

      # generate the query table
      #html = html % {}

      self.response.out.write(html)

appRoute = webapp.WSGIApplication( [
  ('/', HomeHandler),
  ('/sendQueries', SendQueriesHandler),
  ('/data/newPoint', NewDataPointHandler),
  ('/data/newQuery', NewQueryHandler),
  ('/data/editQuery', EditQueryHandler),
  ('/data/deleteQuery', DeleteQueryHandler),
  ('/data/queries', GetQueriesHandler),
  ('/data/points', GetDataPointsHandler),
  ('/data/import', ImportCSVHandler),
  ('/queries', ManageQueriesHandler),
  ('/data', ManageDataHandler),
  ('/account', AccountHandler),
  ('/account/update', UpdateAccountHandler),
  ('/import', ImportDataHandler),
  ('/analyze', AnalyzeDataHandler),
  ('/sms/receive', ReceiveSMSHandler),
  EmailResponseHandler.mapping(),
], debug=True)

def main():
  run_wsgi_app(appRoute)

if __name__ == '__main__':
  main()
