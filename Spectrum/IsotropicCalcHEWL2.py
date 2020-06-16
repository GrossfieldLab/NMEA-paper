import csv
import numpy as np
import math
import sys

maxmode = None
maxfreq = 200

print('Isotropic calculation...')

whole_data = []
input_file = open(sys.argv[1],'r')
outfile = open(sys.argv[2],'w')

if len(sys.argv) > 3:
        maxmode = int(sys.argv[3])

        if len(sys.argv) > 4:
                maxfreq = float(sys.argv[4])

print("{} -> {} with maxmodes={}, maxfreq={}".format(sys.argv[1], sys.argv[2], maxmode, maxfreq))

freqin = []  #quasiharmonic frequencies
xin = []  #x,y, and z dipole derivatives
yin = []
zin = []
nlines = -1
for line in input_file:  #read in quasiharmonic freqs and dipole derivatives
	nlines += 1
	inline = line.split(',')
	freqin.append(float(inline[0]))
	xinline = inline[1]
	yinline = inline[2]
	zinline = inline[3]
	xin.append(float(xinline[0:10]))
	yin.append(float(yinline[0:10]))
	zin.append(float(zinline[0:10]))

if maxmode is None:
        maxmode = len(xin)
        print('Setting maxmode to {}'.format(maxmode))


V=np.array([xin,yin,zin])  # each column corresponds to each freq.

def Ialignxtl(f,gamma):
	totvalue = 0
	for i in range(7,maxmode): #1500
		value = 0
		vectormag = math.sqrt(V[0,i]*V[0,i]+V[1,i]*V[1,i]+V[2,i]*V[2,i])
		value = (((gamma*gamma)/freqin[i])* vectormag*vectormag)/((f-freqin[i])*(f-freqin[i])+gamma*gamma)
		totvalue = totvalue + value
	return totvalue


for f in np.arange(0, maxfreq, 0.1):
	outstring = ''
	ialign = Ialignxtl(f,4)
	outstring = ', '+str(ialign)
	outfile.write(str(f)+outstring+'\n')
	if f % 10 == 0:
		print('f = ',f)
