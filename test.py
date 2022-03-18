import pandas as pd

df_hourly = pd.read_csv('Level0.csv')

time = pd.to_datetime(df_hourly['Timestamp (UTC)'], format='%m/%d/%Y %H:%M')

#df_hourly = td_grouping.filter(lambda x: len(x) >= 0)
grouping = df_hourly.groupby(['Serial Number', time.dt.year, time.dt.month, time.dt.day, time.dt.hour]).transform(lambda x: len(x))
count = grouping['Time Delta']
df_hourly.insert(len(df_hourly.columns),'Entry Count', count)

df_hourly = df_hourly[df_hourly['Entry Count'] * df_hourly['Time Delta'] >= 45]

df_hourly_groups = df_hourly.groupby(['Serial Number', time.dt.year, time.dt.month, time.dt.day, time.dt.hour, 
                                        'Country', 'Site Name', 'Longitude', 'Latitude', 'is_indoors'], as_index = True)

df_hourly = df_hourly_groups[['PM1.0 (ug/m3)','PM2.5 (ug/m3)','PM4.0 (ug/m3)','PM10 (ug/m3)',
                            'PM0.5 NC (#/cm3)','PM1.0 NC (#/cm3)','PM2.5 NC (#/cm3)','PM4.0 NC (#/cm3)',    
                            'PM10 NC (#/cm3)','Typical Particle Size (um)','Temperature (Celsius)',
                            'Relative Humidity (%)', 'Time Delta', 'Entry Count']].mean()

df_hourly = df_hourly.reset_index(level = ['Serial Number', 'Country', 'Site Name', 'Longitude', 'Latitude', 'is_indoors'])
df_hourly.insert(3,'Timestamp (UTC)', df_hourly.index)
df_hourly.insert(9,'Applied PM2.5 Custom Calibration Factor', "")
df_hourly.insert(12,'Applied PM10 Custom Calibration Factor', "")

''' df.loc[(df['Time Delta'] >= 10) & (df['PM1.0 (ug/m3)'].astype(int) >= 1000), ['PM1.0 (ug/m3)']] = 1000
df.loc[(df['Time Delta'] >= 5) & (df['PM1.0 (ug/m3)'] >= 2000), ['PM1.0 (ug/m3)']] = 2000
df.loc[(df['Time Delta'] >= 1) & (df['PM1.0 (ug/m3)'] >= 5000), ['PM1.0 (ug/m3)']] = 5000

df.loc[(df['Time Delta'] >= 10) & (df['PM2.5 (ug/m3)'] >= 1000), ['PM2.5 (ug/m3)']] = 1000
df.loc[(df['Time Delta'] >= 5) & (df['PM2.5 (ug/m3)'] >= 2000), ['PM2.5 (ug/m3)']] = 2000
df.loc[(df['Time Delta'] >= 1) & (df['PM2.5 (ug/m3)'] >= 5000), ['PM2.5 (ug/m3)']] = 5000

df.loc[(df['Time Delta'] >= 10) & (df['PM4.0 (ug/m3)'] >= 1000), ['PM4.0 (ug/m3)']] = 1000
df.loc[(df['Time Delta'] >= 5) & (df['PM4.0 (ug/m3)'] >= 2000), ['PM4.0 (ug/m3)']] = 2000
df.loc[(df['Time Delta'] >= 1) & (df['PM4.0 (ug/m3)'] >= 5000), ['PM4.0 (ug/m3)']] = 5000

df.loc[(df['Time Delta'] >= 10) & (df['PM10 (ug/m3)'] >= 1000), ['PM10 (ug/m3)']] = 1000
df.loc[(df['Time Delta'] >= 5) & (df['PM10 (ug/m3)'] >= 2000), ['PM10 (ug/m3)']] = 2000
df.loc[(df['Time Delta'] >= 1) & (df['PM10 (ug/m3)'] >= 5000), ['PM10 (ug/m3)']] = 5000 '''


df_hourly.to_csv('dsdf.csv', index = False)