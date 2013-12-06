#!/bin/bash

DIR=$(dirname $0)
BASE=$(basename $0 .sh)

SRC='~/Workspace/Reform/reporto/'
DST='tunpixel@tunpixel.webfactional.com:webapps/reportp/reporto'

rsync -avz -c --progress -e ssh --exclude-from "$DIR/$BASE.exclude-list.txt" "$SRC" "$DST" 2> "$DIR/$BASE.err" | tee "$DIR/$BASE.out"

