import cv2 
import numpy as np 
lower_green = np.array([33,106,65]) 
upper_green = np.array([52,250,255]) 
cap = cv2.VideoCapture(0) 
#fourcc = cv2.VideoWriter_fourcc(*'MJPG') 
#out = cv2.VideoWriter('d:/code/python/opencv/output.avi',fourcc, 20.0, (640,480)) 
while(1): 
    _, frame = cap.read() 
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) 
    mask = cv2.inRange(hsv, lower_green, upper_green) 
    mask = cv2.blur(mask, (3,3)) 
    res = cv2.bitwise_and(frame,frame, mask= mask) 

    contours, hierarchy = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for cont in contours:#用來抓顏色的輪廓並框出
        ares = cv2.contourArea(cont)
        if ares<50:   #過濾面積小於50的形狀
            continue
        x,y,w,h = cv2.boundingRect(cont)
        cv2.rectangle(res,(x,y),(x+w,y+h),(0,0,0xff),1)
        if(w%2):
            w+=1
        if(h%2):
            h+=1
        count='The center:',x+w/2,y+h/2
        cv2.putText(res,str(count), (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 0), 1)
        print('The center:',x+w/2,',',y+h/2)
    
    #out.write(res) 

    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask) 
    cv2.imshow('res',res) 
    k = cv2.waitKey(5) & 0xFF 
    if k == 27: 
        break 
cv2.destroyAllWindows() 
cap.release()
