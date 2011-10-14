from google.appengine.ext import webapp
from google.appengine.api import users

from model import User, Query, DataPoint
from lthandler import LoggedInPageHandler
from constants import whitelist

class ImportDataHandler(LoggedInPageHandler):
  def get(self):
    user = self.get_user()
    if not user:
      return
      
    query_id = self.request.get('query_id', None)
    
    params = {
      'user_email': user.email, 
      'query_id': query_id,
    }

    self.register_css(['import_data.css'])

    html = self.render_page('ui/html/import_data.html', params)

    self.response.out.write(html)
