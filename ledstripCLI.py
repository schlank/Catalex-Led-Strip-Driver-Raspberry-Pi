#!/usr/bin/python
import time
import RPi.GPIO as GPIO
import sys, getopt

CLK=11
DAT=12
debug=False
delay=0
red=0
green=0
blue=0
state="Off"
#debug=True
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
            print "0"
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



def AllOff():
  print "All 0"
  SetColor(0,0,0)
#time.sleep(1)
def AllOn():
  print "All 255"
  SetColor(255,255,255)
def Red():
  setColor(255,0,0)
def Green():
  setColor(0,255,0)
def Blue():
  setColor(0,0,255)
def setColor(red,green,blue):
  SetColor(red,green,blue)


def done():
  cleanup()

# for z in range (10):
# 	for x in range(255):
#         	#print "X:%d" % (x)try:
#         	#y=x*10
# 		SetColor(x,x,x)
# 	for x in range(255):
# 		SetColor(255-x,255-x,255-x)

# for x in range(20):
# 	SetColor(255,0,0)
# 	time.sleep(0.1)
# 	SetColor(0,0,255)
# 	time.sleep(0.1)

try:
    opts, args = getopt.getopt(sys.argv[1:],'hs:r:g:b:')
  #  print "got Opts: "
#    print sys.argv
except getopt.GetoptError:
    print 'ledstrip.py -h -s [On|Off] -r [val] -g [val] -b [val] '
    sys.exit(2)
#print "-"
#print opts
#print args
#print "="
for opt, arg in opts:
#    print "Opt: %s" % opt
    if opt == '-h':
        print 'ledstrip.py -h -s [On|Off] -r [val] -g [val] -b [val] '
        sys.exit()
    elif opt in ("-w"):
        red=255
        green=255
        blue=255
    elif opt in ("-s"):
        state = arg
        if state == "On":
            red=255
            green=255
            blue=255
        if state == "Off":
            red=0
            green=0
            blue=0
    elif opt in ("-r"):
       red = int(arg)
    elif opt in ("-g"):
       green = int(arg)
    elif opt in ("-b"):
       blue = int(arg)
#print 'red:', red
#print 'green:', green
#print 'blue:', blue
#print 'state:',state


#if __name__ == "__main__":
#    main(sys.argv[1:])

#print "Init:"
init()
SetColor(red, green, blue)
done()
