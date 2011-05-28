import logging, math
from datetime import datetime, timedelta

from model import User, Query, DataPoint

from common import weekdays, query_average, average

from text_analytics import common_words
from multi_analytics import covariance, avg_int_on_sliced_int, percent_from_avg_int_on_sliced_int, avg_int_on_sliced_text

def analyze_integer_query_data(query):
  datapoints = DataPoint.get_by_query(query)

  analytic_list = []
  # basics
  analytic_list.extend(basic_suite(datapoints))
  # daily basics
  analytic_list.extend(daily_suite(datapoints))

  analytic_list.extend(covariance_suite(query))

  analytic_list.extend(crosssection_suite(query ))

  return analytic_list

def basic_suite(datapoints):
  basic_list = []

  basic_list.append(('Average', float_str_format(average(datapoints))))
  basic_list.append(('Median', median(datapoints)))
  basic_list.append(('Mode', mode(datapoints)))
  basic_list.append(('Range', data_range(datapoints)))
  basic_list.append(('Variance', float_str_format(variance(datapoints))))
  basic_list.append(('Standard Deviation', float_str_format(standard_deviation(datapoints))))

  return basic_list

def daily_suite(datapoints):
  daily_list = []

  daily_list.extend([
    ('Peaks On',  peaks_on_day(datapoints)),
    ('Monday Average',  float_str_format(day_avg(datapoints, 0))),
    ('Tuesday Average',  float_str_format(day_avg(datapoints, 1))),
    ('Wednesday Average',  float_str_format(day_avg(datapoints, 2))),
    ('Thursday Average',  float_str_format(day_avg(datapoints, 3))),
    ('Friday Average',  float_str_format(day_avg(datapoints, 4))),
    ('Saturday Average',  float_str_format(day_avg(datapoints, 5))),
    ('Sunday Average',  float_str_format(day_avg(datapoints, 6))),
  ])

  return daily_list
  
def crosssection_suite(query):
  crosssection_list = []
  user = query.user

  for q in Query.get_by_user(user):
    if q.format == 'integer' and q.name != query.name:
      for x in range(query_range(q)[0], query_range(q)[1]):
        avg_name = 'Average when ' + q.name + ' = ' + str(x)
        avg_value = float_str_format(avg_int_on_sliced_int(query, q, x))
  
        crosssection_list.append((avg_name, avg_value))

        percent_name = 'Change from average when ' + q.name + ' = ' + str(x)
        percent_value =float_str_format(percent_from_avg_int_on_sliced_int(query, q, x))

        crosssection_list.append((percent_name, percent_value))

    elif q.format == 'text':
      for word in common_words(DataPoint.get_by_query(q)).split(', '):
        avg_name = 'Average when "' + word + '" is in ' + q.name
        avg_value = float_str_format(avg_int_on_sliced_text(query, q, word))

        crosssection_list.append((avg_name, avg_value))

        #percent_name = 'Change from average when ' + word + ' in ' +q.name
        #percent_value = float_str_format(percent_from_avg_int_on_sliced_int(query, q, x))

        #crosssection_list[percent_name] = percent_value
        
  return crosssection_list

def covariance_suite(query):
  covariance_list = []
  user = query.user 

  for q in Query.get_by_user(user):
    if q.format == 'integer' and q.name != query.name:
      covariance_list.append(
        ('Covariance with ' + q.name, float_str_format(covariance(query,q))))

  return covariance_list


def float_str_format(fl):
  if fl == None:
    return '0'
  return '%.2f' % (fl)

# we should have a function in here that returns an iterable of the
# range set of the data. Actually, that should be domain.
def query_range(query):
  datapoints = DataPoint.get_by_query(query)
  return data_range(datapoints)

def data_range(datapoints):
  if len(datapoints) == 0:
    return (0,0)

  min = datapoints[0].as_float()
  max = datapoints[0].as_float()

  for dp in datapoints:
    if dp.as_float() > max:
      max = dp.as_float()
    if dp.as_float() < min:
      min = dp.as_float()

  return (min, max)

def mapdata_average(mapData):
  if len(mapData) == 0:
    return None

  sum = 0.0
  for key in mapData.keys():
    sum += mapData[key]

  logging.info('Sum: ' + sum + ' Length: ' + len(mapData))

  average = sum/len(mapData)

  return average

def data_average(datapoints):
  if len(datapoints) == 0:
    return None

  sum = 0
  
  for dp in datapoints:
    sum += dp.as_float()

  average = sum/len(datapoints)

  return average

def variance(datapoints):
  if len(datapoints) == 0:
    return None

  mu = average(datapoints)
  squaresum = 0
 
  for dp in datapoints:
    squaresum += (dp.as_float()-mu)*(dp.as_float()-mu)

  sigma = squaresum/len(datapoints)

  return sigma

def standard_deviation(datapoints):
  if len(datapoints) == 0:
    return None
 
  var = variance(datapoints)
  
  if var == None:
    return None
 
  return math.sqrt(var)

def median(datapoints):
  if len(datapoints) == 0:
    return None

  # sort the values, return the middle. can probably use sorted for this
  values = map(DataPoint.as_float, datapoints)
  values.sort()
  return values[len(values)/2]

def mode(datapoints):
  if len(datapoints) == 0:
    return None

  values = map(DataPoint.as_float, datapoints)
  values.sort()
  val_dict = {}
  for val in values:
    if val in val_dict:
      val_dict[val] += 1
    else:
      val_dict[val] = 1

  values = sorted(val_dict, key=val_dict.get, reverse=True)
  # a little harder than median
  return values[0]

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
      daySum += dp.as_float()
      days += 1

  if days == 0:
    return None

  return daySum/days  



