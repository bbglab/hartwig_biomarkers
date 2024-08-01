import sys
import os

sys.path.insert(0, f'{os.path.dirname(os.getcwd())}/')

from mission_control.treasure_map import REFERENCE_GENES, VHIO_REFERENCE, REPAIR_PATHWAY_GENES
import pandas as pd
import gzip

### Functions to Read VCF file ###
def get_vcf_col_names(vcf_path: str) -> list:
    with gzip.open(vcf_path, "rt") as ifile:
          for line in ifile:
            if line.startswith("#CHROM"):
                  vcf_names = [x for x in line.split('\t')]
                  break
    ifile.close()
    return vcf_names

def read_vcf(vcf_path: str) -> pd.DataFrame:
    names = get_vcf_col_names(vcf_path)
    return pd.read_csv(vcf_path, compression='gzip', comment='#', chunksize=10000, delim_whitespace=True, header=None, names=names).read()

### Functions to extract essential fields for feature creation ###
def get_metadata_df(vcf: pd.DataFrame) -> pd.DataFrame:
    return vcf[["#CHROM", "POS", "ID", "REF", "ALT", "QUAL", "FILTER"]].rename(columns = {'#CHROM':'CHROM'})

def get_sample( fp: str ) -> str:
    return fp.split("/")[-1].split(".purple.")[0]

def filter_PASS( df: pd.DataFrame ) -> pd.DataFrame :
    return df[[True if 'PASS' in i else False for i in df['FILTER']]]

#### pass INFO column #### 
def get_impact_fields( s: str ) :
    impact_fields = s.split("IMPACT=")[1].split(";")[0].split(",")
    return impact_fields    
        
def get_Gene(s: str):
    if 'IMPACT=' in s: 
        return get_impact_fields( s )[0]
    else:
        return -1

def get_Label(s: str):
    if 'IMPACT=' in s: 
        return get_impact_fields( s )[2]
    else:
        return -1    

def get_Predicted_Subclonal(s: str) -> bool:
    if 'SUBCL=' in s and float(s.split('SUBCL=')[-1].split(';')[0]) > .5 : 
        return True
    else:
        return False

def extract_info_fields(s: str) -> dict:
    return {
        'Annotation': get_Label(s),
        'SUBCLONAL': get_Predicted_Subclonal(s),
        'Gene': get_Gene(s)
     }    

def get_info_df(vcf: pd.Series) -> pd.DataFrame:
    return pd.DataFrame([extract_info_fields(i) for i in vcf['INFO']])

### Extract mutation type from REF and ALT 
def mutation_type( ref_alt: set ) -> str:
    if len(ref_alt[0]) != len(ref_alt[1]):
        return "indel"
    elif len(ref_alt[0]) == 1 and len(ref_alt[1]) == 1:
        return "sbs"
    elif len(ref_alt[0]) == 2 and len(ref_alt[1]) == 2:
        return "dbs"
    else:
        return "mbs"

def add_mutation_type(df: pd.DataFrame) -> pd.DataFrame:
    df[['mutation_type']] = [ mutation_type(i) for i in zip(df['REF'], df['ALT'])]
    return df

### Combine into VCF 
def get_quick_vcf(vcf_path: str) -> pd.DataFrame:
    vcf = read_vcf(vcf_path)
    metadata = get_metadata_df( vcf)
    info = get_info_df( vcf )
    together = metadata.join(info)
    clean_df = filter_PASS( together )    
    return add_mutation_type( clean_df )
                      
## Add extra columns 
def get_TMB_gene( df: pd.DataFrame, gene: str ):
    return df.query('Gene=="%s"' % (gene)).shape[0]

def get_TMB_cts( df: pd.DataFrame, filter_label = "" ) -> dict:
    cts = {
    'somatic_TMB'+filter_label : df.query('Annotation!="synonymous_variant"').shape[0],
    'somatic_TMB_clonal'+filter_label : df.query('Annotation!="synonymous_variant" & SUBCLONAL==False').shape[0],
    'somatic_TMB_subclonal'+filter_label : df.query('Annotation!="synonymous_variant" & SUBCLONAL==True').shape[0],
    'somatic_TMB_frameshift'+filter_label: df.query('Annotation=="frameshift_variant"').shape[0],
    'somatic_TMB_indel'+filter_label: df.query('Annotation!="synonymous_variant" & mutation_type=="indel"').shape[0],
    'somatic_TMB_sbs'+filter_label: df.query('Annotation!="synonymous_variant" & mutation_type=="sbs"').shape[0],    
    'somatic_TMB_dbs'+filter_label: df.query('Annotation!="synonymous_variant" & mutation_type=="dbs"').shape[0],     
    'somatic_TMB_mbs'+filter_label: df.query('Annotation!="synonymous_variant" & mutation_type=="mbs"').shape[0],
    'somatic_TMB_vhio': sum([get_TMB_gene(df, gene) for gene in VHIO_REFERENCE]),
    'somatic_TMB_damage_pathway': sum([get_TMB_gene(df, gene) for gene in REPAIR_PATHWAY_GENES])    
    }
    return cts

def get_gene_mts(df: pd.DataFrame, genes: list) -> dict:
    mts = { 'somatic.gene_' + gene + '.mb' : get_TMB_gene(df, gene) for gene in genes}
    return mts
    
def get_sample_features( sample: str, df: pd.DataFrame, genes: list) -> dict:
    sample_features = { 'sampleId' : sample }
    sample_features.update( get_TMB_cts(df) )
    sample_features.update( get_gene_mts(df, genes) )
    return sample_features

def get_somatic_features(vcf_path: str, genes: list) -> dict:
    print("Get somatic features for: " + get_sample(vcf_path)) 
    return get_sample_features( sample=get_sample(vcf_path), df=get_quick_vcf(vcf_path), genes = genes) 
