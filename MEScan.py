###########################################################################################################
#
# MEScan.py
# created by Kenzo Abrahams
#
# This program runs Gosia and compares the calculated intesity ratio with the measure intensity ratio. 
# It takes a Gosia input file, ready for the integration step, as input. It returns a list of data points,
# diagonal and transitional matrix elements, where the difference between the intensities are inbetween 
# a user defined range. Note, this program does not check if the Gosia file is correct.
#
###########################################################################################################


# Python libraries 
import subprocess
from itertools import islice
import sys
import re
import errno
import os
from os import system, remove

# THESE ARE THE ONLY VARIABLES THAT NEEDS TO BE CHANGED
# The variables are:
#
# 	outFile: 			The name of the file containing the final results
#		expRatio:			The experimental intensity ratio
#		targetYield:	The sum of the target yields over all the rings of the particle detector
#		TMEstep:			The value by which the TME must change after every Gosia run
#		DMEstep:			The value by which the DME must change after every Gosia run
#		DME_low:			The lower limit of the range of DMEs to be scanned
#		DME_high:			The upper limit of the range of DMEs to be scanned
#		TME_low:			The lower limit of the range of TMEs to be scanned
#		TME_high:			The upper limit of the range of TMEs to be scanned
#############################################################################################################
outFile = "MEScan_out.txt"
expRatio = 1.6854908997
targetYield = 17274.6
DMEstep = 0.02
TMEstep = 0.02
DME_low = 0.0
DME_high = 0.05
TME_low = 0.5
TME_high = 0.6
#############################################################################################################


# Check if an input file was provided. If not, print out usage statement. 
 
try:
	arg = sys.argv[1]
except IndexError:
	raise SystemExit('Usage: MEScan.py <Inputfile>')
	print(arg[::-1])

def strip_string(string,to_strip):
	if to_strip:
		while string.startswith(to_strip): string = string[len(to_strip):]
		while string.endswith(to_strip): string = string[:-len(to_strip)]
	return string

# Store the input file name
inputFile = arg


# Method: get2Index(filename)
#
# This method takes the filename as input and returns a list containing line numbers of the important 
# sections in the Gosia file. The list has length 5 and contains the follow points in the input file:
#
# 	list[0]:		The line number for the marker LEVE
# 	list[1]:		The line number for the marker ME
#		list[2]:		The line number for the marker EXPT
#		list[3]:		The difference in line number between ME and where line number of the TME
#		list[4]:		The difference in line number between ME and where line number of the DME
#############################################################################################################

def get2Index(inputFile):
	me = []
	meHold = 0
	leveHold = 0
	exptHold = 0

	src = open(inputFile).read()
	pattern = "LEVE"  # or anything else
	for m in re.finditer(pattern, src):
		start = m.start()
		lineno = src.count('\n', 0, start) + 1
		leveHold = lineno
		me.insert(0,lineno)
		#print "LEVE found at " +str(lineno)
		break

	pattern = "ME"
	for m in re.finditer(pattern, src):
		start = m.start()
		lineno = src.count('\n', 0, start) + 1
		meHold = lineno
		me.insert(1,lineno)
		#print "ME found at " +str(lineno)
		break

	pattern = 'EXPT'
	for m in re.finditer(pattern, src):
		start = m.start()
		lineno = src.count('\n', 0, start) + 1
		exptHold = lineno
		me.insert(2,lineno)
		#print "EXPT found at " +str(lineno)
		break

	levelIndex = 0
	data = []
	with open(inputFile,'r') as r:
		lines = islice(r,leveHold,meHold-1)
		for line in lines:
			#print line
			data = re.split(",",line)
			#print data
			if (len(data) == 1):
				hold = data[0].split()
				#print hold
			else:
				hold = data

			if (int(hold[1]) == 1 and int(hold[2]) == 2):
				levelIndex = int(hold[0])
				break
	r.close()
					
	print "levelIndex = " +str(levelIndex)

	linecount = 0
		
	with open(inputFile,'r') as r:	
		lines = islice(r,meHold,exptHold-1)
		for line in lines:
			#print line
			data = re.split(",",line)
			#print data
			if (len(data) == 1):
				hold = data[0].split()
				#print hold
			else:
				hold = data

			if (int(hold[0]) == 1 and int(hold[1]) == levelIndex):
				#print hold[2]
				me.insert(3,linecount)

			if (int(hold[0]) == levelIndex and int(hold[1]) == levelIndex):
				#Sprint hold[2]
				me.insert(4,linecount)
				break

			linecount = linecount + 1

	r.close()
	print me
	return me

########################################################################################################################

me = get2Index(inputFile)
transIndex = me[3]
diagIndex = me[4]


# Method: silentremove(filename)
#
# Deletes the file with the name given.
#
#######################################################################################################################

def silentremove(filename):
    try:
        os.remove(filename)
    except OSError as e: # this would be "except OSError, e:" before Python 2.6
        if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
            raise # re-raise exception if a different error occurred

#######################################################################################################################



# Method: transChange(TME)
#
# This method changes the transitioanl matrix element in the Gosia file, to the given value TME. It uses the line numbers 
# from get2Index() to determine where the TME is.
#
########################################################################################################################

def transChange(transME):
		countLine = 0		

		with open(inputFile,'r') as r:
			new_file_lines = []
			for line in r:
								
				if countLine == (me[1]+me[3]):				
					#print line
					data = line.split()
					if (len(data) == 1):
						#print "it is soooo"
						data = data[0].split(",")
					hold = transME
					#print hold
					line = line.replace(str(data[2]),str(hold))
					#print line

				new_file_lines.append(line)
				countLine += 1
		
		with open(inputFile,'w') as r:
			r.writelines(new_file_lines)

##########################################################################################################################

# Method: diagChange(DME)
#
# This method changes the diagonal matrix element in the Gosia file, to the given value DME. It uses the line numbers 
# from get2Index() to determine where the DME is.
#
########################################################################################################################

def diagChange(diagME):
		countLine = 0		

		with open(inputFile,'r') as r:
			new_file_lines = []
			for line in r:
								
				if countLine == (me[1]+me[4]):				
					#print line
					data = line.split()
					if (len(data) == 1):
						data = data[0].split(",")
					hold = diagME
					#print hold
					line = line.replace(str(data[2]),str(hold))
					#print line

				new_file_lines.append(line)
				countLine += 1
		
		with open(inputFile,'w') as r:
			r.writelines(new_file_lines)

#########################################################################################################################

# Method: readDiag()
#
# This method reads and returns the current value of the diagonal matrix element in the Gosia input file. It uses the 
# line numbers from get2Index() to determine where the DME is.
#
########################################################################################################################

def readDiag():
	with open(inputFile,'r') as r:
			line = r.readlines()[me[1]+me[4]]
			data = line.split()
			if (len(data) == 1):
						data = data[0].split(",")
			print data
			return float(data[2])

##########################################################################################################################

# Method: readTrans()
#
# This method reads and returns the current value of the transitional matrix element in the Gosia input file. It uses the 
# line numbers from get2Index() to determine where the TME is.
#
########################################################################################################################

def readTrans():
	with open(inputFile,'r') as r:
			line = r.readlines()[me[1]+me[3]]
			data = line.split()
			if (len(data) == 1):
						data = data[0].split(",")
			print data
			return float(data[2])

########################################################################################################################

silentremove("autoGos_out.txt")
silentremove("autoGos_all_points.txt")

diagME = DME_low
diagChange(diagME)
transME = TME_low
transChange(transME)
filecount = 0

resHold = -1

while(diagME <= DME_high and transME <= (TME_high + TMEstep)):

	print"DME = "+str(diagME)
	print"TME = "+str(transME)
	cmd = "gosia < "+inputFile
	system(cmd)
	out = strip_string(inputFile,".inp")
	out = out + ".out"
	cmd = "./integratedyields.pl "+out+" >/dev/null 2>&1"
	system(cmd)

	with open("yields.dat") as f:
		beamYield = 0.0
		for line in f:
			#print line
			data = line.split()
			#print float(data[1])
			beamYield += float(data[1])

	ratioHold = targetYield/beamYield
	residual = expRatio - ratioHold
	
	#print beamYield
	print "residual = " +str(residual)
	#print abs(beamYield-targetYield)

	if(residual < 0.09 and residual > -0.09):

		if os.path.exists("autoGos_out.txt"):
			append_write = 'a' # append if already exists
		else:
			append_write = 'w' # make a new file if not
			
		g = open('autoGos_out.txt', append_write)
		g.write( str(diagME) + " " + str(transME) +" " + str(residual) +" match\n")
		g.close()

		diagME += DMEstep
		diagChange(diagME)
		transME = TME_low
		transChange(TME_low)

		print "Got a match; TME = " +str(TME_low)
	
	else:
		#print "it is not 0"
		if (filecount == 0):
			g = open('autoGos_all_points.txt', 'w')
			g.write( str(diagME) + " " + str(transME) +" " + str(residual) +"\n")
			g.close()
			#print "I get till here"
			filecount = filecount + 1
		
			if((resHold != -1 and resHold > 0.0 and residual < 0.0) or (resHold != -1 and resHold < 0.0 and residual > 0.0)):
				resHold = residual
				diagME += DMEstep
				diagChange(diagME)
				transME = TME_low
				transChange(TME_low)
		
			else:
				if((transME+TMEstep) <= TME_high):
					resHold = residual
					transME += TMEstep
					transChange(transME)

				else:
					transME = TME_low
					diagME += DMEstep
					diagChange(diagME)
					transChange(transME)

		else:
			print "I get till here"
			g = open('autoGos_all_points.txt', 'a')
			g.write( str(diagME) + " " + str(transME) +" " + str(residual) +"\n")
			g.close()		 

			if((resHold != -1 and resHold > 0.0 and residual < 0.0) or (resHold != -1 and resHold < 0.0 and residual > 0.0)):
				resHold = residual
				diagME += DMEstep
				diagChange(diagME)
				transChange(TME_low)
						
			else:
				if((transME+TMEstep) <= TME_high):
					resHold = residual
					transME += TMEstep
					transChange(transME)

				else:
					transME = TME_low
					diagME += DMEstep
					diagChange(diagME)
					transChange(transME)
				
