from google.appengine.ext import db
from google.appengine.ext import webapp

from model import User, Query, DataPoint
from com.sms import send_sms

import logging

# yeah, we really need to get on this input validation bandwagon
class UpdateAccountHandler(webapp.RequestHandler):
  def post(self):
    user_email = self.request.get('user_email', None)
    phone = self.request.get('phone_number', None)
    medium = self.request.get('medium', None)
    first_time = self.request.get('first_time', None)
    user = User.get_by_email(user_email)
   
    if phone != None and len(phone) == 10:
      # need to check that no one has this phone number yet
      # also, validate the phone number somewhat
      user.phone = phone
    if medium != None:
      medium = medium.lower()
      if medium == 'sms' or medium == 'email':
        user.query_medium = medium

    user.put()

    if first_time != None and user.phone != None:
      self.first_time_message(user)

    self.response.out.write('success')

  def first_time_message(self, user):
      send_sms(user.phone, "Welcome to Superhuman! Put this number in your phone so you know when we send you queries.")
