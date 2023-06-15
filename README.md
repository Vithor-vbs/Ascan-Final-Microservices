# Streaming Microservice Menager

This is an **Ascan** Challenge !

The idea is to have a subscription manager that can update users subscription status and comments

My solution:

### `Prerequisites / Technologies Used`

- Made with Python and Django framework 
- Used MySQL databases 
- RabbitMQ as message broker, pika as python rabbitMQ client
- Containerized by Docker (docker-compose automated deploy)
- Used React as main frontend engine 

### `Steps`

In both comments and posts services, raise the services by using docker compose

> docker-compose up --build 

after that, at "posts-microservices-frontend-main" use npm install and npm start to create the react app

// Notice that Im using latest node version 18.16
 >npm install

 >npm start


### `How it works`

**1. Setup of Django Application**


> django-admin startproject app

> django-admin startapp core

This will create "/core" and "/app" folders that contains all Django initial setup

I modified settings.py inside /app adding corsheaders and rest-framework in the INSTALLED_APPS

also, modified the database info to match mySQL database

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'subscriptions',
        'USER': 'root',
        'PASSWORD': 'root', 
        'HOST': 'db',
        'PORT':'3306',
    }
}
```

OBS: Notice that this is valid for both of the services

**2. Setup of Docker**

We need to write a Dockerfile that contains the necessary steps to build the image. After building the image, we can use it in our docker-compose to create our services.

Dockerfile will download all the requirements listed on requirements.txt

```
FROM python:3.9
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt
COPY . /app

CMD python manage.py runserver 0.0.0.0:8001
```

Now we can jump on docker-compose configuration. It have 3 services: backend, queue and db

 - backend is our main service, it will run our API in port **8000** for posts and **8001** for comments

 - queue is only created for the message broker client

 - db is for database, we create our database credentials and choose mysql version there

 OBS: backend and queue depends on db

 **3. API Structure**

firstly, create and configure your /core/models.py and /core/urls.py


after defining the API models you can migrate everything to the database

> #python manage.py makemigrations

> #python manage.py migrate

create serializers.py (parsing data to JSON format)

modify views.py. This file holds every API method definition, it is the core of your API, in the case of this project you will find get, post, put, delete in the posts endpoint, and post, delete and get on the comments 

Comments paths:
```
urlpatterns = [
    path('posts/<int:pk>/comments', PostCommentAPIView.as_view()),
    path('comments', CommentsAPIView.as_view()),
    path('posts/<int:post_id>/delete-comments', CommentDeleteView.as_view(), name='delete_comments'),

]
```
Posts paths:
```
urlpatterns = [
    path('posts', PostAPIView.as_view()),
    path('posts/<int:pk>', PostAPIView.as_view()),
]
```

OBS: We are using RabbitMQ as a message broker, so all the api calls are enqueued (rabbitMQ console is being consumed by pika client)

The comments are sent to the post service and only then the comment is processed in the database 

 **4. Frontend**

 React is the library used in this project

 as being a small application, there is just one component, that component makes all of the data fetching and API calls, as well as all design logic. 