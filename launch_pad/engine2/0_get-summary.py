#!/usr/bin/env python
# coding: utf-8

# In[8]:


import sys
import os

sys.path.insert(0, f'{os.path.dirname(os.getcwd())}/')

from mission_control.treasure_map import FPS_DIR, TMP_DIR
from mission_control.summary_help import get_summary_features

import pandas as pd
import pickle 


# #### 0 - Get file paths 

# In[9]:


with open( FPS_DIR + "purity_files.txt", "rb") as fp:
    purity_files = pickle.load(fp) 


# #### 1 - Run it

# In[12]:


features = []
for fp in purity_files:
    print( fp )
    features.append(get_summary_features(fp))    


# #### 2 - Output

# In[13]:


pd.concat(features).to_csv( TMP_DIR + 'summary_features.csv', index = False)

