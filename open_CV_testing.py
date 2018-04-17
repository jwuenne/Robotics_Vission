'''
Created on Aug 8, 2017

@author: jwuenne
'''
import numpy as np
import cv2

# Load an color image in grayscale
img = cv2.imread('cameraframe.jpg',0)
# show image
cv2.namedWindow('image', cv2.WINDOW_NORMAL)  # pre defined window will allow resizing
cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()



class VisionWindow:
    'common class for all Vision camera presentation windows'
    