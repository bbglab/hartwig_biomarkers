import numpy as np
import pandas as pd

hla_A_supertypes = ["A01", "A02", "A03", "A24"]
hla_B_supertypes = ["B07", "B08", "B27", "B44", "B62"]
supertypes = hla_A_supertypes + hla_B_supertypes

def get_HLA_supertype(hla: str, supertype_dict: dict) -> str:
    if type(hla) != str:
        return np.nan
    elif hla.replace(":", "") not in supertype_dict:
        return 'Unclassified'
    else:
        return supertype_dict[hla.replace(":", "")].replace(" ", "_")
    
def binary(num: int) -> int:
    if num > 0:
        return 1
    else: 
        return 0

loci_hla_1 = ['A','B','C']
loci_all = loci_hla_1 + ['DQB1', 'DRB1']

def heterozygosity( alleles: pd.DataFrame, loci: list) -> int:
    store = {}
    for i in [i.split("*") for i in alleles if i.split("*")[0] in loci]:
        if i[0] not in store:
            store[i[0]] = [i[1]]
        else:
            store[i[0]] += [i[1]]
    return sum([1 if len(np.unique(store[i])) > 1 else 0 for i in store ]) 

def format_fun( sample: str, hla_map: dict) -> pd.DataFrame:
    prefix = "hla_"
    doormat = {}
    doormat['sampleId'] = sample
    doormat[prefix +'HLA_all_heterozygous'] = hla_map[sample]['normal_all_het']
    doormat[prefix +'HLA_I_heterozygous'] = hla_map[sample]['normal_hla1_het']
    doormat[prefix +'HLA_all_tumor_heterozygous'] = hla_map[sample]['tumor_all_het']
    doormat[prefix +'HLA_I_tumor_heterozygous'] = hla_map[sample]['tumor_hla1_het']
    doormat[prefix +'HLA_all_LOH'] = hla_map[sample]['loh_all']
    doormat[prefix +'HLA_I_LOH'] = hla_map[sample]['loh_hla1']
    for i in supertypes:
        doormat[prefix +'HLA_contains_' + i] = hla_map[sample]['normal_contains_' + i]
    return pd.DataFrame(doormat, index = [0])
