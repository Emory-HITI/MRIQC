#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np
import cv2
import math
import matplotlib.pyplot as plt
import copy
import xlwt
from xlwt import Workbook

# Workbook is created
wb = Workbook()

sheet1 = wb.add_sheet('Sheet 1')

sheet1.write(0, 1, 'ARRAY1')
sheet1.write(0, 2, 'ARRAY2')
sheet1.write(0, 3, 'ARRAY3')
sheet1.write(1,0,'Row1')
sheet1.write(2,0,'Row2')
sheet1.write(3,0,'Row3')
sheet1.write(4,0,'Row4')
sheet1.write(5,0,'Col1')
sheet1.write(6,0,'Col2')
sheet1.write(7,0,'Col3')
sheet1.write(8,0,'Col4')
#sheet1.write(1, 1, num_spokes_9)
#sheet1.write(2, 1, num_spokes_8)
#sheet1.write(3, 1, num_spokes_7)
#sheet1.write(4, 1, num_spokes_6)

def row_col_extraction(outline_image,localized_array,threshold_image,array_number):
    print("pika")
    length=0
    if (array_number==1):
        arr_num="arr1"
        length=45
    elif (array_number==2):
        arr_num="arr2"
        length=40
    else:
        arr_num="arr3"
        length=36
            
    M=outline_image.shape[1] ## width of the image
    N=outline_image.shape[0] ## height of the image
    dup_localized_array=localized_array.copy() ## creating a copy image to overlay contours
    pixel_location_hor=[0,0]
    pixel_location_vert=[0,0]
    value_hor=0
    value_vert=0
    ## getting the vertical edge points of the whole map
    ## top edges
    top_val=[0,0]
    t_val=0
    for j in range(0,N):
        if(t_val>0):
            break
        for i in range(0,M):
            t_val=outline_image[j,i]
            if (t_val>0):
                top_val[0]=j ## following opencv notation,height(y) coordinate first
                top_val[1]=i## width(x) axis
                break
    ## down_edges
    low_val=[0,0]
    l_val=0
    for j in range(N-1,0,-1):
        if (l_val>0):
            break
        for i in range(M-1,0,-1):
            l_val=outline_image[j,i]
            if (l_val>0):
                low_val[0]=j
                low_val[1]=i
                break
    
    #print("upper edge x is ",top_val[1]," upper edge y is",top_val[0])
    #print ("lower edge x is",low_val[1],"lower edge y is",low_val[0])
    ## iterating from left side
    
    for i in range(0,M):
        if (value_vert>0):
            break
        for j in range(0,N):
            value_vert=outline_image[j,i]
            if (value_vert>0):
                pixel_location_vert[0]=j
                pixel_location_vert[1]=i
                break
    # updating the value when in case edge is straight line in the circle            
    updated_vert_loc=0
    for j in range(pixel_location_vert[0],N):
        if (outline_image[j,pixel_location_vert[1]]==0):
            updated_vert_loc=math.floor((pixel_location_vert[0]+j)/2)
            break
    pixel_location_vert[0]=updated_vert_loc
    #at this point we have starting point from left side of the circle
    #we will now use the above value as a distance measure for getting the correct starting point
    #now getting the point from the above circle
    
    for j in range(0,N):
        if (value_hor>0):
            break
        for i in range(0,M):
            value_hor=outline_image[j,i] ## iterating row wise
            if (value_hor>0):
                pixel_location_hor[0]=j
                pixel_location_hor[1]=i
                distance=0
                distance=math.sqrt(math.pow((pixel_location_vert[0]-pixel_location_hor[0]),2)+math.pow((pixel_location_vert[1]-pixel_location_hor[1]),2))
                if (distance<=35):
                    break
                value_hor=0
      
    updated_hor_loc=0
    
    for i in range(pixel_location_hor[1],M):
        if (outline_image[pixel_location_hor[0],i]==0):
            updated_hor_loc=math.floor((pixel_location_hor[1]+i)/2)
            break
            
    pixel_location_hor[1]=updated_hor_loc
    
    ### This can be used a starting point
    #print("x axis value for left starting",pixel_location_hor[1],"y axis value for right starting",pixel_location_hor[0])
    
    ## iterating from the right side
    pixel_right_hor=[0,0]
    val_r_hor=0
    for i in range(M-1,0,-1):
        if (val_r_hor>0):
            break
        for j in range(0,N//4):
            val_r_hor=outline_image[j,i]
            if ((val_r_hor>0) and (j-top_val[0]<30)): ## using reference point to get the correct point
                pixel_right_hor[0]=j
                pixel_right_hor[1]=i
                break
            val_r_hor=0
    ## updating the value
    
    for j in range(pixel_right_hor[0],N):
        if (outline_image[j,pixel_right_hor[1]]==0):
            pixel_right_hor[0]=math.floor((pixel_right_hor[0]+j)/2)
            break
            
    #print ("right_right_x value is",pixel_right_hor[1],"pixel y right right value",pixel_right_hor[0])            
    ## getting the right side upper value
    pixel_right_vert=[0,0]
    val_r_top=0
    dist=0
    for j in range(0,N):
        if (val_r_top>0):
            break
        for i in range(pixel_right_hor[1]+30,0,-1):
            val_r_top=outline_image[j,i]
            if (val_r_top>0):
                pixel_right_vert[0]=j
                pixel_right_vert[1]=i
                dist=math.sqrt(math.pow((pixel_right_vert[0]-(pixel_right_hor[0]-20)),2)+math.pow((pixel_right_hor[1]-pixel_right_vert[1]),2))
                if (dist<=35):
                    break
            val_r_top=0
    
    #print("right_top_x_value is",pixel_right_vert[1],"right_top_y_value is",pixel_right_vert[0])
    ## updating the values
    for i in range(pixel_right_vert[1],0,-1):
        if (outline_image[pixel_right_vert[0],i]==0):
            pixel_right_vert[1]=math.floor((pixel_right_vert[1]+i)/2)
            break
        
        
    #print("right_top_x_value is",pixel_right_vert[1],"right_top_y_value is",pixel_right_vert[0])    
    
    ### Trying to Crop out the first row
    
    high_upper_value=0 ## getting the top pixel y coordinate
    if (pixel_location_hor[0]<pixel_right_vert[0]):
        high_upper_value=pixel_location_hor[0]
    else:
        high_upper_value=pixel_right_vert[0]
        
    
    num_objects=0 # this value will be updated for each row and coloumn to get distinct number
    # getting the coordinated to crop a rectangle
    high_upper_value-=5 # y coordinate
    top_left_cord=pixel_location_vert[1]-5 # x coordinate
    low_left_cord=high_upper_value+length #y value
    top_right_cord=pixel_right_hor[1]+5 #x value
    wid1=top_right_cord-top_left_cord
    hei1=low_left_cord-high_upper_value
    ####cv2.rectangle(dup_localized_array,(top_left_cord,high_upper_value),(top_left_cord+wid1,high_upper_value+hei1),(255,255,0),2)
    
    # cropping out the row
    row_1=np.zeros((hei1,wid1),np.uint8)
    for i in range(0,wid1):
        for j in range(0,hei1):
            row_1[j,i]=localized_array[j+high_upper_value,i+top_left_cord]
            
    row_1 = cv2.resize(row_1,None,fx=0.7,fy=0.7,interpolation = cv2.INTER_CUBIC)        
    num1=rc_object_count(row_1)  
    if (num1==4):
        cv2.rectangle(dup_localized_array,(top_left_cord,high_upper_value),(top_left_cord+wid1,high_upper_value+hei1),(255,255,0),2)
        
                                           
#     cv2.imshow("outline_image",row_1)
#     cv2.waitKey()
#     cv2.destroyAllWindows()
                                     
    #cropping second and third row subsequently
    for x in range(1,3):
        low_left_cord+=x*length
        high_upper_value+=x*length
        mid_value=[0,0]
        mid_value[0]=(low_left_cord+high_upper_value)//2 # y axis
        mid_value[1]=top_right_cord  # x axis
        for i in range(mid_value[1],M):
            if (localized_array[mid_value[0],i]<7):
                mid_value[1]=i
                break
        wid2=mid_value[1]-top_left_cord
        hei2=low_left_cord-high_upper_value
        if (x==1):
            row_2=np.zeros((hei2,wid2),np.uint8)
            for i in range(0,wid2):
                for j in range(0,hei2):
                    row_2[j,i]=localized_array[j+high_upper_value,i+top_left_cord]
            row_2 = cv2.resize(row_2,None,fx=0.7,fy=0.7,interpolation = cv2.INTER_CUBIC)
            num2=rc_object_count(row_2)
            if (num2==4):
                cv2.rectangle(dup_localized_array,(top_left_cord,high_upper_value),(top_left_cord+(mid_value[1]-top_left_cord),high_upper_value+(low_left_cord-high_upper_value)),(255,255,0),2)
                
                               
                           
        elif (x==2):
            row_3=np.zeros((hei2,wid2),np.uint8)
            for i in range(0,wid2):
                for j in range(0,hei2):
                    row_3[j,i]=localized_array[j+high_upper_value,i+top_left_cord]
            row_3=cv2.resize(row_3,None,fx=0.7,fy=0.7,interpolation = cv2.INTER_CUBIC)
            num3=rc_object_count(row_3)
            if (num3==4):
                cv2.rectangle(dup_localized_array,(top_left_cord,high_upper_value),(top_left_cord+(mid_value[1]-top_left_cord),high_upper_value+(low_left_cord-high_upper_value)),(255,255,0),2)
                
        
                       
        # make it back to initial value
        low_left_cord-=x*length
        high_upper_value-=x*length
        
    #going for fourth row
    low_left_cord+=3*length
    high_upper_value+=3*length
    mid_value[1]=top_right_cord ## x axis
    mid_value[0]=(low_left_cord+high_upper_value)//2  ## y axis
    for i in range(mid_value[1],M):
        if (localized_array[mid_value[0],i]<7):
            mid_value[1]=i
            break
            
    #print(mid_value[0])
    #print(mid_value[1])
    ## will crop out the extended fourth row after detection of first coloumn
    ## Done as a measure to always get the correct coordinates
    
    ### Getting the Coloumns from Right to Left
    value_1=0
    last_col=[0,0]
    for i in range(M-1,0,-1):
        if (value_1>0):
            break
        for j in range(N-1,N//2,-1):
            value_1=outline_image[j,i]
            if (value_1>0):
                last_col[0]=j
                last_col[1]=i
                if (low_val[0]-last_col[0]<=35): ## to check if we got the correct point
                    break
                value_1=0
     
    ## updating the value
    for j in range(last_col[0],0,-1):
        if (outline_image[j,last_col[1]]==0):
            last_col[0]=(last_col[0]+j)//2
            break
            
    #print("last_column x value is",last_col[1],"last_Column y value is",last_col[0])
    
    # now using these values we will get all the values for the last row
    #getting the center coordinates for last column last row
    last_center_val=[0,0]
    last_center_val[0]=last_col[0]
    last_center_val[1]=last_col[1]-length//2;
    # iterating downwards and getting the last point of the column
    last_point_last_col=0
    for j in range(last_center_val[0],N):
        if (localized_array[j,last_center_val[1]]<15):
            last_point_last_col=j
            break
    #backup in case (<threshold) doesn't work
    if (last_point_last_col==0):
        last_point_last_col=last_col[0]
    #now iterating in upwards direction to get the upper point
    last_col_first_point=0
    for j in range(last_center_val[0],0,-1):
        if (localized_array[j,last_center_val[1]]<15):
            last_col_first_point=j
            break
            
    print(last_center_val[1])
    print(last_col_first_point)
    
    last_col_start=last_center_val[1]-length//2;
    if (length==45):
        length-=5
    hei3=last_point_last_col-last_col_first_point 
    wid3=length 
    #overlaying the coloumn  
    ##cropping out the coloumn
    col_4=np.zeros((hei3,wid3),np.uint8)
    for i in range(0,wid3):
        for j in range(0,hei3):
            col_4[j,i]=localized_array[j+last_col_first_point,i+last_col_start]
    col_4 = cv2.resize(col_4,None,fx=0.7,fy=0.7,interpolation = cv2.INTER_CUBIC)
    ncol4=rc_object_count(col_4)
    if (ncol4==4):
        cv2.rectangle(dup_localized_array,(last_col_start,last_col_first_point),(last_col_start+wid3,last_col_first_point+hei3),(255,255,0),2)
        
          
    ##applicable only for fourth row
    if (mid_value[1]<last_center_val[1]): ## kind of a precaution step so that it gets the entire combined row(Otherwise might stop due to threshold)
        mid_value[1]=last_center_val[1]+20
        
    ##now cropping overlaying and cropping the combined fourth row
    row_extend=[]
    for i in range(0,mid_value[1]-top_left_cord):
        for j in range(0,low_left_cord-high_upper_value):
            row_extend.append([j+high_upper_value,i+top_left_cord])
            
    
    
    ## trying to crop the third and second coloumn from right to left direction
    for x in range(1,3):
        last_col_start-=x*length
        last_col_first_point=last_col_first_point
        ## now we will check in upper direction and update the y coordinate
        for j in range(last_col_first_point,0,-1):
            if (localized_array[j,last_col_start+22]<19):
                last_col_first_point=j
                break
        ##similarly checking in the downwards direction
        for j in range(last_point_last_col,N):
            if (localized_array[j,last_col_start+22]<10):
                last_point_last_col=j
                break
        wid4=length
        hei4=last_point_last_col-last_col_first_point
        if (x==1):
            col_3=np.zeros((hei4,wid4),np.uint8)
            for i in range(0,wid4):
                for j in range(0,hei4):
                    col_3[j,i]=localized_array[j+last_col_first_point,i+last_col_start]
            col_3 = cv2.resize(col_3,None,fx=0.7,fy=0.7,interpolation = cv2.INTER_CUBIC)
            ncol3=rc_object_count(col_3)
            if (ncol3==4):
                cv2.rectangle(dup_localized_array,(last_col_start,last_col_first_point),(last_col_start+wid4,last_col_first_point+hei4),(255,255,0),2) 
                
        elif(x==2):
            col_2=np.zeros((hei4,wid4),np.uint8)
            for i in range(0,wid4):
                for j in range(0,hei4):
                    col_2[j,i]=localized_array[j+last_col_first_point,i+last_col_start]
            col_2 = cv2.resize(col_3,None,fx=0.7,fy=0.7,interpolation = cv2.INTER_CUBIC)
            ncol2=rc_object_count(col_3)
            if (ncol2==4):
                cv2.rectangle(dup_localized_array,(last_col_start,last_col_first_point),(last_col_start+wid4,last_col_first_point+hei4),(255,255,0),2) 
                
                    
                    
        ##make the value so that it can be used in future references
        last_col_start+=x*length    
        
    ## going for first combined coloumn
    
    last_col_start-=3*length
    last_col_first_point=last_col_first_point
    # check in upper direction and update the y coordinate
    for j in range(last_col_first_point,0,-1):
        if (localized_array[j,last_col_start+22]<19):
            last_col_first_point=j
            break
    ## similarly checking in downward direction
    
    for j in range(last_point_last_col,N):
        if (localized_array[j,last_col_start+22]):
            last_point_last_col=j
            break
            
    wid6=length
    hei6=last_point_last_col-last_col_first_point
    #overlaying combined col1
    col_extend=[]
    for i in range(0,wid6):
        for j in range(0,hei6):
            col_extend.append([j+last_col_first_point,i+last_col_start])
    ###finding the common elements
    t_row = map(tuple, row_extend)
    t_col = map(tuple, col_extend) 
    s_row = set(t_row)
    s_col = set(t_col)
    s_cr=s_row.intersection(s_col)
    Common_elements=list(s_cr)
    print(len(Common_elements))
    ##Cropping the fourth row by capturing the common elements
    min_x=100000
    min_y=100000
    max_x=0
    max_y=0
    for p in Common_elements:
        if (p[0]<min_y):
            min_y=p[0]
        if (p[0]>max_y):
            max_y=p[0]
        if (p[1]<min_x):
            min_x=p[1]
        if (p[1]>max_x):
            max_x=p[1]
            
    center_val=[0,0]
    center_val[0]=(max_y+min_y)//2
    center_val[1]=(max_x+min_x)//2
    #print("mid value x is",center_val[1])
    #print("mid value y is",center_val[0])
   ## extracting the fourth row 
    #iterating in left direction
    fourth_row_start=[0,0]
    for i in range(center_val[1],0,-1):
        if (threshold_image[center_val[0],i]==0):
            if (abs(top_left_cord-i)<10):
                fourth_row_start[1]=i
                break
                
    ## iterating in the downward direction to get the lower limit
    fourth_row_down_value=0
    for i in range(fourth_row_start[1],fourth_row_start[1]+35):
        for j in range(center_val[0],N):
            if (threshold_image[j,i]==0):
                if (fourth_row_down_value<j):
                    fourth_row_down_value=j
                    break
                break
    
    
    wid7=max_x-fourth_row_start[1]
    hei7=fourth_row_down_value-min_y
    #overlaying fourth row
    #cv2.rectangle(dup_localized_array,(fourth_row_start[1],min_y),(fourth_row_start[1]+wid7,min_y+hei7),(255,255,0),2)
    row_4=np.zeros((hei7,wid7),np.uint8)
    for i in range(0,wid7):
        for j in range(0,hei7):
            row_4[j,i]=localized_array[j+min_y,i+fourth_row_start[1]]
    row_4 = cv2.resize(row_4,None,fx=0.7,fy=0.7,interpolation = cv2.INTER_CUBIC)
    num4=rc_object_count(row_4)
    if (num4==4):
        cv2.rectangle(dup_localized_array,(fourth_row_start[1],min_y),(fourth_row_start[1]+wid7,min_y+hei7),(255,255,0),2)
        
    
            
    
    ## going for first coloumn
    first_col_down_val=0
    for i in range(center_val[1]-10,center_val[1]+10):
        for j in range(center_val[0],N):
            if (threshold_image[i,j]==0):
                if (first_col_down_val<j):
                    first_col_down_val=j
                    break
                break
                
    ## backup case in case threshold image has some breaks in it
    if (first_col_down_val<low_val[1]):
        first_col_down_val=low_val[1]

    #little alteration to x_cordinate of first coloumn to get a better initiation point
    #we try to get first white pixel going from left to right direction
    f_col_x=10000
    for j in range(N-1,N-((N//4)-20),-1):
        for i in range(0,M):
            if (threshold_image[j,i]==255):
                if (i<f_col_x):
                    f_col_x=i
                    
    #print("least x value is ",f_col_x)
    
    if (f_col_x>min_x):
        f_col_x=min_x
        
    if (f_col_x<min_x):
        if (abs(f_col_x-min_x)>8):
            f_col_x+=abs((f_col_x-min_x)//2)
    
    
    wid8=max_x-min_x
    hei8=first_col_down_val+10-min_y
    
    #cv2.rectangle(dup_localized_array,(f_col_x,min_y),(f_col_x+wid8,min_y+hei8),(255,255,0),2)
    
    col_1=np.zeros((hei8,wid8),np.uint8)
    for i in range(0,wid8):
        for j in range(0,hei8):
            col_1[j,i]=localized_array[j+min_y,i+f_col_x]
    col_1 = cv2.resize(col_1,None,fx=0.7,fy=0.7,interpolation = cv2.INTER_CUBIC)
    ncol1=rc_object_count(col_1)
    if (ncol1==4):
        cv2.rectangle(dup_localized_array,(f_col_x,min_y),(f_col_x+wid8,min_y+hei8),(255,255,0),2)
        
            
    ## uncomment if you want to see individual rows and columns at each step
#     cv2.imshow("row1",row_1)
#     cv2.waitKey()
#     cv2.destroyAllWindows()
#     cv2.imshow("row2",row_2)
#     cv2.waitKey()
#     cv2.destroyAllWindows()
#     cv2.imshow("row3",row_3)
#     cv2.waitKey()
#     cv2.destroyAllWindows()
#     cv2.imshow("row4",row_4)
#     cv2.waitKey()
#     cv2.destroyAllWindows()
#     #######
#     cv2.imshow("col1",col_1)
#     cv2.waitKey()
#     cv2.destroyAllWindows()
#     cv2.imshow("col2",col_2)
#     cv2.waitKey()
#     cv2.destroyAllWindows()
#     cv2.imshow("col3",col_3)
#     cv2.waitKey()
#     cv2.destroyAllWindows()
#     cv2.imshow("col4",col_4)
#     cv2.waitKey()
#     cv2.destroyAllWindows()    
    
    cv2.imshow("outline_image",dup_localized_array)
    cv2.waitKey()
    cv2.destroyAllWindows()

    Count_list=[num1,num2,num3,num4,ncol1,ncol2,ncol3,ncol4]
    for x in range(len(Count_list)):
        if (Count_list[x]==4):
            Count_list[x]=1
        else:
            Count_list[x]=0
    
    if (array_number==1):
        sheet1.write(1, 1, Count_list[0])
        sheet1.write(2, 1, Count_list[1])
        sheet1.write(3, 1, Count_list[2])
        sheet1.write(4, 1, Count_list[3])
        sheet1.write(5, 1, Count_list[4])
        sheet1.write(6, 1, Count_list[5])
        sheet1.write(7, 1, Count_list[6])
        sheet1.write(8, 1, Count_list[7])
    elif (array_number==2):
        sheet1.write(1, 2, Count_list[0])
        sheet1.write(2, 2, Count_list[1])
        sheet1.write(3, 2, Count_list[2])
        sheet1.write(4, 2, Count_list[3])
        sheet1.write(5, 2, Count_list[4])
        sheet1.write(6, 2, Count_list[5])
        sheet1.write(7, 2, Count_list[6])
        sheet1.write(8, 2, Count_list[7])
    elif (array_number==3):
        sheet1.write(1, 3, Count_list[0])
        sheet1.write(2, 3, Count_list[1])
        sheet1.write(3, 3, Count_list[2])
        sheet1.write(4, 3, Count_list[3])
        sheet1.write(5, 3, Count_list[4])
        sheet1.write(6, 3, Count_list[5])
        sheet1.write(7, 3, Count_list[6])
        sheet1.write(8, 3, Count_list[7])
        
    wb.save('xlwt example8.xls')    
                                                                                 
#############################################################            


# In[ ]:




