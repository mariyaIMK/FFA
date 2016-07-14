from __future__ import division
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

dm = 600
period = 10.964532 #with 6 decimal places
sm = 0.98 #maximum flux density at which you want to attempt an injection 

beam = sys.argv[1] #give the beam.fil file as an argument

##########################################################################




#=========================================================================

#Define the other variables  

basename = beam.split('.fil',1)[0]
filename = basename + '_dm' + str(dm) +'_p%f'  % (period) + '_sm%.3f' % (sm)

#sm will get altered at each injection in step 3   
#rms is defined in step 1 from prepdata

#========================================================================

#presto bash commands for step 1 

bash_line0 = 'prepdata -nobary -dm '+ str(dm) + ' -o '+ basename + ' ' + beam + ' > prepdata_output.txt'
bash_line1 = 'grep "Data standard deviation:  *" prepdata_output.txt > rms_output.txt'
bash_line2 = 'rfifind -time 2.0 -o '+ basename + ' ' + beam

#=========================================================================

#STEP 1: Before any beam injection 

subprocess.call(bash_line0,shell=True)
subprocess.call(bash_line1,shell=True)

rms_output = open("rms_output.txt")
line = rms_output.readlines()[0]
values = line.split()
rms = (values[3])
print "The rms value for DM " + str(dm) + " is: "+ rms    #take rms from the prepdata output ## Data standard deviation:  2481.55


subprocess.call(bash_line2,shell=True)

#========================================================================

#presto bash commands for step 2

bash_line3 = 'python injectpsr.py --dm '+ str(dm) + ' -p %f' % (period)+ ' -v "1 200 0.5" -s radiometer -c "smean=%.3f' % (sm) + ',gain=10,tsys=33.876,rms=' + rms +'" -o '+ filename +'.fil' + ' ' + basename + '.fil'

bash_line4 = 'prepdata -nobary -dm '+ str(dm) +' -o ' + filename + ' ' + filename + '.fil'

bash_line5 = 'prepfold -nopdsearch -nodmsearch -topo -nosearch -noxwin -p %f'  % (period) + ' -o ' + filename + ' ' + filename + '.fil'

bash_line6 = 'prepdata -nobary -dm '+ str(dm) + ' -mask '+ basename + '_rfifind.mask -o '+ filename + ' '+ filename + '.fil'

bash_line7 = 'python ffa.py ' + filename + '.dat --plot'

#=========================================================================

#STEP 2: Inject, Prepdata, Prepfold, Prepdata, FFA on the right DM 

subprocess.call(bash_line3,shell=True)
subprocess.call(bash_line4,shell=True)
subprocess.call(bash_line5,shell=True)
subprocess.call(bash_line6,shell=True)
subprocess.call(bash_line7,shell=True)

#=========================================================================

#STEP 3: Check if the pulsar was detected 

cands_list_file = filename+'_cands.ffa'
cands_list = open(cands_list_file,'r')

line = cands_list.readlines()[1]
split_line = line.split()
cands_period = (split_line[1])
cands_period = int(re.search(r'\d+', cands_period).group())



#convert and trancate the values 
def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])

cands_period_temp = cands_period/1000
print '*******************************************************************'
print ""
print 'The first candidate has a period of (in seconds): %.3f'% (cands_period_temp)
print 'The injected period is (in seconds): %.6f'  % (period)
cands_period_temp = truncate(cands_period_temp, 2)
period_temp = truncate(period, 2)
print ""


#compare the values in seconds
if cands_period_temp == period_temp:
    print "The pulsar was found as the first candidate at flux density: %.3f" % (sm)
else:
    print "The pulsar was NOT found as the first candidate"
    print "The current flux density is: %.3f" % (sm)
    print ""
    #print "An incrementation of the flux density will follow ..."
    #sm = sm + 0.5 #check increments or call sm function 

print ""
print "DONE"



