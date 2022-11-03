#!/usr/bin/env python
# coding: utf-8

# In[1]:


##implement the IJisodata algorithm
##https://imagej.nih.gov/ij/developer/source/ij/process/AutoThresholder.java.html
##https://github.com/imagej/ImageJ/blob/master/ij/process/AutoThresholder.java
## In this code threshold is that gray value, G.
## For which average of averages of gray values below and above G is equal to G.
def isodata_threshold(hist):
    level=0
    maxvalue=hist.size-1 ## getting the max possible value
    count0=hist[0]## getting the number of pixels with  zero value
    hist[0]=0 ## set to 0 so erased areas aren't included 
    countmax=hist[maxvalue] ## getting number of pixels with max value
    hist[maxvalue]=0 
    min1=0
    while (hist[min1]==0 and (min1<maxvalue)): ## getting the actual minimum pixel intensity value in the image
        min1+=1
    max1=maxvalue    
    while((hist[max1]==0 and (max1>0))): ## getting the actual maximum pixel intensity value in the image
        max1-=1
    if (min1>=max1): ## the case when only one gray level exists in the image 
        hist[0]=count0
        hist[maxvalue]=countmax
        level=hist.size/2
        return level
    ### Calculating threshold for the first time
    movingindex=min1
    inc=max(max1/40,1)
    sum1=0
    sum2=0
    sum3=0
    sum4=0
    for i in range(min1,movingindex+1): ##lower half of threshold
        sum1+=i*hist[i] ## number of elements*intensity level of pixel
        sum2+=hist[i] ## numbers of elements with one specific gray level
    for i in range(movingindex+1,max1+1): ## upper half of the threshold
        sum3+=i*hist[i] 
        sum4+=hist[i]
    result=(sum1/sum2+sum3/sum4)/2 ## getting the threshold value   
    movingindex+=1
    level=int(result)
    while((movingindex+1)<=result and movingindex<(max1-1)): ## iteratively calculating the threshold   
        
        hist[0]=count0 ## putting back the original value in histogram
        hist[maxvalue]=countmax
        level=int(result)
        ###
        sum1=0
        sum2=0
        sum3=0
        sum4=0
        for i in range(min1,movingindex+1):
            sum1+=i*hist[i]
            sum2+=hist[i]
        for i in range(movingindex+1,max1+1):
            sum3+=i*hist[i]
            sum4+=hist[i]
        result=(sum1/sum2+sum3/sum4)/2
        movingindex+=1
    return level
######    
######implement default isodata algorithm
def default_thresh(hist):
    count=0
    n=hist.size ##  gettin the histogram size
    data2=np.zeros(256,dtype=int) ## intializing a zero array with dimensions (1,256)
    ### calculating frequency the two most occuring gray level pixels
    mode=0
    maxcount=0
    for i in range(0,n):
        count=hist[i]
        data2[i]=hist[i]
        if(data2[i]>maxcount): ## calculating the maximum occuring gray level value
            maxcount=data2[i] ## frequency of maximum occuring gray level
            mode=i ## gray level that has highest frequency of occurence
    maxcount2=0
    for i in range(0,n):
        if((data2[i]>maxcount2) and (i!=mode)):
            maxcount2=data2[i] ## frequency of second most occuring gray level
    hmax=maxcount
    if (hmax>(maxcount2*2) and maxcount2!=0):
        hmax=int(maxcount2*1.5)
        data2[mode]=hmax
    return isodata_threshold(data2) 
########
########

######Localization of slice_region
import numpy as np
import cv2
from PIL import Image, ImageDraw
im1=cv2.imread(r"D:\MRI_phantom\Slices\Slice11\Slice11_4.png",0) ## read the image
hist=cv2.calcHist([im1],[0],None,[256],[0,256]) ## calculating the histogram of the image
hist=hist.astype(int)
thresh_value=default_thresh(hist)
ret, thresh1 = cv2.threshold(im1,thresh_value, 255, cv2.THRESH_BINARY)
#cv2.imshow('Binary Threshold', thresh1)
#cv2.waitKey()
#cv2.destroyAllWindows()

########  filling the holes in the thresholded binary image
im_floodfill = thresh1.copy()
h, w = thresh1.shape[:2]
mask = np.zeros((h+2, w+2), np.uint8)
cv2.floodFill(im_floodfill, mask, (0,0), 255);
im_floodfill_inv = cv2.bitwise_not(im_floodfill)
im_out = thresh1 | im_floodfill_inv
im_out_inv=cv2.bitwise_not(im_out)
#cv2.imshow("Foreground", im_out_inv)
#cv2.waitKey()
#cv2.destroyAllWindows()

####### Adding the thresholded and filled image
add_img=cv2.add(thresh1,im_out_inv)
#cv2.imshow('Add_image',add_img)
#cv2.waitKey()
#cv2.destroyAllWindows()

### creating a mask by by making all background pixels black
##[i,j], i is the vertical iterator and j is the horizontal iterator
mask_img=add_img.copy()
height,width=im1.shape
for i in range(0,width): ## processing upper half of the image
    for j in range(0,height):
        if (mask_img[j,i]==255):
            mask_img[j,i]=0
        else:
            if (j<255):
                j+=1
            break
for i in range(0,width): ## processing the lower half of the image
    for j in range(height-1,-1,-1):
        if (mask_img[j,i]==255):
            mask_img[j,i]=0
        else:
            #if (j<255):
                #j+=1
            break
##cv2.imshow("mask_image",mask_img)
##cv2.waitKey()
##cv2.destroyAllWindows()

##flood filling to extract the inner circle
mask_img1= Image.fromarray(mask_img)
seed=(128,128)
mask_img1 = mask_img1.convert("RGB")
rep_value = (255,0, 0) ## red color

ImageDraw.floodfill(mask_img1, seed, rep_value, thresh=1)
#mask_img1.show()
## converting back to opencv image
numpy_image=np.array(mask_img1)
opencv_image=cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)
gray_image = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2GRAY)
#cv2.imshow('grayscale',gray_image)
#cv2.waitKey()
#cv2.destroyAllWindows()

##extracting the coordinates for cropping out the region of interest
## getting the max and min coordinate values for cropping the image
min_x=10000
min_y=10000
max_x=0
max_y=0
for i in range(0,width):
    for j in range(0,height):
        if (gray_image[j,i]!=0 and gray_image[j,i]!=255):
            if (min_x>i):
                min_x=i
            if (min_y>j):
                min_y=j
            if (i>max_x):
                max_x=i
            if (j>max_y):
                max_y=j
#print(min_x,max_x)
#print(min_y,max_y)
final_localized_image=im1[min_y:max_y,min_x:max_x]
cv2.imshow("cropped",final_localized_image)
cv2.waitKey()
cv2.destroyAllWindows()


# In[ ]:




