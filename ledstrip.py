#!/usr/bin/python
import time
import RPi.GPIO as GPIO

CLK=11
DAT=12
debug=False;
delay=0


def init():
	GPIO.setwarnings(debug)
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(CLK, GPIO.OUT)
	GPIO.setup(DAT, GPIO.OUT)

def cleanup():
	GPIO.cleanup()


def Clock():
	GPIO.output(CLK,False)
	time.sleep(delay)	
	GPIO.output(CLK,True)
	time.sleep(delay)	

def Send32Zero():
	for x in range(32):
                GPIO.output(DAT,False)
		if (debug):
			print "0",
		Clock()

def getCode(dat):
	tmp=0
	if ((dat & 0x80) == 0):
      		tmp |= 0x02
	if ((dat & 0x40) == 0):
		tmp|= 0x01
#	print "Get Code [%d] %s : %s" % (dat, tmp, bin(dat))
	return tmp

def SetColor( Red, Green, Blue):
	dx =0
       # print bin(dx)
	dx |= 0x03 << 30
       # print bin(dx)
	dx |= getCode(Blue)
       # print bin(dx)
	dx |= getCode(Green)
       # print bin(dx)
	dx |= getCode(Red)
       # print bin(dx)

        dx |= Blue <<16
       # print bin(dx)
 	dx |= Green <<8
       # print bin(dx)
	dx |= Red
        if (debug):
        	print bin(dx)

	Send(dx)

def Send(dx):
	if (debug):
		print "Sending [%s]" % (bin (dx))
	Send32Zero()
	for x in range(32):
		if ((dx & 0x80000000) != 0 ):
			GPIO.output(DAT,True)
			if (debug):
				print "1",
		else:
			GPIO.output(DAT,False)
			if( debug):
				print "0",
		dx <<= 1
		Clock()
	if (debug):
		print ""
	Send32Zero()


print "Init:"
init()
print "All 0"
SetColor(0,0,0)
#time.sleep(1)
print "All 255"
SetColor(255,255,255)
time.sleep(.2)
print "Red 255"
SetColor(255,0,0)
time.sleep(.2)
print "Green 255"
SetColor(0,255,0)
time.sleep(.2)
print "Blue 255"
SetColor(0,0,255)
time.sleep(.2)
print "All 0"
SetColor(0,0,0)
time.sleep(.2)

for z in range (10):
	for x in range(255):
        	#print "X:%d" % (x)
        	#y=x*10
		SetColor(x,x,x)
	for x in range(255):
		SetColor(255-x,255-x,255-x)

for x in range(20):
	SetColor(255,0,0)
	time.sleep(0.1)
	SetColor(0,0,255)
	time.sleep(0.1)
    


print "All 0"
SetColor(0,0,0)
#time.sleep(1)
print "Cleanup"
cleanup()
