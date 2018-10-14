
#!/usr/bin/python

import serial

# returns total mod 256 as checksum
# input - string
def checksum256(st):
    return reduce(lambda x,y:x+y, map(ord, st)) % 256

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



ser = serial.Serial('COM8',38400)

END_OF_PACKET = 15
BUF_SIZE = 100 
CONTROL_PACKET_ID = 0x60
STARTUP_PACKET_ID = 0x74

index = 0
xx = [0] * BUF_SIZE

while True:
    doprint = False
    xx[index] = ord(ser.read())
    #print "in 0x%x" % xx[index]
    if xx[index] == END_OF_PACKET:
        packet_id = xx[0]
        if packet_id == CONTROL_PACKET_ID:
            typename= "control packet"
            doprint = True
            
        elif packet_id == STARTUP_PACKET_ID:
            typename= "start up packet"
            doprint = True
        else:
            typename= "unknown"
            #if packet_id != 0x61:
            doprint = True
                    
        
        if doprint == True:
            print typename
            for ii  in  range(index):
                print "%d 0x%x" % (ii, xx[ii]) 
            
            print "checksum: 0x%x" % mycheck( xx[0:index-1])

        index = 0 
    else:
        
        index = index + 1
        if index >= BUF_SIZE:
            print "reseting"
            index = 0

