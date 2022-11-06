
# MRIQC

### Automated analysis of weekly MRI Quality Control Images for ACR Accreditation.

This project is developed as part of Google Summer of Code(GSoC) 2022 program.

## Introduction
The project  automates the detection and extraction of key features of MRI phantom images and outputs these results
in an excel file, which can then be futher used for determining the state of MRI equipment being used.


## Modules

### High Contrast Spatial Resolution

The High Contrast spatial Resolution module works for Slice 1 of MRI phantom.

This test takes input from a .dcm file, localizes the three arrays, and calculates the number of distinguishable holes/circles in each row and column. 

The output is an excel file and a contour overlayed image showing which row and column have passed. 

### Low Contrast Object Detectability

The Low Contrast module is developed for Slice 8,9,10, and 11.

This test takes input from a .dcm file, crops out all ten spokes, and calculates the number of distinguishable circles in each spoke.

The output is an excel file and a contour overlayed image showing which spoke has passed.






