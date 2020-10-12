#!/bin/bash

for i in *.pdf; do
    gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.5 -dPDFSETTINGS=/ebook -dNOPAUSE \
        -dQUIET -dBATCH -dColorImageResolution=300 -sOutputFile="new_$i" "$i"
    mv "new_$i" "$i"
done