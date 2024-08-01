#!/usr/bin/env python
# coding: utf-8

# In[3]:


import sys
import os

sys.path.insert(0, f'{os.path.dirname(os.getcwd())}/')
from mission_control.treasure_map import FPS_DIR, TMP_DIR, REFERENCE_GENES
from mission_control.somatic_help import get_somatic_features

import pandas as pd 
import pickle
import warnings
from multiprocessing import Pool
warnings.filterwarnings('ignore')


# #### 0 - Get file paths 

# In[5]:


with open( FPS_DIR + "somatic_files.txt", "rb") as fp:
    somatic_files = pickle.load(fp)  


# #### 1 - Run it

# In[7]:


def somatic_file_task(i_file: str):
    if os.path.isfile(i_file):
        print(i_file)
        return get_somatic_features(i_file, genes=REFERENCE_GENES)
    else:
        print("Missing! " + i_file)


# In[8]:


p = Pool()
features = p.map(somatic_file_task, somatic_files)
p.close()
p.join()


# #### 2 - Output

# In[ ]:


pd.DataFrame(features).to_csv(TMP_DIR + 'somatic_ready.csv', index = False)

