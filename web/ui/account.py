from google.appengine.ext import webapp
from google.appengine.api import users

from model import User, Query, DataPoint
from lthandler import LTHandler
from constants import whitelist

class AccountHandler(LTHandler):
  def get(self):
    user = self.get_user()
    if not user:
      return
      
    logout_url = users.create_logout_url(self.request.uri)

    html_file = open("ui/html/account.html")
    html = html_file.read()

    sms_selected = ''
    email_selected = ''
    
    if user.query_medium == 'email':
      email_selected = 'selected'
    else:
      sms_selected = 'selected'

    # generate the query table
    html = html % {'logout_url': logout_url, 'user_email': user.email, 'user_phonenumber': user.phone, 'sms_selected': sms_selected, 'email_selected': email_selected}

    self.response.out.write(html)
