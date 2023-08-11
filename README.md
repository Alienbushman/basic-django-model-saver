# Django Rest API

A simple API written using the Django Rest Framework using APIView.


## Overview of the architecture

This is a basic CRUD app that demonstrates how you can use django to save the results of machine learning models to a database.

#### models endpoint
get: returns all the models

put: by adding in the model id, it allows you to rename the model

delete: delete the model via the id

post: create a new model


#### predictions endpoint
get: returns all predictions and it gets the model name

post: add a new prediction with the model name

delete: deletes a prediction and/or all predictions that are related to a model name


## How to run for the first time
In the basic running commands, run the commands in the following order for the first time
1) Make migrations
2) Migrate
3) Create super user
4) Run django server
5) Interface with the API via swagger by visiting http://127.0.0.1:8000/ 


## Basic django running commands
Run a django server
```python
python manage.py runserver
```

To view the API via django admin

View here

http://127.0.0.1:8000/admin/

To view the swagger interface

http://127.0.0.1:8000/

Rebuilding the django models
```python
python manage.py makemigrations
```
```python
python manage.py migrate
```

create a new app

```python
django-admin startapp api
```
creating super user Remember to pick a proper one for something actually in production
```python
python manage.py createsuperuser
```