REFORM Platform
===============

....


```
virtualenv .env # create a virtual environment

source .env/bin/activate # activate virtual environment

pip install -r requirements.txt # install requirements including Django, ...

pip freeze > requirements.txt # dump installed requirements

python manage.py syncdb # sync database

python manage.py runserver # run development server

python manage.py runserver 0.0.0.0:8000 # run development server in network

python manage.py dumpdata reports.ENTITY --indent 2 > reports/fixtures/ENTITY.json # dump current db data to fixture file

python manage.py loaddata reports/fixtures/* # load fixture files to db

python manage.py startapp APPNAME # create a n ew application/module

```
