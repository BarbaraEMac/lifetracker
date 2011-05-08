from google.appengine.ext import db
from google.appengine.api import users

from datetime import datetime
from datetime import timedelta

class User(db.Model):
  google_user = db.UserProperty()
  first_name = db.StringProperty()
  email = db.StringProperty()
  
  @staticmethod
  def get_by_google_user(google_user):
    return User.all().filter('google_user =', google_user).get()

  @staticmethod
  def get_by_email(email):
    return User.all().filter('email =', email).get()

  def get_by_first_name(name):
    return User.all().filter('first_name =', first_name).get()

class Query(db.Model):
  format = db.StringProperty(required=True, 
    choices = ('text', 'integer', 'time'))
  user = db.ReferenceProperty(User)
  # the frequency at which to send the query
  frequency = db.IntegerProperty(required=True)
  # the last time we sent this query
  lastSentAt = db.DateTimeProperty(required=True, auto_now_add=True)
  name = db.StringProperty(required=True)
  text = db.StringProperty(required=True)
 
  @staticmethod
  def get_by_id(id):
    return db.get(id)

  @staticmethod
  def get_by_user(user):
    return Query.all().filter('user =', user).fetch(1000)

  def isStale(self):
    if datetime.now() > self.lastSentAt + timedelta(minutes=self.frequency):
      return True
    return False
    

class DataPoint(db.Model):
  text = db.StringProperty(required=True)
  query = db.ReferenceProperty(Query)
  timestamp = db.DateTimeProperty(required=True)

  @staticmethod
  def get_by_query(query, quantity=1000):
    return DataPoint.all().filter('query = ', query).fetch(1000)

  def get_as_dict(self):
    return {'text': self.text, 'query': str(self.query.key()), 'timestamp': self.timestamp.strftime("%s")}

