# backend
## ydl-api submodule backend

## Server setup tutorial
[tutorial](https://github.com/YoungAndDigitalLearning/ydl-api/blob/master/Server-setup-manual.md)

### Sync modules
``` bash
pipenv sync
``` 

### Initialize
``` bash
pip install pipenv==2018.5.18 

pipenv install --python 3.6

pipenv run django-admin startproject ydl_api

```

Install Django rest
``` bash
pipenv install djangorestframework
pipenv install markdown       # Markdown support for the browsable API.
pipenv install django-filter  # Filtering support
```

pipenv run python manage.py runserver
