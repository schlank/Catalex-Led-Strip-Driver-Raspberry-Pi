#!/bin/sh
sudo ./LED.py off
sleep 2
sudo ./LED.py solid 255,255,255
sleep 2
sudo ./LED.py solid 255,0,0
sleep 2
sudo ./LED.py solid 0,255,0
sleep 2
sudo ./LED.py solid 0,0,255
sleep 2
sudo ./LED.py pulse 250,0,0:0,0,255:0,255,0 delay .001 &
sleep 15
touch /tmp/LED.lck
sleep 10
sudo ./LED.py off
sleep 1
sudo ./LED.py strobe 255,0,0:0,0,255 delay .25 &
sleep 10
touch /tmp/LED.lck
sleep 10
sudo ./LED.py off
