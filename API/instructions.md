### Example project API for drinks

**setup virtual env**
- name the virtual env to .venv
>> python3 -m venv .venv

**Activate cirtual env**
>> . .venv/bin/activate
- `(.venv)` should be displayed on the left side of the next terminal line

**install dependancies**
>> pip install django
>> pip install djangorestframework

# Django
>> django-admin
- this will give a list of other commands after django-admin

**Start Project**
>> django-admin startproject example .
- starts a new project names example in the current directory

**Start Server**
>> python manage.py runserver
- setup will show "You have 18 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
Run 'python manage.py migrate' to apply them." error
- open a new terminal, activate virtual env: 
>> . .venv/bin/activate
>> python manage.py migrate
- essential data base tables are created

**Create superuser**
>> python manage.py createsuperuser
- for now:
    usrname: admin
    email: admin@admin.com
    password: admin
- navigate to http://127.0.0.1:8000/admin -> login to see groups and users

**Create a model**
models.py -> create a model
in settings.py -> add 'example' in the 'INSTALLED_APPS' array
>> python manage.py makemigrations example
- replace example with name of the app
- This command will create the model
>> python manage.py migrate
- This command will actually add the model to the DB 

**Admin**
- Add file admin.py -> register different tables to show up in the admin panel
- 








