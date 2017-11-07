#!/bin/sh
./grabber
convert *.ppm 1.jpg
rm *.ppm
python2.7 apitest.py
rm *.jpg