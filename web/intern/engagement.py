from google.appengine.ext import webapp
from google.appengine.api import users

from datetime import datetime, timedelta
from django.utils import simplejson as json

from model import User, Query, DataPoint, ActionLog
from utils.lt_time import nearest_day
from utils.track_walltime import average_walltime, worst_walltime
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
      action = 'ReceivedSMS',
      timewindow = yesterday,
    ).count()

    new_logins = ActionLog.get(
      action = 'FirstTimeLogin',
      timewindow = yesterday,
    ).count()

    dashboard_avg_walltime = average_walltime('/dashboard')
    data_avg_walltime = average_walltime('/data')
    home_avg_walltime = average_walltime('/')
    analyze_avg_walltime = average_walltime('/analyze')
    analyze_json_avg_walltime = average_walltime('/analyzeJSON')

    dashboard_worst_walltime = worst_walltime('/dashboard')
    data_worst_walltime = worst_walltime('/data')
    home_worst_walltime = worst_walltime('/')
    analyze_worst_walltime = worst_walltime('/analyze')
    analyze_json_worst_walltime = worst_walltime('/analyzeJSON')

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
      'dashboard_walltime': dashboard_avg_walltime,
      'data_walltime': data_avg_walltime,
      'home_walltime': home_avg_walltime,
      'analyze_json_walltime': analyze_json_avg_walltime,
      'analyze_walltime': analyze_avg_walltime,
      'dashboard_worst_walltime': dashboard_worst_walltime,
      'data_worst_walltime': data_worst_walltime,
      'home_worst_walltime': home_worst_walltime,
      'analyze_json_worst_walltime': analyze_json_worst_walltime,
      'analyze_worst_walltime': analyze_worst_walltime,
    }

    self.response.out.write(html % params)
