#!/usr/bin/env python
# coding: utf-8

# In[37]:


## Code to count the  number of distict circles/objects in cropped row/Coloumn
import cv2
import numpy as np
def Connected_Objects_Counts(rc_image):
    height=rc_image.shape[0] ## number of coloumns
    width=rc_image.shape[1] ## number of rows
    ## Converting to binary image
    for i in range(0,height):
        for j in range(0,width):
            if(rc_image[i][j]>0):
                rc_image[i][j]=255   
    
    ## Making top 3 rows/coloums black , to avoid false positives and prevent boundary condition in flood fill algorithm
    ##top 3 rows
    for i in range(0,3):
        for j in range(0,width):
            rc_image[i][j]=0
    ## bottom 3 rows        
    for i in range(height-1,height-4,-1):
        for j in range(0,width):
            rc_image[i][j]=0 
    ## Top 3 coloumns
    for i in range(0,height):
        for j in range(0,3):
            rc_image[i][j]=0
    ## Bottom 3 coloumns
    for i in range(0,height):
        for j in range(width-1,width-4,-1):
            rc_image[i][j]=0 
     
    pix_value=128 ## random value used for flood fill algorithm
    num_objects=0
    for i in range(0,height):
        for j in range(0,width):
            if (rc_image[i][j]==255):
                flood_fill(i,j,pix_value,rc_image);
                num_objects+=1
    #print(num_objects)
    return num_objects
      
def flood_fill(i,j,pix_val,image):
    if (image[i][j]!=255):
        return
    image[i][j]=pix_val
    flood_fill(i-1,j,pix_val,image)
    flood_fill(i,j-1,pix_val,image)
    flood_fill(i,j+1,pix_val,image)
    flood_fill(i+1,j,pix_val,image)
        


# In[ ]:




