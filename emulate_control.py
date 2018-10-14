#!/usr/bin/python

import serial
from time import sleep

def mycheck(st):
    sum = 0; 
    for ii in range(len(st)):
        #print "ch 0x%x" % st[ii]
        sum += st[ii] & 127
        sum = sum % 256
    v1 = 127 - sum

    if v1 < 0:
        v1 = v1 + 256
    else:
        v1 = v1 + 128

    return v1



ser_com = serial.Serial('/dev/ttyUSB0',38400)
sleep(.300)

END_OF_PACKET = 15
BUF_SIZE = 100 
CONTROL_PACKET_ID = 0x60
STARTUP_PACKET_ID = 0x74

xx = [0] * BUF_SIZE

def set_relay():
    global ser
    sleep(.5)
    print "relay on"
    ser_com.rts=0
    sleep(.300)
    ser_com.rts=1
    sleep(.05)

def sendstart():
    global ser_com

    data=[]
    data.append(STARTUP_PACKET_ID)
    data.append(0x81)
    data.append(0x8e)
    data.append(0x85)
    data.append(0x80)
    data.append(0x93)
    data.append(0xd4)
    data.append(0xa7)
    data.append(0x80)
    check = mycheck(data)
    data.append(check)
    data.append(END_OF_PACKET)
    print "0x%x" % check
    ser_com.write(bytearray(data))
    ser_com.flush()

def sendcontrol(direction, speed ):
    global ser_com
    maxspeed = 255
    data=[]
    data.append(CONTROL_PACKET_ID)
    data.append( 0x80 | speed >>3 & 0x7f)
    data.append( 0x80 | direction >>3 & 0x7f)
    data.append( 0x80 | maxspeed >>1 & 0x7f)
    data.append( 0x80 |  ((maxspeed  & 0x01) << 6 ) |
                         ((speed     & 0x07) << 3 ) | 
                         ((direction & 0x07) << 0 ) )
    data.append( 128 )   #byte 5
    data.append( 132 )   #byte 6
    data.append( 128 )   #byte 7 
    check  = mycheck(data)
    #print "0x%x" % check
    data.append(check)
    data.append(END_OF_PACKET)
    ser_com.write(data)
    #ser_com.flush()

def testcontrol():
    data = bytearray([0x60,0xb9,0x80,0xff,0xd8,0x80,0x84,0x80,0x8b,0x0f]) 
    ser_com.write(data)
    ser_com.flush()
    sleep(.015)
#send a starup packet


set_relay()
#ser_com.write(bytearray([0]))
#sleep(.01)
sendstart()
#ser_com.write(bytearray([0x05, 0xa0, 0xda]))
#sleep(.02)

direction = 200
speed = 800
vd = 5
while True:

    speed = direction
    sendcontrol(direction, speed)
    sleep(.01)
   
    direction  = direction + vd
    print "dir: %d, speed: %d" % (direction,speed)
    if direction > 1000:
        vd = vd  * -1

    if direction < 200:
        vd = vd * -1
    
