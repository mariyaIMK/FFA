import subprocess
import glob
import time 
import sys
import numpy as np
import re



####This script will perform an injection of synthetic pulsars on one beam 
####This script needs Patrick Lazarus' injection scripts (injectpsr.py), and Emilie Parent's FFA scripts (ffa.py)


##########################################################################

#Configure the following quantities depending on the desired injection 

dm = 10
beam = 'p2030.20131003.G54.79-01.58.C.b0.00000.fil'
period = 10.964532 #with 6 decimal places
smean_max = 0.30 #maximum flux density at which you want to attempt an injection
smean_min = 0.015 #minimum flux density at which you want to attempt an injection 

##########################################################################





#=========================================================================

#Define the other variables accordingly 

sm = #write a function to det'n sm  
rms = #from first prepdata

basename = beam.split('.fil',1)[0]
filename = basename + '_dm' + dm +'_p' + period + 'sm'+ sm ###verify the syntax


#========================================================================

#presto bash commands 

bash_line1 = 'prepdata -nobary -dm '+ dm ' -o '+ basename + ' ' + beam
bash_line2 = 'rfifind -time 2.0 -o '+ basename + ' ' + beam 



bash_line3 = 'python injectpsr.py --dm '+ dm + ' -p '+period+ ' -v "1 200 0.5" -s radiometer -c "smean='+ sm + ',gain=10,tsys=33.876,rms=' +rms+'" -o '+ filename + ' '+ filename + '.fil' 

bash_line4 = 'prepdata -nobary -dm '+ dm ' -o '+ filename + ' '+ filename + '.fil' 

bash_line5 = 'prepfold -nopdsearch -nodmsearch -topo -nosearch -noxwin -p ' + period + ' -o ' + filename + ' '+ filename + '.fil' 

bash_line6 = 'prepdata -nobary -dm '+ dm ' -mask '+ basename + '_rfifind.mask -o '+ filename + ' '+ filename + '.fil'

bash_line7 = 'python ffa.py ' + filename + '.dat --plot'

#=========================================================================



#step 1: Before any beam injection 
subprocess.call(bash_line1,shell=True) #take the rms from here
subprocess.call(bash_line2,shell=True)



#step2: Inject, Prepdata, Prepfold, Prepdata, FFA on the right DM 
subprocess.call(bash_line3,shell=True)
subprocess.call(bash_line4,shell=True)
subprocess.call(bash_line5,shell=True)
subprocess.call(bash_line6,shell=True)
subprocess.call(bash_line7,shell=True)


#step3: Check if the pulsar was detected 
cands_list_file = filename+'_cands.ffa'
cands_list = open(cands_list_file,'r')

lines = cands_list.readlines()[1]
split_line = line.split()
cands_period = (split_line[1])


if cands_period = period #figure out how to compare only the first 2 decimal places
    print "The pulsar was found as the first candidate at flux density: " +sm 
else
    print "The pulsar was NOT found as the first candidate" 
    sm = sm + 0.05 #check increments or call sm function 




