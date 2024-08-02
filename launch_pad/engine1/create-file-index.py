#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
import os

sys.path.insert(0, f'{os.path.dirname(os.getcwd())}/')

from mission_control.treasure_map import I_DIR, TMP_DIR, FPS_DIR, ISOFOX_DIR

import pandas as pd
import pickle


# ### 0 - get samples

# In[2]:


somatic_dir = I_DIR + "somatic/"
isofox_dir = ISOFOX_DIR

samples = pd.read_csv(TMP_DIR + "clinical_short.csv")['sampleId'].tolist()
somatic_samples = [i for i in os.listdir(somatic_dir) if i in samples]
isofox_samples = [i for i in os.listdir(ISOFOX_DIR) if i in samples]


# ### 1 - collect file paths

# In[3]:


somatic_files = []
cnv_files = []
cnv_gene_files = []
purity_files = []
neoepitope_files = []
driver_files = []
sv_files = []
linx_files = []

for sample in somatic_samples:
    linx_files.append(somatic_dir + sample + "/linx/" + sample)
    fp_start = somatic_dir + sample + "/purple/" + sample
    if os.path.isfile( fp_start + '.purple.somatic.vcf.gz' ):
        somatic_files.append( fp_start + '.purple.somatic.vcf.gz')
        cnv_files.append( fp_start + '.purple.cnv.somatic.tsv')
        cnv_gene_files.append( fp_start + '.purple.cnv.gene.tsv')
        purity_files.append( fp_start + '.purple.purity.tsv')
        driver_files.append( fp_start + '.driver.catalog.somatic.tsv')
        sv_files.append( fp_start + '.purple.sv.vcf.gz')
    else:
        print('Missing path! ' + fp_start)      


# In[4]:


isofox_files = []
for sample in isofox_samples:
    if os.path.isfile( isofox_dir + sample  + "/" + sample + ".isf.gene_data.csv" ):
        isofox_files.append( isofox_dir + sample  + "/" + sample + ".isf.gene_data.csv")
        neoepitope_files.append( isofox_dir + sample  + "/" + sample + ".isf.neoepitope.csv" )
    else:
        print('Missing path! ' + isofox_dir + sample  + "/" + sample + ".isf.gene_data.csv") 


# ### 2 - output files

# In[5]:


file_types = ['somatic','cnv', 'cnv_gene', 'purity','neoepitope','driver','sv','linx','isofox']
for i in file_types:
    out = i + "_files"
    with open(FPS_DIR + out + ".txt", "wb") as fp:  
        pickle.dump( globals()[out], fp)

