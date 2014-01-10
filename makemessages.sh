#!/bin/bash
set -x

#django-admin.py makemessages -v 2 --all -e html -e py -i 'node_modules' -i '.env-*' -i 'test'  -i 'base' --ignore=reporto/static/* -i 'reporto/media'
django-admin.py makemessages -v 2 -a -e html -e py -i test -i data -i migrations -i static
