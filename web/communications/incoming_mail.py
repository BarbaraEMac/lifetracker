import logging, email
from google.appengine.ext import webapp
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler

from datetime import datetime

from model import User, Query, DataPoint

class EmailResponseHandler(InboundMailHandler):
  def receive(self, mail_message):
    # we need to make a new data point

    # get the user from the sender
    user_email = mail_message.sender[ mail_message.sender.find('<') + 1 : mail_message.sender.rfind('>') ]
    user = User.get_by_email(user_email)
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
