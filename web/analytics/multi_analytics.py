import logging

from model import User, Query, DataPoint

# what is your average mood on days you sleep for eight hours?
# bucket mood by days
# bucket sleep by days
# throw out all the mood DPs that aren't value
# throw out all the sleep DPs that don't have a corresponding DP in sleep
# average 

def PercentFromAvgIntOnSlicedInt(aquery, bquery, value):
  avg = QueryAverage(aquery)
  slicedAvg = AvgIntOnSlicedInt(aquery, bquery, value)
  if slicedAvg == 0:
    return 0
  return (avg/slicedAvg - 1)*100

# hold b constant and we want the cross section of a
def AvgIntOnSlicedInt(aquery, bquery, value):
  adatapoints = DataPoint.get_by_query(aquery)
  bdatapoints = DataPoint.get_by_query(bquery)
  adata = MapizeIntData(adatapoints)
  bdata = MapizeIntData(bdatapoints)

  # bucket sleep by days
  bdata = BucketToDays(bdata)
  adata = BucketToDays(adata)
 
  # throwout all the sleep dps that aren't 8 
  for key in bdata.keys():
    if not bdata[key] == value:
      del bdata[key]
      
  for key in adata.keys():
    if not key in bdata.keys():
      del adata[key]

  # technically there could still be keys in bdata that aren't in adata
  """for key in bdata.keys():
    if not key in adata.keys():
      del bdata[keys]"""

  if len(adata) == 0:
    return 0

  for key in adata.keys():
    logging.info(bquery.name + ': ' + str(bdata[key]) + ', ' + aquery.name + ': ' + str(adata[key]))


  # average the bdata values 
  avg = MapDataAverage(adata)

  logging.info("Average: " + str(avg))
  logging.info("End\n")

  # return it
  return avg

def Slice(aquery, bquery):
  # how to do this...
  return ''



# this is imperfect, it doesn't completely match up with Variance, 
# which it should. check it out later.
def Covariance(int_query_a, int_query_b):
  # cov = sum for all i (x - xnaught)(y-ynaught) all over N-1
  # we need to match up points between the two datasets

  adatapoints = DataPoint.get_by_query(int_query_a)
  bdatapoints = DataPoint.get_by_query(int_query_b)

  adata = MapizeIntData(adatapoints)
  bdata = MapizeIntData(bdatapoints)

  #if adata is None:
  #  print int_query_a.name + " is none!"

  # tweak the data so we only have a single point for each day 
  # this can return just index: data, since we don't care about the actual
  # times
  adata = BucketToDays(adata)
  bdata = BucketToDays(bdata)

  # tweak the data such that there is a 1:1 mapping between the sets
  adata, bdata = Symmettrysize(adata, bdata)

  # logging.info('\nLength1:' +  str(len(adata)))
  # logging.info('\nLength2: ' + str(len(bdata)))

  # key it from 0...

  # do the actual covariance
  N = len(adata)
  aAvg = MapDataAverage(adata)
  bAvg = MapDataAverage(bdata)

  sum = 0 
  for i in adata.keys():
    # logging.info('adata[i] = ' + str(adata[i]) + ', bdata[i] = ' + str(bdata[i]))
    sum += (adata[i] - aAvg)*(bdata[i] - bAvg)

  # logging.info('aAvg = ' + str(aAvg) + ', bAvg = ' + str(bAvg))

  # logging.info('Sum = ' + str(sum))
  cov = float(sum)/(N-1)
 
  # logging.info('Cov = ' + str(cov))
 
  return cov

# we can make this smarter at some point. e.g. average nearby timestamps
def Symmettrysize(adata, bdata):
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

def MapizeIntData(datapoints):
  map = {}
  for dp in datapoints:
    map[int(dp.timestamp.strftime("%s"))] = int(dp.text)
  return map

def NearestDay(timestamp):
  return (timestamp // 86400)*86400

# input: a bunch of datapoints
# output: a bunch of datapoints such that there is only a single datapoint
#   per day. If we find multiple datapoints for a daty, average them
#   returns the datapoints in map format
def BucketToDays(mapData):
  # foreach datapoint
  #   normalize the timestamp to the start of the day
  #   this will have the effect of bucketing the timestamps into days
  #   since this is not a multi-map.

  for timestamp in mapData.keys():
    data = mapData[timestamp]
    del mapData[timestamp] # remove the old datapoint from the list
    timestamp = NearestDay(timestamp) #normalize the timestamp
    mapData[timestamp] = data  # re-insert the datapoint

  return mapData


def MapDataAverage(mapData):
  sum = 0
  for key in mapData.keys():
    sum += mapData[key]

  average = float(sum)/len(mapData)

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
