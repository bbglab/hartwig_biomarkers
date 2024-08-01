#!/usr/bin/env python
# coding: utf-8

# ### Use pre-computed HLAs to get HLA features
# - Feature description: https://docs.google.com/spreadsheets/d/1iXfZuwswPmr6BATn9nq0wj5cTpwLvcHbSYsQF7bVVok/edit?usp=sharing

# In[1]:


import sys
import os

sys.path.insert(0, f'{os.path.dirname(os.getcwd())}/')

from mission_control.treasure_map import TMP_DIR, REF_DIR, HLAS_DIR
from mission_control.hla_help import *

import pandas as pd
import json
import numpy as np
import math
import pickle


# #### 0 - Read in reference files

# In[2]:


hla_supertypes = pd.read_csv( REF_DIR + "hla_supertypes.txt", sep = "\t")
supertype_dict = {hla_supertypes['hla'].tolist()[i]: 
                  hla_supertypes['supertype'].tolist()[i] 
                  for i in range(hla_supertypes.shape[0])}


# #### 1 -  Extract HLAs for each Sample

# In[3]:


with open( REF_DIR + "hla_map.pkl", "rb") as f:
    hla_map = pickle.load(f)  


# #### 2 - Add Features, supertypes

# In[4]:


for sample in hla_map:
    normal = hla_map[sample]['normal']
    tumor = hla_map[sample]['tumor']
    hla_map[sample]['normal_supertype'] = [get_HLA_supertype(i, supertype_dict) for i in normal]
    hla_map[sample]['tumor_supertype'] = [get_HLA_supertype(i, supertype_dict) for i in tumor]
    for j in supertypes:
        hla_map[sample]['normal_contains_' + j] = binary(sum([1 if i == j else 0 for i in hla_map[sample]['normal_supertype']]))
        hla_map[sample]['tumor_contains_' + j] = binary(sum([1 if i == j else 0 for i in hla_map[sample]['tumor_supertype']]))


# #### 2 - Add features, heterozygosity

# In[5]:


for sample in hla_map:
    hla_map[sample]['normal_hla1_het'] = heterozygosity(hla_map[sample]['normal'], loci_hla_1)
    hla_map[sample]['tumor_hla1_het'] = heterozygosity(hla_map[sample]['tumor'], loci_hla_1)
    hla_map[sample]['normal_all_het'] = heterozygosity(hla_map[sample]['normal'], loci_all)
    hla_map[sample]['tumor_all_het'] = heterozygosity(hla_map[sample]['tumor'], loci_all)
    hla_map[sample]['loh_hla1'] = hla_map[sample]['normal_hla1_het'] - hla_map[sample]['tumor_hla1_het']
    hla_map[sample]['loh_all'] = hla_map[sample]['normal_all_het'] - hla_map[sample]['tumor_all_het']


# In[6]:


with open( REF_DIR + "hla_map_processed.pkl", "wb") as fp:  
    pickle.dump(hla_map, fp)


# #### Send it! 
# - 3,2,1

# In[7]:


hlas_df = pd.DataFrame(None)
for sample in hla_map:
    hlas_df = hlas_df.append(format_fun(sample, hla_map))
hlas_df.to_csv( TMP_DIR + "hla_ready.csv", index=False)        

