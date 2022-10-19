#!/usr/bin/env python
# coding: utf-8

# In[2]:


## implementing shanbhag threshold
##https://github.com/imagej/ImageJ/blob/master/ij/process/AutoThresholder.java
import numpy as np
import math
def Shanbhag(hist):
    threshold=0
    ih=0
    it=0
    first_bin=0
    last_bin=0
    term=0
    tot_ent=0
    min_ent=0
    ent_back=0
    ent_obj=0
    norm_hist=[0 for x in range(0,256)]
    p1=[0 for x in range(0,256)]
    p2=[0 for x in range(0,256)]
    total=0
    for ih in range(0,256):
        total+=hist[ih]
    for ih in range(0,256):
        norm_hist[ih]=hist[ih]/total;
    p1[0]=norm_hist[0]
    p2[0]=1.0-p1[0]
    for ih in range(1,256):
        p1[ih]=p1[ih-1]+norm_hist[ih]
        p2[ih]=1.0-p1[ih]
    
    ### determine the first non zero bin
    first_bin=0
    for ih in range(0,256):
        if (abs(p1[ih])>2.220446049250313E-16):
            first_bin=ih
            break
    ### determine the last non zero bin
    last_bin=255
    for ih in range(255,first_bin-1,-1):
        if (abs(p2[ih])>2.220446049250313E-16):
            last_bin=ih
            break
   ## calculate the total entropy each gray level
    ### and find the threshold that maximises it
    threshold=-1
    min_ent=999999999
    for it in range(first_bin,last_bin+1):
        ent_back=0
        term=0.5/p1[it]
        for ih in range(1,it+1):
            ent_back-=norm_hist[ih]*math.log(1.0-term*p1[ih-1])
        ent_back*=term
        
        ## entropy of objects pixels
        ent_obj=0.0
        term=0.5/p2[it]
        for ih in range(it+1,256):
            ent_obj-=norm_hist[ih]*math.log(1.0-term*p2[ih])
        ent_obj*=term
        
        ## total entropy
        tot_ent=abs(ent_back-ent_obj)
        if (tot_ent<min_ent):
            min_ent=tot_ent
            threshold=it
            
    return threshold               

