import numpy as np 
import cv2 
cap = cv2.VideoCapture(0) 
img = cv2.VideoCapture(1) 
#fourcc = cv2.VideoWriter_fourcc(*'MJPG') 
#out = cv2.VideoWriter('d:/code/python/opencv/output.avi',fourcc, 20.0, (640,480)) 
while(True): 
    ret, frame = cap.read()
    _, video = img.read() 
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #retval, threshold = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY) 
    #out.write(frame) 
    #輸出檔案
    #cv2.line(frame,(0,0),(640,480),(255,255,255),15)
    #繪製線條(檔名,起始座標,終點座標,顏色,寬度)
    #cv2.rectangle(frame,(15,15),(625,465),(0,0,255),15)
    #繪製矩形(檔名,左上座標,右下座標,顏色,寬度)
    frame=cv2.flip(frame,1)
    #影像翻轉(1左右0上下-1上下左右)
    cv2.imshow('frame',frame) 
    cv2.imshow('usbcam',video) 
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break 
cap.release() 
img.release()
#out.release() 
cv2.destroyAllWindows()
