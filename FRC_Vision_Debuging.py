'''
Created on Dec 14, 2017

@author: jwuenne
'''


import numpy as np
import cv2
from matplotlib import pyplot as plt

def nothing(x):
    pass

img = cv2.imread('fullframeforCalibration.jpg',1) # 0 = B&W

# trial window class
class VisionWindow:
    'common class for all Vision camera presentation windows'
    brightness = 0
    contrast = 0
    exposure = 0
    saturation = 0
    gain = 0
    
    
    
    

#img = cv2.line(img,(0,0),(890,890),(255,0,0),5)     # Draw a diagonal blue line with thickness of 5 px

#img = cv2.circle(img,(450,450), 50, (255,0,0), -1)  #  Draw a circle using center and radius

                                #adding text
#font = cv2.FONT_HERSHEY_SIMPLEX
#cv2.putText(img,'OpenCV',(300,350), font, 4,(255,255,255),2,cv2.LINE_AA)
 

#plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
#plt.xticks([]), plt.yticks([])          # to hide tick values on X and Y axis
#plt.show()
#print (img.shape) #returns a tuple of number of rows, columns and channels (if image is color):

red=50
green=100
blue=200

cv2.namedWindow('image', cv2.WINDOW_NORMAL)  # pre defined window will allow resizing

# create trackbars for color change
cv2.createTrackbar('R','image',red,255,nothing)
cv2.createTrackbar('G','image',green,255,nothing)
cv2.createTrackbar('B','image',blue,255,nothing)


cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()




