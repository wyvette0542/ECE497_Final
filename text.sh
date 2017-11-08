
# From: http://www.imagemagick.org/Usage/text/
  convert 1.jpg   -background Khaki  label:'WELCOME' \
          -gravity Center -append    anno_label.jpg
          
  sudo fbi -noverbose -T 1 -a anno_label.jpg

