#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#### The code makes use of Spokes_Crop_All_Slices for Cropping individual Spokes
import xlwt
from xlwt import Workbook
import cv2
import numpy as np
import circle_fit as cf
import math
from skimage import data
from skimage.filters import unsharp_mask
import matplotlib.pyplot as plt
from skimage import io
from skimage.util import img_as_ubyte
from skimage import data, color
from skimage.transform import hough_circle, hough_circle_peaks
from skimage.feature import canny
from skimage.color import rgb2gray
import math
wb = Workbook()
sheet1 = wb.add_sheet('Sheet 1')
sheet1.write(0, 1, 'Slice_number')
sheet1.write(1,0,'Spoke9')
sheet1.write(2,0,'Spoke8')
sheet1.write(3,0,'Spoke7')
sheet1.write(4,0,'Spoke6')
sheet1.write(5,0,'Spoke5')
sheet1.write(6,0,'Spoke4')
sheet1.write(7,0,'Spoke3')
sheet1.write(8,0,'Spoke2')
sheet1.write(9,0,'Spoke1')
sheet1.write(10,0,'Spoke0')

def gammaCorrection(src, gamma):
    invGamma = 1 / gamma

    table = [((i / 255) ** invGamma) * 255 for i in range(256)]
    table = np.array(table, np.uint8)

    return cv2.LUT(src, table)


bicubic_image = cv2.imread(r"D:\MRI_phantom\Slices\Slice_10_cropped\bicubic_Slice10_3.png",0) ###INPUT THE IMAGE
npimage=np.asarray(bicubic_image)
if (math.floor(np.average(bicubic_image))<100):
    result_3 = unsharp_mask(npimage, radius=30, amount=3)
    
elif (math.floor(np.average(bicubic_image))>150):
    gamma_corrected_img=gammaCorrection(bicubic_image, 0.7)
    npimage=np.asarray(gamma_corrected_img)
    result_3 = unsharp_mask(npimage, radius=30, amount=1)
else:
    gamma_corrected_img=gammaCorrection(bicubic_image, 0.8)
    npimage=np.asarray(gamma_corrected_img)
    result_3 = unsharp_mask(npimage, radius=30, amount=2)
    
#cv_image= img_as_ubyte(result_3)
#cv2.imshow("template_image",cv_image)
#cv2.waitKey()
#cv2.destroyAllWindows()    

############# Now the Cropping starts
### Creating a function
template_image_9=cv2.imread(r"C:\Users\praroop_2\Desktop\cir_template_10.png",0)
template_image_8=cv2.imread(r"C:\Users\praroop_2\Desktop\Template\Temp8_enhanced_4.png",0)
template_image_7=cv2.imread(r"C:\Users\praroop_2\Desktop\Template\Temp7_enhanced.png",0)
template_image_6=cv2.imread(r"C:\Users\praroop_2\Desktop\Template\Temp6_enhanced_2.png",0)


# GOING FOR SPOKES 9,8,7,6
def Spokes_match(Cropped_slice,template_image):
    num_spokes=0
    y_cord=[]
    for pika in range(0,3):
        image=Cropped_slice
        img=image.copy()
        w, h = template_image.shape[::-1] ## will take the opposite values
        method = eval('cv2.TM_CCORR_NORMED')
        # Apply template Matching
        res = cv2.matchTemplate(image,template_image,method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        #print(max_val) 
        #print(max_loc)
        y_cord.append(max_loc[1])
        if (max_val>0.9):
            num_spokes+=1
            for i in range(0,w):
                for j in range(0,h):
                    Cropped_slice[max_loc[1]+j][max_loc[0]+i]=0

    y_cord.sort()                
    if (num_spokes==3):
        if (abs((y_cord[2]-y_cord[1])-(y_cord[1]-y_cord[0]))<=4):
            num_spokes=3
        else:
            num_spokes=0
    return(num_spokes) 
    
Number_spokes9=Spokes_match(Cropped_9,template_image_9)
Number_spokes8=Spokes_match(Cropped_8,template_image_8)
Number_spokes7=Spokes_match(Cropped_7,template_image_7)
Number_spokes6=Spokes_match(Cropped_6,template_image_6)
#print(Number_spokes9)
#print(Number_spokes8)
#print(Number_spokes7)
#print(Number_spokes6)  

### GOING FOR SPOKES 5,4,3
def Hough_Circles(image_1,radius_size,canny_thresh):

    average_val=math.floor(np.average(image_1))
    #print(average_val)
    
    image=image_1

    if (canny_thresh==1):
        edges = canny(image, sigma=1, low_threshold=10, high_threshold=20)
    else:
        edges = canny(image, sigma=1, low_threshold=math.floor(0.1*average_val), high_threshold=math.floor(0.15*average_val))
    # Detect One radii
    hough_radii = np.arange(radius_size,6,1)
    hough_res = hough_circle(edges, hough_radii)

    # Select the most prominent  circle
    accums, cx, cy, radii = hough_circle_peaks(hough_res, hough_radii,
                                               total_num_peaks=1)

    for center_y,center_x,radius in zip(cy,cx,radii):
        flag=1
    if (len(radii)==0):
        radius=0
        center_x=-1
        center_y=-1
    return(radius,center_x,center_y)

from PIL import Image, ImageFilter
import numpy as np
import cv2
import math
import matplotlib.pyplot as plt
from skimage.util import img_as_ubyte


def circle_hough_detect(img,filter_size,edge_param,radius_size):
    list_2=[]
    input_image=img
    average_val=math.floor(np.average(img))
    k=0
    rad=[]
    dict_1={}
    num_detec=0
    for k in range(0,3):
        sub_length=math.floor(img.shape[0]/3)
        image_crop1=np.zeros((sub_length,img.shape[1]),np.uint8)
        for i in range(0,img.shape[1]):
            for j in range(0,sub_length):
                image_crop1[j,i]=img[j+(k*sub_length),i]
        average_val=math.floor(np.average(image_crop1))        
        if (average_val<200):
            ##converting to pil and then back
            im_pil = Image.fromarray(image_crop1)
            im2 = im_pil.filter(ImageFilter.MaxFilter(size = filter_size))
            #im2.show()
            image = np.array(im2)
            #image_crop1= cv2.equalizeHist(image)
            image_crop1=image
            #print(True)
        image = img_as_ubyte(image_crop1)

        (radius,center_x,center_y)=Hough_Circles(image,radius_size,edge_param)
        if (radius!=0):
            rad.append(radius)
        if (center_y!=-1):
            list_2.append(center_y+(k*sub_length))
           # print(list_2)
            dict_1[center_y+(k*sub_length)]= center_x
        else:
            list_2.append(center_y)
            dict_1[center_y]=center_x

    list_2.sort()    
    if -1 in list_2:
        num_detec=0
        return num_detec
    elif (abs((list_2[2]-list_2[1])-(list_2[1]-list_2[0]))<=7):
        num_detec=3
        return num_detec
    
    return num_detec    

## for slice 5,4
def cir54(input_slice):
    filters_45=[1,3,5]
    edge_para=[1,0]
    rad=4
    for x in filters_45:
        number_detect=circle_hough_detect(input_slice,x,1,4)
        if (number_detect==3):
            break
        #number_detect=circle_hough_detect(input_slice,x,0,rad)
        #if (number_detect==3):
            #break
    return number_detect

Number_spokes5=cir54(Cropped_5)
Number_spokes4=cir54(Cropped_4)
#print(Number_spokes5)
#print(Number_spokes4)

## for slice 3
def cir3(input_slice):
    filters_3=[1,3,5]
    edge_para=[1,0]
    rad=4
    for x in filters_3:
        number_detect=circle_hough_detect(input_slice,x,1,4)
        if (number_detect==3):
            break
        number_detect=circle_hough_detect(input_slice,x,1,3)
        if (number_detect==3):
            break
    return number_detect
    #print(number_detect)  
    
Number_spokes3=cir3(Cropped_3)
#print(Number_spokes3)

#########
## for slice 2,1,0
def cir210(input_slice):
    filters_210=[3,5]
    edge_para=[1,0]
    rad=4
    for x in filters_210:
        number_detect=circle_hough_detect(input_slice,x,1,3)
        if (number_detect==3):
            break
        #number_detect=circle_hough_detect(input_slice,x,1,3)
        #if (number_detect==3):
            #break
    return number_detect
    #print(number_detect)
Number_spokes2=cir210(Cropped_2)
Number_spokes1=cir210(Cropped_1)
Number_spokes0=cir210(Cropped_0)
#print(Number_spokes2)
#print(Number_spokes1)
#print(Number_spokes0)

sheet1.write(1,1,Number_spokes9)
sheet1.write(2,1,Number_spokes8)
sheet1.write(3,1,Number_spokes7)
sheet1.write(4,1,Number_spokes6)
sheet1.write(5,1,Number_spokes5)
sheet1.write(6,1,Number_spokes4)
sheet1.write(7,1,Number_spokes3)
sheet1.write(8,1,Number_spokes2)
sheet1.write(9,1,Number_spokes1)
sheet1.write(10,1,Number_spokes0)

