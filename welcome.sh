#!/bin/sh
# Here's how to use imagemagick to display text
# Make a blank image
SIZE=320x240
TMP_FILE=/tmp/frame.png

sudo ./on.sh

# From: http://www.imagemagick.org/Usage/text/
convert -background Khaki -font Times-Roman -pointsize 20 \
      -size $SIZE -gravity center\
      label:'Please look directly into the camera\n\nPress GREEN button and wait the red\nLED to flash once to add a new face\n\nPress RED button to verify identity' \
      $TMP_FILE

sudo fbi -noverbose -T 1 $TMP_FILE

# convert -list font
