import sys
import os
import subprocess
import glob

def savio_prep(rawdir = 'raw/', galname = 'draco'):

	rawfiles = glob.glob(rawdir+'/*fits*')
	filenames = [j.replace(rawdir, "") for j in rawfiles]
	
	
	# get rid of drz or drc files from rawlist
	img_names = [x for x in filenames if not 'drc' in x]
	img_names = [x for x in img_names if not 'drz' in x]
	
	
	jobs = open('jobs-list', 'a')
	
	#set up runphot files for all chip1
	for i in range(len(img_names)):
		file = open('runphot_1_'+str(i), 'a')
		file.write("cd /clusterfs/dweisz/salbers/draco/acs" + "\n")
		file.write("python"+ "\n")
		file.write("from dolphot_prep_chip import *" + "\n")
		file.write("dolphot_prep('"+img_names[i]+"' ,'1')"+ "\n")
		file.write("exit()"+ "\n")
		file.write("cd " + img_names[i].replace('.fits.gz', '.chip1')+"\n")
		param_file = 'phot_'+img_names[i][:-8]+'.param'
		file.write("dolphot "+ galname +"_acs_"+ str(i)+".phot -p"+param_file+" >> phot.log" )
		jobs.write("./runphot_1_"+str(i) +"\n")
		file.close()
		
	#set up runphot files for all chip2	
	for i in range(len(img_names)):
		file = open('runphot_2_'+str(i), 'a')
		file.write("cd /clusterfs/dweisz/salbers/draco/acs" + "\n")
		file.write("python"+ "\n")
		file.write("from dolphot_prep_chip import *" + "\n")
		file.write("dolphot_prep('"+img_names[i]+"','2')"+ "\n")
		file.write("exit()"+ "\n")
		file.write("cd " + img_names[i].replace('.fits.gz', '.chip2')+"\n")
		param_file = 'phot_'+img_names[i][:-8]+'.param'
		file.write("dolphot "+ galname +"_acs_"+ str(i)+".phot -p"+param_file+" >> phot.log" )
		jobs.write("./runphot_2_"+str(i) +"\n")
		file.close()
		
		
		
	jobs.close()
	
	
