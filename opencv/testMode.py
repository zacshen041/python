import numpy as np
import time
import serial
import STM32UART as STM
import cv2
from jetcam.csi_camera import CSICamera
cam0 = CSICamera(width=1080, height=720, capture_width=1080, capture_height=720, capture_fps=30) 
fc_com1 = serial.Serial(port="/dev/ttyTHS0", baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=0.2)
lower_green = np.array([33,106,65]) 
upper_green = np.array([52,250,255]) 
time.sleep(1)
nowTime=time.time()
clockTime=time.time()
data='wait'
flag=0
while(True):
    while(data!='wait'):#wait until start
        data=input("Please enter a string:\n")
        if(data=='start'):
            #STM.WRITE(STM.DEVICE_MOTOR_UNLOCK,'1')
            #STM.WRITE(STM.CONTROL_ATTITUDE,'1M')
            nowTime=time.time()
    if fc_com1.inWaiting() > 0 :#receiver
        msg = fc_com1.read_until('\n')
        STM.analysis(msg)

    if(time.time()-clockTime>1):#transmitter
        STM.READ(STM.DEVICE_IMU_DATA)
        clockTime=time.time()
        if(flag==1):
            STM.WRITE(STM.CONTROL_ATTITUDE,'0M')
        #print('Require data')

    if(time.time()-nowTime>5 and flag==0):
        #STM.WRITE(STM.CONTROL_ATTITUDE,'0M')
        flag=1
    if(time.time()-nowTime>10):
        #STM.WRITE(STM.DEVICE_MOTOR_UNLOCK,'0')
        break
    frame = cam0.read()
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

    #cv2.imshow('frame',frame)
    #cv2.imshow('mask',mask) 
    cv2.imshow('res',res)
    if cv2.waitKey(1)==ord('q'):
        break

cam0.release()
cv2.destroyAllWindows()
#messege = fc_com1.readline() 
#print(messege)
#STM.WRITE(STM.DEVICE_MOTOR_UNLOCK,'0')
fc_com1.close()