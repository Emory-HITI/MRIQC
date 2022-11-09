#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pydicom as dicom
import matplotlib.pyplot as plt
import cv2
try:
    image_path=r'data_HC\1.2.840.113619.2.495.11565861.612164.25601.1652700575.99.dcm'
    ds=dicom.dcmread(image_path)
    data=ds.pixel_array
    new_image = ds.pixel_array.astype(float)
    scaled_image_1 = (np.maximum(new_image, 0) / new_image.max()) * 255.0
    scaled_image_1 = np.uint8(scaled_image_1)
    #cv2.imshow("Image",scaled_image_1)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
except:
    scaled_image_1=cv2.imread(r'data_HC\Slice1_1.png')

