#!/bin/bash

trap kill_app INT

function kill_app() {
    kill $$
}

for item in `cat ~/downloads/urls`; do
    echo $item;
    mpv --ytdl-format="bestvideo[ext=mp4][height<=?1080][fps<=30]+bestaudio[ext=m4a]" $item; 
done
