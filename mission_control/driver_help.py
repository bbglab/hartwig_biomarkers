import pandas as pd

def get_sample( fp: str ) -> str:
    return fp.split("/")[-1].split(".linx.")[0]

def get_sample2( fp: str ) -> str:
    return fp.split("/")[-1].split(".driver.")[0]

def create_driver_df( fp: str ) -> pd.DataFrame:
    df = pd.read_csv( fp, sep='\t')
    df.insert(0, "sampleId",get_sample( fp ), True)
    return df

def create_driver_df2( fp: str ) -> pd.DataFrame:
    df = pd.read_csv( fp, sep='\t')
    df.insert(0, "sampleId",get_sample2( fp ), True)
    return df
