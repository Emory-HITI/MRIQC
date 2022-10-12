#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import cv2
from skimage import data
from skimage.filters import threshold_multiotsu

#### Code to find number of distict objects in each row and Column
#### Uses Connected_Objects_Counts() function
def rc_object_count(input_image):
    ## input an opencv image
    np_image=np.asarray(input_image,dtype="uint8")
    connected_obj=0
    thresh_val=[0,0,0]## will save different multi otsu threshold values
    
    for x in range(5,2,-1):
        thresh_val[5-x]= threshold_multiotsu(np_image,classes=x)[-1] ## taking the last threshold value
        ret,thresh1=cv2.threshold(input_image,thresh_val[5-x],255,cv2.THRESH_BINARY)
        connected_obj=Connected_Objects_Counts(thresh1)
        if (connected_obj==4):
            print("threshold_value is",thresh_val[5-x])
            return connected_obj
            break
        ## Backup in case all 3 multi otsu thresholds
        if (x==3 and connected_obj!=4):
            for i in range(0,3):
                for j in range(thresh_val[i]-10,thresh_val[i]+11,2):
                    ret,thresh1=cv2.threshold(input_image,j,255,cv2.THRESH_BINARY)
                    connected_obj=Connected_Objects_Counts(thresh1)
                    if (connected_obj==4):
                        print("threshold_value",j)
                        return connected_obj
                        break
                if (connected_obj==4):
                    return connected_obj
                    break
    return connected_obj

