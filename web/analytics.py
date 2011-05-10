import logging, math

from model import User, Query, DataPoint

def AnalyzeQueryData(query):
  #logging.info('Query_id: ' + query_id + "\n")
  if query.format == 'integer':
    return AnalyzeIntegerQueryData(query)
  else:
    return [{'name': '', 'value': ''}]

def AnalyzeIntegerQueryData(query):
  return [
          {'name': 'Average', 'value': str(Average(query))},
          {'name': 'Variance', 'value': str(Variance(query))},
          {'name': 'Standard Deviation', 'value': str(StandardDeviation(query))},
          {'name': 'PeaksOnDay', 'value': str(PeaksOnDay(query))},
          {'name': 'Monday Average', 'value': str(DayAvg(query, 0))}]

def Average(int_query):
  datapoints = DataPoint.get_by_query(int_query)

  sum = 0
  
  for dp in datapoints:
    sum += int(dp.text)

  average = sum/len(datapoints)

  return average

def Variance(int_query):
  datapoints = DataPoint.get_by_query(int_query)

  mu = Average(int_query)
  squaresum = 0
 
  for dp in datapoints:
    squaresum += (int(dp.text)-mu)*(int(dp.text)-mu)

  sigma = squaresum/len(datapoints)

  return sigma

def StandardDeviation(int_query):
  return math.sqrt(Variance(int_query))
 
# returns the day the query is the highest 
def PeaksOnDay(int_query):
  # for each day of the week, calculate the average of the metric on those days and return the highest

  dayAvgs = {}
  for day in range(0,7):
    dayAvgs[str(day)] = DayAvg(int_query, day)

  dayMax = 0
  maxOnDay = 0

  return max(dayAvgs)

def DayAvg(int_query, day):
  datapoints = DataPoint.get_by_query(int_query)

  daySum = 0
  days = 0
 
  for dp in datapoints:
    if dp.timestamp.weekday() == day:
      daySum += int(dp.text)
      days += 1

  return daySum/days  



