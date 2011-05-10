from google.appengine.ext import webapp
from google.appengine.api import users

from model import User, Query, DataPoint
from analytics import AnalyzeQueryData

class AnalyzeDataHandler(webapp.RequestHandler):
  def get(self):
    google_user = users.get_current_user()
    if google_user == None:
      self.redirect(users.create_login_url(self.request.uri))
    else:
      user = User.get_by_google_user(google_user)
      if user == None:
        user = User(google_user = google_user, 
          first_name='', 
          last_name='', 
          email=google_user.email()
        )

        user.put()
      
      logout_url = users.create_logout_url(self.request.uri)

      html_file = open("ui/analyze.html")
      html = html_file.read()

      query_id = self.request.get('query_id')
      query = Query.get_by_id(query_id)

      analytics = AnalyzeQueryData(query)
      analytics_html = self.GenerateAnalysisView(analytics)

      html = html % {'analytics_rows': analytics_html, 'logout_url': logout_url, 'user_email': user.email, 'query_name': query.name}

      self.response.out.write(html)

  def StatToRow(self, analytic):
    return "<tr><td>%(name)s</td><td>%(value)s</td></tr>" % {'name': analytic['name'], 'value': analytic['value']}

  def GenerateAnalysisView(self, analytics):
    html = ''
    for analytic in analytics:
      html += self.StatToRow(analytic) 
    return html