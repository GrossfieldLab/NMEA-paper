#!/usr/bin/env python
#
# Usage- setup.py model psf n-copies

import loos
import loos.pyloos
import sys
import subprocess
import numpy
import os
import shutil
import math
import copy

fudgexy = 2
fudgez = 1.66
ions_conc = 0.0         # M
pad = 30
padding = 15
Na = 6.0221409e23
waterbox_size = 14.7785



def factorize(n):
    on=n
    factors = []
    i=2
    limit = 1000
    while i<=n and limit>0:
        limit -= 1
        if not n%i:
            n = n//i
            while not n%i:
                n = n//i
            factors.append(i)
        i += 1

    if limit <= 0:
        print 'Warning- factorization limit reached for ', on
    if not factors:
        print 'Warning- could not factorize ', on
        factors=[on]
    return factors


def checkFor235(factors):
    lf = copy.copy(factors)
    if 2 in lf:
        lf.remove(2)
    if 3 in lf:
        lf.remove(3)
    if 5 in lf:
        lf.remove(5)
    return (len(lf) == 0)


def findPMEGridSize(n):
    n = int(math.ceil(n))
    facts = set(factorize(n))
    ok = checkFor235(facts)
    limit = 1000
    while not ok and limit > 0:
        limit -= 1
        n += 1
        facts = set(factorize(n))
        ok = checkFor235(facts)

    if limit <= 0:
        print 'Error- unable to find a PMEGridSize for ', n
        sys.exit(-10)
    return(n)



def randomVector():
    v = numpy.random.normal(size=3)
    v /= numpy.linalg.norm(v)
    return v


def savePDB(fname, system):
    pdb = loos.PDB.fromAtomicGroup(system)
    f = open(fname, 'w')
    f.write(str(pdb))



def writeOMGConfig(fname, boxsize, model, psf, nwaters, salts):
    f = open(fname, 'w')
    print >> f, 'psfgen /home/tromo/Packages/NAMD/NAMD_2.12_Source/Linux-x86_64-g++/psfgen'
    print >> f, 'topology ../toppar/top_all36_prot.rtf'
    print >> f, 'topology ../toppar/top_all36_lipid.rtf'
    print >> f, 'topology ../toppar/top_all36_carb.rtf'
    print >> f, 'topology ../toppar/top_all36_cgenff.rtf'
    print >> f, 'topology ../toppar/toppar_water_ions_namd.str'
    print >> f, 'parameters ../toppar/par_all36_prot_mod.prm'
    print >> f, 'parameters ../toppar/par_all36_lipid.prm'
    print >> f, 'parameters ../toppar/par_all36_carb.prm'
    print >> f, 'parameters ../toppar/par_all36_cgenff.prm'
    print >> f, 'topology ../toppar/toppar_water_ions_namd.str'
    print >> f, 'psf solvated.psf'
    print >> f, 'box %f %f %f' % (boxsize[0], boxsize[1], boxsize[2])


    print >> f, 'protein %s %s NONE 0' % (model, psf)
    print >> f, 'water BULK TIP3 %d %f %f %s' % (nwaters, boxsize[2], waterbox_size, 'water_randomized.pdb')
    print >> f, 'salt SOD SOD %d' % (salts)
    print >> f, 'salt CLA CLA %d' % (salts+8)   # 8 more Cl needed to neutralize


def writeSimParms(fname, boxsize, gridsize):
    f = open(fname, 'w')
    print >> f, 'set BOXSIZEX %f' % boxsize[0]
    print >> f, 'set BOXSIZEY %f' % boxsize[1]
    print >> f, 'set BOXSIZEZ %f' % boxsize[2]
    print >> f, 'set GRIDSIZEX %d' % gridsize[0]
    print >> f, 'set GRIDSIZEY %d' % gridsize[1]
    print >> f, 'set GRIDSIZEZ %d' % gridsize[2]





# Assume polymer is built in y-direction...
def findBoxSize(model):
    bounds = model.boundingBox()
    d = bounds[1] - bounds[0]

    print 'original box size: ', d
    #    maxdim = max(d)
    #    box = [maxdim + pad, maxdim + pad, maxdim + pad]
    #    box = [int(d.x() * fudgexy), int(d.x() * fudgexy), int(d.z() * fudgez)]
    maxrad = model.radius()
    print 'Model radius: ', maxrad
    boxsize = int(math.ceil(2*(maxrad + padding)))
    print 'Padding: ', padding
    print 'New box size: ', boxsize
    box = [boxsize, boxsize, boxsize]
    return(box)


def writeBlueGenePrep(fname, index):
    f = open(fname, 'w')
    print >> f, '#!/bin/bash'
    print >> f, '#SBATCH -p standard --nodes 16 --ntasks-per-node 1 -t 8:00:00 -o "npt-0.%%j.out" -e "npt-0.%%j.err" --job-name "prep-%02d"' % index
    print >> f, 'srun /home/tromo/local/bin/namd2-smp +ppn 64 +CmiNoProcForComThread npt.0.inp'




def createWaterBox():

    os.mkdir('water')
    os.symlink('../water.inp', 'water.inp')
    os.symlink('../water_small.pdb', 'water_small.pdb')
    os.symlink('../water_small.psf', 'water_small.psf')

    water_log = open('water.log', 'w')
    water_err = open('water.err', 'w')
    ok = subprocess.call(['/home/tromo/local/bin/namd2', '+p2', 'water.inp'], stdout = water_log, stderr = water_err)
    if ok != 0:
        print 'Water box processing failed with error code ', ok
        sys.exit(-2)

    subprocess.call(['fixdcd', 'water/water.dcd'])

    # Get traj size...
    water_model = loos.createSystem('water_small.psf')
    water_traj = loos.pyloos.Trajectory('water/water.dcd', water_model)
    last_water = water_traj[len(water_traj)-1]
    savePDB('water_randomized.pdb', last_water)
#    new_water = open('water_randomized.pdb', 'w')
#    subprocess.call(['frame2pdb', 'water_small.psf', 'water/water.dcd', '9'], stdout = new_water)



def makeRestraints(model, selection_string = 'name == "CA"', konst = 1.0):
    duplicate = model.copy()
    for atom in duplicate:
        atom.bfactor(0.0)
    subset = loos.selectAtoms(model, selection_string)
    for atom in subset:
        atom.bfactor(konst)
    return(duplicate)


model = loos.createSystem(sys.argv[1])
model.centerAtOrigin()
psf = sys.argv[2]
index = int(sys.argv[3])

basename = 'run-%02d' % index
print basename
os.mkdir(basename)
os.chdir(basename)

createWaterBox()

boxsize = findBoxSize(model)
print "The original estimated boxsize is (%d, %d, %d)" % (boxsize[0], boxsize[1], boxsize[2])
print "Overriding to 64x64x64..."
boxsize=[64,64,64]
gridsize = []
for dimension in boxsize:
    gridsize.append(findPMEGridSize(dimension))

print "Box size is (%d, %d, %d)" % (boxsize[0], boxsize[1], boxsize[2])
print "Grid size is (%d, %d, %d)" % (gridsize[0], gridsize[1], gridsize[2])


# Assume 55M water
nmols = 55.0 * Na
vol = boxsize[0] * boxsize[1] * boxsize[2] * math.pow(1e-10, 3) * 1e3
#vol = math.pow(boxsize * 1e-10, 3.0) * 1e3   # in L
nwaters = int(math.floor(nmols * vol))
salts = int(math.floor(ions_conc * Na * vol))
print 'Using %d waters' % nwaters
print 'Adding %d each of Na and Cl' % salts



savePDB('init.pdb', model)
shutil.copy('../' + psf, '.')
restrained = makeRestraints(model)
savePDB('restraints.pdb', restrained)

writeOMGConfig('solvate.cfg', boxsize, 'init.pdb', psf, nwaters, salts)

omglog = open('omg.log', 'w')
omgerr = open('omg.err', 'w')
ok = subprocess.call(['OptimalMembraneGenerator.py', 'solvate.cfg'], stdout=omglog, stderr=omgerr)
if ok != 0:
    print 'OMG FAILED: return code = ', ok
    sys.exit(-1)

os.symlink('out/solvated.psf', 'namd.psf')
os.symlink('out/final.pdb', 'start.pdb')
os.symlink('../prep.inp', 'npt.0.inp')
os.symlink('../npt-template.inp', 'npt-template.inp')

writeSimParms('simparms.inp', boxsize, gridsize)
writeBlueGenePrep('blueprep.sh', index)

os.mkdir('output_nvt')
os.mkdir('output_npt')
os.mkdir('output')

os.chdir('..')
