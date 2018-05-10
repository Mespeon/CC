import cv2
import math
import numpy as np
import os

def runTest():
    hasEyes = bool
    image = cv2.imread('/home/marknolledo/CC/eyes/human/3.jpg')
    #for file in os.listdir('eyes/human'):
    #    filepath = '/'.join(['eyes/human', file])
    #    logText = ' '.join(['Reading image: ', filepath])
    #    print(logText)

    #Prepare Detection
    #image = cv2.imread(filepath)
    eyeCascade = cv2.CascadeClassifier('haarcascade_eye.xml')

    #Color Conversion
    imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    imageHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    imageHLS = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)

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
            #cv2.imshow('Canny', imageCanny)
            imageBlur = cv2.GaussianBlur(imageCanny, (7,7), 1)
            #cv2.imshow('Image Gaussian Blur', imageBlur)
            
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

            #Extract red
            lower = np.array([20,100,100], np.uint8)
            upper = np.array([45,255,255], np.uint8)

            #Thresh image
            threshedImg = cv2.inRange(scleraHSV, lower, upper)
            cv2.namedWindow('Color Ranging', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('Color Ranging', 500, 500)
            cv2.imshow('Color Ranging', threshedImg)

            #Slice image to iris level
            cropToIris = cropImage[y - rad: y + rad, x - rad: x + rad]
            irisHSV = cv2.cvtColor(cropToIris, cv2.COLOR_BGR2HSV)
            
            #Contour Features + Thresh + Canny
            canny = cv2.Canny(cropImage, 5, 5, apertureSize = 3)
            ret, thresh = cv2.threshold(canny, 127, 255, 0)
            _, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            #cv2.drawContours(cropToIris, contours, -1, (0, 255, 0), 1)
            print("Contour Tree returned: ", cv2.RETR_TREE)

            cv2.namedWindow('Image Test', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('Image Test', 500,500)
            cv2.imshow('Image Test', cropToSclera)

            cv2.namedWindow('Image Test, Iris', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('Image Test, Iris', 500,500)
            cv2.imshow('Image Test, Iris', irisHSV)
            
            print("Image SD: ", irisHSV.std())
            print("Image Mean: ", irisHSV.mean(), "\n")
            #print(cv2.calcHist(irisHSV, [1], None, [256], [0,256]))

            #Get Color Data
            #gs = cv2.cvtColor(cropToIris, cv2.COLOR_BGR2GRAY)
            #equalize = cv2.equalizeHist(gs)
            #recolor = cv2.cvtColor(equalize, cv2.COLOR_GRAY2BGR)
            hsvData = cv2.cvtColor(scleraHSV, cv2.COLOR_BGR2HSV)

            #cv2.namedWindow('Image Test, Histogram', cv2.WINDOW_NORMAL)
            #cv2.resizeWindow('Image Test, Histogram', 500,500)
            #cv2.imshow('Image Test, Histogram', recolor)

            h = hsvData[:,:,0]
            s = hsvData[:,:,1]
            v = hsvData[:,:,2]

            avgH = h.mean()
            avgS = s.mean()
            avgV = v.mean()
     
            print("Average Hue: ", avgH)
            print("Average Saturation: ", avgS)
            print("Average Value: ", avgV)
            print("Hues: \n", h, "\n")
            print("Saturations: \n", s, "\n")
            print("Values: \n", v, "\n")

            #Print coloration data
            red = np.uint8([[[0,0,255]]])
            green = np.uint8([[[0,255,0]]])
            blue = np.uint8([[[255,0,0]]])

            hsv_red = cv2.cvtColor(red, cv2.COLOR_BGR2HSV)
            hsv_green = cv2.cvtColor(green, cv2.COLOR_BGR2HSV)
            hsv_blue = cv2.cvtColor(blue, cv2.COLOR_BGR2HSV)

            #print("HSV Red Ceiling: ", hsv_red)
            #print("HSV Green Ceiling: ", hsv_green)
            #print("HSV Blue Ceiling: ", hsv_blue)

            #_, contours0, hierarchy0 = cv2.findContours(threshedImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            
            cv2.waitKey(0)
            
    else:
        print("Haar cascade detection failed. Attempting for manual localization... \n")
        kernel = np.ones((5, 5), np.uint8)
        imageCopy = image

        #Contouring
        grayscale = cv2.cvtColor(imageCopy, cv2.COLOR_BGR2GRAY)
        convertHSV = cv2.cvtColor(imageCopy, cv2.COLOR_BGR2HSV_FULL)
        convertHLS = cv2.cvtColor(imageCopy, cv2.COLOR_BGR2HLS)
        
        gaussBlur = cv2.GaussianBlur(grayscale, (5,5), 0)
        threshImage = cv2.adaptiveThreshold(gaussBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        ret, binaryImage = cv2.threshold(threshImage, 127, 255, cv2.THRESH_BINARY_INV)
        closingImage = cv2.morphologyEx(binaryImage, cv2.MORPH_CLOSE, kernel)
        
        _, contours, hierarchy = cv2.findContours(closingImage, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        cnt = contours[0]
        perimeter = cv2.arcLength(cnt,True)
        cnt = max(contours, key = lambda x: cv2.contourArea(x))
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(imageCopy, (x,y), (x+w, y+h), (255, 0, 255), 2)   #bounding box
        cv2.drawContours(imageCopy, cnt, -1, (0, 255, 0), 1)    #features detection

        #Crop image to bounding box
        if len(cnt) is not None:
            print("Eye localized. Cropping to area nearest to contour values. \n")
            cropImage = imageCopy[y:y+h, x:x+w]
            cropHSV = cv2.cvtColor(cropImage, cv2.COLOR_BGR2HSV_FULL)
            cropHLS = cv2.cvtColor(cropImage, cv2.COLOR_BGR2HLS)
        else:
            print("No viable eye found.")
            exit

        #Hough Transform for Iris Localization
        gaussianKernel = np.ones((5,5),np.uint8)
        imageCanny = cv2.Canny(cropHSV, 5, 70, apertureSize = 3)
        #cv2.imshow('Canny', imageCanny)
        imageBlur = cv2.GaussianBlur(imageCanny, (7,7), 1)
        #cv2.imshow('Image Gaussian Blur', imageBlur)

        #iris = cv2.HoughCircles(imageBlur, cv2.HOUGH_GRADIENT, 1.2, 1000, 100, 300)
        iris = cv2.HoughCircles(imageBlur, cv2.HOUGH_GRADIENT, 1.1, 900, 100, 400)
        if iris is not None:
            print("Iris detections at: \n", iris, "\n")
            iris = np.round(iris[0,:].astype('int'))
            for irisX, irisY, radius in iris:
                cv2.circle(cropImage, (irisX, irisY), radius, (0, 0, 255), 2)
                cv2.circle(cropImage, (irisX, irisY), 2, (255, 0, 255), 2)
                sclera = cv2.rectangle(cropImage, (irisX - irisY, irisY - radius), (irisX + irisY, irisY + radius), (255, 0, 0), 2)

        #Crop down again
        cropSecond = cropImage[irisY - radius: irisY + radius, irisX - irisY: irisX + irisY]
        secondHSV = cv2.cvtColor(cropSecond, cv2.COLOR_BGR2HSV)

        #Print coloration data
        #red = np.uint8([[[0,0,255]]])
        #green = np.uint8([[[0,255,0]]])
        #blue = np.uint8([[[255,0,0]]])

        #hsv_red = cv2.cvtColor(red, cv2.COLOR_BGR2HSV)
        #hsv_green = cv2.cvtColor(green, cv2.COLOR_BGR2HSV)
        #hsv_blue = cv2.cvtColor(blue, cv2.COLOR_BGR2HSV)

        #print("HSV Red Ceiling: ", hsv_red)
        #print("HSV Green Ceiling: ", hsv_green)
        #print("HSV Blue Ceiling: ", hsv_blue)
        
        cv2.namedWindow('Image Test, Non-Haar', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Image Test, Non-Haar', 500, 500)
        cv2.imshow('Image Test, Non-Haar', cropSecond)
        cv2.waitKey(0)
        
cv2.destroyAllWindows()
