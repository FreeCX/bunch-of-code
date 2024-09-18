#!/bin/bash

FFPROBE=ffprobe
FFMPEG=ffmpeg
TR=tr

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
check_app $TR

# process all input files
for input in "$@"; do
    # check file exists
    if ! [ -f "$input" ]; then
        echo "error: file $input not found - skipped"
        continue
    fi

    output="${input%.*}_recoded.mp4"

    # get video width and height
    width=`${FFPROBE} "$input" -v error -show_entries stream=width -of csv=p=0 | ${TR} -d '\n\t\r '`
    height=`${FFPROBE} "$input" -v error -show_entries stream=height -of csv=p=0 | ${TR} -d '\n\t\r '`

    size_changed=false
    old_width="$width"
    old_height="$height"
    if [ $(( $width % 2 )) -ne 0 ]; then
        width=$(( $width - 1 ))
        size_changed=true
    fi
    if [ $(( $height % 2 )) -ne 0 ]; then
        height=$(( $height - 1 ))
        size_changed=true
    fi
    if [ "$size_changed" = true ]; then
        echo "Video size changed $old_width x $old_height -> $width x $height"
    fi

    # recode
    ${FFMPEG} -i "$input" -vf crop=$width:$height -c:v libx264 -preset slow -profile:v high -crf 18 -coder 1 \
        -pix_fmt yuv420p -movflags +faststart -g 30 -bf 2 -c:a aac -b:a 384k -profile:a aac_low "$output"
done
