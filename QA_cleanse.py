import pandas as pd
import numpy as np

df_raw = pd.read_csv('mergedfinal.csv')

#drop the calibration columns
df_raw.drop(df_raw.columns[[6, 9]], axis = 1, inplace = True)

#insert Case Error
case_error = df_raw['Device Status'][1:].astype(int).map(lambda x: (f'{x:08b}')).astype(str).map(lambda x: x[0:5]).map(lambda x: x[-1:])
df_raw.insert(len(df_raw.columns), 'Case Error', case_error)

#insert PM Sensor Error
PM_sensor_error = df_raw['Device Status'][1:].astype(int).map(lambda x: (f'{x:08b}')).astype(str).map(lambda x: x[0:4]).map(lambda x: x[-1:])
df_raw.insert(len(df_raw.columns), 'PM Sensor Error', PM_sensor_error)

#Remove T, RH if case_error = 1
df_raw.loc[df_raw['Case Error'] == '1', ['Temperature', 'Relative Humidity']] = None

#Remove PM2.5, PM10 if pm_sensor_error = 1
df_raw.loc[df_raw['PM Sensor Error'] == '1', ['PM2.5 NC', 'PM10 NC']] = None

#delete error columns
df_raw.drop(['Case Error', 'PM Sensor Error'], axis = 1, inplace = True)

#collapse headers
for col in df_raw.columns:
    # get first row value for this specific column
    first_row = df_raw.iloc[0][col]
    new_column_name = str(col) + ' (' + str(first_row) + ')'  #first_row
    # rename the column with the existing column header plus the first row of that column's data 
    df_raw.rename(columns = {col: new_column_name}, inplace = True)

df_raw = df_raw.rename(columns = lambda x: x if not "(nan)" in str(x) else x[:(len(x) - 6)])
df_raw.drop([0], inplace = True)

df_raw["Serial Number"] = df_raw["Serial Number"].astype(np.int64)

#output
df_raw.to_csv('RefinedData.csv', index = False)