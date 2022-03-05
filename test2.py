import pandas as pd
import numpy as np
import os
import glob
#df_sn = pd.read_csv("countrySN.csv", header = 0) 
#print(type(df_sn.loc[int(df_sn[df_sn['Serial Number']==81432123009].index[0]), 'Serial Number']))
#print(int(df_sn[df_sn['Serial Number']==81432123009].index.values[0]))
#print(type(int(df_sn[df_sn['Serial Number']==81432123009].index[0])))



PATH = r"C:\Users\wudar\Desktop\Bergin_Research"
joined_files = os.path.join(PATH, "8143*.csv")
joined_list = glob.glob(joined_files)
#df_values = pd.read_csv('81432123017_2022-01-01_2022-03-03.csv', header = None, sep = r',(?!\s)', nrows = 7)
#site_name = df_values.iloc[3][1]
#print(site_name)
for file in joined_list:
        os.remove(file)
        #df_values = pd.read_csv(file, header = None, nrows = 7)
        #site_name = df_values.iloc[3][1]
