#!/bin/bash

if [ $# -eq 0 ]; then
    echo "usage: $0 <filename>"
    exit 1
fi

# -vf scale=iw:-2

ffmpeg -i "$1" -c:v libx264 -preset slow -profile:v high -crf 18 -coder 1 -pix_fmt yuv420p \
    -movflags +faststart -g 30 -bf 2 -c:a aac -b:a 384k -profile:a aac_low "recoded_$1"
