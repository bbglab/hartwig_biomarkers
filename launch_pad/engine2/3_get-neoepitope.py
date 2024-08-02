#!/usr/bin/env python
# coding: utf-8

# In[2]:


import sys
import os

sys.path.insert(0, f'{os.path.dirname(os.getcwd())}/')

from mission_control.treasure_map import FPS_DIR, TMP_DIR
from mission_control.isofox_help import get_neoepitope_features

import os
import pandas as pd 
import pickle


# #### 0 - Get file paths 

# In[3]:


with open( FPS_DIR + "neoepitope_files.txt", "rb") as fp:
    neoepitope_files = pickle.load(fp)


# #### 1 - Run it

# In[ ]:


features = []
for i_file in neoepitope_files:
    if os.path.isfile(i_file):
        print(i_file)
        features.append(get_neoepitope_features(i_file))
    else:
        print("Missing! " + i_file)        


# #### 2 - Output

# In[4]:


pd.DataFrame( features ).to_csv(TMP_DIR + 'neoepitope_ready.csv', index=False)

