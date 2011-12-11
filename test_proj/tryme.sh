#!/bin/env sh

git clone git@github.com:runekaagaard/django-locking.git
cd django-locking/test_proj
python manage.py syncdb
echo "Try out django-locking at: http://127.0.0.1:8000/admin".
python manage.py runserver
