#!/usr/bin/python
import time
import sys
import RPi.GPIO as GPIO
import os.path
lockfile = "/tmp/LED.lck"
CLK=11
DAT=12
debug=False;
delay=0
clkdelay=0
command = ""
params = ""

for z in range(len(sys.argv)):

   if sys.argv[z]=="off":
      command="off"
   if sys.argv[z]=="solid":
      command="solid"
      colors=sys.argv[z+1].split(',')
   if sys.argv[z]=="delay":
      delay=float(sys.argv[z+1])
#      print "Set Delay to [%f]" % delay
   if sys.argv[z]=="strobe":
      command="strobe"
      params=sys.argv[z+1]
#      print params

   if sys.argv[z]=="pulse":
      command="pulse"
      params=sys.argv[z+1]
     


def init():
	GPIO.setwarnings(debug)
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(CLK, GPIO.OUT)
	GPIO.setup(DAT, GPIO.OUT)

def cleanup():
	GPIO.cleanup()


def Clock():
	GPIO.output(CLK,False)
	time.sleep(clkdelay)	
	GPIO.output(CLK,True)
	time.sleep(clkdelay)	

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
        if Red < 0:
           Red=0;
        if Green < 0:
           Green=0;
        if Blue < 0:
           Blue=0;
	dx =0
	dx |= 0x03 << 30
	dx |= getCode(Blue)
	dx |= getCode(Green)
	dx |= getCode(Red)
        dx |= Blue <<16
 	dx |= Green <<8
	dx |= Red
        dx |= 0 << 24
#        if (debug):
    #   	print bin(dx)
	Send(dx)

def check_lock():
       if (os.path.isfile(lockfile)):
       		os.remove (lockfile)
		return (False)
       else:
                return (True)
def max(a,b,c):
    _max=0
    if a >=_max:
      _max=a
    if b >=_max:
      _max=b
    if c >=_max:
      _max=c
    return (_max)

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


#print "Init:"
init()
#print "All 0"
#SetColor(0,0,0)
#time.sleep(1)
#print "All 255"
#SetColor(255,255,255)
#time.sleep(.2)
#print "Red 255"
#SetColor(255,0,0)
#time.sleep(.2)
#print "Green 255"
#SetColor(0,255,0)
#time.sleep(.2)
#print "Blue 255"
#SetColor(0,0,255)
#time.sleep(.2)
#print "All 0"
#SetColor(0,0,0)
#time.sleep(.2)
#
#for z in range (10):
#	for x in range(255):
#        	#print "X:%d" % (x)
#        	#y=x*10
#		SetColor(x,x,x)
#	for x in range(255):
#		SetColor(255-x,255-x,255-x)
#
#for x in range(20):
#	SetColor(255,0,0)
#	time.sleep(0.1)
#	SetColor(0,0,255)
#	time.sleep(0.1)
#    
#

#print "All 0"
#SetColor(0,0,0)
#time.sleep(1)
#print "Cleanup"


if command=="solid":
   SetColor (int(colors[0]),int(colors[1]),int(colors[2]))

if command=="off":
   SetColor (0,0,0)
   
if command=="strobe":
   looper=True
   while looper:
	looper=check_lock()
#        print params
        for colors in params.split(':'):
#            print colors
            _colors = colors.split(',')
#            print _colors
            red=int(_colors[0])
            green=int(_colors[1])
            blue=int(_colors[2])
            #print "Colors:[%d][%d][%d]" % (red,green,blue)
            SetColor(red,green,blue)
            time.sleep(delay)
        
if command=="pulse":
   looper=True
   while looper:
	looper=check_lock()
#        print colors
        for colors in params.split(':'):
            	_colors = colors.split(',')
        	_max = max(int(_colors[0]),int(_colors[1]),int(_colors[2]))
		for x in range(_max):
			SetColor(-1*_max+int(_colors[0])+x,-1*_max+int(_colors[1])+x,-1*_max+int(_colors[2])+x)
                	time.sleep(delay)
		for x in range(_max):
			SetColor(int(_colors[0])-x,int(_colors[1])-x,int(_colors[2])-x)
                	time.sleep(delay)
        

   

cleanup()
