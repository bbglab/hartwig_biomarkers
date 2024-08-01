import pandas as pd

def get_sample( fp: str ) -> str:
    return fp.split("/")[-1].split(".purple.")[0]

def get_summary_features( fp: str ) -> pd.DataFrame:
    df = pd.read_csv(fp, sep = "\t")
    df = df.add_prefix('summary_')
    df.insert(0, 'sampleId', get_sample(fp))
    return df
