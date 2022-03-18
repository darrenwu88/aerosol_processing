import pandas as pd
import numpy as np
import os
import glob
#df_sn = pd.read_csv("countrySN.csv", header = 0) 
#print(type(df_sn.loc[int(df_sn[df_sn['Serial Number']==81432123009].index[0]), 'Serial Number']))
#print(int(df_sn[df_sn['Serial Number']==81432123009].index.values[0]))
#print(type(int(df_sn[df_sn['Serial Number']==81432123009].index[0])))



PATH = r"C:\Users\wudar\Desktop\Bergin_Research\partialScripts"
joined_files = os.path.join(PATH, "Dhaka*.csv")
joined_list = glob.glob(joined_files)
#df_values = pd.read_csv('81432123017_2022-01-01_2022-03-03.csv', header = None, sep = r',(?!\s)', nrows = 7)
#site_name = df_values.iloc[3][1]
#print(site_name)
#for file in joined_list:
        #print((os.path.splitext(os.path.basename(file))[0]).split('(inside)')[0])

df = pd.read_csv(r"C:\Users\wudar\Desktop\Bergin_Research\partialScripts\81432039072_2021-12-30_2022-01-02.csv", skiprows = 8, header = [0, 1])
df['Timestamp', 'UTC'] =  pd.to_datetime(df['Timestamp', 'UTC'], format='%m/%d/%Y %H:%M')

    #account for times where data isn't continuous
if (len(df['Timestamp', 'UTC']) != 0):
        sensor_timedelta = df['Timestamp', 'UTC'].diff().value_counts().idxmax().total_seconds() / 60
        df.insert(len(df.columns),'Time Delta', sensor_timedelta)

df_hourly = df
timestamp = df_hourly['Timestamp', 'UTC']
#df_hourly['Timestamp', 'UTC'] =  pd.to_datetime(df_hourly['Timestamp', 'UTC'], format='%m/%d/%Y %H:%M')
if (df_hourly['Time Delta'].iloc[0] == 1.0):
        grouping = df_hourly.groupby([df_hourly['Timestamp', 'UTC'].dt.year, df_hourly['Timestamp', 'UTC'].dt.month, df_hourly['Timestamp', 'UTC'].dt.day, df_hourly['Timestamp', 'UTC'].dt.hour])
        df_hourly = grouping.filter(lambda x: len(x) >= 45)
        df_hourly.to_csv('test.csv', index = False )

elif (df_hourly['Time Delta'].iloc[0] == 5.0):
        grouping = df_hourly.groupby([df_hourly['Timestamp', 'UTC'].dt.year, df_hourly['Timestamp', 'UTC'].dt.month, df_hourly['Timestamp', 'UTC'].dt.day, df_hourly['Timestamp', 'UTC'].dt.hour])
        df_hourly = grouping.filter(lambda x: len(x) >= 9)

elif (df_hourly['Time Delta'].iloc[0] == 15.0):
        grouping = df_hourly.groupby([df_hourly['Timestamp', 'UTC'].dt.year, df_hourly['Timestamp', 'UTC'].dt.month, df_hourly['Timestamp', 'UTC'].dt.day, df_hourly['Timestamp', 'UTC'].dt.hour])
        df_hourly = grouping.filter(lambda x: len(x) >= 3)

td = df_hourly['Time Delta'].iloc[0]
completeness_criteria = (60.0 / td) * 0.75
grouping = df_hourly.groupby([df_hourly['Timestamp', 'UTC'].dt.year, df_hourly['Timestamp', 'UTC'].dt.month, df_hourly['Timestamp', 'UTC'].dt.day, df_hourly['Timestamp', 'UTC'].dt.hour])
df_hourly = grouping.filter(lambda x: len(x) >= completeness_criteria)
df_hourly.to_csv('test.csv', index = False )

#df_hourly.set_index(df_hourly['Timestamp', 'UTC'])
df_hourly = df_hourly.groupby([df_hourly['Timestamp', 'UTC'].dt.year, df_hourly['Timestamp', 'UTC'].dt.month, df_hourly['Timestamp', 'UTC'].dt.day, df_hourly['Timestamp', 'UTC'].dt.hour],as_index=False).mean()
print(df_hourly)
df_hourly.insert(0,'Timestamp (UTC)', timestamp)
df_hourly.to_csv('test.csv', index = False)
