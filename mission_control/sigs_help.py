import pandas as pd
import gzip
import pickle

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

m = {'A':'T','T':'A','C':'G','G':'C'}

def filter_sbs( df: pd.DataFrame ) -> pd.DataFrame:
    return df[[ True if (len(i[0]) == 1 and len(i[1]) == 1) else False for i in zip(df['REF'], df['ALT'])]]

def extract_sbs_tnc( df: pd.DataFrame ) -> list:
    sbs = [ i[0]+'>'+i[1] for i in zip(df['REF'], df['ALT'])]
    tnc = [i.split("TNC=")[1] for i in df['INFO']]
    sbs_tnc = [i for i in zip(sbs, tnc)]
    return sbs_tnc

def get_tnc_96( sbs_tnc: set ) -> str:
    sbs = sbs_tnc[0]
    tnc = sbs_tnc[1]
    if sbs[0] in ['C', 'T']:
        return "".join( [tnc[0],'[',sbs,']',tnc[2]])
    else:
        return "".join( [m[tnc[2]],'[',m[sbs[0]],'>',m[sbs[2]],']',m[tnc[0]]])
    
def get_tnc_cts( tncs_96: list ) -> dict:
    cts = {}
    for i in tncs_96:
        if i not in cts:
            cts[i] = 1
        else:
            cts[i] += 1
    return cts

def get_tnc_df( i_file: str ) -> pd.DataFrame:
    
    step0 = read_vcf( i_file )
    step1 = filter_sbs( step0 )
    step2 = extract_sbs_tnc( step1 )
    step3 = [ get_tnc_96(i) for i in step2 if 'N' not in i[1]]
    step4 = get_tnc_cts( step3 )
    step5 = pd.DataFrame( step4, index = [0])
    step6 = step5.reindex(sorted(step5.columns), axis=1)
    step6.insert(0, "sampleId", get_sample( i_file ))
    
    return step6

def get_sample( i_file: str ) -> str:
    return i_file.split('/')[-1].split(".")[0]

