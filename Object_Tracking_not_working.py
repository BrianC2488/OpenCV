#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!/usr/bin/env/python3.5
#OpenCV 3.4.1
#Date 20th January, 2018
#Discription : Measuring angle


import cv2
import numpy as np
import math

# create video capture
cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_SIMPLEX
height = 640
width  = 480

fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
writer = cv2.VideoWriter("angle_tracking.avi", fourcc, 12, (640, 480), True)

while True:

    # read the frames
    _, frame = cap.read()

    # smooth it
    frame = cv2.blur(frame,(3, 3))

    # convert to hsv and find range of blue colors
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    thresh = cv2.inRange(hsv, np.array((110, 50, 50)), np.array((130, 255, 255)))
    thresh2 = thresh.copy()

    # find contours in the threshold image for blue
    _, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # finding contour with maximum area and store it as best_cnt
    max_area = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > max_area:
            max_area = area
            best_cnt = cnt

    # finding centroids of best_cnt and draw a circle there
    M = cv2.moments(best_cnt)
    cx, cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
    cv2.putText(frame, str(cx) + "," + str(cy), (cx, cy + 20), font, 1,(255,255,0), 2, cv2.LINE_AA) #Draw the text for blue
    cv2.circle(frame,(cx, cy), 2,(0, 255, 0), 20)
    cv2.line(frame,(cx, cy),((height, width)[0], cy),(0, 255, 0), 1, cv2.LINE_AA)
    #cv2.line(frame, (cx, cy), (cx, (height, width)[0]), (0, 255, 0), 1, cv2.LINE_AA)
    

    #red (36, 25, 25), (70, 255,255)
    thresh3 = cv2.inRange(hsv, np.array((36, 25, 25)), np.array((70, 255,255)))
    #thresh3 = cv2.inRange(hsv, np.array((0, 150, 0)), np.array((5, 255, 255)))

    # find contours in the threshold image for red
    _, contours4,hierarchy = cv2.findContours(thresh3, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # finding contour with maximum area and store it as best_cnt2
    max_area2 = 0
    for cnt in contours4:
        area2 = cv2.contourArea(cnt)
        if area2 > max_area2:
            max_area2 = area2
            best_cnt2 = cnt

    # for slope of line
    # finding centroids of best_cnt and draw a circle there
    M2 = cv2.moments(best_cnt2)
    cx2, cy2 = int(M2['m10'] / M2['m00']), int(M2['m01'] / M2['m00'])
    cv2.putText(frame, str(cx2) + "," + str(cy2), (cx2, cy2 + 20), font, 1,(255, 255,0), 2, cv2.LINE_AA) #Draw the text for red
    cv2.circle(frame,(cx2, cy2), 2, (0, 255, 0), 20)  
    cv2.line(frame,(cx, cy), (cx2, cy2),(0, 255, 0), 1, cv2.LINE_AA)
    

    #put text angle between blue and red
    cx = float(cx)
    cy = float(cy)
    cx2 = float(cx2)
    cy2 = float(cy2)
    angle = int(math.atan2((cy - cy2), (cx2 - cx)) * 180 // math.pi)
    #cv2.putText(frame, str(angle),(int(cx2) - 10, (int(cy2) + int(cy) + 50) // 2), font, 1, (255, 255, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, str(angle), (int(cx) - 30, int(cy) - 30 ), font, 0.8, (255, 255, 255), 2, cv2.LINE_AA) 
    
    #saving video 
    #writer.write(frame)
    
    # Show it, if key pressed is 'Esc', exit the loop
    cv2.imshow('Measuring Angle2', frame)
    #cv2.imshow('thresh',thresh2)
    
    c = cv2.waitKey(1) % 0x100
    if c == 27 or c == 10:
        break

# Clean up everything before leaving
cv2.destroyAllWindows()
cap.release()


# In[ ]:


print(cx,cy)

