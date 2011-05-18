import logging, math
from datetime import datetime, timedelta

from model import User, Query, DataPoint

def analyze_text_query_data(query):
  datapoints = DataPoint.get_by_query(query)
  analytic_list = []

  analytic_list.extend(basic_suite(datapoints))

  return analytic_list

def basic_suite(datapoints):
  basic_list = []

  basic_list.append(('Common Words', common_words(datapoints)))
  
  return basic_list

# we can probably map reduce this shit
def common_words(datapoints):
  word_counter = {}

  # foreach datapoint
    # tokenize the text
    # add each word into word_counter
  for dp in datapoints:
    words = dp.text.split()
    for word in words:
      logging.info('Word: ' + word)
      if word in word_counter:
        word_counter[word] = word_counter[word] + 1
      else:
        word_counter[word] = 1
  
  # find the three highest word counts in word_counter
  popular = sorted(word_counter, key = word_counter.get, reverse = True)

  # return the top three, if there are three.
  top_three = ''
  length = len(popular)
  if length > 0:
    top_three += popular[0]
  if length > 1:
    top_three += ', ' + popular[1]
  if length > 2: 
    top_three += ', ' + popular[2]

  return top_three
