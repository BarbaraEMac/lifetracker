import logging, math
from datetime import datetime, timedelta

from model import User, Query, DataPoint

from multi_analytics import Covariance

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
  return [{'name': 'Common words', 'value': CommonWords(query)}]

# we can probably map reduce this shit
def CommonWords(query):
  datapoints = DataPoint.get_by_query(query)

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
  return [
    {'name': 'Average Time', 'value': AverageTime(query)},
    {'name': 'Peaks on Day', 'value': HighestDayAverageTime(query)},
    {'name': 'Lowest on Day', 'value': LowestDayAverageTime(query)},
    {'name': 'Average Time on Monday', 'value': AverageTimeOnDay(query,0)},
    {'name': 'Average Time on Tuesday', 'value': AverageTimeOnDay(query,1)},
    {'name': 'Average Time on Wednesday', 'value': AverageTimeOnDay(query,2)},
    {'name': 'Average Time on Thursday', 'value': AverageTimeOnDay(query,3)},
    {'name': 'Average Time on Friday', 'value': AverageTimeOnDay(query,4)},
    {'name': 'Average Time on Saturday', 'value': AverageTimeOnDay(query,5)},
    {'name': 'Average Time on Sunday', 'value': AverageTimeOnDay(query,6)},
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

def AverageTime(query):
  # interpret each datapoint as a timedelta
  # then average them

  datapoints = DataPoint.get_by_query(query)

  totSeconds = 0
  for dp in datapoints:
    totSeconds += timedelta_total_seconds(StringToTimeDelta(dp.text))

  avgSeconds = totSeconds / len(datapoints)

  return timedelta(seconds=avgSeconds)

def HighestDayAverageTime(query):
  highestDay = 0
  highestDayAvg = timedelta(seconds=0 )

  for day in range(0,7):
    if AverageTimeOnDay(query,day) > highestDayAvg:
      highestDay = day
      highestDayAvg = AverageTimeOnDay(query,day)
    
  return weekdays[highestDay]

def LowestDayAverageTime(query):
  lowestDay = 0
  lowestDayAvg = AverageTimeOnDay(query,0)

  for day in range(1,7):
    if AverageTimeOnDay(query,day) < lowestDayAvg:
      lowestDay = day
      lowestDayAvg = AverageTimeOnDay(query,day)
    
  return weekdays[lowestDay]
  
def AverageTimeOnDay(query,day):
  datapoints = DataPoint.get_by_query(query)

  totSeconds = 0
  days = 0
  for dp in datapoints:
    if dp.timestamp.weekday() == day:
      totSeconds += timedelta_total_seconds(StringToTimeDelta(dp.text))
      days += 1

  avgSeconds = totSeconds / days

  return timedelta(seconds=avgSeconds)




def AnalyzeIntegerQueryData(query):
  analytic_list = [
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

  user = query.user 
  for q in Query.get_by_user(user):
    if q.format == 'integer' and q != query:
      analytic_list.append({'name': 'Covariance with ' + q.name,
                            'value': str(Covariance(query,q))})

  return analytic_list

def MapDataAverage(mapData):
  sum = 0
  for key in mapData.keys():
    sum += mapData[key]

  average = sum/len(mapData)

  return average

def DataAverage(datapoints):
  sum = 0
  
  for dp in datapoints:
    sum += int(dp.text)

  average = sum/len(datapoints)

  return average

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

  # logging.info('Variance len(datapoints): ' + str(len(datapoints)))
  # logging.info('Variance average: ' + str(mu))

  sigma = float(squaresum)/len(datapoints)

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



