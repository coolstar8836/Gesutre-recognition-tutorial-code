# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 22:51:42 2020

@author: rajku
"""


import tkinter;
from tkinter import ttk;
import cv2
import numpy
from PIL import Image, ImageTk

'''

GUI window template

1)Control input image transformation window
will contain buttons to launch new windows showing 
binary ,grayscale,and original

2)Drawing control Window

Control whether to show the convex hull , or the defects 


1) 
Create a window using tkinter
create  3 buttons
use grid() to align
use pack() 
Create three command functions



'''


'''
I am thinking of making a main window and then launching two 
windows separately one at at time (maybe )
one to just make it black and white 
and other to add convex hull and dots.
'''


'''
This below class is to show binary transformation of captured image
'''

class GUI_test:
    
    '''
    This below function is just to initialize stuff and start the main
    windows
    '''
    def __init__(self):
        #Some internal variables
        self.bin_flag=1
        self.set_bin_flag=cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU
        
        self.root=tkinter.Tk();
        self.frame=ttk.Frame(self.root,width=600,height=400).grid(columnspan=4,rowspan=4);
        #self.image_disp=tkinter.PhotoImage("test.png")
        self.frame_2=ttk.Frame(self.root,width=300,height=200,relief=tkinter.RIDGE, borderwidth=2)
        self.Image_proc=None
        self.frame_2.grid(rowspan=3,columnspan=3)
        #Buttons for frame_2
        self.btn_Bin=ttk.Button(self.frame_2,text="Make Binary")
        #self.btn_Bin=ttk.Button(self.frame_2,text="Add convex hull ")
        self.btn_switch=ttk.Button(self.frame_2,text="Switch Black and white")
        
        #self.btn_Bin=ttk.Button(self.frame_2,text="Add center defects")
        #bindings for frame_2
        self.btn_Bin.bind("<Button-1>",self.binary)
        self.btn_Bin.grid(row=0,column=0)
        self.btn_switch.bind("<Button-1>",self.Switch_bin)
        self.btn_switch.grid(row=1,column=0)
        self.cap=None
        self.label=ttk.Label(self.frame,text="test")
        self.label.bind("<Button-1>",self.update)
        self.button=ttk.Button(self.frame,text="Exit")
        self.button.bind("<Button-1>",self.close)
        self.button.grid(row=3,column=0)
        self.label.grid(row=0,column=0)
        
        self.root.mainloop()
        
        '''
        This below function is to capture a image from webcam
        and convert it into a format that can be displayed on the 
        window
        '''
        
    def update(self,event):
        self.cap=cv2.VideoCapture(0)
        ret,img_arr=self.cap.read()
        self.Image_proc=img_arr
        cv2.imwrite("test.png", img_arr)
        load=Image.open("test.png")
        img_disp=ImageTk.PhotoImage(load)
        
        self.label.configure(text="",image=img_disp);
        self.label.image=img_disp
        #self.label.place(x=0,y=0)
        
        
        
        '''
        This below function is to trigger conversation into a binary 
        image from the original colour and display it in the label
        
        '''
        
        
    def binary(self,event):
        gray = cv2.cvtColor(self.Image_proc,cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray,(5,5),0)
        ret,thresh1 = cv2.threshold(blur,70,255,self.set_bin_flag)
        cv2.imwrite("test.png", thresh1)
        load=Image.open("test.png")
        img_disp=ImageTk.PhotoImage(load)
        self.label.configure(image=img_disp)
        self.label.image=img_disp
        

    '''
    The below function is to switch between black and white 
    whenever is necessary based on the background 
    because if for some reason I can't control whether my hand 
    is painted white or black it will be useful for getting output and
    demo
    '''
    def Switch_bin(self,event):
        
        if(self.bin_flag==1):
            self.set_bin_flag=cv2.THRESH_OTSU
            self.bin_flag=0
        elif self.bin_flag==0:
            self.set_bin_flag=cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU
            self.bin_flag=1
        
        
        
        
    def close(self,event):
        while(self.cap.isOpened()):
            self.cap.release()





'''
This class below is to add convex hull and defects to image
'''

class GUI_defect:
    def __init__(self):
        self.root=tkinter.Tk();
        self.frame=ttk.Frame(self.root,width=600,height=400).grid(columnspan=4,rowspan=4);
        #self.image_disp=tkinter.PhotoImage("test.png")
        self.frame_2=ttk.Frame(self.root,width=300,height=200,relief=tkinter.RIDGE, borderwidth=2)
        self.Image_proc=None
        self.frame_2.grid(rowspan=3,columnspan=3)
        #Buttons for frame_2
        #self.btn_Bin=ttk.Button(self.frame_2,text="Make Binary")
        self.btn_Bin=ttk.Button(self.frame_2,text="Add convex hull ")
        

defect=GUI_defect()

#The reason why it was showing that early error was 
#that after mainloop is started ,it will check for events
#but i guess it must be builtin that to check if the loop is either
#have not run or something like that,its not related to Tk() alone
#so thats why I am going to try another approach


