#!/usr/bin/python

"""
Sample usage:
  $ python search_analytics_api_******.py 2015-05-01  2015-05-30
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

start_date = str(sys.argv[1]).strip()
end_date = str(sys.argv[2]).strip()
property_url = []

#create output folders at the location
cl_loc = os.getcwd()+"/"+"Country_Level"
cl_path= cl_loc+"/"+start_date+"-"+end_date

#check if the folders exists already
if (os.path.exists(cl_loc)): 
  if (os.path.exists(cl_path)):
    print "Folder for give dates exists at the location", cl_path
  else: 
    os.mkdir(cl_path)
else:
  os.mkdir(cl_loc)
  os.mkdir(cl_path)

def main(argv):
  service, flags = sample_tools.init(
      argv, 'webmasters', 'v3', __doc__, __file__, parents=[argparser], #understand what __doc__ and __file__ is 
      scope='https://www.googleapis.com/auth/webmasters.readonly')

  # Any days without data will be missing from the results.  
  request_one = {
      'startDate': start_date,
      'endDate': end_date,
      'dimensions': ['country', 'date'],
      'rowLimit': 5000,
      'startRow':0}

  request_two = {
      'startDate': start_date,
      'endDate': end_date,
      'dimensions': ['country', 'date'],
      'rowLimit': 5000,
      'startRow':5000}

  final_data = pd.DataFrame()

  for url in property_url:
    try:
      response = execute_request(service, url, request_one)
      firsthalf_data = response['rows']
      firsthalf_data = json_normalize(firsthalf_data)
# get another 5000 rows of data
      response = execute_request(service, url, request_two)
      sechalf_data = response['rows']
      sechalf_data = json_normalize(sechalf_data)
# drop duplicates
      firsthalf_data['Country'],firsthalf_data['Date'] = firsthalf_data['keys'].apply(get_first),firsthalf_data['keys'].apply(get_second)
      sechalf_data['Country'],sechalf_data['Date'] = sechalf_data['keys'].apply(get_first),sechalf_data['keys'].apply(get_second)
      firsthalf_data.drop('keys', axis=1, inplace=True)
      sechalf_data.drop('keys', axis=1, inplace=True)
# merge dataframes together
      firsthalf_data = firsthalf_data.append(sechalf_data, ignore_index=True)
      firsthalf_data = firsthalf_data.assign(site = url)
      final_data = final_data.append(firsthalf_data, ignore_index=True)
      print "Finished with: ", url
    except:
      print "Failed to pull: ", url

  # Store date in files
  file_name = cl_path+"/"+str(start_date+end_date)+"country_level"+".csv"
  final_data.to_csv(file_name, encoding="utf-8")


def execute_request(service, url, request):
    return service.searchanalytics().query(siteUrl=url, body=request).execute()

def get_first(key_list):
  return key_list[0]

def get_second(key_list):
  return key_list[1]


if __name__ == '__main__':
  main(sys.argv)
