from google.appengine.ext import db
from google.appengine.ext import webapp

from google.appengine.api import users
from django.utils import simplejson as json

from model import User, Query, DataPoint, TemplateMetric
from com.sms import send_sms

import logging
from lthandler import LTHandler
from constants import whitelist

# yeah, we really need to get on this input validation bandwagon
class UpdateAccountHandler(LTHandler):
  def post(self):
    user = self.get_user()
    if not user:
      return

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

class FirstTimeUserHandler(LTHandler):
  def get(self): # this should really be post, all these db-writes
    user = self.get_user()
    if not user:
      return

    # unpack the values from the query string
    program = self.request.get('program')
    sms = self.request.get('sms', None) 

    if sms != None and len(sms) == 10:
      # need to check that no one has this phone number yet
      # also, validate the phone number somewhat
      user.phone = sms
      user.query_medium = 'sms' # favour sms over email
      user.put()

    metrics = None

    if program == 'casual':
      metrics = json.loads(open('scripts/casual_program.json').read())
    else:
      metrics = json.loads(open('scripts/moderate_program.json').read())

    for metric in metrics:
      if metric == None:
        continue

      # add the metric
      name = metric["name"]
      frequency = int(metric["frequency"])
      text = metric['text']
      user_email = self.request.get('user_email')
      format = metric['format']
      template = TemplateMetric.get_by_name(name)

      query = Query(
        name = name,
        # we should really do normalization inside the Query constructor,
        # but it will take some time to figure out how, lacking a nearby
        # python badass
        normalized_name = Query.normalize_name(name), 
        text = text,
        frequency = frequency,
        user = user,
        format = format,
        template = template,
      )

      query.put()
    
    self.redirect('/dashboard?first_time=true')


""" 
This is a hack to allow us to redirect to a login url with a custom
callback url determined on the client. There may be a cleaner way to do this
rather than just exposing this function as a URL, but we can worry about
that later.
"""
class LoginURLGetterHandler(LTHandler):
  def get(self):
    url = self.request.get('url');
    self.response.out.write(users.create_login_url(url))
