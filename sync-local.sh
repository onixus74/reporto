#!/bin/bash

DIR=$(dirname $0)
BASE=$(basename $0 .sh)

SRC='tunpixel@tunpixel.webfactional.com:webapps/reporto/reporto/'
DST="$HOME/Workspace/Reform/reporto-remote/"

rsync -avz -c --progress --delete -e ssh --exclude-from "$DIR/$BASE.exclude-list.txt" "$SRC" "$DST" 2> "$DIR/$BASE.err" | tee "$DIR/$BASE.out"

