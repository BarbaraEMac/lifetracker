from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app 
from google.appengine.api import users

from api.data import NewDataPointHandler
from api.data import NewQueryHandler
from api.data import EditQueryHandler
from api.data import DeleteQueryHandler
from api.data import GetQueriesHandler
from api.data import GetDataPointsHandler
from api.data import GetDataPointsForQueryHandler
from api.data import DeleteDataPointHandler
from api.data import ImportCSVHandler
from api.data import ExportCSVHandler
from api.account import FirstTimeUserHandler
from api.account import LoginURLGetterHandler
from api.account import UpdateAccountHandler
from ui.dashboard import DashboardHandler
from ui.manage_data import ManageDataHandler
from ui.analyze import AnalyzeDataHandler
from ui.analyze import AnalyzeDataJSONHandler
from ui.analyze import TextMetricWordFrequencies
from ui.account import AccountHandler
from ui.home import HomeHandler
from ui.no_invite import NoInviteHandler
from ui.tos import TOSHandler
from ui.import_data import ImportDataHandler
from ui.export_data import ExportDataHandler
from com.sms import ReceiveSMSHandler
from com.sms import TropoSMSScriptHandler
from com.incoming_mail import EmailResponseHandler
from com.send_queries import SendQueriesHandler
from scripts.init_templates import InitTemplatesHandler

from backend.memcache_refresh import MemcacheRefreshHandler
from backend.analytics_refresh import AnalyticsRefreshHandler

from intern.engagement import EngagementDashboardHandler

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
  ('/data/pointsForQuery', GetDataPointsForQueryHandler),
  ('/data/deletePoint', DeleteDataPointHandler),
  ('/data/import', ImportCSVHandler),
  ('/data/export', ExportCSVHandler),
  ('/dashboard', DashboardHandler),
  ('/data', ManageDataHandler),
  ('/account', AccountHandler),
  ('/account/update', UpdateAccountHandler),
  ('/firstTimeUser', FirstTimeUserHandler),
  ('/import', ImportDataHandler),
  ('/export', ExportDataHandler),
  ('/analyze', AnalyzeDataHandler),
  ('/analyzeJSON', AnalyzeDataJSONHandler),
  ('/analyze/text/wordFrequencies', TextMetricWordFrequencies),
  ('/sms/receive', ReceiveSMSHandler),
  ('/sms/tropo.py', TropoSMSScriptHandler),
  ('/scripts/init_templates', InitTemplatesHandler),
  ('/loginURL', LoginURLGetterHandler),
  ('/intern/engagement', EngagementDashboardHandler),
  ('/no-invite', NoInviteHandler),
  ('/tos', TOSHandler),

  ('/backend/memcache-refresh', MemcacheRefreshHandler),
  ('/backend/analytics-refresh', AnalyticsRefreshHandler),
  EmailResponseHandler.mapping(),
], debug=True)

def main():
  run_wsgi_app(appRoute)

if __name__ == '__main__':
  main()
