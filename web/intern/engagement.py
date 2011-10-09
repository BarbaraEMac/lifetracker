from google.appengine.ext import webapp
from google.appengine.api import users

from datetime import datetime, timedelta

from model import User, Query, DataPoint, ActionLog
from utils.time import nearest_day
from lthandler import LTHandler
from constants import whitelist

class EngagementDashboardHandler(LTHandler):
  def get(self):
    user = self.get_user()
    if not user:
      return

    logout_url = users.create_logout_url(self.request.uri)
    
    yesterday = datetime.now() - timedelta(hours=24)

    new_datapoints = ActionLog.get(
      action = 'NewDatapoint',
      timewindow = yesterday,
    ).count()

    new_metrics = ActionLog.get(
      action = 'NewMetric', 
      timewindow = yesterday,
    ).count()

    queries_sent = ActionLog.get(
      action = 'SentQuery',
      timewindow = yesterday,
    ).count()

    sms_sent = ActionLog.get(
      action = 'SentSMS',
      timewindow = yesterday,
    ).count()

    emails_sent = ActionLog.get(
      action = 'SentEmail',
      timewindow = yesterday,
    ).count()

    emails_received = ActionLog.get(
      action = 'ReceivedEmail',
      timewindow = yesterday,
    ).count()

    sms_received = ActionLog.get(
      action = 'ReceivedEmail',
      timewindow = yesterday,
    ).count()

    new_logins = ActionLog.get(
      action = 'FirstTimeLogin',
      timewindow = yesterday,
    ).count()

    # hackey high-number for now.
    total_metrics = Query.all().count(100000)
    total_datapoints = DataPoint.all().count(100000)

    f = open('intern/html/engagement.html')
    html = f.read()

    params = {
      'new_datapoints': new_datapoints,
      'new_metrics': new_metrics,
      'total_metrics': total_metrics,
      'total_datapoints': total_datapoints,
      'queries_sent': queries_sent,
      'sms_sent': sms_sent,
      'emails_sent': emails_sent,
      'sms_received': sms_received,
      'emails_received': emails_received,
      'new_logins': new_logins,
    }

    self.response.out.write(html % params)
