"""
Sample usage:  $ python thisfilename.py YYYY-MM-DD YYYY-MM-DD
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
property_url = ['www.example.com'] #replace this with your actual verified property before executing the script

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
  count = 0
  final_data = pd.DataFrame()
  startcount = 0 
  while startcount <= 10000:
    for url in property_url:
      try:
        #'rows' selects only rows from the incoming data
        response = execute_request(service, url, request_data(start_date, end_date, startcount))
        response = response['rows'] 
        response = clean_response(response, url, start_date, end_date)
        final_data = final_data.append(response, ignore_index = True)
        print "Finished with {} {}".format(url, startcount)
        count = count+1
      except Exception as e:
        print e
        print "No response for: ", url, startcount
    startcount = startcount + 5000
    count = count+1
 
  print "Total loops", count
  # saving to file(s) 
  file_name = cl_path+"/"+str(start_date+end_date)+"-country-level"+".csv"
  final_data.to_csv(file_name, encoding="utf-8")
  print "File created at", cl_path

def request_data(start_date, end_date, startrow):
  request = {
      'startDate': start_date,
      'endDate': end_date,
      'dimensions': ['country', 'date'],
      'startRow': startrow,
      'rowLimit': 5000 # row limit
      }
  return request

'''clean_response takes a request for various search types and cleanses it and converts it into a pandas df and returns'''
def clean_response(response, url, start_date, end_date):
  response = json_normalize(response)
  response['Country'], response['Date'] = response['keys'].apply(get_first), response['keys'].apply(get_second)
  response.drop('keys', axis=1, inplace=True)
  response = response.assign(site = url)
  return response

def execute_request(service, url, request):
  return service.searchanalytics().query(siteUrl=url, body=request).execute()

def get_first(key_list):
  return key_list[0]

def get_second(key_list):
  return key_list[1]



if __name__ == '__main__':
  main(sys.argv)