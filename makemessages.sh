#!/bin/bash
set -x

#django-admin.py makemessages -v 2 --all -e html -e py -i 'node_modules' -i '.env-*' -i 'test'  -i 'base' --ignore=reporto/static/* -i 'reporto/media'
django-admin.py makemessages -v 2 -a -e html -e py  -i reporto -i test -i data -i migrations -i static -i node_modules
django-admin.py makemessages -v 2 -a -d djangojs -e js -i reporto -i test -i data -i migrations -i components -i dependencies -i theme -i node_modules
