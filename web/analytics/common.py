from model import User, Query, DataPoint

weekdays = {
  0: 'Monday',
  1: 'Tuesday',
  2: 'Wednesday',
  3: 'Thursday',
  4: 'Friday',
  5: 'Saturday',
  6: 'Sunday',
}

def query_average(query):
  datapoints = DataPoint.get_by_query(query)
  return average(datapoints)

def average(datapoints):
  if len(datapoints) == 0:
    return None

  sum = 0
  
  for dp in datapoints:
    sum += float(dp.text)

  average = sum/len(datapoints)

  return average
