'''
Created on Aug 10, 2017

@author: jwuenne
'''

import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread('photo.jpg',1) # 0 = B&W


img = cv2.line(img,(0,0),(890,890),(255,0,0),5)     # Draw a diagonal blue line with thickness of 5 px

img = cv2.circle(img,(450,450), 50, (255,0,0), -1)  #  Draw a circle using center and radius
cv2.imwrite('ninja.jpg',img)                        # Save image with added graphics as a new JPG file
 
img_ninja = cv2.imread('ninja.jpg',1)  #load ninja.jpg file  image with added  graphics
 
 # Convert BGR to HSV
hsv = cv2.cvtColor(img_ninja, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
lower_blue = np.array([110,50,50])
upper_blue = np.array([130,255,255])

    # Threshold the HSV image to get only blue colors
mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Bitwise-AND mask and original image
res = cv2.bitwise_and(img_ninja,img_ninja, mask=mask)

##contours, hierarchy = cv2.findContours(res,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

cv2.imshow('frame',img_ninja)
cv2.imshow('bluemask',mask)
cv2.imshow('bitwise',res)

cv2.waitKey(0)
cv2.destroyAllWindows()



plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
#plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
plt.show()
print (img.shape) #returns a tuple of number of rows, columns and channels (if image is color):



