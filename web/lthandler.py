from google.appengine.ext import webapp
from google.appengine.api import users

from model import User, Query, DataPoint, TemplateMetric, ActionLog

from analytics.analytics import overview
from constants import whitelist, admins
import logging

class LTHandler(webapp.RequestHandler):
  def get_user(self):
    user = None

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

    # this enables admins to see pages in any user's context
    if self.request.get('admin', None) == 'true' and user.email in admins:
      user_email = self.request.get('user_email')
      user = User.get_by_email(user_email)

    return user

