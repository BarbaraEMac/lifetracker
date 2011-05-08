from google.appengine.ext import db
from google.appengine.ext import webapp

from google.appengine.api import mail

from model import User, Query, DataPoint

from datetime import datetime

def SendByEmail(query):
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

def SendByAndroidPush(query):
  return ''

def SendQuery(query):
  query.lastSentAt = datetime.now() # refresh the query
  query.put() # commit it
  return SendByEmail(query)

# it may be a problem if this takes a long time
class SendQueriesHandler(webapp.RequestHandler):
  def get(self):
    self.response.out.write("Cronning this fucker!")

    queries = Query.all().fetch(1000)

    for query in queries:
      if query.isStale():
        print query.name + " is stale"
        SendQuery(query)
        return


