import sys
import os
import subprocess
import glob


def dolphot_prep(img_name, chip_num, rawdir = 'raw/'):
	
	log_file = 'phot.log'
	param_file = 'phot_'+img_name[:-8]+'.param'
	
	#copy images from raw into working directory
	
	subprocess.call("cp " +rawdir+img_name+" "+ os.getcwd(), shell=True)
	
	# check if it is zipped, and if so, unzip it	

	if img_name.split(".")[-1] == 'gz':
		subprocess.call("gunzip " + img_name, shell=True)
		img_name = img_name.strip(".gz")
	
		
	if os.path.isdir(img_name[:-5]+'.chip'+chip_num) is False:	
		subprocess.call("mkdir "+img_name[:-5]+'.chip'+chip_num, shell=True)
	
	
	not_chip_num = 0	
	if (chip_num == '1'):
		not_chip_num = '2'
	if (chip_num == '2'):
		not_chip_num = '1'
			
	
	subprocess.call("acsmask " + img_name + " > " + log_file, shell=True)
	subprocess.call("splitgroups " + img_name + " > " + log_file, shell=True)
	subprocess.call("calcsky "+ img_name.replace('.fits', '.chip'+chip_num) +"  15 35 -128 2.25 2.00 >> " + log_file, shell=True)
	subprocess.call('mv '+img_name.replace('.fits', '.chip'+chip_num+'.fits') +' '+img_name.replace('.fits', '.chip'+chip_num), shell= True)
	subprocess.call('mv '+img_name.replace('.fits', '.chip'+chip_num+'.sky.fits') +' '+img_name.replace('.fits', '.chip'+chip_num), shell = True)
	subprocess.call('rm '+img_name.replace('.fits', '.chip'+not_chip_num+'.fits'), shell = True)
	subprocess.call('mv '+log_file +' '+img_name.replace('.fits', '.chip'+chip_num), shell = True)	
	
	file = open(param_file, 'a')
	file.write("Nimg = 1"+ "\n")
	file.write("img0_file = " + img_name[:-5]+'.chip'+chip_num + "\n")
	file.write("img0_shift = " + "0 0"  + "\n" )
	file.write("img0_xform = " + "1 0 0" + "\n")
	file.write("img1_file = " + img_name[:-5] + '.chip'+chip_num + "\n")
	file.write("img1_shift = " + "0 0"  + "\n" )
	file.write("img1_xform = " + "1 0 0" + "\n")
	file.close()
	
	dolparams(param_file)
	
	subprocess.call('mv '+param_file +' '+img_name.replace('.fits', '.chip'+chip_num), shell = True)	

def dolparams(paramfile):
	
	dolphot_params = {
	'RAper': 3,
	'Rchi': 3.0,
	'PSFPhot': 1,
	'FitSky': 2,
	'RSky0': 15,
	'RSky1': 35,
	'SkipSky': 2,
	'SkySig': 2.25,
	'SecondPass': 5,
	'SearchMode': 1,
	'SigFind': 2.5,
	'SigFindMult':0.85,
	'SigFinal': 3.5,
	'SubResRef': 1,
	'MaxIT': 25,
	'NoiseMult': 0.10,
	'FSat': 0.999,
	'FlagMask': 4,
	'ApCor': 1,
	'Force1': 1,
	'Align': 0,
	'Rotate': 1,
	'RCentroid': 1,
	'PosStep': 0.25,
	'dPosMax': 2.5,
	'RCombine': 3.0,
	'RPSF': 10,
	'SigPSF': 5.0,
	'PSFres': 1,
	'psfoff': 0.0,
	'DiagPlotType': 'PS',
	'UseWCS': 0,
	'ACSpsfType': 0,
	'ACSuseCTE': 0,
	'WFC3UVISpsfType': 0,
	'WFC3IRpsfType': 0,
	'WFC3useCTE': 0,
	'CombineChi': 1,
	'#FakeStars': 'fake.list',
	'#FakeMatch': 3.0,
	'#FakeStarPSF': 1.5,
	'#RandomFake':1,
	
	
	
	
	
	}

	file = open(paramfile, 'a')
	for i in dolphot_params.keys():
    		file.write(i+ ' = ' +np.str(dolphot_params[i])+"\n")
    	file.close()
