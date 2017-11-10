#!/bin/sh
# Here's how to use imagemagick to display text
# Make a blank image
SIZE=320x240
TMP_FILE=/tmp/frame.png

sudo ./on.sh

# From: http://www.imagemagick.org/Usage/text/
convert -background Khaki -font Times-Roman -pointsize 20 \
      -size $SIZE -gravity center\
      label:'Press left button to add a new face\nPress right button to verify identity' \
      $TMP_FILE

sudo fbi -noverbose -T 1 $TMP_FILE

# convert -list font
