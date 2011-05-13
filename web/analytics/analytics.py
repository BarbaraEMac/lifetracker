import logging, math
from datetime import datetime, timedelta

from model import User, Query, DataPoint

from multi_analytics import Covariance, AvgIntOnSlicedInt, PercentFromAvgIntOnSlicedInt 

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
  if query.format == 'integer':
    return AnalyzeIntegerQueryData(query)
  elif query.format =='time':
    return AnalyzeTimeQueryData(query)
  elif query.format == 'text':
    return AnalyzeTextQueryData(query)
  else:
    return [{'name': '', 'value': ''}]

def AnalyzeTextQueryData(query):
  datapoints = DataPoint.get_by_query(query)
  return [{'name': 'Common words', 'value': CommonWords(datapoints)}]

# we can probably map reduce this shit
def CommonWords(datapoints):
  word_counter = {}

  # foreach datapoint
    # tokenize the text
    # add each word into word_counter
  for dp in datapoints:
    words = dp.text.split()
    for word in words:
      logging.info('Word: ' + word)
      if word in word_counter:
        word_counter[word] = word_counter[word] + 1
      else:
        word_counter[word] = 1
  
  # find the three highest word counts in word_counter
  popular = sorted(word_counter, key = word_counter.get, reverse = True)

  # return the top three
  return popular[0] + ', ' + popular[1] + ', ' + popular[2]



def AnalyzeTimeQueryData(query):
  datapoints = DataPoint.get_by_query(query)
  return [
    {'name': 'Average Time', 'value': AverageTime(datapoints)},
    {'name': 'Peaks on Day', 'value': HighestDayAverageTime(datapoints)},
    {'name': 'Lowest on Day', 'value': LowestDayAverageTime(datapoints)},
    {'name': 'Average Time on Monday', 'value': AverageTimeOnDay(datapoints,0)},
    {'name': 'Average Time on Tuesday', 'value': AverageTimeOnDay(datapoints,1)},
    {'name': 'Average Time on Wednesday', 'value': AverageTimeOnDay(datapoints,2)},
    {'name': 'Average Time on Thursday', 'value': AverageTimeOnDay(datapoints,3)},
    {'name': 'Average Time on Friday', 'value': AverageTimeOnDay(datapoints,4)},
    {'name': 'Average Time on Saturday', 'value': AverageTimeOnDay(datapoints,5)},
    {'name': 'Average Time on Sunday', 'value': AverageTimeOnDay(datapoints,6)},
    ]

def StringToTimeDelta(string):
  # assume every dp is x:y
  hours = int(string[ : string.find(':') ])
  minutes = int(string[string.find(':') + 1 : ])

  if hours == '':
    hours = 0
  if minutes == '':
    minutes = 0

  # here we're assuming if a time is before 6, it is pm. 
  # this is a shaky assumption and should be revisited soon.
  if hours < 6:
    hours +=12

  return timedelta(hours=int(hours), minutes=int(minutes))

def timedelta_total_seconds(td):
  return td.seconds + td.days*86400

def AverageTime(datapoints):
  # interpret each datapoint as a timedelta
  # then average them

  totSeconds = 0
  for dp in datapoints:
    totSeconds += timedelta_total_seconds(StringToTimeDelta(dp.text))

  avgSeconds = totSeconds / len(datapoints)

  return timedelta(seconds=avgSeconds)

def HighestDayAverageTime(datapoints):
  highestDay = 0
  highestDayAvg = timedelta(seconds=0 )

  for day in range(0,7):
    if AverageTimeOnDay(datapoints,day) > highestDayAvg:
      highestDay = day
      highestDayAvg = AverageTimeOnDay(datapoints,day)
    
  return weekdays[highestDay]

def LowestDayAverageTime(datapoints):
  lowestDay = 0
  lowestDayAvg = AverageTimeOnDay(datapoints,0)

  for day in range(1,7):
    if AverageTimeOnDay(datapoints,day) < lowestDayAvg:
      lowestDay = day
      lowestDayAvg = AverageTimeOnDay(datapoints,day)
    
  return weekdays[lowestDay]
  
def AverageTimeOnDay(datapoints,day):
  totSeconds = 0
  days = 0
  for dp in datapoints:
    if dp.timestamp.weekday() == day:
      totSeconds += timedelta_total_seconds(StringToTimeDelta(dp.text))
      days += 1

  avgSeconds = totSeconds / days

  return timedelta(seconds=avgSeconds)



def FloatStrFormat(fl):
  return '%.2f' % (fl)

def AnalyzeIntegerQueryData(query):
  datapoints = DataPoint.get_by_query(query)
  analytic_list = [
          {'name': 'Average', 'value': FloatStrFormat(Average(datapoints))},
          {'name': 'Range', 'value': (Range(datapoints))},
          {'name': 'Variance', 'value': FloatStrFormat(Variance(datapoints))},
          {'name': 'Standard Deviation', 'value': FloatStrFormat(StandardDeviation(datapoints))},
          {'name': 'Peaks On', 'value': PeaksOnDay(datapoints)},
          {'name': 'Monday Average', 'value': FloatStrFormat(DayAvg(datapoints, 0))},
          {'name': 'Tuesday Average', 'value': FloatStrFormat(DayAvg(datapoints, 1))},
          {'name': 'Wednesday Average', 'value': FloatStrFormat(DayAvg(datapoints, 2))},
          {'name': 'Thursday Average', 'value': FloatStrFormat(DayAvg(datapoints, 3))},
          {'name': 'Friday Average', 'value': FloatStrFormat(DayAvg(datapoints, 4))},
          {'name': 'Saturday Average', 'value': FloatStrFormat(DayAvg(datapoints, 5))},
          {'name': 'Sunday Average', 'value': FloatStrFormat(DayAvg(datapoints, 6))},
        ]

  user = query.user 
  for q in Query.get_by_user(user):
    if q.format == 'integer' and q.name != query.name:
      analytic_list.extend([{'name': 'Covariance with ' + q.name,
                            'value': FloatStrFormat(Covariance(query,q))}])

  for q in Query.get_by_user(user):
    if q.format == 'integer' and q.name != query.name:
      for x in range(QueryRange(q)[0], QueryRange(q)[1]):
        analytic_list.extend([
          {'name': 'Average when ' + q.name + ' = ' + str(x),
            'value': FloatStrFormat(AvgIntOnSlicedInt(query, q, x))},
          {'name': 'Change from average when ' + q.name + ' = ' + str(x),
            'value': FloatStrFormat(PercentFromAvgIntOnSlicedInt(query, q, x))}
        ])
  
  return analytic_list

def QueryRange(query):
  datapoints = DataPoint.get_by_query(query)
  return Range(datapoints)

def Range(datapoints):
  min = int(datapoints[0].text)
  max = int(datapoints[0].text)

  for dp in datapoints:
    if int(dp.text) > max:
      max = int(dp.text)
    if int(dp.text) < min:
      min = int(dp.text)

  return (min, max)

def MapDataAverage(mapData):
  sum = 0
  for key in mapData.keys():
    sum += mapData[key]

  logging.info('Sum: ' + sum + ' Length: ' + len(mapData))

  average = float(sum)/float(len(mapData))

  return average

def DataAverage(datapoints):
  sum = 0
  
  for dp in datapoints:
    sum += int(dp.text)

  average = float(sum)/len(datapoints)

  return average

def QueryAverage(query):
  datapoints = DataPoint.get_by_query(query)
  return Average(datapoints)

def Average(datapoints):
  sum = 0
  
  for dp in datapoints:
    sum += int(dp.text)

  average = float(sum)/len(datapoints)

  return average

def Variance(datapoints):
  mu = Average(datapoints)
  squaresum = 0
 
  for dp in datapoints:
    squaresum += (int(dp.text)-mu)*(int(dp.text)-mu)

  sigma = float(squaresum)/len(datapoints)

  return sigma

def StandardDeviation(datapoints):
  return math.sqrt(Variance(datapoints))
 
# returns the day the query is the highest 
def PeaksOnDay(datapoints):
  maxDayAvg = 0
  maxOnDay = 0

  for day in range(0,7):
    if DayAvg(datapoints, day) > maxDayAvg:
      maxOnDay = day
      maxDayAvg = DayAvg(datapoints, day)

  return weekdays[maxOnDay]

def DayAvg(datapoints, day):
  daySum = 0
  days = 0
 
  for dp in datapoints:
    if dp.timestamp.weekday() == day:
      daySum += int(dp.text)
      days += 1

  return float(daySum)/days  



