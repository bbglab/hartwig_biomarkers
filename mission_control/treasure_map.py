from os import getcwd 
import pandas as pd

### directories ### 
I_DIR = "/workspace/datasets/hartwig/20220809/20220809/"
O_DIR = "/workspace/datasets/hartwig/20220809/20220809/biomarkers/"
TMP_DIR = "/workspace/datasets/hartwig/20220809/20220809/biomarkers/tmp/"
FPS_DIR = "/workspace/datasets/hartwig/20220809/20220809/biomarkers/fps/"
REF_DIR = "/workspace/datasets/hartwig/20220809/20220809/biomarkers/ref/"
SIGS_DIR = "/workspace/datasets/hartwig/20220809/20220809/biomarkers/tmp/sigs/"
HLAS_DIR = "/workspace/datasets/hartwig/xhla_hlatypes/"
CODE_DIR = f"{getcwd()}/"
ISOFOX_DIR = "/workspace/datasets/hartwig/20230322/isofox/data_isofox/"

### pre-defined sets ### 
CANONICAL_GENES = pd.read_csv(REF_DIR + 'ensembl_canonical_transcripts.csv', sep = '\t')['GeneName'].tolist()
VHIO_REFERENCE  = pd.read_csv(REF_DIR + "vhio-card-300-v4.csv", sep = ";")['Genes'].tolist()

REFERENCE_GENES = list(set(CANONICAL_GENES + VHIO_REFERENCE))

CPI_REPORTED_GENES = ['SERPINB3','SERPINB4', 'B2M', 'JAK1','KRAS', 'TP53', 'PTEN','RTK','STK11', 'BAP1']
REPAIR_PATHWAY_GENES = ['BRCA1', 'BRCA2', 'ATM', 'POLE', 'ERCC2', 'FANCA', 'MSH2', 'MLH1', 'POLD1', 'MSH6']
