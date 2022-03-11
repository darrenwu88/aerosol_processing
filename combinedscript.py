import requests
import json
from datetime import datetime
import os
import pandas as pd
import numpy as np
import glob

""" 
    Author: Darren Wu 
    Date: 2/28/2022

    This program parses through all the downloaded sensor data from the API and merges all the .csv files together. 
    It sorts the merged .csv file by timestamp. The individual "merged data" can also be sourced from their respective
    serial number, longitude, and latitude values in the same row.

    Unlike the merge_csv.py script, this program is able to take multiple .json "secret keys" as inputs; therefore, 
    collaborators' sensors' data can be aggregated together as well.

    The script also deploys QA operations on the .csv files for the Bergin Lab. See QA_cleanse.py for more info.

"""

def get_data(json_fname):
#replace filename with your file from TSI-Link API
    with open(json_fname) as cred_file:  
        cred_data = json.load(cred_file)

#read security token cache file
    CACHE_FILENAME = "TOKENCACHE_" + json_fname[8:-5] + ".txt" #identifying token for each secret
    tok_expires = 86400 #24 hrs typical
    BUFFER = 60 #seconds.  How long it takes to run the rest of your program 
# after reading the security token.  Increase if needed.
    tokencached = False
    if os.path.exists(CACHE_FILENAME):
        modified=os.path.getmtime(CACHE_FILENAME)
        now = datetime.now().timestamp()    
        delta = now - modified
        if delta < (tok_expires - BUFFER):  #if token is still valid, read it
            tokencached = True
        else:
            tokencached = False
            print("Token code expired: get new token and write to file")
    else:
        tokencached = False
        print("No token code file found")
    
    if tokencached == True:
        cfile = open(CACHE_FILENAME,'r')
        tok_code = cfile.read()
        print("Read valid token code")
        cfile.close()
    else:
    #need to get token and write to file
        url = "https://tsilink.com/oauth/token"
        payload = json.dumps({
        "grant_type": "client_credentials",
        "client_id": cred_data['id'],                  
        "audience": cred_data['audience'],
        "client_secret": cred_data['secret'], 
        })
    
        headers = {
        'Content-Type': 'application/json'
        }
    
        response = requests.request("POST", url, headers=headers, data=payload)
        response_json = response.json()
        tok_code = response_json['access_token']
        tok_type = response_json['token_type'] 
        tok_expires = int(response_json['expires_in'])
    
        cfile = open(CACHE_FILENAME,'w')
        cfile.write(tok_code)
        cfile.close()
        print("Token written to file")

    url = "https://tsilink.com/api/v2/external/devices"
    payload={}
    headers={}
    tok_code = "Bearer " + tok_code
    headers['Authorization'] = tok_code
    response = requests.request("GET", url, headers=headers, data=payload)
    response_json = response.json()
#Extract useful information from response and store in sensor_info dict
    num_sensors = len(response_json)
    sensor_info = []
    for dic in response_json:
        meta = dic['metadata']
        dic2 = {}
        dic2.update({
            'account_id': dic['account_id'], 
            'device_id': dic['device_id'],
            'model': dic['model'], 
            'serial': dic['serial'],
            'friendlyName': meta['friendlyName'],
            'is_indoor': meta['is_indoor'],
            'latitude': meta['latitude'], 
            'longitude': meta['longitude'],
            })
        sensor_info.append(dic2)
    
#print(sensor_info)

    url = "https://tsilink.com/api/v2/external/telemetry"
    params={}
    payload={}
    headers={}
    fname_s = fname_e = ""
    data_start_date = data_age = data_end_date = ""
    headers['Authorization'] = tok_code
#optional arguments
    headers.update({'Accept': 'text/csv'})  #comment out this line for json
    #data_age="&age=1" #days of data (can be used with start date)
    data_start_date = "&start_date=2021-12-01T00:00:00.000Z"  #use UTC format.  
    data_end_date = "&end_date=2021-12-31T23:59:59.000Z"  #use UTC format
    if (data_start_date != "" and data_end_date != ""):
        fname_s = data_start_date[12:22]  #only want the date part of the string
        fname_e = data_end_date[10:20]
    for x in range(num_sensors):
        filename = sensor_info[x]['serial']+"_"+fname_s+"_"+fname_e+".csv"
        dev_id="?device_id="+sensor_info[x]['device_id']
        response = requests.request("GET", url+dev_id+data_age+data_start_date+\
                                    data_end_date, headers=headers, data=payload)
#-------------- Save telemetry data to .csv files --------------
        f = open(filename,"w")
        f.write("device_id,"+sensor_info[x]['device_id']+"\n")
        f.write("model,"+sensor_info[x]['model']+"\n")
        f.write("serial,"+sensor_info[x]['serial']+"\n")
        f.write("friendlyName,"+sensor_info[x]['friendlyName']+"\n")
        f.write("is_indoor,"+format(sensor_info[x]['is_indoor'])+"\n")
        f.write("latitude,"+format(sensor_info[x]['latitude'])+"\n")
        f.write("longitude,"+format(sensor_info[x]['longitude'])+"\n")
        f.write("\n")
        f.write(response.text)
        f.close()

def mergeindividual():
    PATH = r"C:\Users\wudar\Desktop\Bergin_Research"

#retrieve data (.csv files) from TSI-LINK API
    get_data("secrets-c2mgvpsfp7ufo92pvpp0.json")
    get_data("secrets-c4257c0qi9clu8nikfgg.json")
    get_data("secrets-c3pq1sgqi9clu8nik8sg.json")
    get_data("secrets-c3ntnbr5lksr8n0vf7d0.json")
    get_data("secrets-c3r1gb0qi9clu8nik91g.json")
    get_data("secrets-c3t9bo8qi9clu8nikakg.json")
    get_data("secrets-c3smtl0qi9clu8nikadg.json")
#create file list by matching files with "8143" index in their serial number/filename. 
    joined_files = os.path.join(PATH, "8143*.csv")
    joined_list = glob.glob(joined_files)

#add 3 cols within each csv file (sensor): serial number, long, lat
    for file in joined_list:
    #retrieve values from sensor ID data
        df_values = pd.read_csv(file, header = None, sep = r',(?!\s)', nrows = 7)
        serial_number = df_values.iloc[2][1]
        lat_value = df_values.iloc[5][1]
        long_value = df_values.iloc[6][1]
        site_name = df_values.iloc[3][1]
        is_indoors = df_values.iloc[4][1]
    #retrieve values from countrysn.csv
        df_sn = pd.read_csv("countrySN.csv", header = 0)  
        country = df_sn.loc[int(df_sn[df_sn['Serial Number'] == int(serial_number)].index[0]), 'Country']

    #read df
        df = pd.read_csv(file, skiprows = 8, header = [0, 1])  
    
    #Serial / Site Name / Country / Timestamp / Long / Lat / is_indoors   format 
        df.insert(0,"Serial Number", serial_number)
        df.insert(1,"Country", country)
        df.insert(2,'Site Name', site_name)
        df.insert(4,"Longitude", long_value)
        df.insert(5,"Latitude", lat_value)
        df.insert(6,"is_indoors", is_indoors)
    
    #calculate time delta of sensor data retrieval (e.g. 15 min or 1 min usually)
        timetime =  pd.to_datetime(df['Timestamp', 'UTC'], format='%m/%d/%Y %H:%M')

    #account for times where data isn't continuous
        if (len(timetime) != 0):
                sensor_timedelta = timetime.diff().value_counts().idxmax().total_seconds() / 60
                df.insert(len(df.columns),'Time Delta', sensor_timedelta)


    #for shuba, comment out otherwise
        df.insert(4, "Year", timetime.dt.strftime('%Y'))
        df.insert(5, "Month", timetime.dt.strftime('%m'))
        df.insert(6, "Day", timetime.dt.strftime('%d'))
        df.insert(7, "Hour", timetime.dt.strftime('%H'))

        #overwrite csv files
        df.to_csv(file, index = False)

    #merge all csv files in file list
    df_test = pd.concat(map(lambda file: pd.read_csv(file, header = [0,1]), joined_list), ignore_index = True)

    #Remove NaN populated values in the units row
    df_test = df_test.rename(columns = lambda x: x if not "Unnamed" in str(x) else "")

    #output
    df_test.to_csv("RAW.csv", index = False)


#option to delete the original files (for storage space purposes)
    for file in joined_list:
        os.remove(file)

#method for outputting merged everything   
def mergeeverything():
    
    mergeindividual()

    df_raw = pd.read_csv('RAW.csv')
    #df_raw = mergeindividual()
    
    #drop the calibration columns
    #df_raw.drop(df_raw.columns[[6, 9]], axis = 1, inplace = True)
    #df_raw.drop(df_raw.columns[[9, 12]], axis = 1, inplace = True)

    #collapse headers
    for col in df_raw.columns:
        # get first row value for this specific column
        first_row = df_raw.iloc[0][col]
        new_column_name = str(col) + ' (' + str(first_row) + ')'  #first_row
        # rename the column with the existing column header plus the first row of that column's data 
        df_raw.rename(columns = {col: new_column_name}, inplace = True)

    df_raw = df_raw.rename(columns = lambda x: x if not "(nan)" in str(x) else x[:(len(x) - 6)])
    df_raw.drop([0], inplace = True)

    #sort datetime column correctly
    df_raw["Timestamp (UTC)"] = pd.to_datetime(df_raw["Timestamp (UTC)"])
    df_raw = df_raw.sort_values(by = "Timestamp (UTC)", ascending = True, kind = 'mergesort')
    #reformat datetime into original format 
    df_raw["Timestamp (UTC)"] = df_raw["Timestamp (UTC)"].dt.strftime("%m/%d/%Y %H:%M")

    #revert type of serial number column
    df_raw["Serial Number"] = df_raw["Serial Number"].astype(np.int64)


    df_raw.to_csv('Level0.csv', index = False)

    ### LEVEL 1 QA

    #insert Case Error
    case_error = df_raw['Device Status'][1:].astype(int).map(lambda x: (f'{x:08b}')).astype(str).map(lambda x: x[0:5]).map(lambda x: x[-1:])
    df_raw.insert(len(df_raw.columns), 'Case Error', case_error)

    #insert PM Sensor Error
    PM_sensor_error = df_raw['Device Status'][1:].astype(int).map(lambda x: (f'{x:08b}')).astype(str).map(lambda x: x[0:4]).map(lambda x: x[-1:])
    df_raw.insert(len(df_raw.columns), 'PM Sensor Error', PM_sensor_error)

    #Remove T, RH if case_error = 1
    df_raw.loc[df_raw['Case Error'] == '1', ['Temperature (Celsius)', 'Relative Humidity (%)']] = None

    #Remove PM2.5, PM10 if pm_sensor_error = 1
    df_raw.loc[df_raw['PM Sensor Error'] == '1', 
        ['PM1.0 (ug/m3)', 'PM2.5 (ug/m3)', 'PM4.0 (ug/m3)', 'PM10 (ug/m3)', 
        'PM1.0 NC (#/cm3)', 'PM0.5 NC (#/cm3)', 'PM1.0 NC (#/cm3)', 'PM2.5 NC (#/cm3)', 
        'PM4.0 NC (#/cm3)', 'PM10 NC (#/cm3)', 'Typical Particle Size (um)']] = None

    #delete error columns
    df_raw.drop(['Case Error', 'PM Sensor Error'], axis = 1, inplace = True)

    ### OUTPUT
    #output
    df_raw.to_csv('Level1.csv', index = False)

    

#user input for RAW or MERGED file
userinput = input("Which output do you want: RAW or MERGED? (1/2)")

if userinput == "1":
    print("hahaha")

elif userinput == "2":
    mergeeverything()

else:
    print("Wrong user input. Try again.")

