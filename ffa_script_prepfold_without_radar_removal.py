import subprocess 
import sys
import numpy as np
import re
"""
This script makes prepfold plots by taking files with candidates lists produced by sifting_ffa.py. 

"""
cands_list_file = str(sys.argv[1])
cands_list = open(cands_list_file,'r')
lines = cands_list.readlines()[1:]
i=0

for fullline in lines: 
    if fullline.startswith("without"):
        i+=1
	continue

lines = lines[:i]

for line in lines:
    split_line = line.split()
    beam =(split_line[0])
    if beam.endswith('.dat'):
        p = float(split_line[1])/1000
        bash_line = 'prepfold -nosearch -noxwin -topo -p '+str(p)+' '+ beam
        subprocess.call(bash_line,shell=True)
                              
print "Done"
