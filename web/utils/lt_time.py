# all the functions haviing to do with manipulating time should go
# in here

from google.appengine.ext import webapp
import datetime

# dt.strftime does not work in this file. I have no idea why. For now,
# just don't call it.
def datetime_as_int(dt):
  return int(dt.strftime("%s"))

def nearest_day(timestamp):
  return (timestamp // 86400)*86400

# EDT is UTC - 4, so 1600 UTC is 1200 EDt
def morning(timestamp):
  return nearest_day(timestamp) + 14*60*60 # 10 am in EST, since we get 
  # times in UTC. yes this is hackey, but timestamps in appengine are
  # a bitch

def afternoon(timestamp):
  return nearest_day(timestamp) + 16*60*60 # noon EST

def evening(timestamp):
  return nearest_day(timestamp) + 22*60*60 # 6:00 EST

def nighttime(timestamp):
  return nearest_day(timestamp) + 27*60*60 + 59*60 # 23:59

def is_morning(now):
  if now >= morning(now) and now < afternoon(now):
    return True
  return False

def is_afternoon(now):
 if now >= afternoon(now) and now < evening(now):
    return True
 return False

def is_evening(now):
  if now >= evening(now) and now < nighttime(now):
    return True
  return False

def is_daytime(now):
  # if it is between 10 am and midnight
  if now > morning(now) and now < nighttime(now):
    return True
  else:
    return False
