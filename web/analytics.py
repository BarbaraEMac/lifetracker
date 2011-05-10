import logging, math

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
          {'name': 'Peaks On', 'value': str(PeaksOnDay(query))},
          {'name': 'Monday Average', 'value': str(DayAvg(query, 0))},
          {'name': 'Tuesday Average', 'value': str(DayAvg(query, 1))},
          {'name': 'Wednesday Average', 'value': str(DayAvg(query, 2))},
          {'name': 'Thursday Average', 'value': str(DayAvg(query, 3))},
          {'name': 'Friday Average', 'value': str(DayAvg(query, 4))},
          {'name': 'Saturday Average', 'value': str(DayAvg(query, 5))},
          {'name': 'Sunday Average', 'value': str(DayAvg(query, 6))},
        ]

def AnalyzeTextQueryData(query):
  return [{}]

def MostCommonWord(query):
  # map reduce this shit
  return ''


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
  maxDayAvg = 0
  maxOnDay = 0

  for day in range(0,7):
    if DayAvg(int_query, day) > maxDayAvg:
      maxOnDay = day
      maxDayAvg = DayAvg(int_query, day)

  return weekdays[maxOnDay]

def DayAvg(int_query, day):
  datapoints = DataPoint.get_by_query(int_query)

  daySum = 0
  days = 0
 
  for dp in datapoints:
    if dp.timestamp.weekday() == day:
      daySum += int(dp.text)
      days += 1

  return daySum/days  



