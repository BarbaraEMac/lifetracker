import math

from model import User, Query, DataPoint

from utils.lt_time import nearest_day
from datetime import datetime

from common import query_average, average

def integer_cross_section(data, value):
  for key in data.keys():
    if not data[key] == value:
      del data[key]

  return data

def text_cross_section(data, value):
  for key in data.keys():
    if data[key].find(value) == -1:
      del data[key]

  return data

# what is your average mood on days you eat oatmeal?
# mapize each dataset
# bucket mood and breakfast by days
# throw out datapoints in breakfast that arent 'value'
# symmettrisize the datasets
# return the average over mood
def avg_int_on_sliced_text(aquery, bquery, value):
  adatapoints = DataPoint.get_by_query(aquery)
  bdatapoints = DataPoint.get_by_query(bquery)
  adata = mapize_int_data(adatapoints)
  bdata = mapize_data(bdatapoints) # not int data!

  # bucket to days
  adata = bucket_to_days(adata)
  bdata = bucket_to_days(bdata)

  # throw out all the datapoints that aren't 'value'
  bdata = text_cross_section(bdata, value)

  adata, bdata = symmettrysize(adata, bdata)   

  avg = map_data_average(adata)

  return avg

# what is your average mood on days you sleep for eight hours?
# bucket mood by days
# bucket sleep by days
# throw out all the mood DPs that aren't value
# throw out all the sleep DPs that don't have a corresponding DP in sleep
# average 

def percent_from_avg_int_on_sliced_int(aquery, bquery, value):
  avg = query_average(aquery)
  slicedAvg = avg_int_on_sliced_int(aquery, bquery, value)

  if slicedAvg == 0:
    return None

  return (avg/slicedAvg - 1)*100

# hold b constant and we want the cross section of a
def avg_int_on_sliced_int(aquery, bquery, value):
  adatapoints = DataPoint.get_by_query(aquery)
  bdatapoints = DataPoint.get_by_query(bquery)
  adata = mapize_int_data(adatapoints)
  bdata = mapize_int_data(bdatapoints)

  # bucket sleep by days
  bdata = bucket_to_days(bdata)
  adata = bucket_to_days(adata)
 
  # throwout all the sleep dps that aren't 8 

  bdata = integer_cross_section(bdata, value)
     
  symmettrysize(adata, bdata)

  if len(adata) == 0:
    return 0

  # average the bdata values 
  avg = map_data_average(adata)

  # return it
  return avg

# the covariance divided by the product of the standard deviations
def correlation_coefficient(aquery, bquery):
  cov = covariance(aquery, bquery)
  
  adatapoints = DataPoint.get_by_query(aquery)
  bdatapoints = DataPoint.get_by_query(bquery)

  sdA = standard_deviation(adatapoints)
  sdB = standard_deviation(bdatapoints)

  if cov is None or sdA is None or sdB is None:
    return None
  
  cc = cov / (sdA * sdB)

  return cc

def sum_squared_diff_avg(datapoints):
  # get the average
    
  return 0


# this is imperfect, it doesn't completely match up with Variance, 
# which it should. check it out later.
def covariance(int_query_a, int_query_b):
  # cov = sum for all i (x - xnaught)(y-ynaught) all over N-1
  # we need to match up points between the two datasets

  adatapoints = DataPoint.get_by_query(int_query_a)
  bdatapoints = DataPoint.get_by_query(int_query_b)

  adata = mapize_int_data(adatapoints)
  bdata = mapize_int_data(bdatapoints)

  #if adata is None:
  #  print int_query_a.name + " is none!"

  # tweak the data so we only have a single point for each day 
  # this can return just index: data, since we don't care about the actual
  # times
  adata = bucket_to_days(adata)
  bdata = bucket_to_days(bdata)

  # tweak the data such that there is a 1:1 mapping between the sets
  adata, bdata = symmettrysize(adata, bdata)


  # key it from 0...

  # do the actual covariance
  N = len(adata)

  if N <= 1: # we divide by N-1 just below
    return None

  aAvg = map_data_average(adata)
  bAvg = map_data_average(bdata)

  sum = 0.0
  for i in adata.keys():
    sum += (adata[i] - aAvg)*(bdata[i] - bAvg)

  if N-1 <= 0:
    cov = 0
  else:
    cov = sum/(N-1)
 
  return cov

# we can make this smarter at some point. e.g. average nearby timestamps
def symmettrysize(adata, bdata):
  # tweak the data such that we have a 1:1 mapping between the sets
  # sort both sets
  # foreach datapoint
  #   if there is not a corresponding point in the other set
  #     throw it out

  for key in adata.keys():
    if not key in bdata:
      del adata[key]
       
  for key in bdata.keys():
    if not key in adata:
      del bdata[key] 

  return adata, bdata

def mapize_int_data(datapoints):
  map = {}
  for dp in datapoints:
    map[dp.timestamp_as_int()] = dp.as_float()
  return map

def mapize_data(datapoints):
  map = {}
  for dp in datapoints:
    map[dp.timestamp_as_int()] = dp.text
  return map

# input: a bunch of datapoints
# output: a bunch of datapoints such that there is only a single datapoint
#   per day. If we find multiple datapoints for a daty, average them
#   returns the datapoints in map format
def bucket_to_days(mapData):
  # foreach datapoint
  #   normalize the timestamp to the start of the day
  #   this will have the effect of bucketing the timestamps into days
  #   since this is not a multi-map.

  for timestamp in mapData.keys():
    data = mapData[timestamp]
    del mapData[timestamp] # remove the old datapoint from the list
    timestamp = nearest_day(timestamp) #normalize the timestamp
    mapData[timestamp] = data  # re-insert the datapoint

  return mapData


def map_data_average(mapData):
  if len(mapData) == 0:
    return None

  sum = 0.0
  for key in mapData.keys():
    sum += mapData[key]

  average = sum/len(mapData)

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
