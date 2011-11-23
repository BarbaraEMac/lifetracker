from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.api import mail

from datetime import datetime

from model import User, Query, DataPoint, ActionLog
from lthandler import LTHandler

from sms import send_sms
from utils.time import is_daytime

import logging

def send_by_email(query):
  # get the user
  user = query.user
  subject = query.name
  to = user.email
  sender = 'Lifetracker <data@lifetrckr.appspotmail.com>'
  # construct the message
  body = query.text

  params = {
    'query_id': str(query.key()),
    'query_text': query.text,
  }

  body = open('ui/html/email_form.html').read() % params
      
  # send the message
  message = mail.EmailMessage(
    sender = sender,
    subject = subject,
    to = to,
    html = body)

  message.send()

  ActionLog.log('SentEmail')

def send_query_by_sms(query):
  text = query.text + ' Please reply "' + query.name + ': value"'
  send_sms(query.user.phone, text)  

  ActionLog.log('SentSMS')

def send_query(query):
  if query.user.query_medium == 'sms':
    send_query_by_sms(query)
  else:
    send_by_email(query)

  logging.info("Sent Query: " + query.name + " for user " + query.user.email)
  query.lastSentAt = datetime.now() # refresh the query
  query.put() # commit it

  ActionLog.log('SentQuery')

# it will be a problem if this takes a long time
class SendQueriesHandler(LTHandler):
  def get(self):
    start = datetime.now().strftime('%s')
    users = User.all().fetch(1000)

    for user in users:
      queries = Query.get_by_user(user)
      for query in queries:
        if query.is_stale() and query.is_time_to_send():
          send_query(query)
          break # only send one query per user every interval

    end = datetime.now().strftime('%s')

    logging.info('SendQueries started at ' + start)
    logging.info('SendQueries finished at ' + end)
