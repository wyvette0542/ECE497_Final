#!/bin/sh
./grabber
convert *.ppm 1.jpg
rm *.ppm
sudo fbi -noverbose -T 1 -a 1.jpg 
python2.7 apitest.py
rm *.jpg
