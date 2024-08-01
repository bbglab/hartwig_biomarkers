import pandas as pd
import statistics

def get_cnv_sample( fp: str ) -> str:
    return fp.split("/")[-1].split(".purple.")[0]

#### 1) compute functions
def compute_prop_scna( df: pd.DataFrame ) -> float: # proportion of genome with copy number change
    df = df[df['chromosome'].isin([str(i) for i in range(23)])] ## filter to non-sex 
    df[['size']] = df['end'] - df['start']
    df[['pct']] = (df['end'] - df['start'])/df['size'].sum()
    df[['cnv_contribution']] = df['pct'] * df['copyNumber']
    return df['cnv_contribution'].sum()

def compute_copy_loss_burden( df: pd.DataFrame ) -> int:  # number of genes with copy number change
    df_sex = df[df['chromosome'].isin(['X','Y'])]
    df_non_sex = df[df['chromosome'].isin([str(i) for i in range(23)])]
    sex_chr_burden = sum(df_sex['minCopyNumber'] > 1.5) + sum(df_sex['maxCopyNumber'] < .5)
    non_sex_chr_burden = sum(df_non_sex['minCopyNumber'] > 3) + sum(df_non_sex['maxCopyNumber'] < 1)
    return sex_chr_burden + non_sex_chr_burden

def compute_loh( min_copy_number: float, minor_allele_ploidy: float ) -> int:
    if( min_copy_number > .7 and minor_allele_ploidy < .3): ### thresholds from Fran
        return 1
    else: 
        return 0

def get_region_copy_number( df: pd.DataFrame, region: str) -> int:
    return statistics.mean(df.query('region=="%s"' % (region))['minCopyNumber'])

def get_region_loh( df: pd.DataFrame, region: str ) -> int:
    tmp = df.query('region=="%s"' % (region))
    min_copy_number = statistics.mean(tmp['minCopyNumber'])
    minor_allele_ploidy = statistics.mean(tmp['minMinorAlleleCopyNumber'])
    return compute_loh(min_copy_number, minor_allele_ploidy)

def get_cnv_region_features( df: pd.DataFrame ) -> dict:
    df[['region']] = [i.replace("-",".") for i in 'chr' + df['chromosome'].astype(str) + "." + df['chromosomeBand'].astype(str)]
    regions = df['region'].unique()
    look_around = {'cnv.region_cn_' + region : get_region_copy_number(df, region) for region in regions}
    look_around.update({'cnv.region_loh_' + region : get_region_loh(df, region) for region in regions})
    return look_around

#### 2) feature construction functions 
def get_scna( fp: str ) -> dict:
    print( "Get SCNA: " + get_cnv_sample(fp))
    df = pd.read_csv( fp, sep = "\t")
    features = {'sampleId': get_cnv_sample(fp)}
    features.update({'cnv_scna': compute_prop_scna(df)})
    return features

def get_cnv_gene_features( fp: str ) -> dict:
    print( "Get CNV gene features: " + get_cnv_sample(fp))
    df = pd.read_csv( fp, sep = "\t") 
    features = {'sampleId' : get_cnv_sample(fp)}    
    features.update({'cnv_copy_loss_burden': compute_copy_loss_burden(df)})
    features.update( get_cnv_region_features(df) )
    return features
