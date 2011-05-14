from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users

from api.data import NewDataPointHandler
from api.data import NewQueryHandler
from api.data import EditQueryHandler
from api.data import DeleteQueryHandler
from api.data import GetQueriesHandler
from api.data import GetDataPointsHandler
from api.data import ImportCSVHandler
from api.update_account import UpdateAccountHandler
from ui.manage_queries import ManageQueriesHandler
from ui.manage_data import ManageDataHandler
from ui.analyze import AnalyzeDataHandler
from ui.account import AccountHandler
from ui.home import HomeHandler
from ui.import_data import ImportDataHandler
from com.sms import ReceiveSMSHandler
from com.incoming_mail import EmailResponseHandler
from com.send_queries import SendQueriesHandler

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
