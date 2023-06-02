#!/bin/bash

FFPROBE=ffprobe
FFMPEG=ffmpeg

function check_app {
    if ! type -P $1 &> /dev/null; then
        echo "error: cannot find $1 app"
        exit 1
    fi
}

if [ $# -eq 0 ]; then
    echo "telegram video converter"
    echo "usage: $0 <filename> <filename> ..."
    exit 1
fi

# check for apps
check_app $FFPROBE
check_app $FFMPEG

# process all input files
for input in "$@"; do
    # check file exists
    if ! [ -f "$input" ]; then
        echo "error: file $input not found - skipped"
        continue
    fi

    output="${input%.*}_recoded.mp4"

    # get video width and height
    width=`${FFPROBE} "$input" -v error -show_entries stream=width -of csv=p=0`
    height=`${FFPROBE} "$input" -v error -show_entries stream=height -of csv=p=0`

    if [ $(( $width % 2 )) -ne 0 ]; then
        width=$(( $width - 1 ))
    fi
    if [ $(( $height % 2 )) -ne 0 ]; then
        height=$(( $height - 1 ))
    fi

    # recode
    ${FFMPEG} -i "$input" -vf crop=$width:$height -c:v libx264 -preset slow -profile:v high -crf 18 -coder 1 \
        -pix_fmt yuv420p -movflags +faststart -g 30 -bf 2 -c:a aac -b:a 384k -profile:a aac_low "$output"
done
