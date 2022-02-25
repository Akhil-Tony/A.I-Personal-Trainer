import cv2 as cv
import mediapipe as mp
import numpy as np
import math

def rescaled(frame,factor=.2):
    height = int(frame.shape[0] * factor)
    width = int(frame.shape[1] * factor)
    rescaled_frame = cv.resize(frame,(width,height))
    return rescaled_frame

def get_points(frame):
    frame_rgb = cv.cvtColor(frame,cv.COLOR_BGR2RGB)
    processed = pose.process(frame_rgb)
    h,w = frame.shape[0],frame.shape[1]
    points = []
    if processed.pose_landmarks:
        for idx,lms in enumerate(processed.pose_landmarks.landmark):
            x,y = int(lms.x*w),int(lms.y*h)
            points.append((x,y))        
    return points

def get_angle(p1,p2,p3):
    angle = math.atan2(p3[1]-p2[1],p3[0]-p2[0])-math.atan2(p1[1]-p2[1],p1[0]-p2[0])
    angle = math.degrees(angle)
    if angle<0:
        angle+=360
    return int(angle)

video = cv.VideoCapture('squat2.mp4')
mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils
count = 0
direction = 0

while True:
    success,frame = video.read()
    if success:
        frame = rescaled(frame,.5)
        
        points = get_points(frame)
        points = points[24],points[26],points[28],points[23],points[25],points[27]
        
        angle = get_angle(points[0],points[1],points[2])
        percentage = int( np.interp(angle,(195,275),(0,100)) )
        bar = int( np.interp(angle,(195,275),(10,310)) )
        
        
        cv.line(frame,points[3],points[0],(255,0,0),2)
        cv.line(frame,points[0],points[1],(255,0,0),2)
        cv.line(frame,points[1],points[2],(255,0,0),2)
        cv.line(frame,points[3],points[4],(255,0,0),2)
        cv.line(frame,points[4],points[5],(255,0,0),2)
        
        for p in points:
            cv.circle(frame,p,3,(255,0,0),1)
            cv.circle(frame,p,6,(0,0,255),2)
            cv.circle(frame,p,10,(0,0,255),2)
            
        if percentage == 100:
            if direction == 0:
                count += .5
                direction = 1
        if percentage == 0:
            if direction == 1:
                count += .5
                direction = 0
        
        cv.rectangle(frame,(1,520),(87,620),(0,255,0),-1)
        cv.putText(frame,str(int(count)),(10,600),cv.FONT_HERSHEY_COMPLEX,3,(255,0,0),2)
        
        cv.rectangle(frame,(10,80),(bar,110),(147,20,255),-1)
        cv.rectangle(frame,(10,80),(310,110),(0,255,0),2)
        
        cv.imshow('personal trainer',frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            video.release()
            cv.destroyAllWindows()
            break
    else:
        video.release()
        cv.destroyAllWindows()
        break
video.release()
cv.destroyAllWindows()