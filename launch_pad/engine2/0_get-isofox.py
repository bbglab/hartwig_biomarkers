#!/usr/bin/env python
# coding: utf-8

# In[14]:


import sys
import os

sys.path.insert(0, f'{os.path.dirname(os.getcwd())}/')

from mission_control.treasure_map import FPS_DIR, TMP_DIR, REFERENCE_GENES
from mission_control.isofox_help import get_clean_expression, filter_to_reference_genes, df_cleaner

import pandas as pd
import pickle
from multiprocessing import Pool

field = sys.argv[1] #"AdjTPM or RawTPM"
#field = "RawTPM"


# #### 0 - Get file paths 

# In[2]:


with open( FPS_DIR + "isofox_files.txt", "rb") as fp:
    isofox_files = pickle.load(fp)


# #### 1 - Run it

# In[5]:


def isofox_file_task( i_file: str):
    if os.path.isfile(i_file):
        print(i_file)
        return get_clean_expression( i_file, col = field )
    else:
        print("Missing! " + i_file)


# In[4]:


p = Pool()
features = p.map(isofox_file_task, isofox_files)
p.close()
p.join()


# In[5]:


full_df = pd.concat( features ).transpose()
reference_df = filter_to_reference_genes( full_df, REFERENCE_GENES ) 


# #### 2 - Output

# In[6]:


reference_df.to_csv( TMP_DIR + 'cibersort_prep_' + field + '.csv', index = True)
#df_cleaner(reference_df).to_csv( TMP_DIR + 'isofox_' + field + '_features.csv', index = False)
df_cleaner(full_df, REFERENCE_GENES).to_csv( TMP_DIR + 'isofox_' + field + '_features.csv', index = False)

