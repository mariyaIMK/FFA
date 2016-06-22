import subprocess 
import glob 
import time 
import re

"""
Prior to run this code, must create a directory called accelcands
It will move the "*_ACCEL_0" files to accelcands

"""


time_init = time.time()
filenms = glob.glob("p2030.*_DM*.dat")

for filenm in filenms:
	bash_line = "accelsearch -zmax 0 -numharm 16 "+ filenm
	subprocess.call(bash_line,shell=True)
	outfile = re.sub('\.dat$','_ACCEL_0',filenm)
	bash_line2 = "mv "+outfile+" accelcands/"
	subprocess.call(bash_line2,shell=True)

print "Time total : ",time.time()-time_init
