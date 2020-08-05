# NMEA-paper
Scripts used to generate data and figures for anisotropic terahertz spectroscopy paper

Romo, Grossfield, and Markelz, "Identification of functionally important collective vibrations through terahertz Normal Mode Ensemble Analysis"

Simulation: parameters and input files for running the MD simulations

Spectrum: collection of scripts used to compute the VDOS and absorbance spectra, including the CHARMM input scripts

Analysis: scripts to analyze and average the data, including the projections of modes onto the difference between structures

random-projections: code to generate the distribution of dot products in high dimensions. Used to create Supplemental Figure 3.

## Figures
The following describes the salient scripts used in preparation of each figure.

### Figure 1
* dipolederivative_extract.py
* fastcalc.py
* postprocess.py
* process_aniso.sh

### Figure 2
* dipolederivative_extract.py
* IsotropicCalcHEWL2.py
* xeig.py
* process_iso.sh
* process_vdos.sh

### Figure 3
* dipolederivative_extract.py
* fastcalc.py
* postprocess.py
* process_aniso.sh

### Figure 4
* dipolederivative_extract.py
* IsotropicCalcHEWL2.py
* xeig.py
* process_iso.sh
* process_vdos.sh

### Figure 5
* xeig.py
* generate_diffvec.py
* process_diffvec.sh


### SI Figure 1
* dipolederivative_extract.py
* IsotropicCalcHEWL2.py
* xeig.py
* process_iso.sh
* process_vdos.sh

### SI Figure 2
* dipolederivative_extract.py
* IsotropicCalcHEWL2.py
* xeig.py
* process_iso.sh
* process_vdos.sh

### SI Movie 1
* dipolederivative_extract.py
* fastcalc.py
* postprocess.py
* process_aniso.sh

### SI Figure 3
* dipolederivative_extract.py
* fastcalc.py
* postprocess.py
* process_aniso.sh

### SI Figure 4
* dipolederivative_extract.py
* fastcalc.py
* postprocess.py
* process_aniso.sh

### SI Figure 5
* dipolederivative_extract.py
* fastcalc.py
* postprocess.py
* process_aniso.sh

