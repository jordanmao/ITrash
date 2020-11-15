import cv2
import TargetTrajectoryTracker
import imutils
import numpy
import time
 
def detectObject(mask):
    #============================================================
    # Source: https://www.pyimagesearch.com/2015/09/21/opencv-track-object-movement/
    # Using the mask found from the previous step, we use the
    # algorithm below to find and circle the contours.
    #============================================================

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    centre = None
   
    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        if radius > 10:
            if M["m00"]!=0:
                centre = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
    #============================================================
    return centre;

def convertPixeltoMetre(point):
    xScale = 2.25
    yScale = 2.25

    return (point[0]/500 * xScale, point[1]/500 * yScale)


def convertMetretoPixel(point):
   xScale = 2.25
   yScale = 2.25

   return (int(point[0]/xScale * 500), int(point[1]/yScale * 500))

              
# Intialize Video Capture
vs = cv2.VideoCapture(0)
#vs = cv2.VideoCapture("Test_video.MOV")

# Intialize Background Subtractor
subtractor = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=100, detectShadows=False )


out = cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (500,500))

for x in range(30):
    ret, frame = vs.read()

while(True):
    
#    coord = TargetTrajectoryTracker.predictCoord((5, 20, 0), (15, 30, 0), 0.5)
#    print("X Coord")
#    print(coord[0])
#    print("Y Coord")
#    print(coord[1])
#    break

    # Get current frame
    ret, frame = vs.read()
    
    # Resize the image
    frame = cv2.resize(frame, (500, 500))

    # Grayscale the image
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Resize the image
    resize = cv2.resize(gray, (500, 500))
    
    # Apply mask onto the image
    mask = subtractor.apply(resize)
    
    centreOne = detectObject(mask)

    if centreOne!=None:
#        print("Sleep Start")
        time.sleep(0.5);
#        print("Sleep Stop")
        
        
        
        # Get current frame
        ret, frame = vs.read()
        
        # Resize the image
        frame = cv2.resize(frame, (500, 500))

        # Grayscale the image
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Resize the image
        resize = cv2.resize(gray, (500, 500))
        
        # Apply mask onto the image
        mask = subtractor.apply(resize)
        
        centreTwo = detectObject(mask)
#        print("500-centreOne[1]")
#        print(500-centreOne[1])

        if centreTwo!=None:
            centreOne = convertPixeltoMetre(centreOne)
            centreTwo = convertPixeltoMetre(centreTwo)

            coord = TargetTrajectoryTracker.predictCoord((centreOne[0], 500-centreOne[1]), (centreTwo[0], 500-centreTwo[1]), 0.5)

            centreOne = convertMetretoPixel(centreOne)
            centreTwo = convertMetretoPixel(centreTwo)
            coord = convertMetretoPixel(coord)

    
            pos1 = "(" + str(centreOne[0]) + ", "+ str(500 - centreOne[1]) + ")"
            pos2 = "(" + str(centreTwo[0]) + ", "+ str(500 - centreTwo[1]) + ")"
            pos3 = "(" + str(int(coord[0])) + ", "+ str(500 - int(coord[1])) + ")"

            cv2.putText(frame, pos1, centreOne, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2, cv2.LINE_AA)
            cv2.putText(frame, pos2, centreTwo, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(frame, pos3, (int(coord[0]), 500-int(coord[1])), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2, cv2.LINE_AA)

            cv2.circle(frame, centreOne, 5, (0, 0, 255), -1)    # red
            cv2.circle(frame, centreTwo, 5, (0, 255, 0), -1)    # green
            cv2.circle(frame, (int(coord[0]), 500-int(coord[1])), 5, (255, 0, 0), -1)   # blue

#            cv2.imshow("Frame2", frame)
#            time.sleep(0.5);
#            time.sleep(100);
#
#            break
    

    out.write(frame)


    # Display the final image
    cv2.imshow("Frame3", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture
vs.release()
cv2.destroyAllWindows()



    

