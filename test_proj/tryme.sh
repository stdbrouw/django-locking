git clone git@github.com:runekaagaard/django-locking.git
cd django-locking/test_proj
python manage.py syncdb
echo "Try out django-locking at: http://localhost/admin:8000".
python runserver
