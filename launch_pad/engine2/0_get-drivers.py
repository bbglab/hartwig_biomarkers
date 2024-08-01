#!/usr/bin/env python
# coding: utf-8

# In[3]:


import sys
import os 

sys.path.insert(0, f'{os.path.dirname(os.getcwd())}/')

from mission_control.treasure_map import FPS_DIR, TMP_DIR
from mission_control.driver_help import create_driver_df, create_driver_df2

import pandas as pd
import pickle


# In[4]:


with open( FPS_DIR + "linx_files.txt", "rb") as fp:
    linx_paths = pickle.load(fp)  
    
with open( FPS_DIR + "driver_files.txt", "rb") as fp:
    driver_files = pickle.load(fp)      


# In[5]:


driver_files[0]


# In[ ]:


driver_dfs_linx = []
for i in linx_paths:
    driver_dfs_linx.append(create_driver_df(i+'.linx.drivers.tsv'))    
    
driver_dfs_purple = []
for i in driver_files:
    driver_dfs_purple.append(create_driver_df2(i))       


# In[7]:


pd.concat( driver_dfs_linx ).to_csv( TMP_DIR + 'drivers_DB_linx.csv', index = False)
pd.concat( driver_dfs_purple ).to_csv( TMP_DIR + 'drivers_DB_purple.csv', index = False)

