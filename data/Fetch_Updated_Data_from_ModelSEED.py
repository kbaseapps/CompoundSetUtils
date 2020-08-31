#!/usr/bin/env python
from urllib.request import urlopen
import sys,json

MSD_git_url = "https://raw.githubusercontent.com/ModelSEED/ModelSEEDDatabase/"
MSD_commit = "v1.0"

##
## Compounds
##
file = urlopen(MSD_git_url+MSD_commit+"/Biochemistry/Structures/Unique_ModelSEED_Structures.txt")
inchi_structures=dict()
inchikey_structures=dict()

for line in file.readlines():
    line=line.decode('utf-8')
    line=line.strip('\n')
    array=line.split('\t')
    if(array[1] == 'InChI'):
        inchi_structures[array[0]]=array[5]
    if(array[1] == 'InChIKey'):
        inchikey_structures[array[0]]=array[5]
        
with open('Compound_Structures.json','w') as inchi_file:
    inchi_file.write(json.dumps(inchi_structures))

with open('Inchikey_IDs.json','w') as inchikey_file:
    inchikey_file.write(json.dumps(inchikey_structures))
