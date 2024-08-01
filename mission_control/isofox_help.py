import pandas as pd

def get_clean_expression( file_path: str, col = 'AdjTPM' ) -> pd.DataFrame:
    gene = pd.read_csv( file_path)
    sample = file_path.split("/")[-1].split(".")[0]
    filter_and_rename = gene[['GeneName',col]].set_index('GeneName').rename(columns = {col: sample})
    clean = filter_and_rename.reset_index().groupby('GeneName').agg(lambda x: x.mean()).transpose()
    return clean

def filter_to_reference_genes( ge_df: pd.DataFrame, reference_genes: list ) -> pd.DataFrame:    
    keep = [ True if i in reference_genes else False for i in ge_df.reset_index()['GeneName']]
    return ge_df[keep]

def labeller( i: str, REFERENCE_GENES: list):
    if i in REFERENCE_GENES:
        return "isofox_"
    else:
        return "isofox.nr_"
        
def df_cleaner( ref_df: pd.DataFrame, REFERENCE_GENES: list ) -> pd.DataFrame:
    df = ref_df.transpose()
    df.columns = [labeller(i, REFERENCE_GENES) + i for i in df.columns]
    df['sampleId'] = df.index
    df.insert(0, "sampleId", df.pop("sampleId") )
    return df 

def get_neoepitope_features( i_file: str ) -> dict:
    features = {}
    sample = i_file.split("/")[-1].split(".")[0]
    features.update({'sampleId': sample})
    features.update({'isofox_neoepitope_count': pd.read_csv(i_file).shape[0]})
    return features
