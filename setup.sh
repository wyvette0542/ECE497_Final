#!/bin/sh
chmod +x on.sh
chmod +x welcome.sh
chmod +x grab.sh
chmod +x cleanup.sh
chmod +x main.py
chmod +x apitest.py
gcc grabbertemp.c -lv4l2 -o grabber
echo "Successfully setup program. Run main.py to continue."