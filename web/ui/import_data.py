from google.appengine.ext import webapp
from google.appengine.api import users

from model import User, Query, DataPoint
from lthandler import LTHandler
from constants import whitelist

class ImportDataHandler(LTHandler):
  def get(self):
    user = self.get_user()
    if not user:
      return
      
    logout_url = users.create_logout_url(self.request.uri)

    html_file = open("ui/html/import_data.html")
    html = html_file.read()

    query_id = self.request.get('query_id', None)
    
    # generate the query table
    html = html % {'logout_url': logout_url, 'user_email': user.email, 'query_id': query_id}

    self.response.out.write(html)
