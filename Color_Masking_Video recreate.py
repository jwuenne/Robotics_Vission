'''
Created on Aug 10, 2017

@author: jwuenne
'''

# This example will open a multiple windows and display sequential frames that represent the various manipulations to the image
# it also can identify the blue blocks on a sheet of paper and draw boundaries around them.
#  this is the main code for off season experimenting this file was duplicated at the start of 2018 challenge for season tracking   


import cv2
import numpy as np
import time
from _overlapped import NULL
 

cap = cv2.VideoCapture(0)   #Establishes "cap" as the source "aka  capture"

###################  Constant for Focal Length for distance measurement
FOCAL_LENGTH = 920.65
#OFFICE = True  # this is used to quickly change form Office camera to robot camera
OFFICE = False
CUBE = True

###### Declarations ###########################
 

    
    
def nothing(x): #used as a null function for trackbar()  need to satisfy trackbar function call
    pass

############### Set initial camera properties ######################################################################

cap.set(3,1280)     #Pixel Width  range (-2 to  1920)
cap.set(4,720)      #Pixel Height range (-2 to  1080)

###################  Exposure settings based on physical environment  ################################

if ( OFFICE == False ):
################### Robot Exposure settings ################################

    cap.set(cv2.CAP_PROP_EXPOSURE,-11)  #Exposure    range (-2 to  -11)
    cap.set(cv2.CAP_PROP_BRIGHTNESS,120)  #Brightness  range (0 to 255)
    cap.set(cv2.CAP_PROP_CONTRAST,128)  #Contrast  range (0 to 255)
    cap.set(cv2.CAP_PROP_SATURATION,120)  #Saturation  range (0 to 255)  0= B&W 255 gets more red
    cap.set(cv2.CAP_PROP_GAIN,0)  # 80% sure this is Gain   range (0 to 255)
    
    #Robot Green mask settings
    lowerHSV = [5,0,0]         
    upperHSV = [80,255,255]     
    lowerGreen = np.array([lowerHSV[0],lowerHSV[1],lowerHSV[2]])    # lower_Green = np.array([110,50,50])      experiment with different values
    upperGreen = np.array([upperHSV[0],upperHSV[1],upperHSV[2]])    # upper_Green = np.array([130,255,255])    experiment with different values
    

if ( OFFICE == True):
################### Office Exposure settings ################################
    cap.set(cv2.CAP_PROP_EXPOSURE,-7)   #Exposure    range (-2 to  -11)
    cap.set(cv2.CAP_PROP_BRIGHTNESS,150)  #Brightness  range (0 to 255)
    cap.set(cv2.CAP_PROP_CONTRAST,128)  #Contrast  range (0 to 255)
    cap.set(cv2.CAP_PROP_SATURATION,120)  #Saturation  range (0 to 255)  0= B&W 255 gets more red
    cap.set(cv2.CAP_PROP_GAIN,0)  # 80% sure this is Gain   range (0 to 255)
    
    #Robot Green mask settings
    lowerHSV = [60,0,0]         # values found using track bar controls.
    upperHSV = [82,146,77]      # values found using track bar controls.
    lowerGreen = np.array([lowerHSV[0],lowerHSV[1],lowerHSV[2]])    # lower_Green = np.array([110,50,50])      experiment with different values
    upperGreen = np.array([upperHSV[0],upperHSV[1],upperHSV[2]])    # upper_Green = np.array([130,255,255])    experiment with different values
    
   
if ( CUBE == True):
################### Office Exposure settings ################################
    cap.set(cv2.CAP_PROP_EXPOSURE,-10)   #Exposure    range (-2 to  -11)
    cap.set(cv2.CAP_PROP_BRIGHTNESS,141)  #Brightness  range (0 to 255)
    cap.set(cv2.CAP_PROP_CONTRAST,128)  #Contrast  range (0 to 255)
    cap.set(cv2.CAP_PROP_SATURATION,120)  #Saturation  range (0 to 255)  0= B&W 255 gets more red
    cap.set(cv2.CAP_PROP_GAIN,0)  # 80% sure this is Gain   range (0 to 255)
    
    #Robot Green mask settings
    lowerHSV = [27,0,0]         # values found using track bar controls.
    upperHSV = [32,250,250]      # values found using track bar controls.
    lowerGreen = np.array([lowerHSV[0],lowerHSV[1],lowerHSV[2]])    # lower_Green = np.array([110,50,50])      experiment with different values
    upperGreen = np.array([upperHSV[0],upperHSV[1],upperHSV[2]])    # upper_Gre
   
    
######################   Initialize values
_,frame = cap.read() #     Get a frame from the camera and collect information on frame size and center, not to assume a certain resolution setting   #######################
frameHeight = frame.shape[0]
frameWidth = frame.shape[1]
frameCenter_X = int(frameWidth/2)
frameCenter_Y = int(frameHeight/2)

#####  create locations for text that will scale with image resolution
distanceText_x = int (frameWidth*.5)
distanceText_y = int (frameHeight*.97)
frameRateText_x = int (frameWidth*.8)
frameRateText_y = int (frameHeight*.97)
targetOffsetText_x = int (frameWidth*.05)
targetOffsetText_y = int (frameHeight*.97)
boundRectText_x = int (frameWidth*.2)
boundRectText_y = int (frameHeight*.90)
    
###########        Establish variables for  camera track bars  ##############################
exposure = 0 - int(cap.get(cv2.CAP_PROP_EXPOSURE))     # convert exposure to a  positive for track bar, no negative values allowed in track bar
brightness = int(cap.get(cv2.CAP_PROP_BRIGHTNESS))
gain = int(cap.get(cv2.CAP_PROP_GAIN))



##################     Get a frame from the camera and Collect information on frame size and center   #######################
#_,frame = cap.read()
#frameHeight = frame.shape[0]
#frameWidth = frame.shape[1]
#frameCenter_X = int(frameWidth/2)
#frameCenter_Y = int(frameHeight/2)

###############################   Define and set position of 4 windows ##################################
 
cv2.namedWindow('HSV_frame',cv2.WINDOW_NORMAL)        # Set HSV View
cv2.moveWindow('HSV_frame',10,10)
cv2.resizeWindow('HSV_frame',711,400)
cv2.createTrackbar('Brightness','HSV_frame',brightness,255,nothing)
cv2.createTrackbar('Gain','HSV_frame',gain,255,nothing)
cv2.createTrackbar('Exposure','HSV_frame',exposure,11,nothing)

cv2.namedWindow('Mask_image',cv2.WINDOW_NORMAL)         # Set MASK View
cv2.moveWindow('Mask_image',721,10)
cv2.resizeWindow('Mask_image',711,400)

cv2.namedWindow('bit_And_image',cv2.WINDOW_NORMAL)         # Set bitAND  View
cv2.moveWindow('bit_And_image',10,410)
cv2.resizeWindow('bit_And_image',711,400)

cv2.namedWindow('contour_image',cv2.WINDOW_NORMAL)         # Set final  View
cv2.moveWindow('contour_image',721,410)
cv2.resizeWindow('contour_image',711,400)


cv2.namedWindow('HSV_controls',cv2.WINDOW_NORMAL)        # Set HSV controls View
cv2.moveWindow('HSV_controls',10,600)
cv2.resizeWindow('HSV_controls',1400,300)
cv2.createTrackbar('Lower H','HSV_controls',lowerHSV[0],110,nothing)
cv2.createTrackbar('lower S','HSV_controls',lowerHSV[1],255,nothing)
cv2.createTrackbar('lower V','HSV_controls',lowerHSV[2],255,nothing)

cv2.createTrackbar('Upper H','HSV_controls',upperHSV[0],110,nothing)
cv2.createTrackbar('Upper S','HSV_controls',upperHSV[1],255,nothing)
cv2.createTrackbar('Upper V','HSV_controls',upperHSV[2],255,nothing)

#################  Initialize variables used for calculating the approximate Frames Per Second (FPS)
fpsCount =1
fpsSum =0
framesPerSec = str(0)

##########  Define minimum and max aspect ratios for object identification
ratioMax = 5.2     #2.7
ratioMin = 4.0      #2.2


while(1):       # This is a simple continuous loop that recursively grabs frames from the system default camera.
    #########################################################
    t0 = time.time()    # Get starting time of loop
    #########################################################
    
    
    _, frame = cap.read()   # Read a BGR frame from the camera and store in "frame"
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)    # Convert BGR frame to HSV format so that you can more easily filter on a color

    # Apply Threshold to the HSV image to get only green colors, based on lower_green, upper_green
    mask = cv2.inRange(hsv, lowerGreen, upperGreen)
    
    # Bitwise-AND mask and original image and the green mask to get a final result that "only" has the green colors.
    res = cv2.bitwise_and(frame,frame, mask= mask)
    
    maskcopy = mask  #make a copy of mask, some documents suggest that the contours function changes the image that is passed. 
    image, contours, hierarchy = cv2.findContours(maskcopy,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)     # Find all contours in teh frame
    
    
    # Draw cross hairs at middle of frame for a reference point 
    frame = cv2.line(frame,(frameCenter_X-100,frameCenter_Y),(frameCenter_X+100,frameCenter_Y),(255,255,255),1)     # Draw  horizontal line
    frame = cv2.line(frame,(frameCenter_X,frameCenter_Y-100),(frameCenter_X,frameCenter_Y+100),(255,255,255),1)     # Draw vertical line
   
    
    if len(contours) >= 2:  # Avoid processing null contours, IMPORTANT since we are searching for at minimum 2 contours needs to be greater that "1" IE 2
        
      ####################### look for contours of interest and only work with them #################################
    
        areaArray = []          #  create blank list area for sort Clear List
                                #  Calculate the area of each contour and store in an array
        for i, c in enumerate(contours):
            area = cv2.contourArea(c)
            areaArray.append(area)
   
    # Zip the area array and the contours array together and then sort them from largest area to smallest area and place in sorted data array
        sorteddata = sorted(zip(areaArray, contours), key=lambda x: x[0], reverse=True)
        largestContour = sorteddata[0][1]           # First element is the largest
        secondLargestContour = sorteddata[1][1]     # 2nd is the next largest 
        
        #cv2.drawContours(frame, contours, -1, (255,0,0), 2)              # to Draw all contours us this
        cv2.drawContours(frame, largestContour, -1, (255,0,0), 3)         # Draw Largest  contour 
        cv2.drawContours(frame, secondLargestContour, -1, (255,0,0), 3)   # Draw second largest contour 
        
        
        (xg1,yg1,wg1,hg1) = cv2.boundingRect(largestContour)         # get bounding rectangle information for largest contour
        (xg2,yg2,wg2,hg2) = cv2.boundingRect(secondLargestContour)   # get bounding rectangle information for 2nd largest contour
        
                 
        #calculate  aspect ratio of Largest contour 
        aspect_ratio1 = float(wg1)/hg1

     
        # only calculate center and apply reticle if contour is believed to be validated (within ratioValues) 
        if (ratioMin <= aspect_ratio1 <= ratioMax):
                     
                     #################  Calculate center of contour and draw cross hairs on center of target
            centerOfTarget_X = int(xg1+wg1/2)
            centerOfTarget_Y = int(yg1+hg1/2)
            frame = cv2.circle(frame,(centerOfTarget_X,centerOfTarget_Y),20, (0,0,255), 1)  #  Draw a circle using center and radius of target
            frame = cv2.line(frame,(centerOfTarget_X-20,centerOfTarget_Y),(centerOfTarget_X+20,centerOfTarget_Y),(0,0,255),1)     # Draw a red horizontal line
            frame = cv2.line(frame,(centerOfTarget_X,centerOfTarget_Y-20),(centerOfTarget_X,centerOfTarget_Y+20),(0,0,255),1)     # Draw a red horizontal line
    
            #################  Calculate offset from center of frame to center of target  ###################
            targetOffset_X = centerOfTarget_X - frameCenter_X
            targetOffset_Y = frameCenter_Y - centerOfTarget_Y
                     
            #################  Print offset on frame  ###################
            targetOffset_str = "OffSet: "+str(targetOffset_X)+","+str(targetOffset_Y)
            cv2.putText(frame,targetOffset_str,(targetOffsetText_x,targetOffsetText_y), cv2.FONT_HERSHEY_SIMPLEX, 1.5,(255,255,255),2,cv2.LINE_AA)  # write offset to the processed frame
            
            #################  testing of distance calculation  ###################
            distance = round((4*FOCAL_LENGTH)/wg1,1)     #calculate the distance based on the width of the largest contour   
          
            distance_str = str(distance)+" in"
            cv2.putText(frame,distance_str,(distanceText_x,distanceText_y), cv2.FONT_HERSHEY_SIMPLEX, 1.5,(255,255,255),2,cv2.LINE_AA)         
                     
    
    
    ######################################################## get current positions of camera track bar's ###############################
    brightness = cv2.getTrackbarPos('Brightness','HSV_frame')
    gain = cv2.getTrackbarPos('Gain','HSV_frame')  
    exposure = 0-cv2.getTrackbarPos('Exposure','HSV_frame')#track bar is only positive
    
    # update camera settings with current track bar values 
    cap.set(cv2.CAP_PROP_EXPOSURE,exposure)  #Exposure    range (-2 to  -11)
    cap.set(cv2.CAP_PROP_BRIGHTNESS,brightness)  #Brightness  range (0 to 255)
    cap.set(cv2.CAP_PROP_GAIN,gain)  # Gain   range (0 to 255)
    
     ##########################################################  get current positions of HSV track bar's #################################
    lowerHSV[0] = cv2.getTrackbarPos('Lower H','HSV_controls')
    lowerHSV[1] = cv2.getTrackbarPos('Lower S','HSV_controls')  
    lowerHSV[2] = cv2.getTrackbarPos('Lower V','HSV_controls')
    upperHSV[0] = cv2.getTrackbarPos('Upper H','HSV_controls')
    upperHSV[1] = cv2.getTrackbarPos('Upper S','HSV_controls')  
    upperHSV[2] = cv2.getTrackbarPos('Upper V','HSV_controls')
    
    lowerGreen = np.array([lowerHSV[0],lowerHSV[1],lowerHSV[2]])   # update lower green based on track bars
    upperGreen = np.array([upperHSV[0],upperHSV[1],upperHSV[2]])    # update upper  green based on track bars
   
    
     ###########################################
    t1 = time.time()    # Get ending time for FPS  loop 
    ###########################################
    
    
    ##################################     manage FPS averaging 
    fpsSum = fpsSum + (t1-t0)
    if (fpsCount == 10 ):
        framesPerSec = "FPS:"+str(int(1/(fpsSum/10)))   #Calculate frames per sec., and convert to a string
        fpsCount = 0 # reset counter
        fpsSum = 0  #reset sum
    
    cv2.putText(frame,framesPerSec,(frameRateText_x,frameRateText_y), cv2.FONT_HERSHEY_SIMPLEX, 1.5,(255,255,255),2,cv2.LINE_AA)  # write FPS to the processed frame
   
    cv2.rectangle(frame, (xg1, yg1), (xg1+wg1, yg1+hg1), (0, 255, 0), 2) # draw bounding rectangle for largest contour
    cv2.rectangle(frame, (xg2, yg2), (xg2+wg2, yg2+hg2), (0, 255, 0), 2) # draw bounding rectangle for 2nd largest  contour
    
    boundRect_Str = 'Lrg_Rct =' + str(wg1)+"w X" + str(hg1)+"h, corner:" + str(xg1)+','+ str(yg1) # create string to write rectangle dimensions to screen
    
    cv2.putText(frame,boundRect_Str,(boundRectText_x,boundRectText_y), cv2.FONT_HERSHEY_SIMPLEX, 1.2,(0,255,0),2,cv2.LINE_AA) 
    #cv2.rectangle(frame, (xg1, yg1), (xg1+wg1, yg1+hg1), (0, 255, 0), 2) # draw bounding rectangle
    
    fpsCount =fpsCount+1 #increment  counter
    ##################################      end manage FPS averaging 
    
    
    
# show all images as video in while loop for troubleshooting only.
    
    cv2.imshow('Mask_image',mask)
    cv2.imshow('bit_And_image',res)
    cv2.imshow('contour_image',frame)
    cv2.imshow('HSV_frame',hsv)
  
  
   # areaArray = []              #create blank list area for sort  Clear List
     #order contours into an array by area
    #for i, c in enumerate(contours):
    #    area = cv2.contourArea(c)
   #     areaArray.append(area)
   
    # Zip the area array and the contours array together and then sort them  from largest area to smallest area and place in sorted data
   # sorteddata = sorted(zip(areaArray, contours), key=lambda x: x[0], reverse=True)
    
        
    # exit while loop using escape key
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()     # Best practice is to clean up all windows before exiting.



#print("framecenter =",frameCenter_X,frameCenter_Y)
#print(frame.shape)
#*******************************************************************************************************************************
# below is essentially the same work that is done above in the loop, but on a single frame (static) using the last frame from the while loop above
# i was just using this for learning...
#*******************************************************************************************************************************
#cv2.imshow('HSV-frame',hsv)
#cv2.imshow('Camera-frame',frame)
#cv2.imshow('Mask Image',mask)  # show final image
#cv2.imshow('Result of Applied Blue Mask to original image',res)
#maskcopy = mask  #make a copy of mask
#image, contours, hierarchy = cv2.findContours(maskcopy,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#cv2.drawContours(frame, contours, -1, (255,0,0), 2)
#res = cv2.resize(frame,(int(frameWidth/2),int(frameHeight/2)),interpolation = cv2.INTER_AREA)

cv2.imshow('Final Frame with contours',frame)

cv2.imwrite("fullframeforCalibration.jpg",frame)  #write to a file so we can analyze for calibration
#res =cv2.resize(frame,(int(frameWidth/3),int(frameHeight/3)), interpolation= cv2.INTER_AREA)   # reduce size of image to half the pixels in width and height.
#cv2.imwrite("smallframe.jpg",frame)
#cv2.imshow('resize of Frame with contours',res)

# focalLength = (wg*24)/5         #focal length calculated at 24in was determined to be 494.4
#distance = (5*494.4)/wg     #calculate the distance
if (len(contours) > 0):
    print("largest Area Contour:", sorteddata[0][0])
    distance = (5*494.4)/wg1     #calculate the distance
    print("Distance=",distance)
if (len(contours) >=1):
    print("2nd largest Area Contour:", sorteddata[1][0])
#print("Distance=",distance)
print("camera prop 0=",cap.get(0))
print("camera prop 1=",cap.get(1))
print("camera prop 2=",cap.get(2))
print("camera prop 3 (Pixel WIDTH) =",cap.get(3))
print("camera prop 4 (Pixel HEIGHT) =",cap.get(4))
print("camera prop 5=",cap.get(5))
print("camera prop 6=",cap.get(6))
print("camera prop 7=",cap.get(7))
print("camera prop 8=",cap.get(8))
print("camera prop 9=",cap.get(9))
print("camera prop 10 (BRIGHTNESS) =",cap.get(10))
print("camera prop 11 (CONTRAST) =",cap.get(11))
print("camera prop 12 (SATURATIO) =",cap.get(12))
print("camera prop 13=",cap.get(13))
print("camera prop 14 (GAIN) =",cap.get(14))
print("camera prop 15 (EXPOSURE) =",cap.get(15))
print("camera prop 16=",cap.get(16))
print("camera prop 17=",cap.get(17))
print("camera prop 18=",cap.get(18))
print("camera prop 19=",cap.get(19))
print("camera prop 20=",cap.get(20))

print("aspect_ratio1 = ",aspect_ratio1)



#print("largest  Contour:", sorteddata[0][1])
#print("contours:",contours)



k = cv2.waitKey(0) & 0xFF
if k == 27:
    cv2.destroyAllWindows()     # clean up after ESC key. Best practice is to clean up all windows before exiting.




