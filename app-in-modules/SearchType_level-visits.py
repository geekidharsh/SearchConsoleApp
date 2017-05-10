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
searchType_dir = os.getcwd()+"/"+"SearchType_Level"
searchType_path = searchType_dir+"/"+"SearchType-Level-"+start_date+"-"+end_date

#check if the folder exists already
if os.path.exists(searchType_dir): 
  if os.path.exists(searchType_path):
    print "Folder for give dates exists at the location", searchType_dir
  else: 
    os.mkdir(searchType_path)
else:
  os.mkdir(searchType_dir)
  os.mkdir(searchType_path)

def main(argv):
  service, flags = sample_tools.init(
      argv, 'webmasters', 'v3', __doc__, __file__, parents=[argparser], #understand what __doc__ and __file__ is 
      scope='https://www.googleapis.com/auth/webmasters.readonly')
  final_data = pd.DataFrame()
  # Any days without data will be missing from the results.  
  # Get daily clicks for the date range
  request_web = {
      'startDate': start_date,
      'endDate': end_date,
      'dimensions': ['date'],
      'startRow':0,
      'searchType': ['web']
  }
  request_img = {
      'startDate': start_date,
      'endDate': end_date,
      'dimensions': ['date'],
      'startRow':0,
      'searchType': ['image']
  }
  request_vid = {
      'startDate': start_date,
      'endDate': end_date,
      'dimensions': ['date'],
      'startRow':0,
      'searchType': ['video']
  }

  for url in property_url:
    try:
      #request data for various searchtypes
      response_web = execute_request(service, url, request_web)
      response_img = execute_request(service, url, request_img)
      response_vid = execute_request(service, url, request_vid)

      #stores all incoming data here. 'rows' selects only rows from the incoming data
      web_data = response_web['rows']
      img_data = response_img['rows']
      vid_data = response_vid['rows']

      #normalize all kinds of data
      web_data = json_normalize(web_data)
      img_data = json_normalize(img_data)
      vid_data = json_normalize(vid_data)

      #clean up data
      # web
      web_data['Date'] = web_data['keys']
      web_data.drop('keys', axis=1, inplace=True)
      web_data = web_data.assign(site = url, searchType = 'web')
      final_data = final_data.append(web_data, ignore_index = True)
      # image
      img_data['Date'] = img_data['keys']
      img_data.drop('keys', axis=1, inplace=True)
      img_data = img_data.assign(site = url, searchType = 'image')
      final_data = final_data.append(img_data, ignore_index = True)
      # video
      vid_data['Date'] = vid_data['keys']
      vid_data.drop('keys', axis=1, inplace=True)
      vid_data = vid_data.assign(site = url, searchType = 'video')
      final_data = final_data.append(vid_data, ignore_index = True)

      #store data in based on type
      print "Finished with: ", url
    except Exception as e:
      print e
      print "Failed to pull: ", url
      
  file_name = searchType_path+"/"+"visits-by_searchtype"+start_date+end_date+".csv"
  final_data.to_csv(file_name, encoding="utf-8")

def execute_request(service, url, request):
    return service.searchanalytics().query(siteUrl=url, body=request).execute()


if __name__ == '__main__':
  main(sys.argv)
