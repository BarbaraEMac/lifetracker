from google.appengine.ext import webapp
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler
from google.appengine.api import mail

from datetime import datetime

from model import User, Query, DataPoint, ActionLog

import logging, email

def forward_to_users(incoming_message):
  sender = incoming_message.sender
  to = ''
  html = ''
  subject = incoming_message.subject

  users = User.all()
  for user in users:
    to += user.email + ', '

  for content_type, body in incoming_message.bodies('text/html'):
    html = body.decode()

  message = mail.EmailMessage(
    sender = incoming_message.sender,
    to = to,
    subject = incoming_message.subject,
    html = html)

  message.send()

def forward_to_admins(incoming_message):
  html = ''
  for content_type, body in incoming_message.bodies('text/html'):
    html = body.decode()

  message = mail.EmailMessage(
    sender = incoming_message.sender,
    to = 'gareth.macleod@gmail.com',
    subject = incoming_message.subject,
    html = html)

  message.send()

# TODO: put this in a common utility class
def is_admin(user):
  if user.email == 'gareth.macleod@gmail.com':
    return True
  return False

class EmailResponseHandler(InboundMailHandler):
  def receive(self, mail_message):
    # we need to make a new data point

    # get the user from the sender field
    user_email = mail_message.sender[ mail_message.sender.find('<') + 1 : mail_message.sender.rfind('>') ]
    user = User.get_by_email(user_email)

    if is_admin(user) and mail_message.to.find('users@') != -1:
      forward_to_users(mail_message)
      return

    if mail_message.to.find('feedback@') != -1:
      forward_to_admins(mail_message)
      return

    # get the datapoint from the body
    data = ''
    query_name = mail_message.subject[ mail_message.subject.rfind("Re:") + 4: ]
  
    query = Query.get_by_user_and_name(user, query_name)

    for content_type, body in mail_message.bodies('text/html'):
      data = body.decode()[ : body.decode().find('<')]

    # get the time from now()
    timestamp = datetime.now()

    log_str = "Want to create a new datapoint for user %s and with value %s and query name %s and query %s and timestamp %s" % (user_email, data, query_name, query.key(), timestamp)

    logging.info("Received a message from " + mail_message.sender)
    logging.info(log_str)

    # create and put the datapoint
    # dp = DataPoint(...)
    dp = DataPoint( 
      text = data,
      query = query,
      timestamp = timestamp)
      
    dp.put()
    ActionLog.log('ReceivedEmail')
    ActionLog.log('NewDatapoint', query.name, user=user)

    query.refresh()
