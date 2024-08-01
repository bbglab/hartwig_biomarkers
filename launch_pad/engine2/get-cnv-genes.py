#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
import os

sys.path.insert(0, f'{os.path.dirname(os.getcwd())}/')

from mission_control.treasure_map import FPS_DIR, TMP_DIR
from mission_control.cnv_help import get_cnv_gene_features

import os
import pandas as pd 
import pickle
import statistics
import warnings
from multiprocessing import Pool
warnings.filterwarnings('ignore')


# #### 0 - Get file paths 

# In[2]:


with open( FPS_DIR + "cnv_gene_files.txt", "rb") as fp:
    cnv_gene_files = pickle.load(fp)


# #### 1 - Run it

# In[ ]:


def cnv_gene_file_task(i_file: str):
    if os.path.isfile(i_file):
        print(i_file)
        return get_cnv_gene_features(i_file)
    else:
        print("Missing! " + i_file)


# In[ ]:


p = Pool()
features = p.map(cnv_gene_file_task, cnv_gene_files)
p.close()
p.join()


# #### 2 - Output

# In[4]:


pd.DataFrame(features).to_csv( TMP_DIR + 'cnv_gene_ready.csv', index = False) 

