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
sm = 0.30 #maximum flux density at which you want to attempt an injection 

##########################################################################





#=========================================================================

#Define the other variables accordingly 


basename = beam.split('.fil',1)[0]
filename = basename + '_dm' + str(dm) +'_p%f'  % (period) + '_sm%.3f' % (sm)

#sm will get altered at each injection in step 3   
#rms is defined in step 1 from prepdata

#========================================================================

#presto bash commands 

bash_line0 = 'prepdata -nobary -dm '+ str(dm) + ' -o '+ basename + ' ' + beam + ' > prepdata_output.txt'
bash_line1 = 'grep "Data standard deviation:  *" prepdata_output.txt > rms_output.txt'
bash_line2 = 'rfifind -time 2.0 -o '+ basename + ' ' + beam 


bash_line3 = 'python injectpsr.py --dm '+ str(dm) + ' -p %f' % (period)+ ' -v "1 200 0.5" -s radiometer -c "smean=%.3f' % (sm) + ',gain=10,tsys=33.876,rms=' +rms+'" -o '+ filename +'.fil' + ' ' + basename + '.fil' 

bash_line4 = 'prepdata -nobary -dm '+ str(dm) +' -o ' + filename + ' ' + filename + '.fil' 

bash_line5 = 'prepfold -nopdsearch -nodmsearch -topo -nosearch -noxwin -p %f'  % (period) + ' -o ' + filename + ' ' + filename + '.fil' 

bash_line6 = 'prepdata -nobary -dm '+ str(dm) + ' -mask '+ basename + '_rfifind.mask -o '+ filename + ' '+ filename + '.fil'

bash_line7 = 'python ffa.py ' + filename + '.dat --plot'

#=========================================================================



#step 1: Before any beam injection 
subprocess.call(bash_line0,shell=True)
subprocess.call(bash_line1,shell=True)

rms_output = open("rms_output.txt")
line = rms_output.readlines()[0]
values = line.split()
rms = (values[3])
print "The rms value for DM " + str(dm) + " is: "+ rms    #take rms from the prepdata output ## Data standard deviation:  2481.55
    

subprocess.call(bash_line2,shell=True)



#step2: Inject, Prepdata, Prepfold, Prepdata, FFA on the right DM 

for trial in trials 

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

    if float(format(cands_period,'.2f')) == float(format(period,'.2f')): 
        print "The pulsar was found as the first candidate at flux density: %f"  % (sm) 
    else
        print "The pulsar was NOT found as the first candidate"
        print "The current flux density is: %f"  % (sm)
        print ""
        print "An incrementation of the flux density will follow ..." 
        #sm = sm + 0.5 #check increments or call sm function 
print "done"





