import logging, math
from datetime import datetime, timedelta

from model import User, Query, DataPoint

from common import weekdays

def analyze_time_query_data(query):
  datapoints = DataPoint.get_by_query(query)
  analytic_list = {}

  analytic_list.update(basic_suite(datapoints))

  analytic_list.update(daily_suite(datapoints))

  return analytic_list

def basic_suite(datapoints):
  basic_list = {}

  basic_list['Average Time'] = average_time(datapoints)
  
  return basic_list

def daily_suite(datapoints):
  daily_list = {}

  daily_list['Peaks on Day'] = highest_day_average_time(datapoints)
  daily_list['Lowest on Day'] = lowest_day_average_time(datapoints)
  daily_list['Average Time on Monday'] = average_time_on_day(datapoints,0)
  daily_list['Average Time on Tuesday'] = average_time_on_day(datapoints,1)
  daily_list['Average Time on Wednesday'] = average_time_on_day(datapoints,2)
  daily_list['Average Time on Thursday'] = average_time_on_day(datapoints,3)
  daily_list['Average Time on Friday'] = average_time_on_day(datapoints,4)
  daily_list['Average Time on Saturday'] = average_time_on_day(datapoints,5)
  daily_list['Average Time on Sunday'] = average_time_on_day(datapoints,6)
    
  return daily_list

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
