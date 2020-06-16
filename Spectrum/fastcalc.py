#!/usr/bin/env python
# Adapted by Tod D. Romo, Grossfield Lab, 2016
#
# Usage-
#    python fastcalc.py input.csv output.csv
#
# Note: shape of output and iteration bounds are hard-coded



import sys
import csv
import numpy as np
import math
import time

maxfreq = 3000

print('Anisotropic calculation...')

indata = np.genfromtxt(sys.argv[1],delimiter=",")
(m, n) = indata.shape
if maxfreq is None:
        maxfreq = m
        print('Setting maxfreq to {}'.format(maxfreq))
nmodes = m

outfilename = sys.argv[2]
freqin = []  #quasiharmonic frequencies
xin = []  #x,y, and z dipole derivatives
yin = []
zin = []

freqin = indata[:,0]
xin = indata[:,1]
yin = indata[:,2]
zin = indata[:,3]


def pvec(theta):  #THz polarization vector
        pvector1 = math.cos((theta*math.pi)/180)*np.array([0,0,1])
        pvector2 = math.sin((theta*math.pi)/180)*np.array([1/(math.sqrt(2)),-1/(math.sqrt(2)),0])
        return pvector1 + pvector2


#Tetragonal Crystal Group Rotation Matricies
R0 = np.array([[1.0,0,0],[0,1.0,0],[0,0,1.0]])
R1 = np.array([[-1.0,0,0],[0,-1.0,0],[0,0,1.0]])
R2 = np.array([[0,-1.0,0],[1.0,0,0],[0,0,1.0]])
R3 = np.array([[0,1.0,0],[-1.0,0,0],[0,0,1.0]])
R4 = np.array([[-1.0,0,0],[0,1.0,0],[0,0,-1.0]])
R5 = np.array([[1.0,0,0],[0,-1.0,0],[0,0,-1.0]])
R6 = np.array([[0,1.0,0],[1.0,0,0],[0,0,-1.0]])
R7 = np.array([[0,-1.0,0],[-1.0,0,0],[0,0,-1.0]])
#R0 = np.array([[1,0,0], [0,1,0], [0,0,1]])
#R1 = np.array([[0,-1,0], [1, -1, 0], [0, 0, 1]])
#R2 = np.array([[-1, 1, 0], [-1, 0, 0], [0, 0, 1]])



R = np.array([R0,R1,R2,R3,R4,R5,R6,R7],float)

#R = np.array([R0,R1,R2],float)


V=np.array([xin,yin,zin])  # each column corresponds to each freq.

def Ialignxtl(f,gamma,theta):
        totvalue = 0
        pv = pvec(theta)
        pv2 = float(np.dot(pv, pv))
        for j in range(8):    # Change to match # of symops
                totvaluei = 0
                product = np.dot(R[j,:,:],V)
                for i in range(6,nmodes):		#(len(xin)): #994 #2195 #494
                        subproduct=product[:,i]
                        product2 = float(np.dot(subproduct,pv))
                        value = ((gamma/freqin[i])* product2*product2)/(((f-freqin[i])*(f-freqin[i])+gamma*gamma)*pv2)
                        totvaluei = value + totvaluei
                totvalue = totvalue + totvaluei
        return totvalue


outabs=np.zeros((maxfreq,14))
start_time = time.time()
for f in range(maxfreq):
        outstring = ''
        for k in range(13):
                fout = float(f)/10.0
                outabs[f,0]=fout
                outabs[f,k+1]=Ialignxtl(fout,4,k*15)
        if f % 10 == 0:
                elapsed_time = time.time() - start_time
                average_per_freq = elapsed_time / (f+1)
                remaining = (maxfreq - f + 1) * average_per_freq
                print('f = {} (avg={:.2f} s, remain={:.2f} m)'.format(f, average_per_freq, remaining/60.0))

total_time = time.time() - start_time
print('Calculation took {} seconds'.format(total_time))

np.savetxt(outfilename, outabs, delimiter=',')#, newline='\n')
