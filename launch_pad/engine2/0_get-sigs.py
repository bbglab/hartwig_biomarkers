#!/usr/bin/env python
# coding: utf-8

# In[5]:


import sys
import os

sys.path.insert(0, f'{os.path.dirname(os.getcwd())}/')

from mission_control.treasure_map import FPS_DIR, SIGS_DIR
from mission_control.sigs_help import get_sample, get_tnc_df

import pandas as pd 
import pickle
from multiprocessing import Pool


# #### 0 - Get file paths 

# In[2]:


with open( FPS_DIR + "somatic_files.txt", "rb") as fp:
    somatic_files = pickle.load(fp)  


# #### 1 - Collect TNC counts

# In[ ]:


def tnc_file_task( i_file: str):
    if os.path.isfile(i_file):
        print(i_file)
        return get_tnc_df( i_file )
    else:
        print("Missing! " + i_file)


# In[ ]:


p = Pool()
tncs = p.map( tnc_file_task, somatic_files )
p.close()
p.join()


# In[6]:


pd.concat(tncs).fillna(0).to_csv( SIGS_DIR + 'tncs.csv' )

