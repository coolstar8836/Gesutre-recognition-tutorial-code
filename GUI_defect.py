# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 12:27:38 2020

@author: rajku
"""

import tkinter;
from tkinter import ttk;
import cv2
import numpy as np
from PIL import Image, ImageTk


class GUI_defect:
    def __init__(self):
        self.Image_proc=None
        
        self.root=tkinter.Tk();
        self.frame=ttk.Frame(self.root,width=600,height=400).grid(columnspan=4,rowspan=4);
        
        self.label=ttk.Label(self.frame,text="test")
        
        #Gridding widgets for frame_1
        self.label.grid(row=0,column=0)
        #Bindings widgest for frame_1
        self.label.bind("<Button-1>",self.update)
        
        #Frame_2 start
        self.frame_2=ttk.Frame(self.root,width=300,height=200,relief=tkinter.RIDGE, borderwidth=2)
        self.frame_2.grid(rowspan=3,columnspan=3)
        #Buttons for frame_2
        self.btn_Bin=ttk.Button(self.frame_2,text="Add Output")
        
        #bindings for frame_2
        self.btn_Bin.bind("<Button-1>",self.add_hull)
        
        
        #gridding widgets for frame_2
        self.btn_Bin.grid(row=0,column=0)
        
        #Starting event feedback loop
        self.root.mainloop()
        
    def update(self,event):
        self.cap=cv2.VideoCapture(0)
        ret,img_arr=self.cap.read()
        self.Image_proc=img_arr
        cv2.imwrite("test.png", img_arr)
        load=Image.open("test.png")
        img_disp=ImageTk.PhotoImage(load)
        
        self.label.configure(text="",image=img_disp);
        self.label.image=img_disp
        
    def add_hull(self,event):
        img=self.Image_proc
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        #Converting the captured image to grayscale
        blur = cv2.GaussianBlur(gray,(5,5),0)
        #Some more processing
        ret,thresh1 = cv2.threshold(blur,70,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
        #Converted to binary image
        img2=img
        img2,contours, hierarchy = cv2.findContours(thresh1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        drawing = np.zeros(img.shape,np.uint8)
        #finding contours 
        max_area=0
       
        for i in range(len(contours)):
                cnt=contours[i]
                area = cv2.contourArea(cnt)
                if(area>max_area):
                    max_area=area
                    ci=i
        cnt=contours[ci]
        hull = cv2.convexHull(cnt)
        moments = cv2.moments(cnt)
        if moments['m00']!=0:
                    cx = int(moments['m10']/moments['m00']) # cx = M10/M00
                    cy = int(moments['m01']/moments['m00']) # cy = M01/M00
                  
        centr=(cx,cy)       
        cv2.circle(img,centr,5,[0,0,255],2)       
         
              
        cnt = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
        hull = cv2.convexHull(cnt,returnPoints = False)
        
        #always true if condition
        if(1):
            defects = cv2.convexityDefects(cnt,hull)
            mind=0
            maxd=0
 
            for i in range(defects.shape[0]):
                s,e,f,d = defects[i,0]
                start = tuple(cnt[s][0])
                end = tuple(cnt[e][0])
                far = tuple(cnt[f][0])
                dist = cv2.pointPolygonTest(cnt,centr,True)
                cv2.line(img,start,end,[0,255,0],2)
                cv2.circle(img,far,5,[0,0,255],-1)
                
            print(i)
            i=0
        cv2.imwrite("test.png",img)
        load=Image.open("test.png")
        img_disp=ImageTk.PhotoImage(load)
        self.label.configure(image=img_disp)
        self.label.image=img_disp

        
defect=GUI_defect()
        