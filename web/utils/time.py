# all the functions haviing to do with manipulating time should go
# in here

from datetime import datetime

def datetime_as_int(dt)
  return int(dt.strftime('%s'))

def nearest_day(timestamp):
  return (timestamp // 86400)*86400

def morning(timestamp):
  return nearest_day(timestamp) + 10*60*60 # 10 am

def nighttime(timestamp):
  return nearest_day(timestamp) + 23*60*60 + 59*60 # 23:59

def is_daytime():
  # if it is between 10 am and midnight
  now = datetime_as_int(datetime.now())
  if now > morning(now) and now < nighttime(now):
    return True
  else:
    return False
