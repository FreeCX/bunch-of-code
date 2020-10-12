#!/bin/bash

video_file="$1"
width="$2"
timecode="$3"

if [ -z "$video_file" -o -z "$width" -o -z "$timecode" ]; then
    echo "mkv2gif converter (with subtitles)"
    echo "arguments: <mkv-file> <width> <timecode> <-sub>"
    exit
fi
subtitle_file=${video_file%.mkv}.ass

echo -en "[*] Cut video by timecode..."
if [ -f "$subtitle_file" ]; then
    mkvmerge -o "./output.mkv" -S --split parts:$timecode "$video_file" "$subtitle_file" > /dev/null
else
    mkvmerge -o "./output.mkv" --split parts:$timecode "$video_file" > /dev/null
fi
echo -en "[DONE]\n[*] Converting video to compatible format..."
ffmpeg -i "./output.mkv" -strict -2 -vf subtitles="output.mkv" "output.mp4" 2> /dev/null
mkdir "frames"
ffmpeg -i "./output.mp4" -vf scale="$width":-1 -r 10 "frames/ffout%03d.png" 2> /dev/null
echo -en "[DONE]\n[*] Make 'output.gif' file..."
convert -delay 7 -loop 0 frames/ffout*.png output.gif 2> /dev/null
echo -en "[DONE]\n[*] Delete temp file..."
rm -rf "frames" output.{mp4,mkv}
echo -en "[DONE]\n"