import math
from datetime import datetime, timedelta

from model import User, Query, DataPoint

from common import weekdays

def time_overview(query):
  datapoints = DataPoint.get_by_query(query)
  return 'Average Time: ' + str(average_time(datapoints))
 
def analyze_time_query_data(query):
  datapoints = DataPoint.get_by_query(query)
  analytic_list = []

  analytic_list.extend(basic_suite(datapoints))

  analytic_list.extend(daily_suite(datapoints))

  return analytic_list

def basic_suite(datapoints):
  basic_list = []

  basic_list.append(('Average Time', str(average_time(datapoints))))
  
  return basic_list

def daily_suite(datapoints):
  daily_list = []

  daily_list.extend([
    ('Peaks on Day', highest_day_average_time(datapoints)),
    ('Lowest on Day', lowest_day_average_time(datapoints)),
    ('Average Time on Monday', str(average_time_on_day(datapoints,0))),
    ('Average Time on Tuesday', str(average_time_on_day(datapoints,1))),
    ('Average Time on Wednesday', str(average_time_on_day(datapoints,2))),
    ('Average Time on Thursday', str(average_time_on_day(datapoints,3))),
    ('Average Time on Friday', str(average_time_on_day(datapoints,4))),
    ('Average Time on Saturday', str(average_time_on_day(datapoints,5))),
    ('Average Time on Sunday', str(average_time_on_day(datapoints,6))),
  ])
    
  return daily_list

def string_to_time_delta(string):
  # assume every dp is x:y
  try: 
    hours = int(string[ : string.find(':') ])
    minutes = int(string[string.find(':') + 1 : ])
  except ValueError:
    hours = 0
    minutes = 0

  # here we're assuming if a time is before 6, it is pm. 
  # this is a shaky assumption and should be revisited soon.
  if hours < 6:
    hours +=12

  return timedelta(hours=hours, minutes=minutes)

def timedelta_total_seconds(td):
  return td.seconds + td.days*86400

def average_time(datapoints):
  if len(datapoints) == 0:
    return None

  # interpret each datapoint as a timedelta
  # then average them

  totSeconds = 0
  for dp in datapoints:
    totSeconds += timedelta_total_seconds(string_to_time_delta(dp.text))

  avgSeconds = totSeconds / len(datapoints)

  return str(timedelta(seconds=avgSeconds))

def highest_day_average_time(datapoints):
  highestDay = 0
  highestday_avg = timedelta(seconds=0 )

  for day in range(0,7):
    this_day_avg = average_time_on_day(datapoints,day)
    if this_day_avg == None:
      continue
    elif this_day_avg > highestday_avg:
      highestDay = day
      highestday_avg = average_time_on_day(datapoints,day)
    
  return weekdays[highestDay]

def lowest_day_average_time(datapoints):
  lowestDay = 0
  lowestday_avg = average_time_on_day(datapoints,0)

  for day in range(1,7):
    this_day_avg = average_time_on_day(datapoints,day)

    if this_day_avg == None:
      continue
    elif lowestday_avg == None:
      lowest_day_avg = this_day_avg
    elif this_day_avg < lowestday_avg:
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

  if days == 0:
    return None

  avgSeconds = totSeconds / days

  return timedelta(seconds=avgSeconds)
