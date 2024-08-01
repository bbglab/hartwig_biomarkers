#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
import os

sys.path.insert(0, f'{os.path.dirname(os.getcwd())}/')

from mission_control.treasure_map import FPS_DIR, TMP_DIR
from mission_control.cnv_help import get_scna

import os
import pandas as pd 
import pickle
import warnings
warnings.filterwarnings('ignore')


# #### 0 - Get file paths 

# In[2]:


with open( FPS_DIR + "cnv_files.txt", "rb") as fp:
    cnv_files = pickle.load(fp)  


# #### 1 - Run it

# In[5]:


features = []
for i_file in cnv_files:
    if os.path.isfile(i_file):
        features.append(get_scna(i_file))
    else:
        print("Missing path! " + i_file)


# #### 2 - Output

# In[4]:


pd.DataFrame(features).to_csv( TMP_DIR + 'cnv_ready.csv', index = False) 

