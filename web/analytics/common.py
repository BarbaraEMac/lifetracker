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
  sum = 0
  
  for dp in datapoints:
    sum += int(dp.text)

  average = float(sum)/len(datapoints)

  return average
