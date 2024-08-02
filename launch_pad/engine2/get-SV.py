#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
import os

sys.path.insert(0, f'{os.path.dirname(os.getcwd())}/')

from mission_control.treasure_map import FPS_DIR, TMP_DIR

import pandas as pd 
import pickle


# ### 0 - Get file paths 

# In[2]:


with open( FPS_DIR + "linx_files.txt", "rb") as fp:
    linx_files = pickle.load(fp)  


# ### 1 - Run it

# In[ ]:


features = []
for fp in linx_files:
    linx_dict = {}
    linx_dict["sampleId"] = fp.split("/")[-1]
    for i in ['breakend', 'clusters', 'svs', 'fusion', 'links']:
        linx_dict["sv_" + i] = pd.read_csv(fp +'.linx.'+i+'.tsv',sep = "\t").shape[0]
    features.append(linx_dict)


# ### 2 - Output

# In[ ]:


pd.DataFrame(features).to_csv( TMP_DIR + 'sv_ready.csv', index = False)

