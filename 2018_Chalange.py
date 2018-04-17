'''
Created on Jan 6, 2018

@author: JWuenne
'''
from matplotlib.cbook import Null


'''
Created on Aug 10, 2017

@author: jwuenne
'''

# This example will open a multiple windows and display sequential frames that represent the various manipulations to the image
# it also can identify the blue blocks on a sheet of paper and draw boundaries around them. 


import cv2
import numpy as np
import time
from _overlapped import NULL
 

cap = cv2.VideoCapture(0)   #Establishes "cap" as the source "aka  capture"

###################  Constant for Focal Length for distance measurement
FOCAL_LENGTH = 920.65


location = 'OFFICE'
#location = 'ROBOT'
#location = 'CUBE'

###### Declarations ###########################

   
    
def nothing(x): #used as a null function for trackbar(), need to satisfy trackbar function call
    pass


def find_Switch_Contours(contours):
    'Searches the list of contours and finds the left and right switch contours '

    areaArray = []          #  create blank list area for sort 
                                
    for i, c in enumerate(contours):    #  Calculate the area of each contour and store the areas in an array
        area = cv2.contourArea(c)
        areaArray.append(area)
   
    # Zip the area array and the contours array together and then sort them from largest area to smallest area and place in sorted data array
    sorteddata = sorted(zip(areaArray, contours), key=lambda x: x[0], reverse=True)
    #largestContour = sorteddata[0][1]           # First element is the largest
    #secondLargestContour = sorteddata[1][1]     # 2nd is the next largest 
    
    #search through the sorted list and find the 2 contours that match the shape of the target
    targetContours = [] # Define list for target contours
    count = 0 # counter to know when to stop looking, when 2 are found
                
    for i, c in enumerate(sorteddata):              # search through the sorted list until 2 matching contours are found.
        if count == 0 :
            (xg,yg,wg,hg) = cv2.boundingRect(c[1])  # Get the rectangle information from the element c[1] so the aspect ratio can be calculated
            aspectRatio = float(wg)/hg
            extent = c[0] / (wg*hg)                 # calculate extent of contour using the area (c[0]) from the sorted array
            if (ratioMin <= aspectRatio <= ratioMax): # and (extentMin <= extent <= extentMax)):
                targetContours.append(c[1])             #if the contour matches the aspect ratio that you are looking for then append it to the list of identified contours
                count +=1                               #increment the counter if the aspect ratio matches
        elif count == 1 :
            (xg,yg,wg,hg) = cv2.boundingRect(c[1])  # Get the rectangle so aspect ratio can be calculated
            aspectRatio = float(wg)/hg
            extent = c[0] / (wg*hg)                 # calculate extent of contour using the area from the sorted array
                                                    # now you could make sure angles are similar to insure objects are parallel to each other have more confidence in the numbers
            if (ratioMin <= aspectRatio <= ratioMax): # and (extentMin <= extent <= extentMax)):
                targetContours.append(c[1])
                count +=1       
        elif count > 1 :  # stop iterating on the list of contours because 2 were found.
            break
                        
    if count > 1 :          # if the count is less  than 1 then 2 contours that match the criteria were not found  go to the bottom and return null.
                                
        largestContour = targetContours[0]          # First element is the largest
        secondLargestContour = targetContours[1]
        
        #   Get bounding rectangles on both contours so we can determine which one is on the left and which i son the right.      
        (xg1,yg1,wg1,hg1) = cv2.boundingRect(largestContour)         # get bounding rectangle information for largest contour
        (xg2,yg2,wg2,hg2) = cv2.boundingRect(secondLargestContour)   # get bounding rectangle information for 2nd largest contour
        
        ### determine which of the 2 largest contours is left marker and which is right marker
        if xg1 > xg2 :                      # largest contour is the right marker
            rightContour = largestContour
            leftContour =  secondLargestContour 
            
        else:
            leftContour = largestContour
            rightContour =  secondLargestContour
            
               
        return (leftContour, rightContour,True)
    
    elif (count <= 1):
        return(Null, Null,False)  # if 2 contours were not found then return Null value

    ######################### End of Find switch contour function #############################




############### Set initial camera properties ######################################################################

cap.set(3,1280)     #Pixel Width  range (-2 to  1920)
cap.set(4,720)      #Pixel Height range (-2 to  1080)

###################  Exposure settings based on physical environment  ################################

if ( location == 'ROBOT' ):   ################### Robot Exposure settings ################################
    cap.set(cv2.CAP_PROP_EXPOSURE,-11)  #Exposure    range (-2 to  -11)
    cap.set(cv2.CAP_PROP_BRIGHTNESS,70)  #Brightness  range (0 to 255)
    cap.set(cv2.CAP_PROP_CONTRAST,128)  #Contrast  range (0 to 255)
    cap.set(cv2.CAP_PROP_SATURATION,120)  #Saturation  range (0 to 255)  0= B&W 255 gets more red
    cap.set(cv2.CAP_PROP_GAIN,0)  # 80% sure this is Gain   range (0 to 255)
    
    # assign Robot Green mask settings
    lowerHSV = [50,0,0]         
    upperHSV = [70,255,166]     
    lowerGreen = np.array([lowerHSV[0],lowerHSV[1],lowerHSV[2]])    # lower_Green = np.array([110,50,50])      experiment with different values
    upperGreen = np.array([upperHSV[0],upperHSV[1],upperHSV[2]])    # upper_Green = np.array([130,255,255])    experiment with different values
    
elif (location == 'OFFICE'):   ################# Office Exposure settings ################################
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
    
   
elif ( location == 'CUBE'):    ################### Office Exposure settings ################################
    cap.set(cv2.CAP_PROP_EXPOSURE,-10)   #Exposure    range (-2 to  -11)
    cap.set(cv2.CAP_PROP_BRIGHTNESS,141)  #Brightness  range (0 to 255)
    cap.set(cv2.CAP_PROP_CONTRAST,128)  #Contrast  range (0 to 255)
    cap.set(cv2.CAP_PROP_SATURATION,120)  #Saturation  range (0 to 255)  0= B&W 255 gets more red
    cap.set(cv2.CAP_PROP_GAIN,0)  # 80% sure this is Gain   range (0 to 255)
    
    #Robot yellow mask settings
    lowerHSV = [21,0,0]         # values found using track bar controls.
    upperHSV = [37,250,250]      # values found using track bar controls.
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
extentText_x = int (frameWidth*.1)
extentText_y = int (frameHeight*.1)
    
###########        Establish variables for  camera track bars  ##############################
exposure = 0 - int(cap.get(cv2.CAP_PROP_EXPOSURE))     # convert exposure to a  positive for track bar, no negative values allowed in track bar
brightness = int(cap.get(cv2.CAP_PROP_BRIGHTNESS))
gain = int(cap.get(cv2.CAP_PROP_GAIN))


###############################   Define and set position of 4 windows ##################################
 
cv2.namedWindow('HSV_frame',cv2.WINDOW_NORMAL)        # Set HSV View, upper left and create track bars in window
cv2.moveWindow('HSV_frame',10,10)
cv2.resizeWindow('HSV_frame',711,400)
cv2.createTrackbar('Brightness','HSV_frame',brightness,255,nothing)
cv2.createTrackbar('Gain','HSV_frame',gain,255,nothing)
cv2.createTrackbar('Exposure','HSV_frame',exposure,11,nothing)

cv2.namedWindow('Mask_image',cv2.WINDOW_NORMAL)        # Set MASK View, upper right
cv2.moveWindow('Mask_image',721,10)
cv2.resizeWindow('Mask_image',711,400)

cv2.namedWindow('bit_And_image',cv2.WINDOW_NORMAL)     # Set bitAND  View, lower left
cv2.moveWindow('bit_And_image',10,410)
cv2.resizeWindow('bit_And_image',711,400)

cv2.namedWindow('contour_image',cv2.WINDOW_NORMAL)     # Set final  View, lower right
cv2.moveWindow('contour_image',721,410)
cv2.resizeWindow('contour_image',711,400)


cv2.namedWindow('HSV_controls',cv2.WINDOW_NORMAL)      # Set HSV controls View, bottom center and create track bars in window
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
ratioMax = 0.33     # 0.2 # Estimate of potential skew from vertical
ratioMin = 0.12     # tape width / tape height 2/15.3  minus a little for tolerance  
extentMax = 1.0     # extent is the ratio of the bounding 
extentMin = 0.75



while(1):   ############ This is a simple continuous loop that recursively grabs frames from the system default camera.
                    #########################################################
    t0 = time.time()    # Get starting time of loop used for FSP approximation
                    #########################################################
    
    _, frame = cap.read()   # Read a BGR frame from the camera and store in "frame"
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)    # Convert BGR frame to HSV format so that you can more easily filter on a color

    # Apply Threshold to the HSV image to get only green colors, based on lower_green, upper_green
    mask = cv2.inRange(hsv, lowerGreen, upperGreen)
    
    # Bitwise-AND mask and original image and the green mask to get a final result that "only" has the green colors.
    #res = cv2.bitwise_and(frame,frame, mask= mask)
    
    maskcopy = mask  # make a copy of mask,  documents suggest that the contours function changes the image that is passed. 
    image, contours, hierarchy = cv2.findContours(maskcopy,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)     # Find all contours in the frame
    
    
    # Draw cross hairs at middle of frame for a reference point 
    frame = cv2.line(frame,(frameCenter_X-100,frameCenter_Y),(frameCenter_X+100,frameCenter_Y),(255,255,255),1)     # Draw  horizontal line
    frame = cv2.line(frame,(frameCenter_X,frameCenter_Y-100),(frameCenter_X,frameCenter_Y+100),(255,255,255),1)     # Draw vertical line
   
    
    if len(contours) >= 2:  # Avoid processing null contours, IMPORTANT since we are searching for at minimum 2 contours needs to be greater that "1" IE 2
        
        ############# search through all of the contours  and find the ones you want to work with them #################
        leftContour,rightContour,targetSuccess = find_Switch_Contours(contours)
        
        if (targetSuccess == True):
            (xgL,ygL,wgL,hgL) = cv2.boundingRect(leftContour)  # get bounding rectangle information for left contour
            (xgR,ygR,wgR,hgR) = cv2.boundingRect(rightContour)   # get bounding rectangle information for 2nd right  contour          
                        
            # calculate Object Extents so they can be displayed in the screen
            areaLeftContour = cv2.contourArea(leftContour)
            areaRightContour = cv2.contourArea(rightContour)
            extentLeft = float(areaLeftContour) / (wgL*hgL)  # extent of left contour
            extentRight = float(areaRightContour) / (wgR*hgR)  # extent of left contour
              
            #calculate  aspect ratio of Left contour 
            aspect_ratioLeft = float(wgL)/hgL
            aspect_ratioRight = float(wgR)/hgR        
                         
            #cv2.drawContours(frame, contours, -1, (255,0,0), 2)              # to Draw all contours us this
            cv2.drawContours(frame, leftContour, -1, (255,0,0), 3)         # Draw Left  contour 
            cv2.drawContours(frame, rightContour, -1, (255,0,0), 3)        # Draw Right contour 
            #cv2.drawContours(frame, approxContour, -1, (255,0,0), 3)        # Draw Right contour 
            
            
            # only calculate center and apply reticle if contour is believed to be validated (within ratioValues) 
            #if ((ratioMin <= aspect_ratioLeft <= ratioMax) and (ratioMin <= aspect_ratioRight <= ratioMax)):
                         
            #################  Calculate center of overall target (both contours) and draw cross hairs on center of target
            centerOfTarget_X = int(xgL + (xgR+wgR-xgL)/2)
            centerOfTarget_Y = int(ygL + hgL/2) 
            
            #draw reticals
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
            distance = round((4*FOCAL_LENGTH)/wgL,1)     #calculate the distance based on the width of the largest contour   
            distance_str = str(distance)+" in"
            cv2.putText(frame,distance_str,(distanceText_x,distanceText_y), cv2.FONT_HERSHEY_SIMPLEX, 1.5,(255,255,255),2,cv2.LINE_AA)
            
            #################  Create string for displaying the Extent calculations
            extent_str = 'LE={0:.3f} RE={1:.3f}'.format(extentLeft,extentRight)
            #extent_str = 'LE'+str(extentLeft)+',  RE'+str(extentRight)
            cv2.putText(frame,extent_str,(extentText_x,extentText_y), cv2.FONT_HERSHEY_SIMPLEX, 1.2,(255,255,255),2,cv2.LINE_AA)
            
    
    ################################################ get current positions of camera track bar's ###############################
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
        
    fpsCount =fpsCount+1 #increment  counter
    
    cv2.putText(frame,framesPerSec,(frameRateText_x,frameRateText_y), cv2.FONT_HERSHEY_SIMPLEX, 1.5,(255,255,255),2,cv2.LINE_AA)  # write FPS to the processed frame
   
    #cv2.rectangle(frame, (xgL, ygL), (xgL+wgL, ygL+hgL), (0, 255, 0), 2) # draw bounding rectangle for Left contour
    #cv2.rectangle(frame, (xgR, ygR), (xgR+wgR, ygR+hgR), (0, 255, 0), 2) # draw bounding rectangle for Right  contour
    if targetSuccess == True:
        # create string to write rectangle dimensions to screen
        boundRect_Str = 'LEFT_Rct =' + str(wgL)+"w X" + str(hgL)+"h, corner:" + str(xgL)+','+ str(ygL) 
        #  write rectangle dimensions to screen
        cv2.putText(frame,boundRect_Str,(boundRectText_x,boundRectText_y), cv2.FONT_HERSHEY_SIMPLEX, 1.2,(0,255,0),2,cv2.LINE_AA) 
    
        cv2.rectangle(frame, (xgL, ygL), (xgR+wgR, ygR+hgR), (0, 255, 0), 2) # draw bounding rectangle
    
   
    ##################################      end manage FPS averaging 
    
    
    
# show all images as video in while loop for troubleshooting only.
    
    cv2.imshow('Mask_image',mask)
    #cv2.imshow('bit_And_image',res)
    cv2.imshow('contour_image',frame)
    cv2.imshow('HSV_frame',hsv)
  
          
    # exit while loop using escape key
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()     # Best practice is to clean up all windows before exiting.






cv2.imshow('Final Frame with contours',frame)

cv2.imwrite("fullframeforCalibration.jpg",frame)  #write to a file so we can analyze for calibration
#res =cv2.resize(frame,(int(frameWidth/3),int(frameHeight/3)), interpolation= cv2.INTER_AREA)   # reduce size of image to half the pixels in width and height.
#cv2.imwrite("smallframe.jpg",frame)
#cv2.imshow('resize of Frame with contours',res)

# focalLength = (wg*24)/5         #focal length calculated at 24in was determined to be 494.4
#distance = (5*494.4)/wg     #calculate the distance
#if (len(contours) > 0):
    #print("Left  Contour:", sorteddata[0][0])
    #distance = (5*494.4)/(wg1)    #calculate the distance
    #print("Distance=",distance)
#if (len(contours) >=1):
    #print("2nd largest Area Contour:", sorteddata[1][0])
#print("Distance=",distance)
#print("camera prop 0=",cap.get(0))
#print("camera prop 1=",cap.get(1))
#print("camera prop 2=",cap.get(2))
#print("camera prop 3 (Pixel WIDTH) =",cap.get(3))
#print("camera prop 4 (Pixel HEIGHT) =",cap.get(4))
#print("camera prop 5=",cap.get(5))
#print("camera prop 6=",cap.get(6))
#print("camera prop 7=",cap.get(7))
#print("camera prop 8=",cap.get(8))
#print("camera prop 9=",cap.get(9))
#print("camera prop 10 (BRIGHTNESS) =",cap.get(10))
#print("camera prop 11 (CONTRAST) =",cap.get(11))
#print("camera prop 12 (SATURATIO) =",cap.get(12))
#print("camera prop 13=",cap.get(13))
#print("camera prop 14 (GAIN) =",cap.get(14))
#print("camera prop 15 (EXPOSURE) =",cap.get(15))
#print("camera prop 16=",cap.get(16))
#print("camera prop 17=",cap.get(17))
#print("camera prop 18=",cap.get(18))
#print("camera prop 19=",cap.get(19))
#print("camera prop 20=",cap.get(20))

#print("aspect_ratio Left = ",aspect_ratioLeft)
#print("aspect_ratio Right = ",aspect_ratioRight)


#print("largest  Contour:", sorteddata[0][1])
#print("contours:",contours)
##print("contours:",sorteddata)


k = cv2.waitKey(0) & 0xFF
if k == 27:
    cv2.destroyAllWindows()     # clean up after ESC key. Best practice is to clean up all windows before exiting.



