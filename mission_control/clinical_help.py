from typing import Optional

import numpy as np
import math
import pandas as pd
from datetime import datetime
import re

def format_mechanism( s: str, split: str ) -> str:
    return split.join(re.sub(r'[0-9]+', '', s.replace(" ", "")).split('\n')[:-1])

def format_endDate(s: str, split: str) -> str:
    return split.join([i.split("    ")[1] for i in s.split("\n")[0:-1]])

def flatten_data( df: pd.DataFrame, flatten_fields: list, split: str ) -> pd.DataFrame:
    df_flat = df.groupby( flatten_fields ).agg({'startDate': lambda x: split.join(x), 
                                 'endDate': lambda x: ''.join(str(x)), 
                                 'name': lambda x: split.join(x), 
                                 'type': lambda x: split.join(x),
                                 'mechanism': lambda x: ''.join( str(x) )}).reset_index()
    df_flat[['mechanism']] = [format_mechanism(i, split) for i in df_flat['mechanism']]
    df_flat[['startDate']] = [i.split(split)[0] for i in df_flat['startDate']]
    df_flat[['endDate']] = [format_endDate(i, split).split(split)[-1] for i in df_flat['endDate']]
    df_flat[['last_type']] = [i.split(split)[-1] for i in df_flat['type']]
    df_flat[['last_mechanism']] = [i.split(split)[-1] for i in df_flat['mechanism']]
    return df_flat

def last_date(d1: str, d2: str) -> Optional[int]:
    if all([type(d1)==str, type(d2)==str]):
        if datetime.strptime(d1, "%Y-%m-%d") > datetime.strptime(d2, "%Y-%m-%d"):
            return d1
        else: 
            return d2
    elif (type(d1) == str):
        return d1
    elif (type(d2) == str):
        return d2
    else:
        return None

def days_between(d1: str, d2: str) -> Optional[int]:
    if all([type(d1)==str, type(d2)==str]):
        d1 = datetime.strptime(d1, "%Y-%m-%d")
        d2 = datetime.strptime(d2, "%Y-%m-%d")
        return abs((d2 - d1).days)
    else: 
        return None

def group_recist_evaluation( i: str ) -> Optional[str]:
    died = i[0]
    response = i[1]   
    if response in ['CR', 'PR']:
        return 'R'
    elif response in ["SD", "Non-CR/Non-PD", "ND", "Clinical progression", "PD"]:
        return 'D'
    elif died:
        return 'D'
    else: 
        return None 

def group_recist_evaluation_binary( i: str ) -> Optional[int]:
    recist_evaluation_group = group_recist_evaluation(i)
    if recist_evaluation_group in ['R']:
        return 1
    elif recist_evaluation_group in ['D']:
        return 0
    else: 
        return None
    
def add_recist_group( df: pd.DataFrame, c: str ) -> pd.DataFrame:
    df[[c+'_group']] = [ group_recist_evaluation(i) for i in zip(df['os_event'], df['response'] ) ]
    return df
    
def add_recist_group_binary( df: pd.DataFrame, c: str ) -> pd.DataFrame:
    df[[c+'_binary']] = [ group_recist_evaluation_binary(i) for i in zip(df['os_event'], df['response'] ) ]
    return df

def add_features( df: pd.DataFrame ) -> pd.DataFrame:
    df = add_recist_group(df, 'firstResponse')
    df = add_recist_group(df, 'lastResponse')
    df = add_age_cat(df)  
    return df   

def tumor_grouper( location: str ) -> str:
    if location not in ['Skin', 'Lung', 'Urothelial tract']:
        return 'Other'
    else:
        return location
    
def add_tumor_location_group( df: pd.DataFrame, col: str ) -> pd.DataFrame:
    df[['tumor_location_group']] = [ tumor_grouper(i) for i in df[col].tolist()]
    return df

def clean_biopsy_field( field: str ) -> str:
    step1 = str(field).lower()
    if 'lymph' in step1:
        return 'lymph'
    elif 'liver' in step1:
        return 'liver'
    elif 'lung' in step1: 
        return 'lung'
    elif 'skin' in step1 or 'cutan' in step1:
        return 'skin'
    elif 'primary' in step1:
        return 'primary'
    else:
        return 'other'

def time_to_last_response( patient_died, time_to_death_in_days, last_response_time_in_days ):
    if patient_died:
        return time_to_death_in_days
    else:
        return last_response_time_in_days

def time_to_progression( progression, time_to_progression, patient_died, time_to_death_in_days, last_response_time_in_days ):
    if progression:
        return time_to_progression
    elif patient_died: 
        return time_to_death_in_days
    else:
        return last_response_time_in_days

def get_full_response_mechanism( treatment: str, response_mechanism: str ) -> str:
    if str(response_mechanism) != 'nan':
        return response_mechanism
    elif str(treatment) in ['Pembrolizumab','Nivolumab']:
        return 'Anti-PD-1'
    elif str(treatment) == 'Ipilimumab':
        return 'Anti-CTLA-4'
    elif str(treatment) == 'Atezolizumab':
        return 'Anti-PD-L1'
    elif '/' in str(treatment):
        return 'Multiple mechanism'
    else:
        return 'Non-immunotherap-other' 

def column_namer( col: str ) -> str:
    if col in response:
        return 'Y_' + col
    if col in survival:
        return 'Survival_' + col
    if col in filters:
        return 'Filter_' + col
    if col in clin:
        return 'clinical_' + col
    if (col in ['patientIdentifier', 'sampleId']) or ('Survival' in col):
        return col
    else: 
        return 'ID_'+ col

def sort_col_names( df: pd.DataFrame ) -> pd.DataFrame:
    idx = df.columns.sort_values().tolist()
    df = df[idx]
    df.insert(0, 'patientIdentifier', df.pop('patientIdentifier') )
    df.insert(1, "sampleId", df.pop("sampleId") )
    return df  

response = [ 'last_response', 'best_response', 'relapse',
             'last_response_group','best_response_group',
             'last_response_binary', 'best_response_binary',
             'last_response_time_in_days', 'best_response_time_in_days']
survival = [ 'os_event', 'time_to_os_event', 'pfs_event', 'time_to_pfs_event']
filters = ['meta_responseMeasured', 'meta_treatmentGiven']
clin = ['meta_tumorPurity', 'meta_primaryTumorLocation', 'age_at_treatment_start',
            'meta_primaryTumorType', 'tumor_location_group',
            'meta_gender','meta_hasSystemicPreTreatment', 'meta_hasRadiotherapyPreTreatment','meta_treatment', 'meta_treatmentType', 'response_mechanism',
            'post_contains_Chemotherapy', 'post_contains_Immunotherapy', 'post_contains_Hormonal', 
            'pre_contains_Chemotherapy', 'pre_contains_Immunotherapy', 'pre_contains_Hormonal', 'pre_contains_Targeted', 'post_contains_Targeted',
            'biopsy_site', 'biopsy_distal_proximal', 'time_from_biopsy_to_treatment', 'meta_consolidatedTreatmentType', 'pre_treatment_duration',
            'pre_to_post_treatment_time'
       ]

def relapse_or_delayed_response( i ):
    if i[0] + i[1] + i[2]  == 3:
        return 1
    else:
        return 0

def pfs_event( progression: int, died: int) -> int:
    if progression > 0 or died > 0:
        return 1
    else:
        return 0

def survival_at_t( treatment_start_date, last_response_time_in_days, time_to_death_in_days, t):
    treatment_start_year = int(treatment_start_date.split("-")[0])
    if treatment_start_year <= 2019:
        if time_to_death_in_days <= t:
            return 0
        else: 
            return 1
    else: 
        if time_to_death_in_days <= t:
            return 0
        elif time_to_death_in_days > t:
            return 1
        elif last_response_time_in_days > t:
            return 1
        else: 
            return None

### Mapping metastatses to distal or proximal (dictionary from Abel) ###
dict_met = {'Ovary':{'Lymph node':'proximal',
                     'Peritoneum':'proximal',
                     'Liver':'distal'},
            'Bone/Soft tissue':{'Lymph node':'proximal'},
            'Bone marrow':{'Primary':'unknown'},
            'Lung':{'Lung':'proximal',
                    'Lymph node':'proximal',
                    'Liver':'distal',
                    'subcutaneous':'distal',
                    'Adrenal gland':'distal',
                    'Bone':'distal',
                    'Primary':'unknown',
                    'Pleural fluid':'proximal',
                    'subcutis':'distal',
                    'Spleen':'distal',
                    'skin':'distal',
                    'rectum':'distal',
                    'pleural lesion':'proximal',
                    'metastasis right leg':'distal',
                    'pelvis':'distal',
                    'mamma':'distal',
                    'Kidney':'distal',
                    'intramuscular':'distal',
                    'fatty tissue':'distal',
                    'CNS':'distal',
                    'brain':'distal',
                    'thoraxwall':'proximal'},
            'Urothelial tract':{'Lymph node':'proximal',
                                'Liver':'distal',
                                'Primary':'unknown',
                                'Peritoneum':'proximal',
                                'Lung':'distal',
                                'Bone':'distal',
                                'Adrenal gland':'proximal',
                                'metastatic lesion':'unknown',
                                'Subcutaneous mass':'distal',
                                'small pelvis soft tissue':'proximal',
                                'sigmoid':'distal',
                                'Psoas':'distal',
                                'Muscle tissue':'distal',
                                'abdominal':'unknown',
                                'Abdominal mass intra-abdominal':'unknown',
                                'Groin':'proximal',
                                'CNS':'distal',
                                'Bladder':'proximal',
                                'bladder':'proximal',
                                'abdominal wall (intramuscular)':'proximal',
                                'Abdominal wall (intramuscular)':'proximal',
                                'Thoracic wall (subcutaneous mass)':'distal'},
            'Unknown':{'Liver':'unknown',
                       'Mass':'unknown'},
            'Penis':{'Lymph node':'distal'},
            'Head and neck':{'Lymph node':'proximal',
                             'Primary':'unknown',
                             'skinlesion':'proximal',
                             'soft tissue costa':'distal'},
            'Pancreas':{'Liver':'distal'},
            'Skin':{'Lymph node':'proximal',
                    'Liver':'distal',
                    'skin':'proximal',
                    'subcutaneous':'proximal',
                    'Primary':'unknown',
                    'Subcutaneous':'proximal',
                    'Lung':'distal',
                    'Skin/subcutaneous':'proximal',
                    'Bone':'distal',
                    'Skin':'proximal',
                    'skin/subcutaneous':'proximal',
                    'subcutane':'proximal',
                    'Peritoneum':'distal',
                    '(Sub)cutaneous':'proximal',
                    'cutaneous':'proximal',
                    'subcutis':'proximal',
                    'Mamma':'distal',
                    'Soft mass':'unknown',
                    'subcutaneous fat':'proximal',
                    'Subcutaneous lesion thorax wall':'proximal',
                    'subcutaneous mass':'proximal',
                    'Subcutaneous mass':'proximal',
                    'subcutaneous metastasis':'proximal',
                    'Subcutane metastasis.':'proximal',
                    'Subcutaneus leasion':'proximal',
                    'subcutaan lower leg right':'proximal',
                    'Soft tissue (muscle)':'distal',
                    'soft tissue':'unknown',
                    'skin, medial left upper leg':'proximal',
                    'small intestin (intraluminal lesion)':'distal',
                    'Leg':'unknown',
                    'Adrenal gland':'distal',
                    'breast/mamma':'distal',
                    'intra-abdominal':'distal',
                    'intramuscular':'distal',
                    'left mamma':'distal',
                    'Left maximus gluteus':'distal',
                    'Neck':'unknown',
                    'Skin/subcutaeous':'proximal',
                    'Skin/Subcutaneous':'proximal',
                    'SKIN':'proximal',
                    'skin left back':'proximal',
                    'skin lesion':'proximal',
                    '(Sub)cutaneous lesion':'proximal',
                    'Skin/ Subcutaneous':'proximal',
                    'Thoracic wall intramuscular':'distal',
                    'subcatenous':'proximal'},
            'Gallbladder':{'Liver':'proximal'},
            'Kidney':{'Bone':'distal',
                      'Lymph node':'proximal',
                      'Liver':'distal',
                      'Kidney':'proximal',
                      'Lung':'distal',
                      'abdominal wall (subcutaneous)':'proximal',
                      'duodenum':'distal',
                      'Intra abdominal mass (fatty tissue)':'proximal',
                      'Mamma/axilla':'distal',
                      'Muscle dorsum':'distal',
                      'Peritoneum':'proximal',
                      'Skin':'distal',
                      'Sternum':'distal',
                      'subcutaneos':'proximal',
                      'Subcutaneous':'proximal'},
            'Colorectum':{'Lymph node':'proximal',
                          'Peritoneum':'proximal'},
            'Stomach':{'Liver':'distal'},
            'Small intestine':{'colon':'proximal',
                               'Liver':'distal'},
            'Vulva':{'Liver':'distal',
                     'Subcutaneous lesion':'proximal'},
            'Prostate':{'Lymph node':'proximal',
                        'Liver':'distal',
                        'Bone':'distal'},
            'Breast':{'Breast':'proximal'},
            'Mesothelium':{'Lung':'proximal',
                           'Primary':'unknown',
                           'Extrathoracic':'distal',
                           'omentum':'distal',
                           'Peritoneum':'distal',
                           'Pleural abnormality':'proximal',
                           'Pulmonary pleurae':'proximal'}
           }

def distal_proximal_biopsy( i, dict_met ):
    tumor_location = i[0]
    biopsy_site = i[1]
    if tumor_location in dict_met:
        tmp = dict_met[tumor_location]
        if biopsy_site in tmp:
            distal_proximal = tmp[biopsy_site]
            if distal_proximal == "distal":
                return 1
            elif distal_proximal == "proximal":
                return 0
            else:
                return None
        else:
            return None
    else: 
        return None
