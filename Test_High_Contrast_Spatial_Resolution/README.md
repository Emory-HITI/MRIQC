
# HIGH CONTRAST SPATIAL RESOLUTION TEST

### General Workflow

* The input image is first converted from .dcm to .png format.
* The next step is localizing the region of interest, for which we use the NCC (Normalized cross-correlation) technique. This crops out the three arrays located at the center of Slice1.
* Further, we crop out the individual arrays(1.1mm,1mm,0.9mm) by dividing the image into three equal parts.
* The three cropped out arrays are further fine tuned in terms of localizing, by again using NCC.
* All three arrays are scaled up by a factor of 20 using bicubic interpolation.
* Each array is now sequentially processed, and all four rows and columns are extracted.
* The number of distinguishable circles in each row/column is calculated using multi-otsu threshold.
* The final results of all three arrays are output as an excel file. 

### Result Impacting Factors
* In Row_Column_Extraction.py, the  extracted rows and columns are scaled down by a factor of 0.7 before calculating the number of distinguishable holes.
* Change in the downscaling factor can change the results, as downsampling might lead to loss of information but will save computation time.
## Running the High Contrast Spatial Resolution 

To deploy this project run

```bash
  $ python Shanbhag_Threshold.py
  $ python Connected_Objects_Count.py 
  $ python RC_Object_Count.py
  $ python Row_Column_Extraction.py
  $ python Dicom_To_Png_HC.py 
  $ python High_Contrast_Spatial_Resolution_Complete_Pipeline.py 
```
All .py files should be run in the same order, as the output of one gets passed to another.

OR

run this single file:-

```bash 
  $python .\run_module.py
```



