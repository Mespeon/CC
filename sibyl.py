#OpenCV 2 HAAR Eye Cascade-based Eye Finder
#Eye Detection Script
#CURRENTLY ONLY USABLE IN PYTHON 3.4
#CANNOT BE LINKED TO GUI FOR NOW

#Version 1.0 - initial
#This script contains sources forked from OpenCV repo in Github.

import cv2
import numpy as np
import os

#List all files
for filename in os.listdir('eyes/cartoon'):
    file = filename
    filestring = '/'.join(['eyes/cartoon', file])
    print("Testing the following image:")
    print(filestring)
    
    #Cascade loading
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')  #HAAR Face Cascade
    eyeCascade = cv2.CascadeClassifier('haarcascade_eye.xml')   #HAAR Eye Cascade

    #Input
    testImage = cv2.imread(filestring)   #input image
    grayscaleThis = cv2.cvtColor(testImage, cv2.COLOR_BGR2GRAY) #load image in grayscale

    #Cascade running
    eyes = eyeCascade.detectMultiScale(grayscaleThis, 1.3, 5, minSize=(100, 100))
    for (x, y, w, h) in eyes:
        #Draw rectangle over every eye detected in image, if any
        find = cv2.rectangle(testImage, (x, y), (x + w, y + h), (255, 255, 0), 2)

    #Output
    cv2.namedWindow('Eye Detection', cv2.WINDOW_NORMAL) #declare window
    cv2.resizeWindow('Eye Detection', 600,600)  #resize window and image
    cv2.imshow('Eye Detection', testImage)  #show image and window

    cv2.waitKey(0)  #terminate key listening

cv2.destroyAllWindows() #terminate program
