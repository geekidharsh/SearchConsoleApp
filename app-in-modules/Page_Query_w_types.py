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

# change property url with the properties you have verified on Google Webmaster Tool
property_url = ['http://www.example1.com', 'https://www.example2.com', 'http://www.example3.com', 'https://www.example4.com']
# to enable data from all search types be pulled in a single script run
searchtypes = ['web', 'image', 'video']

#create output folders at the location
pq_loc = os.getcwd()+"/"+"Page_Query"
pq_path= pq_loc+"/"+start_date+"-"+end_date
file_path = pq_path+"/"

#check if the folders exists already
if (os.path.exists(pq_loc)): 
  if (os.path.exists(pq_path)):
    print "Error: Folder for given dates exists at the location:", pq_path
  else: 
    os.mkdir(pq_path)
    for types in searchtypes:
      os.mkdir(file_path+types)
else:
  os.mkdir(pq_loc)
  os.mkdir(pq_path)
  for types in searchtypes:
    os.mkdir(file_path+types)


def main(argv):
  service, flags = sample_tools.init(
      argv, 'webmasters', 'v3', __doc__, __file__, parents=[argparser], #understand what __doc__ and __file__ is 
      scope='https://www.googleapis.com/auth/webmasters.readonly')
  filecount = 0
  # Any days without data will be missing from the results.  
  for url in property_url:
    for types in searchtypes:
      try:
        #Run two different request to pull incoming data and store them. 'rows' selects only rows from the incoming data
        # first_response
        response = execute_request(service, url, request_data(0, types))
        first_response = response['rows']
        first_response = json_normalize(first_response)
        # cleaning the data below
        first_response['URL'], first_response['Query'] = first_response['keys'].apply(get_first),first_response['keys'].apply(get_second)        
        first_response.drop('keys', axis=1, inplace=True)
        first_response = first_response.assign(searchtype = types) 
        first_response = first_response.assign(startDate = start_date) 
        first_response = first_response.assign(endDate = end_date)
        
        # Repeat the same process in second_response
        if types == 'video': #ignoring second response for videos with rows over 5000 while running others
          pass
        else:
          response = execute_request(service, url, request_data(5000, types))
          second_response = response['rows']
          second_response = json_normalize(second_response)
          second_response['URL'], second_response['Query'] = second_response['keys'].apply(get_first),second_response['keys'].apply(get_second)
          second_response.drop('keys', axis=1, inplace=True)
          second_response = second_response.assign(searchtype = types) 
          second_response = second_response.assign(startDate = start_date) 
          second_response = second_response.assign(endDate = end_date)
          # merging both responses together in a single dataframe
          first_response = first_response.append(second_response, ignore_index=True)
          
        #saving to file(s)
        file_name = file_path+types+"/"+str(url).replace("://","-")+"-"+types+".csv"
        first_response.to_csv(file_name, encoding="utf-8")
        filecount = filecount+1
        print "Finished all of\t:\t", url, types
      except Exception as e:
        print "Error on:\t", url, types, e
  
  print "\n"+str(filecount)+" new files page-query files generated at the location." 

def request_data(startrow, searchtype):
  request = {
      'startDate': start_date,
      'endDate': end_date,
      'dimensions': ['page', 'query'],
      'startRow': startrow,
      'rowLimit': 5000, # row limit has been changed for testing
      'searchType': searchtype}
  return request

def execute_request(service, url, request):
  return service.searchanalytics().query(siteUrl=url, body=request).execute()

def get_first(key_list):
  return key_list[0]

def get_second(key_list):
  return key_list[1]

if __name__ == '__main__':
  main(sys.argv)
