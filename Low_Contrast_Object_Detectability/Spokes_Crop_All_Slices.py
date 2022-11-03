#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import cv2
import math

################
####### Function to Crop out the spokes from Scaled_Localized Image
############
def rotate_around_point(point, radians, origin=(0, 0)): ## Rotation Matrix to Crop the spokes at an angle
    x, y = point
    o1, o2 = origin

    px = o1 + math.cos(radians) * (x - o1) + math.sin(radians) * (y - o2)
    py = o2 + -math.sin(radians) * (x - o1) + math.cos(radians) * (y - o2)

    return px, py

def rightleft(image):     ### Function to make finer adjustments After Cropping procedure
    flag=0
    height=image.shape[0]
    width=image.shape[1]
    right=0
    left=0
    for i in range(0,height):
        for j in range(0,width//2):
            left+=image[i,j]

    for i in range(0,height):
        for j in range(width//2,width):
            right+=image[i,j]
    ## using flag value as a paramter to see which side are the spokes tilted
    ratio_value=right/left
    if (ratio_value>1):
        ## Holes are tilted more towards the right side
        flag=1
        print(ratio_value-1)
        return(abs(1-ratio_value),flag)
    else:
        ###Holes are tilted more towards the left side
        print(1-ratio_value)
        return (abs(1-ratio_value),flag)
    
def Crop_Angled(image,theta):  ## Cropping at the specified angle
    theta=np.radians(theta)
    blank_image1=np.zeros((76,23),np.uint8)
    for i in range(0,23):
        for j in range(0,76):
            xc,yc=rotate_around_point((i+77,j+2),theta,(image.shape[0]/2,image.shape[1]/2))
            #print(image.shape[0],image.shape[1])
            if (math.floor(xc)>=image.shape[1]):
                xc=xc-1;
            if (math.floor(yc)>=image.shape[0]):
                yc=yc-1;
            #print(xc,yc)    
            blank_image1[j,i]=image[math.floor(yc),math.floor(xc)]  
            # here xc would be number of rows and yc would be number of rows
    (diff,direction)=rightleft(blank_image1)
    #print(diff)
    return(blank_image1,diff,direction)    


def Crop_Spoke(image,theta): ## Giving the Final Cropped Spoke
    (Cropped_image,diff,direction)=Crop_Angled(image,theta)
    if (diff>0.05):
        list_1=[]
        if (direction==1): ## more shifted towards the right side
            list_1.append(diff)
            #print(diff)
            for i in range(theta-1,theta-5,-1):
                print(i)
                (temp_img,difference,dirc)=Crop_Angled(image,i)
                #print(difference)
                list_1.append(difference)
            #print(list_1)    
            min_value=min(list_1)    
            min_index=list_1.index(min_value)
            (Cropped_image,difference,dirc)=Crop_Angled(image,theta-min_index)
            return Cropped_image
        else:
            list_1.append(diff)
            for i in range(theta,theta+5):
                (temp_img,difference,dirc)=Crop_Angled(image,i)
                list_1.append(difference)
            min_value=min(list_1)    
            min_index=list_1.index(min_value)
            (Cropped_image,difference,dirc)=Crop_Angled(image,theta+min_index)
            return Cropped_image
    return Cropped_image  


bicubic_image = cv2.imread(r"D:\MRI_phantom\Slices\Slice_11_cropped\bicubic_Slice_11_1.png",0) ## input Scaled_localized Slice
#### Rotation Angles Corresponding to Different Spokes in different Slices
#######
List_1=[11,48,85,120,156,191,225,260,297,334] ##corresponding to slice11     
#List_1=[19,57,93,129,163,198,234,270,306,343] ##corresponding to slice10
##List_1=[29,66,102,138,173,208,243,279,315,352] ## corresponding to Slice9
##List_1=[40,75,111,145,180,216,252,289,324,1] ## correspoding to slice8 


#### Cropping out all the Spokes
Cropped_0=Crop_Spoke(bicubic_image,List_1[0])
Cropped_1=Crop_Spoke(bicubic_image,List_1[1])
Cropped_2=Crop_Spoke(bicubic_image,List_1[2])
Cropped_3=Crop_Spoke(bicubic_image,List_1[3])
Cropped_4=Crop_Spoke(bicubic_image,List_1[4])
Cropped_5=Crop_Spoke(bicubic_image,List_1[5])
Cropped_6=Crop_Spoke(bicubic_image,List_1[6])
Cropped_7=Crop_Spoke(bicubic_image,List_1[7])
Cropped_8=Crop_Spoke(bicubic_image,List_1[8])
Cropped_9=Crop_Spoke(bicubic_image,List_1[9])


### Concatinating all the Cropped Images to show as a single Image (For Reference)
Hori = np.concatenate((Cropped_0,Cropped_1,Cropped_2,Cropped_3,Cropped_4,Cropped_5,Cropped_6,Cropped_7,Cropped_8,Cropped_9), axis=1)
cv2.imshow('HORIZONTAL', Hori) 
cv2.waitKey()
cv2.destroyAllWindows()


