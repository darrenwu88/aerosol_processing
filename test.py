import pandas as pd
import numpy as np

df_test = pd.read_csv('81432039074_2021-12-30_2022-01-02.csv', skiprows = 8, header = [0, 1])
#df_test['Timestamp']['UTC'] = pd.to_datetime(df_test['Timestamp']['UTC'])
#df_test = df_test.sort_values(by = ("Timestamp (UTC)"), ascending = True)

df_test['Timestamp']['UTC'] =  pd.to_datetime(df_test['Timestamp']['UTC'], format='%m/%d/%Y %H:%M')
df_test.to_csv('test.csv', index = False)