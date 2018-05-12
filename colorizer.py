import cv2
import math
import numpy as np
import os

#Open premade text file
#dataSet = open('dataset.txt', 'r')
#dataSet.write("Hello World!\n")
#dataSet.write("Line 1\n")
#dataSet.write("Line 2\n")

lineWrites = int(1)

for file in os.listdir('/home/marknolledo/CC/training/cataract/negative/img'):
    filepath = '/'.join(['/home/marknolledo/CC/training/cataract/negative/img', file])
    print("Reading ", filepath, "\nExtracting color data...")

    #Read file
    image = cv2.imread(filepath)

    #Convert color
    toHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    #Print color data
    sd = toHSV.std()
    mean = toHSV.mean()

    h = toHSV[:,:,0]
    s = toHSV[:,:,1]
    v = toHSV[:,:,2]

    avgH = h.mean()
    avgS = s.mean()
    avgV = v.mean()

    disorder = str("Normal")

    #Format values
    sd2 = '{:.2f}'.format(sd)
    mean2 = '{:.2f}'.format(mean)
    avgH2 = '{:.2f}'.format(avgH)
    avgS2 = '{:.2f}'.format(avgS)
    avgV2 = '{:.2f}'.format(avgV)

    print("Image Standard Deviation: ", sd2)
    print("Image Mean: ", mean2)
    print("Average Hue: ", avgH2)
    print("Average Saturation: ", avgS2)
    print("Average Value: ", avgV2)
    print("\nWriting into dataset...")
    #lineJoin = ','.join([float(sd2), float(mean2), float(avgH2), float(avgS2), float(avgV2), disorder])
    #print(lineJoin, "\nWrite OK!\n\n")

    #Write into dataset
    with open('dataset.csv', 'a') as dataset:
        dataset.write(sd2)
        dataset.write(",")
        dataset.write(mean2)
        dataset.write(",")
        dataset.write(avgH2)
        dataset.write(",")
        dataset.write(avgS2)
        dataset.write(",")
        dataset.write(avgV2)
        dataset.write(",")
        dataset.write(disorder)
        dataset.write("\n")

    lineWrites+=1

print("Writing complete!\nLines written: ", lineWrites)
