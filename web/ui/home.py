from google.appengine.ext import webapp
from google.appengine.api import users

from django.utils import simplejson as json

from model import User, TemplateMetric
from lthandler import LTHandler
from constants import whitelist
from utils.track_walltime import track_walltime

class HomeHandler(LTHandler):
  @track_walltime
  def get(self):
    google_user = users.get_current_user()
    if google_user != None:
      user = User.get_by_google_user(google_user)
      if user != None and user.is_whitelisted:
        self.redirect('/dashboard');
      else:
        self.redirect(users.create_logout_url('/no-invite'))
      

    f = open('ui/html/home.html')
    html = f.read()

    login_url = users.create_login_url(self.request.uri)

    params = {
      'login_url': login_url,
      'template_metrics': TemplateMetric.json_list()
    }

    html = html % params

    self.response.out.write(html)
      
