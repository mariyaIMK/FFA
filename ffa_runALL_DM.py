import subprocess 
import glob
import time
import ffa 

time_initial = time.time()

#apply the ffa for all DM.00.dat files

filename = glob.glob("*_DM*.00.dat")


for filenm in filename:
       subprocess.call("python ffa.py %s"%filenm, shell=True) 


#keep track of the time needed to run the ffa on all DM.00.dat files 
time_final=time.time()
print "Time it took: ", time_final-time_initial 
