import numpy as np
import time
import serial
import struct

READ_DATA = 0x0000

FIRMWARE_VERSION = 0x0000
BAUDRATE =0x0001
COPTER_MANUFACTURER=0x0100
COPTER_SERIAL_NUM=0x0101
COPTER_FRAME_TYPE=0x0102
COPTER_WEIGHT=0x0103
COPTER_WHEELBASE=0x0104
COPTER_BOARD_INFORMATION=0x0105
RTOS_VERSION=0x0200
RTOS_TASK_LIST=0x0201

DEVICE_ATTACH_LIST=0x300
DEVICE_IMU_INFORMATION=0x0301
DEVICE_IMU_STATUS=0x0302
DEVICE_IMU_PARAMETER=0x0303
DEVICE_IMU_DATA=0x0304
DEVICE_IMU_CALIBRATE=0x0305

DEVICE_MAG_INFORMATION=0x030B
DEVICE_MAG_STATUS=0x030C
DEVICE_MAG_PARAMETER=0x030D
DEVICE_MAG_DATA=0x030E
DEVICE_MAG_CALIBRATE=0x030F

DEVICE_BARO_INFORMATION=0x0315
DEVICE_BARO_STATUS=0x0316
DEVICE_BARO_PARAMETER=0x0317
DEVICE_BARO_DATA=0x0318

DEVICE_GPS_INFORMATION=0x031F
DEVICE_GPS_STATUS=0x0320
DEVICE_GPS_PARAMETER=0x0321
DEVICE_GPS_DATA=0x0322

DEVICE_RC_INFORMATION=0x0329
DEVICE_RC_STATUS=0x032A
DEVICE_RC_PARAMETER=0x032B
DEVICE_RC_DATA=0x032C
DEVICE_RC_CALIBRATE=0x032D
DEVICE_RC_AUX_MAP=0x032E

DEVICE_RANGEFINDER_INFORMATION=0x0333
DEVICE_RANGEFINDER_STATUS=0x0334
DEVICE_RANGEFINDER_PARAMETER=0x0335
DEVICE_RANGEFINDER_DATA=0x0336

DEVICE_OPTICALFLOW_INFORMATION=0x033D
DEVICE_OPTICALFLOW_STATUS=0x033E
DEVICE_OPTICALFLOW_PARAMETER=0x033F
DEVICE_OPTICALFLOW_DATA=0x0340

DEVICE_MOTOR_BOUNDARY_THRUST=0x0347
DEVICE_MOTOR_CALIBRATE=0x0348
DEVICE_MOTOR_UNLOCK=0x0349
DEVICE_MOTOR_TEST_SAFTY_CHECK=0x034A
DEVICE_MOTOR_DATA=0x034B

FLIGHT_STATUS=0x0400
FLIGHT_MODE=0x0401
FLIGHT_RATE=0x0402
FLIGHT_ATTITUDE=0x0403
FLIGHT_VELOCITY=0x0404
FLIGHT_POSITION=0x0405

CONTROL_RATE=0x0500
CONTROL_ATTITUDE=0x0501
CONTROL_VELOCITY=0x0502
CONTROL_POSITION=0x0503


def bytesToFloat(h1,h2,h3,h4):
    ba=bytearray()
    ba.append(h4)
    ba.append(h3)
    ba.append(h2)
    ba.append(h1)
    return struct.unpack("!f",ba)[0]

fc_com1 = serial.Serial(
    port="/dev/ttyTHS0",
    baudrate=115200,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=0.2
)

def analyss(msg):
    if(msg[5]==0x03 and msg[6]==0x04):
            b=msg
            f1 = bytesToFloat(b[9],b[10],b[11],b[12])
            f2 = bytesToFloat(b[13],b[14],b[15],b[16])
            f3 = bytesToFloat(b[17],b[18],b[19],b[20])
            f4 = bytesToFloat(b[21],b[22],b[23],b[24])
            f5 = bytesToFloat(b[25],b[26],b[27],b[28])
            f6 = bytesToFloat(b[29],b[30],b[31],b[32])
            print(f1)
            print(f2)
            print(f3)
            print(f4)
            print(f5)
            print(f6)
        else:
            print(msg)
        fc_com1.flushInput()
def READ(reg):
    string1=[]
    string0=[]
    string1.append(0x10)#ID
    string1.append(int(reg/0x100))
    string1.append(int(reg%0x100))
    string1.append(0)
    string1.append(0)
    string0.append(13)
    string0.append(10)
    fc_com1.write(b'#APB')
    fc_com1.write(bytes(string1))
    fc_com1.write(bytes([(int(reg/0x100)+int(reg%0x100))&0xFF]))
    #fc_com1.write('\r\n'.encode())
    fc_com1.write(bytes(string0))
    #print(len(b'#APB'))
    #print(len(bytes(string1)))
    #print(len(bytes([(reg+0x10)&0xFF])))
    #print(len('\r\n'.encode()))

def WRITE(reg, data):
    dataCrc = 0
    size=len(data)
    for i in range(0,size):
        dataCrc += ord(data[i])
    string1=[]
    primable='#APB'
    string1.append(0x10)
    string1.append(int(reg/0x100))
    string1.append(int(reg%0x100))
    string1.append(int(size/0x100))
    string1.append(int(size%0x100))

    fc_com1.write(primable.encode())
    fc_com1.write(bytes(string1))
    if(type(data)==str):
        fc_com1.write(data.encode())
    else:
        fc_com1.write(bytes(data))

    fc_com1.write(bytes([(int(reg/0x100)+int(reg%0x100)+int(size/0x100)+int(sie%0x100)+dataCrc)&0xFF]))
    fc_com1.write('\r\n'.encode())
    #print(np.size([(reg+size+dataCrc+0x10)&0xFF]))

if __name__ == '__main__':
    READ(FLIGHT_STATUS)
    WRITE(DEVICE_MOTOR_UNLOCK,'1')
    delay(3)
    WRITE(DEVICE_MOTOR_UNLOCK,'0')