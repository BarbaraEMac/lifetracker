
from google.appengine.ext import webapp
from google.appengine.api import users

from django.utils import simplejson as json

from model import User, TemplateMetric
from lthandler import LTHandler
from constants import whitelist
from utils.track_walltime import track_walltime

class NoInviteHandler(LTHandler):
  @track_walltime
  def get(self):
    html = open('ui/html/no_invite.html').read()
    self.response.out.write(html)
