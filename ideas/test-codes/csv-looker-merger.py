#!/usr/bin/python

import argparse
import sys
import os
from googleapiclient import sample_tools
import pandas as pd
from pandas.io.json import json_normalize
import json



#create output folders at the location
location = os.getcwd()
files = [] #store the files found at the location
counter = 0
for file in os.listdir(location):
    try:
      if file.endswith(".csv"):
        print "files found:\t", file
        files.append(str(file))
        counter = counter+1
    except Exception as e:
      raise e
print "Total files:\t", counter

def main():
  final_data = pd.DataFrame()

  for file in files:
    try:      
      in_file.from_csv(file)
      # cleaning the data below
      first_response['URL'], first_response['Query'] = first_response['keys'].apply(get_first),first_response['keys'].apply(get_second)        
      first_response.drop('keys', axis=1, inplace=True)
      first_response = first_response.assign(searchtype = types) 
      first_response = first_response.assign(startDate = start_date) 
      first_response = first_response.assign(endDate = end_date)
        
        # Repeat the same process in second_response
        if types == 'video': #ignoring second response for videos with rows over 5000 while running others
          final_data = final_data.append(first_response, ignore_index = True)
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
          final_data = final_data.append(first_response, ignore_index = True)
        print "Finished all of\t:\t", url, types
      except Exception as e:
          print "Error on:\t", url, types, e        
  

# saving to file(s) 
  file_name = file_path+"/"+str(start_date+end_date)+"-page-query"+".csv"
  final_data.to_csv(file_name, encoding="utf-8")
  filecount = filecount+1
  print "\n"+str(filecount)+" new files page-query files generated at the location." 


if __name__ == '__main__':
  main(sys.argv)
