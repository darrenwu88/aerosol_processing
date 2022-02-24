import os
import glob
import requests
import pandas as pd
import numpy as np

#subprocess pack
from subprocess import call

""" 
    Author: Darren Wu 
    Date: 2/18/2022

    This program parses through all the downloaded sensor data from the API and merges all the .csv files together. 
    It sorts the merged .csv file by timestamp. The individual "merged data" can also be sourced from their respective
    serial number, longitude, and latitude values in the same row.

"""

#define PATH var from retrieved data
PATH = r"C:\Users\wudar\Desktop\Bergin"

#retrieve data (.csv files) from TSI-LINK API
call(["python", "get_data.py"])

#create file list by matching files with "8143" index in their serial number/filename. 
joined_files = os.path.join(PATH, "8143*.csv")
joined_list = glob.glob(joined_files)

#add 3 cols within each csv file (sensor): serial number, long, lat
for file in joined_list:
    #retrieve values from sensor ID data
    df_values = pd.read_csv(file, header = None, nrows = 7)
    serial_number = df_values.iloc[2][1]
    lat_value = df_values.iloc[5][1]
    long_value = df_values.iloc[6][1]

    df = pd.read_csv(file, skiprows = 8, header = [0, 1])   
   
    # Serial / Timestamp / Long / Lat   format
    df.insert(0,"Serial Number", serial_number)
    df.insert(2,"Longitude", long_value)
    df.insert(3,"Latitude", lat_value)

    #overwrite csv files
    df.to_csv(file, index = False)

#merge all csv files in file list
df_test = pd.concat(map(lambda file: pd.read_csv(file, header = [0,1]), joined_list), ignore_index = True)

#Sort by datetime in merged csv file
df_test = df_test.sort_values(by = ("Timestamp", "UTC"), ascending = True)

#Remove NaN populated values in the units row
df_test = df_test.rename(columns = lambda x: x if not "Unnamed" in str(x) else "")

#output
df_test.to_csv("merged.csv", index = False)

#option to delete the original files (for storage space purposes)
for file in joined_list:
    os.remove(file)