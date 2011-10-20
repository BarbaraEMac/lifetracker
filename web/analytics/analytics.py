import math
from datetime import datetime, timedelta

from model import User, Query, DataPoint

from text_analytics import analyze_text_query_data
from time_analytics import analyze_time_query_data
from integer_analytics import analyze_integer_query_data

from text_analytics import text_overview
from time_analytics import time_overview
from integer_analytics import integer_overview

# gives a string 'overview' for each query type. 
def overview(query):
  if query.format == 'number': 
    return integer_overview(query)
  elif query.format =='time':
    return time_overview(query)
  elif query.format == 'text':
    return text_overview(query)
  else:
    return [{'name': '', 'value': ''}]

def analyze_query_data(query):
  if query.format == 'number': 
    return analyze_integer_query_data(query)
  elif query.format =='time':
    return analyze_time_query_data(query)
  elif query.format == 'text':
    return analyze_text_query_data(query)
  else:
    return [{'name': '', 'value': ''}]

