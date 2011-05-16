from google.appengine.ext import webapp
from google.appengine.api import users

from analytics.analytics import analyze_query_data
from model import User, Query, DataPoint

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

      html_file = open("ui/html/analyze.html")
      html = html_file.read()

      query_id = self.request.get('query_id')
      query = Query.get_by_id(query_id)

      analytics = analyze_query_data(query)
      analytics_html = self.generate_analysis_view(analytics)

      html = html % {'analytics_rows': analytics_html, 'logout_url': logout_url, 'user_email': user.email, 'query_name': query.name}

      self.response.out.write(html)

  #def stat_to_row(self, analytic):
  def stat_to_row(self, name, value):
    #return "<tr><td>%(name)s</td><td>%(value)s</td></tr>" % {'name': analytic['name'], 'value': analytic['value']}
    return "<tr><td>%(name)s</td><td>%(value)s</td></tr>" % {'name': name, 'value': value}

  def generate_analysis_view(self, analytics):
    html = ''
    # we could make analytics a simple map
    # then we could do:
    # for key, value in analytics
    #   ...
    """for analytic in analytics:
      html += self.stat_to_row(analytic)"""
    for (name, value) in sorted(analytics.items()):
      html += self.stat_to_row(name, value)
    return html
