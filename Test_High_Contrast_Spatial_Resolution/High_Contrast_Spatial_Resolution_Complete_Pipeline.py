#!/usr/bin/env python
# coding: utf-8

# In[5]:


###The code is dependent on--- row_col_extraction,Shanbhag,Connected_Objects_Counts,rc_object_count

import numpy as np
import cv2
import math
#original_slice_img=cv2.imread(r"D:\MRI_phantom\High_spatial_resolution_Slices\Slice1_1.png",0)
original_slice_img=scaled_image_1
template_image=cv2.imread(r"data_HC\slice1_template.png",0)


#### Localizing the region of interest
image=original_slice_img
img=image.copy()
w, h = template_image.shape[::-1]
blank_image=np.zeros((h,w),np.uint8)
method = eval('cv2.TM_CCORR_NORMED')
res = cv2.matchTemplate(image,template_image,method)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
#print(max_val) 
for i in range(0,w):
    for j in range(0,h):
        blank_image[j,i]=original_slice_img[max_loc[1]+j][max_loc[0]+i]
########
template_image2=cv2.imread(r"data_HC\Template_slice1_array1.png",0)

### calculating the approximate location of 3 arrays
approx_arr1=np.zeros((template_image.shape[0],template_image.shape[1]//3),np.uint8)
approx_arr2=np.zeros((template_image.shape[0],template_image.shape[1]//3),np.uint8)
approx_arr3=np.zeros((template_image.shape[0],template_image.shape[1]//3),np.uint8)
for i in range(0,template_image.shape[1]//3):
    for j in range(0,template_image.shape[0]):
        approx_arr1[j,i]=blank_image[j,i] 
        approx_arr2[j,i]=blank_image[j,i+(template_image.shape[1]//3)]
        approx_arr3[j,i]=blank_image[j,i+2*(template_image.shape[1]//3)]
        
##### Fine tuning the location using NCC
arr1=np.zeros((template_image2.shape[0],template_image2.shape[1]),np.uint8)
arr2=np.zeros((template_image2.shape[0],template_image2.shape[1]),np.uint8)
arr3=np.zeros((template_image2.shape[0],template_image2.shape[1]),np.uint8)
image1=approx_arr1
image2=approx_arr2
image3=approx_arr3
w, h = template_image2.shape[::-1]
method = eval('cv2.TM_CCORR_NORMED')
res1= cv2.matchTemplate(image1,template_image2,method)
res2= cv2.matchTemplate(image2,template_image2,method)
res3= cv2.matchTemplate(image3,template_image2,method)
min_val1, max_val1, min_loc1, max_loc1 = cv2.minMaxLoc(res1)
min_val2, max_val2, min_loc2, max_loc2 = cv2.minMaxLoc(res2)
min_val3, max_val3, min_loc3, max_loc3 = cv2.minMaxLoc(res3)
#print(max_val1)
#print(max_val2)
#print(max_val3)
for i in range(0,w):
    for j in range(0,h):
        arr1[j,i]=approx_arr1[max_loc1[1]+j][max_loc1[0]+i]
        arr2[j,i]=approx_arr2[max_loc2[1]+j][max_loc2[0]+i]
        arr3[j,i]=approx_arr3[max_loc3[1]+j][max_loc3[0]+i]
        
        
##### Calculating the number of visible holes for array1,array2 and array3
for x in range(1,4):
    if (x==1):
        arr=arr1
    elif (x==2):
        arr=arr2
    elif (x==3):
        arr=arr3
    bicubic_img = cv2.resize(arr,(380,380),interpolation = cv2.INTER_CUBIC) ###bicubic_image
    im1=bicubic_img
    hist=cv2.calcHist([im1],[0],None,[256],[0,256]) ## calculating the histogram of the image
    hist=hist.astype(int)
    thresh_value=Shanbhag(hist)
    ret, threshold_image = cv2.threshold(im1,thresh_value, 255, cv2.THRESH_BINARY) ### threshold_image
    thresh = cv2.threshold(threshold_image, 240 ,255, cv2.THRESH_BINARY_INV)[1]
    outline_image = cv2.Canny(thresh, 50, 255, 1) ### outline image
    outline_image=outline_image
    localized_array=bicubic_img
    threshold_image=threshold_image
    row_col_extraction(outline_image,localized_array,threshold_image,x)
    


# In[ ]:




