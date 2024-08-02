#!/usr/bin/env python
# coding: utf-8

# ## Clinical Data - Join, Organize, Clean
# - Most important notebook for Hartwig analysis

# In[1]:


import sys
import os

sys.path.insert(0, f'{os.path.dirname(os.getcwd())}/')

from mission_control.treasure_map import I_DIR, TMP_DIR
from mission_control.clinical_help import *


# In[2]:


meta = pd.read_csv( I_DIR + "metadata.tsv", sep='\t')
pre = pd.read_csv( I_DIR + "pre_biopsy_drugs.tsv", sep='\t')
post = pd.read_csv( I_DIR + "post_biopsy_drugs.tsv", sep='\t')
response = pd.read_csv( I_DIR + "treatment_responses.tsv", sep='\t')


# ### 0 - Flatten data + Merge Data

# In[3]:


pre_flat = flatten_data(pre, ['patientIdentifier'], "/")
post_flat = flatten_data(post, ['patientIdentifier', 'sampleId'], "/")

pre_flat.columns = ['pre_' + i if i not in ['patientIdentifier', 'sampleId'] else i for i in pre_flat.columns]
post_flat.columns = ['post_' + i if i not in ['patientIdentifier', 'sampleId'] else i for i in post_flat.columns]
meta.columns = ['meta_' + i if i not in ['patientIdentifier', 'sampleId'] else i for i in meta.columns]
response.columns = ['response_' + i if i not in ['patientIdentifier', 'sampleId', 'response', 'responseDate'] else i for i in response.columns]

for j in ['Chemotherapy', 'Immunotherapy', 'Hormonal','Androgen', 'Targeted', 'estrogen']:
    pre_flat[['pre_contains_' + j]] = [True if j in i else False for i in pre_flat['pre_type']]
for j in ['Chemotherapy', 'Immunotherapy', 'Hormonal', 'Androgen', 'Targeted', 'estrogen']:
    post_flat[['post_contains_' + j]] = [True if j in i else False for i in post_flat['post_type']]   
    
join1 = pd.merge( left = post_flat, right = meta, on = ["sampleId"], how = "left" )
join2 = pd.merge( left = join1, right = response, on = ["patientIdentifier", "sampleId"], how = "left" )
clinical = pd.merge( left = join2, right = pre_flat, on = ["patientIdentifier"], how = "left" )    


# ### 1 - Add fields

# In[4]:


def days_between(d1: str, d2: str) -> Optional[int]:
    if all([type(d1)==str, type(d2)==str]) and d1 != 'NaN' and d2 != 'NaN' and d1 != "" and d2 != "":
        d1 = datetime.strptime(d1, "%Y-%m-%d")
        d2 = datetime.strptime(d2, "%Y-%m-%d")
        return abs((d2 - d1).days)
    else:
        return None


# In[5]:


### Time Fields ###
clinical[['last_measured_date']] = [last_date(clinical['meta_treatmentEndDate'].tolist()[i], clinical['responseDate'].tolist()[i]) for i in range(clinical.shape[0])]
clinical[['pre_treatment_duration']] = [days_between(clinical['pre_startDate'].tolist()[i], clinical['pre_endDate'].tolist()[i]) for i in range(clinical.shape[0])]
clinical[['pre_to_post_treatment_time']] = [days_between(clinical['pre_endDate'].tolist()[i], clinical['meta_treatmentStartDate'].tolist()[i]) for i in range(clinical.shape[0])]
clinical[['treatment_duration']] = [days_between(clinical['meta_treatmentStartDate'].tolist()[i], clinical['meta_treatmentEndDate'].tolist()[i]) for i in range(clinical.shape[0])]
clinical[['time_from_biopsy_to_treatment']] = [days_between(clinical['meta_biopsyDate'].tolist()[i], clinical['meta_treatmentStartDate'].tolist()[i]) for i in range(clinical.shape[0])]
clinical[['time_to_response_in_days']] = [days_between(clinical['meta_treatmentStartDate'].tolist()[i], clinical['responseDate'].tolist()[i]) for i in range(clinical.shape[0])]
clinical[['time_to_death_in_days']] = [days_between(clinical['meta_treatmentStartDate'].tolist()[i], clinical['meta_deathDate'].tolist()[i]) for i in range(clinical.shape[0])]
clinical[['time_to_last_measurement_in_days']] = [days_between(clinical['meta_treatmentStartDate'].tolist()[i], clinical['last_measured_date'].tolist()[i]) for i in range(clinical.shape[0])]
clinical[["age_at_treatment_start"]] = [ float(str(clinical["meta_treatmentStartDate"].tolist()[i]).split("-")[0]) - float(clinical["meta_birthYear"].tolist()[i]) for i in range(clinical.shape[0])]

### Indicators ### 
clinical[['os_event']] = [ int(not math.isnan(i)) for i in clinical['time_to_death_in_days']]
clinical[["response_mechanism"]] = [ get_full_response_mechanism(clinical['post_name'].tolist()[i], clinical['response_mechanism'].tolist()[i]) for i in range(clinical.shape[0])]
clinical[['progression']] = [int(clinical['response'].tolist()[i] == "PD") for i in range(clinical.shape[0])]
clinical = add_tumor_location_group(clinical, 'meta_primaryTumorLocation')
clinical[['biopsy_site']] = [clean_biopsy_field(i) for i in clinical['meta_biopsySite']]
clinical[['biopsy_distal_proximal']] = [distal_proximal_biopsy(i,dict_met) for i in list(zip(clinical.meta_primaryTumorLocation, clinical.meta_biopsySite))]

### Responses ###
clinical = add_recist_group( clinical, 'response' )
clinical = add_recist_group_binary( clinical, 'response' )
clinical['response'] = pd.Categorical(clinical['response'], ["CR", "PR", "SD", "Non-CR/Non-PD", "ND", "Clinical progression", "PD"])
clinical = clinical.drop(labels = ["meta_firstResponse","meta_responseDate","response_startDate","response_endDate","post_startDate", "post_endDate"], axis = 1)


# ### 2 - Get 'Short'
# - Flatten dataframe

# In[6]:


clinical_last = ( 
    clinical.sort_values(["responseDate"], ascending = True)
        .groupby(['patientIdentifier','sampleId'])
        .tail(1)
        .rename( columns = {
            'response': 'last_response', 
            'response_group': 'last_response_group', 
            'responseDate': 'last_response_date', 
            'time_to_response_in_days': 'last_response_time_in_days', 
            'response_binary': 'last_response_binary'
        })
)
clinical_best = (
    clinical.sort_values(["response","responseDate"], ascending = True)
        .groupby(['patientIdentifier','sampleId'])
        .head(1)
        .rename( columns = {
            'response': 'best_response', 
            'response_group': 'best_response_group', 
            'responseDate': 'best_response_date', 
            'time_to_response_in_days': 'best_response_time_in_days', 
            'response_binary': 'best_response_binary'
        })
     [['patientIdentifier','sampleId','best_response', 'best_response_group', 'best_response_binary', 'best_response_date', 'best_response_time_in_days']]
)
clinical_progression = (
    clinical.sort_values(["progression","responseDate"], ascending = [False,True])
        .groupby(['patientIdentifier','sampleId'])
        .head(1)
        .rename( columns = {
            'responseDate': 'progression_date', 
            'time_to_response_in_days': 'progression_time'
        })
    [['patientIdentifier','sampleId','progression_date', 'progression_time']]
)     
clinical_short = (clinical_last.merge(clinical_best, on=['patientIdentifier','sampleId'])
                               .merge(clinical_progression, on=['patientIdentifier','sampleId']))


# #### Derive more clinical endpoints

# In[7]:


clinical_short[['pfs_event']] = [ pfs_event( clinical_short['os_event'][i], clinical_short['progression'][i])
                                for i in range(clinical_short.shape[0])]

clinical_short['time_to_os_event'] = [time_to_last_response( 
                                                clinical_short['os_event'][i],
                                                clinical_short['time_to_death_in_days'][i],
                                                clinical_short['time_to_last_measurement_in_days'][i])
                                           for i in range(clinical_short.shape[0])]

clinical_short['time_to_pfs_event'] = [time_to_progression(  clinical_short['progression'][i],
                                                             clinical_short['progression_time'][i],
                                                             clinical_short['os_event'][i],
                                                             clinical_short['time_to_death_in_days'][i],
                                                             clinical_short['time_to_last_measurement_in_days'][i])
                                           for i in range(clinical_short.shape[0])]

clinical_short[['relapse']] = [relapse_or_delayed_response(i) for i in zip(clinical_short['pfs_event'], clinical_short['best_response_group'] == 'R', clinical_short['time_to_pfs_event'] > clinical_short['best_response_time_in_days'])]
clinical_short[['delayed_response']] = [relapse_or_delayed_response(i) for i in zip(clinical_short['pfs_event'], clinical_short['best_response_group'] == 'R', clinical_short['time_to_pfs_event'] < clinical_short['best_response_time_in_days'])]

clinical_short[['Survival_at_6_months']] = [survival_at_t( 
     clinical_short['meta_treatmentStartDate'][i], 
     clinical_short['time_to_last_measurement_in_days'][i], 
     clinical_short['time_to_death_in_days'][i], 183) for i in range(clinical_short.shape[0])]

clinical_short[['Survival_at_12_months']] = [survival_at_t( 
     clinical_short['meta_treatmentStartDate'][i], 
     clinical_short['time_to_last_measurement_in_days'][i], 
     clinical_short['time_to_death_in_days'][i], 365) for i in range(clinical_short.shape[0])]

clinical_short[['Survival_at_18_months']] = [survival_at_t( 
     clinical_short['meta_treatmentStartDate'][i], 
     clinical_short['time_to_last_measurement_in_days'][i], 
     clinical_short['time_to_death_in_days'][i], 551) for i in range(clinical_short.shape[0])]


# #### 3 - Tidy up and output

# In[8]:


clinical_short.columns =  [column_namer(i) for i in clinical_short.columns.tolist()]
clinical_short = sort_col_names(clinical_short)
clinical_short = clinical_short.fillna(value=np.nan)


# In[9]:


clinical_short.to_csv( TMP_DIR + "clinical_short.csv", index=False)
clinical.to_csv( TMP_DIR + "clinical_long.csv", index=False)

