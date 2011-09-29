from google.appengine.ext import webapp
from google.appengine.api import users

from datetime import datetime

from model import User, Query, DataPoint, ActionLog
from utils.time import nearest_day
from constants import whitelist

class EngagementDashboardHandler(webapp.RequestHandler):
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
