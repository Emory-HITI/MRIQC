
# LOW CONTRAST OBJECT DETECTABILITY

The low contrast object detectability works for Slices 8,9,10 ,and 11. It calculates the number
of distinguishable circles in all ten spokes.


### General Workflow

* The input image is first converted from .dcm to .png format.
* The inner circle is then localized/Cropped out using morphological operations.
* The localized image is scaled up by a factor of 2 using bicubic interpolation.
* The image is gamma-corrected and sharpened using unsharp masking.
* All ten spokes are then cropped out using a rotation matrix and a prior knowledge of angles at which all spokes are placed.
* The cropping out of the spokes is fine-tuned by comparing gray level intensities on the right, and left sides of cropped spoke.
* Spokes 9 to 6 are processed using NCC for the number of different circles.
* A threshold value is set, and a template is passed. If the correlation value is above the threshold, then that specific circle is considered resolved.
* This is done for all 3 circles in each spoke.
* Spoke 5 to 0 are processed using Circular Hough Transform Technique.
* Parameters of Hough Transform are changed for individual spoke, as the size of the circle decreases as we go from spoke 5 to 0.
* The final results of all ten spokes are output as an excel file.

### Result Impacting Factors

* Change in values of gamma correction and unsharp masking , used as preprocessing.
* Change in template image used for detection in Spoke 9 to 6.
* Changing the value of  the threshold used for considering a circle as resolved.





## Running the Low Contrast Object Detectability

To deploy this project run

```bash
  $ python3 Dicom_To_Png.py
  $ python3 Localization_Low_Contrast_Object_Detectability.py.py
  $ python3 Spokes_Crop_All_Slices.py
  $ python3 LC_Test_Spokes_Circle_Count.py
```

All .py files should be run in the same order, as the output of one gets passed to another.
