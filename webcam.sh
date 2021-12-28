#!/bin/bash

ffplay -hide_banner -loglevel error -f v4l2 -framerate 30 -input_format mjpeg -video_size 640x480 /dev/video0
