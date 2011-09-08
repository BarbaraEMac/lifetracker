import logging
from google.appengine.ext import webapp
from datetime import datetime

from model import User, Query, DataPoint

import twilio

API_VERSION = '2010-04-01'

ACCOUNT_SID = 'ACa777d270a2a38c86e85047b3dbb67df0'
ACCOUNT_TOKEN = 'b219417b1407f177de18c4a24c50dea2'

CALLER_ID = '6502048725'

account = twilio.Account(ACCOUNT_SID, ACCOUNT_TOKEN) 

def send_sms(toNumber, text):
  data = {
    'From': CALLER_ID,
    'To': str(toNumber),
    'Body': text,
  }

  try:  
    account.request('/%s/Accounts/%s/SMS/Messages' \
    % (API_VERSION, ACCOUNT_SID), 'POST', data)
  except Exception, e:
    logging.info(e)


# we should probably have some security on this thang
class ReceiveSMSHandler(webapp.RequestHandler):
  def post(self):
    sender_phone = self.request.get('From')
    body = self.request.get('Body')

    # normalize the phone number to 10 digits
    # '+12268681112' => '2268681112'
    sender_phone = sender_phone[len(sender_phone) - 10:]
    logging.info('Got text from ' + sender_phone)

    # get the user
    user = User.get_by_phone(sender_phone)
    if not user:
      logging.error("Couldn't get the user for phone: " + sender_phone)
      return

    # parse the response
    query_value_pairs = self.parse_body(body)

    for query_name in query_value_pairs:
      value = query_value_pairs[query_name]

      if query_name == '' or value == '':
        logging.error('Got a bad response');
        return

      query = Query.get_by_user_and_name(user, query_name)

      if not query:
        logging.error("Couldn't get query for user " + user.email + ' and query ' + query.name)
        continue

      timestamp = datetime.now()
      
      dp = DataPoint(
        user = user,
        query = query,
        text = value,
        timestamp = timestamp,
      )

      dp.put()

      query.refresh()

      logging.info('Received datapoint ' + query_name + ': ' + value + '\n')

    self.response.out.write('<Response><Sms>Got it!</Sms></Response>')


  # need some validation in here too
  def parse_body(self, response):
    pairs = response.split(';')
    query_value_pairs = {}

    for pair in pairs:
      try: 
        query_name = pair [ : pair.index(':')]
        value = pair[pair.index(':') + 1:]
        query_value_pairs[query_name] = value
      except Exception, e:
        logging.error(e)
        continue 
        #return '', ''

      logging.info('Parsed response: ' + query_name + ': ' + value)

    return query_value_pairs

