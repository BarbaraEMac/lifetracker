from google.appengine.ext import webapp
from google.appengine.api import users

from model import User, Query, DataPoint, TemplateMetric, ActionLog, InviteCode

from analytics.analytics import overview
from constants import whitelist, admins
import logging

# This logic is kinda spaghetti-code right now.
# This will return a user object if the user is authorized to view the
# page, or None and redirect to /no-invite otherwise.
class LTHandler(webapp.RequestHandler):
  def get_user(self, invite_code_name=None):
    user = None

    google_user = users.get_current_user()

    # not logged in to google
    if google_user == None:
      self.redirect(users.create_login_url(self.request.uri))
      return None

    user = User.get_by_google_user(google_user)

    # user was not in our database, so its a first-time login
    if user == None:
      user = User(google_user = google_user, 
        first_name='', 
        last_name='', 
        email=google_user.email()
      )

      user.put() 

    # now we have a user, but are they whitelisted 
    # or do they have an invite?

    if invite_code_name != None:
      invite_code = InviteCode.get_by_name(invite_code_name)

      # is this code valid?
      if invite_code != None and invite_code.use_code() == True:
        user.is_whitelisted = True
        user.put()
      else: 
        user = None
    elif user.is_whitelisted != True:
      user = None

    # this enables admins to see pages in any user's context
    if self.request.get('admin', None) == 'true' and user.email in admins:
      user_email = self.request.get('user_email')
      user = User.get_by_email(user_email)

    # if we've gotten this far and the user is none, it means this user is 
    # not whitelisted
    if user == None:
      self.redirect(users.create_logout_url('/no-invite'))

    return user

class LoggedInPageHandler(LTHandler):
  styles = []
  scripts = []

  def render_page(self, html_file, params):
    content_html = open(html_file).read() % params

    js = self.render_js()
    css = self.render_css()

    logout_url = users.create_logout_url(self.request.uri)

    template_html = open('ui/html/template.html').read() 

    template_params = {
      'css': css, 
      'js': js, 
      'page_content': content_html, 
      'logout_url': logout_url}

    html = template_html % template_params

    return html

  def register_css(self, css_list):
    self.styles = css_list

  def register_js(self, script_list):
    self.scripts = script_list

  def render_css(self):
    css_html = ''
    for css_file in self.styles:
      css_html += self.link_tag(css_file) + "\n  "
    return css_html

  def render_js(self):
    js_html = ''
    for js_file in self.scripts:
      js_html += self.script_tag(js_file) + "\n  "
    return js_html

  def link_tag(self, css_file):
    return '<link rel="stylesheet" type="text/css" href="css/%(filename)s"/>' % {'filename': css_file}

  def script_tag(self, js_file):
    if js_file.find('http://') == 0 or js_file.find('https://') == 0:
      return '<script src="%(filename)s" type="text/javascript"></script>' % {'filename': js_file}
    else:
      return '<script src="js/%(filename)s" type="text/javascript"></script>' % {'filename': js_file}


