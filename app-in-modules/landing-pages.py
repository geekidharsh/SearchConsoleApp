"""
Sample usage:  $ python search_analytics_api_******.py 2015-05-01  2015-05-30
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
property_url = ['www.harshvardhanpandey.com'] #replace this with your actual verified property before executing the script

#create output folders at the location
lp_loc = os.getcwd()+"/"+"Landing_Pages"
lp_path= lp_loc+"/"+start_date+"-"+end_date

#check if the folders exists already
if (os.path.exists(lp_loc)): 
  if (os.path.exists(lp_path)):
    print "Error: Folder for given dates exists at the location", lp_path
  else: 
    os.mkdir(lp_path)
else:
  os.mkdir(lp_loc)
  os.mkdir(lp_path)

def main(argv):
  service, flags = sample_tools.init(
      argv, 'webmasters', 'v3', __doc__, __file__, parents=[argparser],
      scope='https://www.googleapis.com/auth/webmasters.readonly')
  urls = property_url # temp list to keep all properties
  final_data = pd.DataFrame() #empty dataframe declared here
  startcount = 0
  while len(urls) > 0:
    for url in urls:
      try:
        #'rows' selects only rows from the incoming data
        response = execute_request(service, url, request_data(start_date, end_date, startcount))
        response = response['rows'] 
        response = clean_response(response, url, start_date, end_date)
        final_data = final_data.append(response, ignore_index = True)
        print "Finished working on {} {}".format(url, startcount)
      except Exception as e:
        print "Not enough response for {} at rows {}.".format(url, startcount)
        urls.remove(url)
    startcount = startcount + 5000
  else:
    print "Urls left {}".format(len(urls))
  # saving to file(s) 
  file_name = lp_path+"/"+str(start_date+end_date)+"-pages-all"+".csv"
  final_data.to_csv(file_name, encoding="utf-8")
  print "File created at", lp_path

def request_data(start_date, end_date, startrow):
  request = {
      'startDate': start_date,
      'endDate': end_date,
      'dimensions': ['page'],
      'startRow': startrow,
      'rowLimit': 5000 # row limit
      }
  return request

'''clean_response takes a request for various search types and cleanses it and converts it into a pandas df and returns'''
def clean_response(response, url, start_date, end_date):
  response = json_normalize(response)
  response['URL'] = response['keys'].apply(get_first)
  response.drop('keys', axis=1, inplace=True)
  response = response.assign(startDate = start_date, endDate = end_date, site = url)
  return response

def execute_request(service, url, request):
  return service.searchanalytics().query(siteUrl=url, body=request).execute()

def get_first(key_list):
  return key_list[0]

if __name__ == '__main__':
  main(sys.argv)
