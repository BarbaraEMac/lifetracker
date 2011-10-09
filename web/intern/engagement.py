from google.appengine.ext import webapp
from google.appengine.api import users

from datetime import datetime

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

    new_datapoints = ActionLog.get(
      action = 'NewDatapoint',
      timewindow = datetime.fromtimestamp(nearest_day(int(datetime.now().strftime("%s"))))
    ).count()

    new_metrics = ActionLog.get(
      action = 'NewMetric', 
      timewindow = datetime.fromtimestamp(nearest_day(int(datetime.now().strftime("%s"))))
    ).count()

    queries_sent = ActionLog.get(
      action = 'SentQuery',
      timewindow = datetime.fromtimestamp(nearest_day(int(datetime.now().strftime("%s"))))
    ).count()

    sms_sent = ActionLog.get(
      action = 'SentSMS',
      timewindow = datetime.fromtimestamp(nearest_day(int(datetime.now().strftime("%s"))))
    ).count()

    emails_sent = ActionLog.get(
      action = 'SentEmail',
      timewindow = datetime.fromtimestamp(nearest_day(int(datetime.now().strftime("%s"))))
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
    }

    self.response.out.write(html % params)
