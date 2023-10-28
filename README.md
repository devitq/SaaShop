[![Pipeline Status](https://gitlab.crja72.ru/django_2023/students/201154-itq-dev-47231/badges/main/pipeline.svg)](https://gitlab.crja72.ru/django_2023/students/201154-itq-dev-47231/-/pipelines)

# Creating translations
## Creating .po file for ru
```
> django-admin makemessages -l ru
```
## Compiling translations
```
> django-admin compilemessages
```

# ER Diagram
ER diagram for db is stored in ER.jpg
# Dev setup
## Creating virtual enviroment
### Linux
```
> pip install virtualenv
> virtualenv virtualenv_name
> source virtualenv_name/bin/activate
```
### Windows
```
> python -m venv venv
> venv\bin\activate
```
## Setup .env file
### Linux
```
> cp .env.template .env
```
And change .env for your needs
### Windows
```
> copy .env.template .env
```
And change .env for your needs

## Installing requirements
Prod requirements installation
```
> pip install -r requirements/prod.txt
```
Dev requirements installation
```
> pip install -r requirements/dev.txt
```
Test requirements installation
```
> pip install -r requirements/test.txt
```
Linting requirements installation
```
> pip install -r requirements/lints.txt
```

# Dev run
```
> python manage.py runserver
```