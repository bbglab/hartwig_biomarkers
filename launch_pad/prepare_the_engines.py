import sys
import os

CODE_DIR = f'{os.path.dirname(os.getcwd())}/'

engine_map = {
    '0_get-clinical/0_get-clinical.ipynb': 'engine1',
    '1_create-file-index/create-file-index.ipynb': 'engine1', 
   
    '2_get-somatic/get-somatic.ipynb': 'engine2',
    '3_get-isofox/0_get-isofox.ipynb': 'engine2',
    '3_get-isofox/3_get-neoepitope.ipynb': 'engine2',
    '4_get-cnv/get-cnv-overall.ipynb': 'engine2',
    '4_get-cnv/get-cnv-genes.ipynb': 'engine2',
    '5_get-HLA/get-hla.ipynb': 'engine2',
    '6_get-svs/get-SV.ipynb': 'engine2',
    '7_get-sigs/0_get-sigs.ipynb': 'engine2',
    '8_get-summary/0_get-summary.ipynb': 'engine2',
    '9_get-drivers/0_get-drivers.ipynb': 'engine2',

    '0_get-clinical/1_get-clinical.ipynb': 'engine3',   
    '3_get-isofox/1_get-cibersort.ipynb': 'engine3',
    '3_get-isofox/2_get-isofox.ipynb': 'engine3', 
    '5_get-HLA/get-lilac.ipynb': 'engine3',
    '7_get-sigs/1_get-sigs.ipynb': 'engine3',
    '8_get-summary/1_get-summary.ipynb': 'engine3',
    '9_get-drivers/1_get-drivers.ipynb': 'engine3',
    
    'last_step/combine.ipynb': 'engine4'
}
for i in engine_map:
    cmd = 'jupyter nbconvert --to script ' + CODE_DIR + i + ' --output ' + CODE_DIR + 'launch_pad/' + engine_map[i] + "/" + i.split("/")[-1].split(".ipynb")[0]
    os.system(cmd) 
