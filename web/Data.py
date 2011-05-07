from google.appengine.ext import webapp

from model import User, Query, DataPoint

class NewQueryHandler(webapp.RequestHandler):
  def post(self):
    self.response.out.write("Done")

# called to add a datapoint to a user's dataset
# To hit this, send a post to "{base-url}/response" with
# data question_id, user_id, data, and a timestamp
class NewDataPointHandler(webapp.RequestHandler):
  def post(self):
    query_id = self.request.get('question')
    user_id = self.request.get('user')
    data = self.request.get('data')
    time = self.request.get('time', '')

    # get the question from the DB
    # get the user from the DB
    # add a Response object to the DB
    
    user = User.get_by_google_user(user_id)
    query = db.get(query_id) #hmmm

    dataPoint = DataPoint(
      text = data,
      question = question,
    )

    dataPoint.put()

    self.response.out.write("Got it boss.\n")

class GetQueriesHandler(webapp.RequestHandler):
  def get(self):
    self.response.out.write("Done")

class GetDataPointsHandler(webapp.RequestHandler):
  def get(self):
    self.response.out.write("Done")
