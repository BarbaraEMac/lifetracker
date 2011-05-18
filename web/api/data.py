from google.appengine.ext import db
from google.appengine.ext import webapp

from datetime import datetime
from django.utils import simplejson as json

from model import User, Query, DataPoint

class NewQueryHandler(webapp.RequestHandler):
  def post(self):
    name = self.request.get("name")
    frequency = int(self.request.get("frequency"))
    text = self.request.get('text')
    user_email = self.request.get('user_email')
    format = self.request.get('format')

    user = User.get_by_email(user_email)

    query = Query(
      name = name,
      # we should really do normalization inside the Query constructor,
      # but it will take some time to figure out how, lacking a nearby
      # python badass
      normalized_name = Query.normalize_name(name), 
      text = text,
      frequency = frequency,
      user = user,
      format = format,
    )

    query.put()

class EditQueryHandler(webapp.RequestHandler):
  def post(self):
    query_id = self.request.get('query_id')
    name = self.request.get('name', None)
    frequency = self.request.get('frequency', None)
    text = self.request.get('text', None)
    #user_email = self.request.get('user_email', None) #hmm
    #format = self.request.get('format', None) #hmm

    query = db.get(query_id)
    if not query:
      self.response.out.write('failure!')
      return

    if name:
      query.name = name
    if frequency:
      query.frequency = int(frequency)
    if text:
      query.text = text

    query.put()
    
    self.response.out.write("success")

class DeleteQueryHandler(webapp.RequestHandler):
  def post(self):
    query_id = self.request.get('query_id')

    query = db.get(query_id)
    if not query:
      self.response.out.write('failure!')
      return
   
    # delete all the datapoints associated with the query as well.
    datapoints = DataPoint.get_by_query(query)

    for dp in datapoints:
      dp.delete()

    # finally, delete the query 
    query.delete()
  
# called to add a datapoint to a user's dataset
# To hit this, send a post to "{base-url}/response" with
# data question_id, user_id, data, and a timestamp
class NewDataPointHandler(webapp.RequestHandler):
  def post(self):
    query_id = self.request.get('query_id')
    #user_email = self.request.get('user')
    data = self.request.get('data')
    time = self.request.get('time') #self.request.get('time', '')

    # get the question from the DB
    # get the user from the DB
    # add a Response object to the DB
    
    #user = User.get_by_email(user_email)
    query = db.get(query_id) #hmmm

    dataPoint = DataPoint(
      text = data,
      query = query,
      timestamp = datetime.now()
    )

    dataPoint.put()

    self.response.out.write('success')

class GetQueriesHandler(webapp.RequestHandler):
  def get(self):
    user_email = self.request.get('user_email')
    
    user = User.get_by_email(user_email)

    queries = Query.get_by_user(user)

    query_ids = []
    for query in queries:
      query_ids.append(str(query.key()))

    self.response.out.write(json.dumps(query_ids))

# TODO: more filters for the datapoints.
#   get only for some query
#   get only for some time-range
class GetDataPointsHandler(webapp.RequestHandler):
  def get(self):
    user_email = self.request.get('user_email')
    
    user = User.get_by_email(user_email)
    queries = Query.get_by_user(user)

    datapoints = []

    for query in queries:
      for datapoint in DataPoint.get_by_query(query):
        datapoints.append(datapoint.get_as_dict())

    self.response.out.write(json.dumps(datapoints))

class ImportCSVHandler(webapp.RequestHandler):
  def post(self):
    user_email = self.request.get('user_email')
    query_id = self.request.get('query_id')
    csv_data = self.request.get('csv_data')

    user = User.get_by_email(user_email)
    query = Query.get_by_id(query_id)

    for duple in self.parse_csv_data(csv_data):
      timestamp = duple[0]
      text = duple[1]

      # for testing
      self.response.out.write("<p>%s: %s\n</p>" % (timestamp, text))

      dp = DataPoint(
        timestamp = duple[0],
        query = query,
        text = duple[1])
    
      dp.put()

    self.redirect('/data')

  def parse_csv_data(self, csv_data):
    # split into lines
    # for each line
    #   split into timestamp and datapoint
    # add to a list and return
    duples = []

    lines = csv_data.split('\n')
    for line in lines:
      splitline = line.split(',')
      duple = (datetime.fromtimestamp(int(splitline[0])), splitline[1])
      duples.append(duple)

    return duples

    self.response.out.write('success!')