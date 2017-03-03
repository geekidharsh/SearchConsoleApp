#!/usr/bin/python
"""
Sample usage: $ python filename.py 2015-05-01  2015-05-30
"""
import argparse
import sys
import os
from googleapiclient import sample_tools
import pandas as pd
from pandas.io.json import json_normalize
import json

# Declare command-line flags.
argparser = argparse.ArgumentParser(add_help=False)
argparser.add_argument('start_date', type=str,
                       help=('Start date of the requested date range in '
                             'YYYY-MM-DD format.'))
argparser.add_argument('end_date', type=str,
                       help=('End date of the requested date range in '
                             'YYYY-MM-DD format.'))

# take start and end dates from command line flags and store them in arrays
start_date = str(sys.argv[1]).strip()
end_date = str(sys.argv[2]).strip()

# list of all properties to pull data from
# Make sure all the properties list are verified by google under Google Developer Console and that oauth2 is enabled for search console
property_url = ['www.harshvardhanpandey.com']

#create output folders at the location
query_loc = os.getcwd()+"/"+"Page-Query"
query_path= query_loc+"/"+start_date+"-"+end_date

#check if the folders exists already
if (os.path.exists(query_loc)): 
  if (os.path.exists(query_path)):
    print "Error: Folder for given dates exists at the location", query_path
  else: 
    os.mkdir(query_path)
else:
  os.mkdir(query_loc)
  os.mkdir(query_path)

# main function takes the arugments and loops through each url to request data in batches
def main(argv):
  service, flags = sample_tools.init(
      argv, 'webmasters', 'v3', __doc__, __file__, parents=[argparser],
      scope='https://www.googleapis.com/auth/webmasters.readonly')

'''
Below will declare:
  1. an empty dataframe to collect all the cleansed responses into one
  2. startcount is the startrow for request made to the api in request dict. It starts with 0 and is inremented by 
    5000 after every outer loop until 60000 rows. This value can be increased further as needed.
  3. start row is incremented in batches of 5000 only, as per the google doc, row_limit can't be less than 1 and more than 5000.
  4. search_type is a list of all types of search data available with Google : web, image and video searches.
'''
  final_data = pd.DataFrame()
  startcount = 0
  count = 0
  search_type = ['web', 'image', 'video']
  while startcount <= 60000:
    for types in search_type:
      for url in property_url:
        try:
          #'rows' selects only rows from the incoming data
          response = execute_request(service, url, request_data(start_date, end_date, startcount, types))
          response = response['rows']
          response = clean_response(response, url, start_date, end_date, types)
          final_data = final_data.append(response, ignore_index = True)
          print "Finished with {}{}{}".format(url, startcount, types)
          count = count+1

        except Exception as e:
          print e
          print "No response for: ", url, startcount, types
    startcount = startcount + 5000
  print "Total loops", count

  file_name = query_path+"/"+str(start_date+end_date)+"-new-page_query-all.csv"
  final_data.to_csv(file_name, encoding="utf-8")
  print "file saved at:\t", file_name

'''
request_data collects user request within the app and returns a dict collection
'''
def request_data(start_date, end_date, startrow, type):
  request = {
      'startDate': start_date,
      'endDate': end_date,
      'dimensions': ['page', 'query'],
      'startRow': startrow,
      'rowLimit': 5000, # row limit
      'searchType': type
      }
  return request

'''
clean_response takes a request for various search types and cleanses it and converts it into a pandas df and returns
'''
def clean_response(response, url, start_date, end_date, types):
  response = json_normalize(response)
  response['URL'], response['Query'] = response['keys'].apply(key_val), response['keys'].apply(key_val1)
  response.drop('keys', axis=1, inplace=True)
  response = response.assign(site = url, startDate = start_date, endDate = end_date, searchType = types)
  return response

'''
take 'key' values from response['rows'] at [0] and [1] breaks them in to individual indices and returns them
'''
def key_val(key):
  return key[0]

def key_val1(key):
  return key[1]

'''
execute_request makes the actual request to the api servers
'''
def execute_request(service, url, request):
    return service.searchanalytics().query(siteUrl=url, body=request).execute()


if __name__ == '__main__':
  main(sys.argv)