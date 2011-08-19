from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.api import mail

from datetime import datetime

from model import User, Query, DataPoint
from sms import send_sms
from utils.time import is_daytime

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
  text = query.text + ' Please reply "' + query.name + ': value"'
  send_sms(query.user.phone, text)  

def send_query(query):
  if query.user.query_medium == 'sms':
    send_query_by_sms(query)
  else:
    send_by_email(query)

  query.lastSentAt = datetime.now() # refresh the query
  query.put() # commit it

# it will be a problem if this takes a long time
class SendQueriesHandler(webapp.RequestHandler):
  def get(self):
    users = User.all().fetch(1000)

    for user in users:
      queries = Query.get_by_user(user)
      for query in queries:
        now = int(datetime.now().strftime('%s'))
        if query.is_stale() and is_daytime(now):
          send_query(query)
          break # only send one query per user every interval

