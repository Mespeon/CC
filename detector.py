import cv2
import math
import numpy as np
import os

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import classifier as nb

def getImage(self):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    fileName, _ = QFileDialog.getOpenFileName(self, 'Open File', "", 'Image Files (*.jpg);;Image Files (*.jpeg);;Image Files (*.png)', options = options)
    if fileName:
        runTest(fileName)
    else:
        pass

def runTest(imageSrc):
    #hasEyes = bool

    #Prepare Detection
    image = cv2.imread(imageSrc)
    eyeCascade = cv2.CascadeClassifier('haarcascade_eye.xml')

    #Color Conversion
    imageHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV_FULL)

    #Detect Eyes
    detect = eyeCascade.detectMultiScale(imageHSV, 1.3, 5, minSize=(100,100))
    if len(detect) > 0:
        for x, y, w, h in detect:
            print("Eye detections at: \n", detect, "\n")
            eye = cv2.rectangle(image, (x,y), (x + w, y + h), (255, 255, 0), 2)
            # SET POSITION, WIDTH, AND HEIGHT OF DETECTED EYE/S
            X = detect[0,0]
            Y = detect[0,1]
            W = detect[0,2]
            H = detect[0,3]
                
            #Slice image to bounding box
            cropImage = image[y:y+h, x:x+w]
            #gsCrop = cv2.cvtColor(cropImage, cv2.COLOR_BGR2GRAY)    #Convert cropped image to GS

            #Hough Transform for Iris Localization
            gaussianKernel = np.ones((5,5),np.uint8)
            imageCanny = cv2.Canny(cropImage, 5, 70, apertureSize = 3)
            imageBlur = cv2.GaussianBlur(imageCanny, (7,7), 1)
            
            iris = cv2.HoughCircles(imageBlur, cv2.HOUGH_GRADIENT, 1.1, 900, 100, 400)
            
            if iris is not None:
                print("Iris detections at: \n", iris, "\n")
                iris = np.round(iris[0,:].astype('int'))
                for x, y, rad in iris:
                    #ir = cv2.circle(cropImage, (x, y), rad, (0, 0, 255), 2)
                    cv2.circle(cropImage, (x, y), 1, (255, 0, 255), 2)
                    #pupil = cv2.rectangle(cropImage, (x-y,y-rad), (x + y, y + rad), (255, 0, 0), 2)
                    #pupil = cv2.rectangle(cropImage, (x - rad,y - rad), (x + rad, y + rad), (255, 0, 0), 2)
                    
            #Slice image to sclera level
            cropToSclera = cropImage[y - rad: y + rad, x - y: x + y]
            scleraHSV = cv2.cvtColor(cropToSclera, cv2.COLOR_BGR2HSV)

            #Slice image to iris level
            cropToIris = cropImage[y - rad: y + rad, x - rad: x + rad]
            irisHSV = cv2.cvtColor(cropToIris, cv2.COLOR_BGR2HSV)

            #Image Windows
            cv2.namedWindow('Image Test', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('Image Test', 500,500)
            cv2.imshow('Image Test', cropToSclera)

            cv2.namedWindow('Image Test, Iris', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('Image Test, Iris', 500,500)
            cv2.imshow('Image Test, Iris', irisHSV)

            #Get Color Data
            hsvData = cv2.cvtColor(scleraHSV, cv2.COLOR_BGR2HSV)

            sd = '{:.2f}'.format(scleraHSV.std())
            mean = '{:.2f}'.format(scleraHSV.mean())
            h = hsvData[:,:,0]
            s = hsvData[:,:,1]
            v = hsvData[:,:,2]

            avgH = '{:.2f}'.format(h.mean())
            avgS = '{:.2f}'.format(s.mean())
            avgV = '{:.2f}'.format(v.mean())

            print("Image SD: ", sd)
            print("Image Mean: ", mean)
            print("Average Hue: ", avgH)
            print("Average Saturation: ", avgS)
            print("Average Value: ", avgV)

            print("Classifying...\n\n")
            nb.runClassify(float(sd),float(mean),float(avgH),float(avgS),float(avgV))

            cv2.waitKey(0)
            
    else:
        print("Haar cascade detection returned nothing. Attempting for manual localization... \n")
        kernel = np.ones((5, 5), np.uint8)
        imageCopy = image

        #Contouring
        grayscale = cv2.cvtColor(imageCopy, cv2.COLOR_BGR2GRAY)
        convertHSV = cv2.cvtColor(imageCopy, cv2.COLOR_BGR2HSV_FULL)
        
        gaussBlur = cv2.GaussianBlur(grayscale, (5,5), 0)
        threshImage = cv2.adaptiveThreshold(gaussBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        ret, binaryImage = cv2.threshold(threshImage, 127, 255, cv2.THRESH_BINARY_INV)
        closingImage = cv2.morphologyEx(binaryImage, cv2.MORPH_CLOSE, kernel)
        
        _, contours, hierarchy = cv2.findContours(closingImage, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        cnt = contours[0]
        perimeter = cv2.arcLength(cnt,True)
        cnt = max(contours, key = lambda x: cv2.contourArea(x))
        x, y, w, h = cv2.boundingRect(cnt)
        #cv2.rectangle(imageCopy, (x,y), (x+w, y+h), (255, 0, 255), 1)   #bounding box
        #cv2.drawContours(imageCopy, cnt, -1, (0, 255, 0), 1)    #features detection

        #Crop image to bounding box
        if len(cnt) is not None:
            print("Eye localized. Cropping to area nearest to contour values. \n")
            cropImage = imageCopy[y:y+h, x:x+w]
            cropHSV = cv2.cvtColor(cropImage, cv2.COLOR_BGR2HSV_FULL)
        else:
            print("No viable eye found.")
            exit

        #Hough Transform for Iris Localization
        gaussianKernel = np.ones((5,5),np.uint8)
        imageCanny = cv2.Canny(cropHSV, 5, 70, apertureSize = 3)
        imageBlur = cv2.GaussianBlur(imageCanny, (7,7), 1)

        iris = cv2.HoughCircles(imageBlur, cv2.HOUGH_GRADIENT, 1.1, 900, 100, 400)
        if iris is not None:
            print("Iris detections at: \n", iris, "\n")
            iris = np.round(iris[0,:].astype('int'))
            if iris.any():
                for irisX, irisY, radius in iris:
                    sclera = cv2.rectangle(cropImage, (irisX - irisY, irisY - radius), (irisX + irisY, irisY + radius), (255, 0, 0), 0)
            else:
                pass

        #Slice image to sclera level
        cropToSclera = cropImage[irisY - radius: irisY + radius, irisX - irisY: irisX + irisY]
        scleraHSV = cv2.cvtColor(cropToSclera, cv2.COLOR_BGR2HSV)

        #Slice image to iris level
        cropToIris = cropImage[irisY - radius: irisY + radius, irisX - radius: irisX + radius]
        irisHSV = cv2.cvtColor(cropToIris, cv2.COLOR_BGR2HSV)
        
        #Windows
        cv2.namedWindow('Image Test, Non-Haar', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Image Test, Non-Haar', 500, 500)
        cv2.imshow('Image Test, Non-Haar', cropToSclera)

        #Get Color Data
        hsvData = cv2.cvtColor(scleraHSV, cv2.COLOR_BGR2HSV)

        sd = '{:.2f}'.format(scleraHSV.std())
        mean = '{:.2f}'.format(scleraHSV.mean())
        h = hsvData[:,:,0]
        s = hsvData[:,:,1]
        v = hsvData[:,:,2]

        avgH = '{:.2f}'.format(h.mean())
        avgS = '{:.2f}'.format(s.mean())
        avgV = '{:.2f}'.format(v.mean())

        print("Image SD: ", sd)
        print("Image Mean: ", mean)
        print("Average Hue: ", avgH)
        print("Average Saturation: ", avgS)
        print("Average Value: ", avgV)

        print("Classifying...\n\n")
        nb.runClassify(float(sd),float(mean),float(avgH),float(avgS),float(avgV))

        cv2.waitKey(0)
        
    cv2.destroyAllWindows()
