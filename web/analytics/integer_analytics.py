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
  return '%.2f' % (fl)

# we should have a function in here that returns an iterable of the
# range set of the data. Actually, that should be domain.
def query_range(query):
  datapoints = DataPoint.get_by_query(query)
  return data_range(datapoints)

def data_range(datapoints):
  min = int(datapoints[0].text)
  max = int(datapoints[0].text)

  for dp in datapoints:
    if int(float(dp.text)) > max:
      max = int(float(dp.text))
    if int(float(dp.text)) < min:
      min = int(float(dp.text))

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

def variance(datapoints):
  mu = average(datapoints)
  squaresum = 0
 
  for dp in datapoints:
    squaresum += (int(dp.text)-mu)*(int(dp.text)-mu)

  sigma = float(squaresum)/len(datapoints)

  return sigma

def standard_deviation(datapoints):
  return math.sqrt(variance(datapoints))

def median(datapoints):
  # sort the values, return the middle. can probably use sorted for this
  values = map(DataPoint.get_as_float, datapoints)
  values.sort()
  return values[len(values)/2]

def mode(datapoints):
  values = map(DataPoint.get_as_float, datapoints)
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
      daySum += int(dp.text)
      days += 1

  return float(daySum)/days  



