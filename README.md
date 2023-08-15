# crm

1. Create database in MariDB or MySQL
2. Set up DB connection in settings.py

```
pipenv install
pipenv shell
cd mysite
python manage.py makemigrations humanity
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
curl localhost:8000/humanity/seed
```
