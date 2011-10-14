from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.api import users

from model import User, Query, DataPoint
from lthandler import LoggedInPageHandler
from constants import whitelist

class ExportDataHandler(LoggedInPageHandler):
  def get(self):
    user = self.get_user()
    if not user:
      return

    query_id = self.request.get('query_id', None)
    query = db.get(query_id)

    params = {
      'user_email': user.email, 
      'query_id': query_id, 
      'query_name': query.name,
    }

    self.register_css(['export_data.css']) 
    self.register_js(['export.js'])

    html = self.render_page('ui/html/export_data.html', params)

    self.response.out.write(html)


