from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import memcache

from django.utils import simplejson as json

from utils.time import *

from datetime import datetime
from datetime import timedelta

import logging

class User(db.Model):
  google_user = db.UserProperty()
  first_name = db.StringProperty()
  email = db.StringProperty()
  phone = db.StringProperty()
  query_medium = db.StringProperty(
    choices = ('sms', 'email'), default='email')

  @staticmethod
  def get_by_google_user(google_user):
    return User.all().filter('google_user =', google_user).get()

  @staticmethod
  def get_by_email(email):
    return User.all().filter('email =', email).get()

  @staticmethod
  def get_by_phone(phone):
    return User.all().filter('phone =', phone).get()

# a log of actions taken by users on the site
class ActionLog(db.Model):
  action = db.StringProperty(required = True)
  timestamp = db.DateTimeProperty(required = True)
  user = db.ReferenceProperty(User)
  data = db.StringProperty()

  @staticmethod
  def log(action, user = None, data = None):
    event = ActionLog(action = action, timestamp = datetime.now())

    if data != None:
      event.data = data
    if user != None:
      event.user = user

    event.put()

  @staticmethod
  def get(action = None, user = None, timewindow = None):
    results = ActionLog.all()
    if action != None:
      results.filter('action =', action)
    if user != None:
      results.filter('user =', user)
    if timewindow != None:
      results.filter('timestamp >', timewindow)

    return results

class Globals(db.Model):
  k = db.StringProperty()
  v = db.StringProperty()

  @staticmethod
  def get(k):
    gvar = Globals.all().filter('k =', k).get()
    if gvar == None:
      return None
    return gvar.v

class TemplateMetric(db.Model):
  format = db.StringProperty(required=True, 
    choices = ('text', 'number', 'time'))
  frequency = db.IntegerProperty(required=True)
  name = db.StringProperty(required=True)
  normalized_name = db.StringProperty(required=True)
  text = db.StringProperty(required=True)

  @staticmethod
  def json_list():
    template_metrics = TemplateMetric.all().fetch(1000)

    tms = {}
    for tm in template_metrics:
      tms[tm.name.lower()] = tm.as_dict()

    return json.dumps(tms)

  def as_dict(self):
    return {'name': self.name,
            'frequency': self.frequency,
            'format': self.format,
            'text': self.text,
            'template_id': str(self.key())}

class Query(db.Model):
  format = db.StringProperty(required=True, 
    choices = ('text', 'number', 'time'))
  user = db.ReferenceProperty(User)
  # the frequency at which to send the query
  frequency = db.IntegerProperty(required=True)
  # when to try and send the query, subset of {morning, afternoon, evening}
  ask_when = db.StringListProperty()
  # the last time we sent this query
  lastSentAt = db.DateTimeProperty(required=True, auto_now_add=True)
  name = db.StringProperty(required=True)
  normalized_name = db.StringProperty(required=True)
  text = db.StringProperty(required=True)
  template = db.ReferenceProperty(TemplateMetric, required=False)

  @staticmethod
  def get_by_id(id):
    return db.get(id)

  @staticmethod
  def get_by_user(user):
    return Query.all().filter('user =', user).fetch(1000)
 
  @staticmethod 
  def get_by_user_and_name(user, name):
    return Query.all().filter('user =', user).filter('normalized_name =', Query.normalize_name(name)).get()

  @staticmethod
  def normalize_name(name):
    return name.lower().strip()

  def is_time_to_send(self):
    now = int(datetime.now().strftime('%s'))

    if 'morning' in self.ask_when and is_morning(now):
      return True
    elif 'afternoon' in self.ask_when and is_afternoon(now):
      return True
    elif 'evening' in self.ask_when and is_evening(now):
      return True

    return False
    
  def is_stale(self):
    if datetime.now() > self.lastSentAt + timedelta(minutes=self.frequency):
      return True
    return False

  def refresh(self):
    logging.info("Refreshing query: " + self.name)
    self.lastSentAt = datetime.now()
    self.put()
    

class DataPoint(db.Model):
  text = db.StringProperty(required=True)
  query = db.ReferenceProperty(Query)
  timestamp = db.DateTimeProperty(required=True)

  def lt_put(self):
    # update the metrics's modified timestamp in memcache
    mck_metric_last_update = str(self.query.key()) + '.last-update'
    now = datetime.now().strftime("%s")

    memcache.set(
      key=mck_metric_last_update, 
      value=now,
      time=86400
    )

    # then put the datapoint
    self.put()

  def lt_delete(self):
    # update the metrics's modified timestamp in memcache
    mck_metric_last_update = str(self.query.key()) + '.last-update'
    now = datetime.now().strftime("%s")

    memcache.set(
      key=mck_metric_last_update, 
      value=now,
      time=86400
    )

    # then delete the datapoint
    self.delete()

  @staticmethod
  def get_by_query(query, quantity=1000):
    return DataPoint.all().filter('query = ', query).order('timestamp').fetch(1000)

  @staticmethod
  def get_by_query_most_recent(query):
    return DataPoint.all().filter('query = ', query).order('-timestamp').fetch(1)
    
  def get_as_dict(self):
    return {'text': self.text, 'query': str(self.query.key()), 'timestamp': self.timestamp_as_int()}

  def timestamp_as_int(self):
    return int(self.timestamp.strftime("%s"))

  def as_float(dp): # I may be breaking standards here
    # need to surround this with try brackets
    text_float = ''

    try:
      text_float = float(dp.text)
    except ValueError:
      text_float = 0.0
    
    return text_float

