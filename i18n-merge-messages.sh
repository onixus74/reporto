#!/bin/bash
set -x

msgmerge ./locale/ar/LC_MESSAGES/django.po ./base/locale/ar/LC_MESSAGES/django.po > ./locale/ar/LC_MESSAGES/django.po
