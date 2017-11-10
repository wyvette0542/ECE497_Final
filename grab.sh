#!/bin/sh
./grabber
convert *.ppm 1.jpg
rm *.ppm
convert 1.jpg -background Khaki -pointsize 18 label:'Checking......' \
          -gravity Center -append    checking.jpg
sudo fbi -noverbose -T 1 -a checking.jpg 
python2.7 apitest.py
rm *.jpg
