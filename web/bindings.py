from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users

from api.Data import NewDataPointHandler
from api.Data import NewQueryHandler
from api.Data import EditQueryHandler
from api.Data import DeleteQueryHandler
from api.Data import GetQueriesHandler
from api.Data import GetDataPointsHandler
from api.Data import ImportCSVHandler
from api.update_account import UpdateAccountHandler
from ui.manage_queries import ManageQueriesHandler
from ui.manage_data import ManageDataHandler
from ui.analyze import AnalyzeDataHandler
from ui.account import AccountHandler
from ui.home import HomeHandler
from ui.import_data import ImportDataHandler
from communications.sms import ReceiveSMSHandler
from communications.incoming_mail import EmailResponseHandler
from communications.SendQueries import SendQueriesHandler

from model import User, Query, DataPoint


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
