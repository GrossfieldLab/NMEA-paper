#!/bin/bash -x

for d in run-?? ; do
    cd $d
    ../setb.py start.pdb 'name == "CA"' >restraints.pdb
    ../setb.py start.pdb 'backbone' >fixed_backbone.pdb
    cd ..
done
