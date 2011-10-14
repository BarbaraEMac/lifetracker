from google.appengine.ext import webapp
from google.appengine.api import users

from model import User, Query, DataPoint
from lthandler import LoggedInPageHandler
from constants import whitelist

class AccountHandler(LoggedInPageHandler):
  def get(self):
    user = self.get_user()
    if not user:
      return
      
    sms_selected = ''
    email_selected = ''
    
    if user.query_medium == 'email':
      email_selected = 'selected'
    else:
      sms_selected = 'selected'

    # generate the query table
    params = {
      'user_email': user.email, 
      'user_phonenumber': user.phone, 
      'sms_selected': sms_selected, 
      'email_selected': email_selected,
    }

    self.register_css(['account.css'])
    self.register_js(['account.js'])

    html = self.render_page('ui/html/account.html', params)

    self.response.out.write(html)
