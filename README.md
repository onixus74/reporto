REFORM Platform
===============

...


```
virtualenv .env # create a virtual environment

source .env-dev/bin/activate # activate virtual environment

pip install -r requirements.txt # install requirements including Django, ...

pip freeze --local > requirements.txt # dump installed requirements

python manage.py syncdb # sync database

python manage.py runserver # run development server

python manage.py runserver 0.0.0.0:8000 # run development server in network

python manage.py dumpdata APP.ENTITY --indent 2 > APP/data/ENTITY.json # dump current db data to fixture file

python manage.py loaddata APP/data/* # load fixture files to db

python manage.py startapp APPNAME # create a n ew application/module

python manage.py schemamigration --auto APP # detect schema changes and create a migration

python manage.py migrate APP # execute migration

```

```
source .env-heroku/bin/activate # activate staging virtual environment

foreman run python manage.py ... # execute tasks in staging environment (DB, ...)

foreman run python manage.py collectstatic

foreman run python manage.py compress

foreman start # run application in staging environment

git push heroku heroku:master # push to staging
```
