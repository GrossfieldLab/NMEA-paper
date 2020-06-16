#!/bin/env python


import sys
import numpy as np
import loos
import math

model = loos.createSystem(sys.argv[1])
subset = loos.selectAtoms(model, sys.argv[2])
pn = len(subset) * 3

data = np.load(sys.argv[3])
eigenvectors = data['arr_0']

eigenvectors = eigenvectors[0:pn, :]
(n, m) = eigenvectors.shape
natoms = int(n / 3)
#if natoms != len(model):
#    print 'Error- eigenvectors do not match model (%d vs %d)' % (natoms, len(model))

eigenvectors = np.square(eigenvectors)
alphas = np.sum(eigenvectors, 0)

zero_warning = 0
for mode in range(6,m):
    sum = 0.0
    for i in range(natoms):
        i3 = i * 3
        u = (eigenvectors[i3,mode] + eigenvectors[i3+1, mode] + eigenvectors[i3+2, mode]) / (alphas[mode])
        if (u > 0.0):
            sum += u * math.log(u)
        else:
            zero_warning += 1
    k = math.exp(-sum) / natoms
    print(mode, '\t', k)

# Should go to stderr...
if zero_warning > 0:
    print('# Warning- there were %{} zero u found'.format(zero_warning))



def buildMassTable(model_name, psf_name, subset_selection):
    model = loos.createSystem(model_name)
    psf = loos.createSystem(psf_name)

    # First, fix masses...
    mass_table = {}
    for atom in psf:
        name = atom.name()
        mass = atom.mass()
        if name in mass_table:
            if mass != mass_table[name]:
                print('Error- multiple masses found for {} ({} vs {})'.format(name, mass, mass_table[name]))
                sys.exit(-10)
        else:
            mass_table[name] = mass


    protein = loos.selectAtoms(model, subset_selection)
    masses = []
    for atom in protein:
        name = atom.name()
        if name not in mass_table:
            print('Error- could not find {} in mass table'.format(name))
            sys.exit(-11)
        atom.mass(mass_table[name])
        masses.append(mass_table[name])

    return masses
