import logging, math
from datetime import datetime, timedelta

from model import User, Query, DataPoint

from multi_analytics import covariance, avg_int_on_sliced_int, percent_from_avg_int_on_sliced_int 

weekdays = {
  0: 'Monday',
  1: 'Tuesday',
  2: 'Wednesday',
  3: 'Thursday',
  4: 'Friday',
  5: 'Saturday',
  6: 'Sunday',
}

def analyze_query_data(query):
  if query.format == 'integer':
    return analyze_integer_query_data(query)
  elif query.format =='time':
    return analyze_time_query_data(query)
  elif query.format == 'text':
    return analyze_text_query_data(query)
  else:
    return [{'name': '', 'value': ''}]

def analyze_text_query_data(query):
  datapoints = DataPoint.get_by_query(query)
  return [{'name': 'Common words', 'value': common_words(datapoints)}]

# we can probably map reduce this shit
def common_words(datapoints):
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



def analyze_time_query_data(query):
  datapoints = DataPoint.get_by_query(query)
  return [
    {'name': 'average Time', 'value': average_time(datapoints)},
    {'name': 'Peaks on Day', 'value': highest_day_average_time(datapoints)},
    {'name': 'Lowest on Day', 'value': lowest_day_average_time(datapoints)},
    {'name': 'average Time on Monday', 'value': average_time_on_day(datapoints,0)},
    {'name': 'average Time on Tuesday', 'value': average_time_on_day(datapoints,1)},
    {'name': 'average Time on Wednesday', 'value': average_time_on_day(datapoints,2)},
    {'name': 'average Time on Thursday', 'value': average_time_on_day(datapoints,3)},
    {'name': 'average Time on Friday', 'value': average_time_on_day(datapoints,4)},
    {'name': 'average Time on Saturday', 'value': average_time_on_day(datapoints,5)},
    {'name': 'average Time on Sunday', 'value': average_time_on_day(datapoints,6)},
    ]

def string_to_time_delta(string):
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

def average_time(datapoints):
  # interpret each datapoint as a timedelta
  # then average them

  totSeconds = 0
  for dp in datapoints:
    totSeconds += timedelta_total_seconds(string_to_time_delta(dp.text))

  avgSeconds = totSeconds / len(datapoints)

  return timedelta(seconds=avgSeconds)

def highest_day_average_time(datapoints):
  highestDay = 0
  highestday_avg = timedelta(seconds=0 )

  for day in range(0,7):
    if average_time_on_day(datapoints,day) > highestday_avg:
      highestDay = day
      highestday_avg = average_time_on_day(datapoints,day)
    
  return weekdays[highestDay]

def lowest_day_average_time(datapoints):
  lowestDay = 0
  lowestday_avg = average_time_on_day(datapoints,0)

  for day in range(1,7):
    if average_time_on_day(datapoints,day) < lowestday_avg:
      lowestDay = day
      lowestday_avg = average_time_on_day(datapoints,day)
    
  return weekdays[lowestDay]
  
def average_time_on_day(datapoints,day):
  totSeconds = 0
  days = 0
  for dp in datapoints:
    if dp.timestamp.weekday() == day:
      totSeconds += timedelta_total_seconds(string_to_time_delta(dp.text))
      days += 1

  avgSeconds = totSeconds / days

  return timedelta(seconds=avgSeconds)



def float_str_format(fl):
  return '%.2f' % (fl)

def analyze_integer_query_data(query):
  datapoints = DataPoint.get_by_query(query)
  analytic_list = [
          {'name': 'average', 'value': float_str_format(average(datapoints))},
          {'name': 'range', 'value': (data_range(datapoints))},
          {'name': 'variance', 'value': float_str_format(variance(datapoints))},
          {'name': 'Standard Deviation', 'value': float_str_format(standard_deviation(datapoints))},
          {'name': 'Peaks On', 'value': peaks_on_day(datapoints)},
          {'name': 'Monday average', 'value': float_str_format(day_avg(datapoints, 0))},
          {'name': 'Tuesday average', 'value': float_str_format(day_avg(datapoints, 1))},
          {'name': 'Wednesday average', 'value': float_str_format(day_avg(datapoints, 2))},
          {'name': 'Thursday average', 'value': float_str_format(day_avg(datapoints, 3))},
          {'name': 'Friday average', 'value': float_str_format(day_avg(datapoints, 4))},
          {'name': 'Saturday average', 'value': float_str_format(day_avg(datapoints, 5))},
          {'name': 'Sunday average', 'value': float_str_format(day_avg(datapoints, 6))},
        ]

  user = query.user 
  for q in Query.get_by_user(user):
    if q.format == 'integer' and q.name != query.name:
      analytic_list.extend([{'name': 'covariance with ' + q.name,
                            'value': float_str_format(covariance(query,q))}])

  for q in Query.get_by_user(user):
    if q.format == 'integer' and q.name != query.name:
      for x in range(query_range(q)[0], query_range(q)[1]):
        analytic_list.extend([
          {'name': 'average when ' + q.name + ' = ' + str(x),
            'value': float_str_format(avg_int_on_sliced_int(query, q, x))},
          {'name': 'Change from average when ' + q.name + ' = ' + str(x),
            'value': float_str_format(percent_from_avg_int_on_sliced_int(query, q, x))}
        ])
  
  return analytic_list

def query_range(query):
  datapoints = DataPoint.get_by_query(query)
  return data_range(datapoints)

def data_range(datapoints):
  min = int(datapoints[0].text)
  max = int(datapoints[0].text)

  for dp in datapoints:
    if int(dp.text) > max:
      max = int(dp.text)
    if int(dp.text) < min:
      min = int(dp.text)

  return (min, max)

def mapdata_average(mapData):
  sum = 0
  for key in mapData.keys():
    sum += mapData[key]

  logging.info('Sum: ' + sum + ' Length: ' + len(mapData))

  average = float(sum)/float(len(mapData))

  return average

def data_average(datapoints):
  sum = 0
  
  for dp in datapoints:
    sum += int(dp.text)

  average = float(sum)/len(datapoints)

  return average

def query_average(query):
  datapoints = DataPoint.get_by_query(query)
  return average(datapoints)

def average(datapoints):
  sum = 0
  
  for dp in datapoints:
    sum += int(dp.text)

  average = float(sum)/len(datapoints)

  return average

def variance(datapoints):
  mu = average(datapoints)
  squaresum = 0
 
  for dp in datapoints:
    squaresum += (int(dp.text)-mu)*(int(dp.text)-mu)

  sigma = float(squaresum)/len(datapoints)

  return sigma

def standard_deviation(datapoints):
  return math.sqrt(variance(datapoints))
 
# returns the day the query is the highest 
def peaks_on_day(datapoints):
  maxday_avg = 0
  maxOnDay = 0

  for day in range(0,7):
    if day_avg(datapoints, day) > maxday_avg:
      maxOnDay = day
      maxday_avg = day_avg(datapoints, day)

  return weekdays[maxOnDay]

def day_avg(datapoints, day):
  daySum = 0
  days = 0
 
  for dp in datapoints:
    if dp.timestamp.weekday() == day:
      daySum += int(dp.text)
      days += 1

  return float(daySum)/days  



