import cv2
import numpy as np
import time
import PoseModule as pm


cap = cv2.VideoCapture('assets/BicepCurl2.mp4')
detector = pm.poseDetector()
Rcount=0
Lcount=0
Rdirection=0
Ldirection=0
PreviousTime = 0

def rescale_frame(frame, percent=75):
    scale_percent = 75
    width = int(frame.shape[1]*scale_percent/250)
    height = int(frame.shape[0]*scale_percent/250)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
    

while True:
    success, img = cap.read()

    #Resizes video
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    if height >= 1080.0 or width >= 1920.0:
        img = rescale_frame(img, percent=1)

    img = detector.findPose(img, False)
    lmList = detector.getPosition(img, False)

    if len(lmList) != 0:
        #Left Arm
        LAangle = detector.findAngle(img, 11,13,15)
        #Right Arm
        RAangle = detector.findAngle(img, 12, 14, 16)

        Rpercentage = np.interp(RAangle, (55,160),(0,100))
        Lpercentage = np.interp(LAangle, (55,160),(0,100))
        bar = np.interp(RAangle, (55,160), (650,100))

        #Check for dumbbell curls on right arm
        if Rpercentage == 100:
            if Rdirection ==0:
                Rcount +=0.5
                Rdirection = 1
        if Rpercentage == 0:
            if Rdirection ==1:
                Rcount += 0.5
                Rdirection = 0
        #Check for dumbbell curls on left arm
        if Lpercentage == 100:
            if Ldirection ==0:
                Lcount +=0.5
                Ldirection = 1
        if Lpercentage == 0:
            if Ldirection ==1:
                Lcount += 0.5
                Ldirection = 0

        cv2.putText(img, str(int(Rcount)), (50,500), cv2.FONT_HERSHEY_PLAIN, 5, (255,0,0), 5)
        cv2.putText(img, str(int(Lcount)), (550,500), cv2.FONT_HERSHEY_PLAIN, 5, (255,0,0), 5)

    #Display FPS
    CurrentTime = time.time()
    fps = 1/(CurrentTime-PreviousTime)
    PreviousTime = CurrentTime
    cv2.putText(img, str(int(fps)),(100,50), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,255),3)
    cv2.putText(img, str('FPS'),(20,50), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255),2)
    # cv2.rectangle(img, (100,13),(160,55),(0,0,255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)