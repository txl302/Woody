import cv2
import socket
import numpy
import threading
import os
import time

import json

from Woody_motion import Woody_motion as Wm
from Woody_network import Woody_network as Wn


import numpy as np

import itertools

import pypot.dynamixel

import threading
from random import randint

face_cascade = cv2.CascadeClassifier('Woody_vision/haarcascade_frontalface_alt.xml')
rectangleColor = (0,165,255)  

cap = cv2.VideoCapture(0)
res_w = 320
res_h = 240
cap.set(3,res_w);
cap.set(4,res_h);

a = 0
b = 0

move1 = 0.0
move2 = 0.0

flag_s = 0
flag_n = 0


def vision():
    global a
    global b

    global flag_s

    while True:

        ret, img = cap.read()

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        maxArea = 0  
        x = 0  
        y = 0  
        w = 0  
        h = 0

        for (_x,_y,_w,_h) in faces:
            if _w*_h > maxArea:
                x = _x
                y = _y
                w = _w
                h = _h
                maxArea = w*h
        if maxArea > 0:
            cv2.rectangle(img,(x,y),(x+w,y+h),rectangleColor,4)
            a = x+w/2 - res_w/2
            b = y+h/2 - res_h/2

            flag_s = 1
     
        cv2.imshow('img',img)
        k = cv2.waitKey(20) & 0xff
        if k == 27:
            break

def motion():

    global a
    global b

    global flag_s
    global flag_n

    current_pos_1 = Wm.get_present_position((1,))
    current_pos_2 = Wm.get_present_position((2,))
    print(current_pos_1)
    while True:
        if(flag_s == 1):

            current_pos_1 = Wm.get_present_position((1,))
            current_pos_2 = Wm.get_present_position((2,))

            current_pos_1 = current_pos_1[0]
            current_pos_2 = current_pos_2[0]

            if(a < -30):
                current_pos_1 = current_pos_1 + 2
            if(a > 30):
                current_pos_1 = current_pos_1 - 2
            #if(b < -30):
                #current_pos_2 = current_pos_2 - 1
            #if(b > 30):
                #current_pos_2 = current_pos_2 + 1
                
            Wm.move_to([1, ], [current_pos_1, ])

            flag_s = 0

##            if(b < -30):
##                current_pos_1 = current_pos_1 - 4
##            if(b > 30):
##                current_pos_1 = current_pos_1 + 4
##                
##            Wm.move_to([1,2], [current_pos_1,current_pos_2])

        elif((flag_s == 0) & (flag_n == 1)):
            current_pos_1 = Wm.get_present_position((1,))
            current_pos_2 = Wm.get_present_position((2,))

            current_pos_1 = current_pos_1[0]
            current_pos_2 = current_pos_2[0]

            if(a_n < -30):
                current_pos_1 = current_pos_1 + 4
            if(a_n > 30):
                current_pos_1 = current_pos_1 - 4
            #if(b < -30):
                #current_pos_2 = current_pos_2 - 1
            #if(b > 30):
                #current_pos_2 = current_pos_2 + 1
                
            Wm.move_to([1, ], [current_pos_1, ])

            flag_n = 0

##            if(b < -30):
##                current_pos_1 = current_pos_1 - 4
##            if(b > 30):
##                current_pos_1 = current_pos_1 + 4
##                
##            Wm.move_to([1,2], [current_pos_1,current_pos_2])
                
     
        flag_s = 0
        time.sleep(0.02)

def network_s():
    global flag_n

    global a
    global b

    while True:
        while(flag_s == 1):
            data = [a, b]
            print(data)
            Wn.sendto_Rin(data)
            

            time.sleep(0.02)

def network_r():
    global flag_n

    global a_n
    global b_n

    while True:

        data = Wn.recefrom_Rin()

        flag_n = 1

        a_n = data[0]
        b_n = data[1]

        time.sleep(0.02)

def server_test():    
    while True:

        ret, img = cap.read()
     
        cv2.imshow('img',img)

        Rn.sendto_Server_img(img)
        k = cv2.waitKey(20) & 0xff
        if k == 27:
            break


def main():
    thre_v = threading.Thread(target = vision)
    thre_m = threading.Thread(target = motion)

    thre_ns = threading.Thread(target = network_s)

    thre_v.start()
    thre_m.start()
    thre_ns.start()  
    

	
if __name__ == '__main__':

    server_test()
