from datetime import datetime, timedelta
from time import time
from django.utils import simplejson as json
import logging

from model import ActionLog

def worst_walltime(page):
  yesterday = datetime.now() - timedelta(hours=24)

  request_times = ActionLog.get(
    action = 'Walltime',
    timewindow = yesterday,
    page=page, 
  ).fetch(1000)

  if len(request_times) < 1:
    return None

  max_rt = 0

  for rt in request_times:
    try:
      data = json.loads(rt.data)
    except TypeError:
      continue
    except ValueError:
      continue
     
    if int(data['walltime']) > max_rt:
      max_rt = int(data['walltime'])

  return max_rt

def average_walltime(page):
  yesterday = datetime.now() - timedelta(hours=24)

  request_times = ActionLog.get(
    action = 'Walltime',
    timewindow = yesterday,
    page=page, 
  ).fetch(1000)

  if len(request_times) < 1:
    return None

  total_walltime = 0
  for rt in request_times:
    try:
      data = json.loads(rt.data)
    except TypeError:
      continue
    except ValueError:
      continue

    wt = int(data['walltime'])
    total_walltime += wt

  avg_walltime = total_walltime / len(request_times)
  return avg_walltime

""" place this decorator before web handlers and it will log the time
  it take to generate that page on each request """
def track_walltime(handler):
  def track(self):
    start = time()

    response =  handler(self)

    end = time()

    walltime = int((end - start)*1000)

    data = {
     'walltime': walltime,
    }

    ActionLog.log(
      action='Walltime',
      data=json.dumps(data),
      page=self.request.path,
    )
    
    return response

  return track
