from google.appengine.ext import webapp

class HomeHandler(webapp.RequestHandler):
  def get(self):
      html_file = open("ui/home.html")
      html = html_file.read()

      self.response.out.write(html)
