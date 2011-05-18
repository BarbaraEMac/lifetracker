from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.api import mail

from datetime import datetime

from model import User, Query, DataPoint
from sms import send_sms
from analytics.multi_analytics import nearest_day

from datetime import datetime

def send_by_email(query):
  # get the user
  user = query.user
  subject = query.name
  to = user.email
  sender = 'Lifetracker <data@lifetrckr.appspotmail.com>'
  # construct the message
  body = query.text

  # send the message
  message = mail.EmailMessage(
    sender = sender,
    subject = subject,
    to = to,
    html = body)

  message.send()

def send_query_by_sms(query):
  text = query.text + ' Please reply "query-name: value"'
  send_sms(query.user.phone, text)  

def send_query(query):
  if query.user.query_medium == 'sms':
    send_query_by_sms(query)
  else:
    send_by_email(query)

  query.lastSentAt = datetime.now() # refresh the query
  query.put() # commit it

def morning(timestamp):
  return nearest_day(timestamp) + 10*60*60 # 10 am

def nighttime(timestamp):
  return nearest_day(timestamp) + 23*60*60 + 59*60 # 23:59

def is_daytime():
  # if it is between 10 am and midnight
  now = datetime.now()
  if now > morning(now) and now < nighttime(now):
    return True
  else:
    return False

# it will be a problem if this takes a long time
class SendQueriesHandler(webapp.RequestHandler):
  def get(self):
    self.response.out.write("Cronning this fucker!")

    queries = Query.all().fetch(1000)

    for query in queries:
      if query.is_stale() && is_daytime(): # only send when people are wake
        print query.name + " is stale"
        send_query(query)
        return


