﻿<h2 align="center">Командный проект Api_yamdb</h2>

-----------------------------------------------------------------------------

## Описание проекта:

Проект YaMDb служит для сбора рецензий и оценок реальных пользователей на
различные произведения. Публиковать отзывы могут только зарегистрированные
пользователи прошедшие аутентификацию по JWT токену. Пользователи могут так же
делиться своим мнением на рецензии других пользователей. Контент на сайте
модерируется пользователями с группами (модератор, администратор).


-----------------------------------------------------------------------------

### 🔧 Инструменты разработки:
[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org)
[![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com)
[![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)](https://www.django-rest-framework.org)
[![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)](https://jwt.io)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)

**Технологический стек:**

- Python >= 3.7
- Django >= 2.2.16
- DRF >= 3.12.4
- DRF-simplejwt >= 5.2.2
- sqlite3

-----------------------------------------------------------------------------

## Как установить проект:

##### 1) Клонировать репозиторий

```
git clone git@github.com:Dazzy132/api_final_yatube.git
```

##### 2) Создать виртуальное окружение проекта

```
python -m venv venv
```

##### 3) Активировать виртуальное окружение

```
source venv/bin/activate
```

##### 4) Установить зависимости проекта

```
pip install -r requirements.txt
```

##### 5) Выполнить команду для выполнения миграций

    python manage.py migrate

##### 6) Создать суперпользователя

    python manage.py createsuperuser

##### 7) Запустить сервер

    python manage.py runserver

-----------------------------------------------------------------------------

## Как пользоваться проектом:

При переходе на страницу ```http://127.0.0.1:8000/redoc``` будут отображены
все доступные эндпоинты для работы API сервиса и нужные поля для отправки.

-----------------------------------------------------------------------------

## Немного примеров работы с API проекта


- 🔷 Регистрация на проекте. Сообщение с кодом будет отправлено на почту
- ```POST http://127.0.0.1:8000/api/v1/auth/signup/```


### **Request samples**
```
{
    "email": "string",
    "username": "string"
}
```

### **Response samples**
```
{
    "email": "string",
    "username": "string"
}
```

-----------------------------------------------------------------------------

- 🔷 Получение токена для работы на проекте. Требуется ввести код с почты
- ```POST http://127.0.0.1:8000/api/v1/auth/token/```

### **Request samples**
```
{
    "username": "string",
    "confirmation_code": "string"
}
```

### **Response samples**
```
{
    "token": "string"
}
```

-----------------------------------------------------------------------------

- 🔷 Изменение данных своей учетной записи  
- ```PATCH http://127.0.0.1:8000/api/v1/users/me/```

### **Request samples**
```
{
    "username": "string",
    "confirmation_code": "string"
}
```

### **Response samples**
```
{
    "token": "string"
}
```

-----------------------------------------------------------------------------

- 🔷 Получить список всех произведений
- ```GET http://127.0.0.1:8000/api/v1/titles/```

### **Response samples**
```
{
    "count": 10,
    "next": http://127.0.0.1:8000/api/v1/titles/?page=3,
    "previous": http://127.0.0.1:8000/api/v1/titles/,
    "results": [
        {
            "id": 6,
            "category": "string",
            "genre": [
                "string"
            ],
            "name": "string",
            "year": 2022,
            "rating": 5.0
        },
        ...
    ]
}
```

-----------------------------------------------------------------------------

- 🔷 Получить конкретное произведение по его идентификатору
- ```GET http://127.0.0.1:8000/api/v1/titles/1/```

### **Response samples**
```
{
    "id": 1,
    "category": "string",
    "genre": [
        "string"
    ],
    "name": "string",
    "year": 2022,
    "rating": 7.0
}
```

-----------------------------------------------------------------------------

- 🔷 Получить все рецензии на произведение
- ```GET http://127.0.0.1:8000/api/v1/titles/1/reviews/```

### **Request samples**
```
{
    "count": 1,
    "next": http://127.0.0.1:8000/api/v1/titles/1/reviews/?page=3,
    "previous": http://127.0.0.1:8000/api/v1/titles/1/reviews/,
    "results": [
        {
            "id": 6,
            "text": "string",
            "author": "username",
            "score": 5,
            "pub_date": "2022-11-23T12:12:14.250891Z"
        }
    ]
}
```

-----------------------------------------------------------------------------

- 🔷 Добавить свою рецензию на произведение
- ```POST http://127.0.0.1:8000/api/v1/titles/1/reviews/```

### **Request samples**
```
{
    "text": "string",
    "score": 1
}
```

### **Response samples**
```
{
    "id": 1,
    "text": "string",
    "author": "string",
    "score": 5,
    "pub_date": "2019-08-24T14:15:22Z"
}
```

-----------------------------------------------------------------------------

- 🔷 Получить конкретную рецензию на произведение

- ```GET http://127.0.0.1:8000/api/v1/titles/1/reviews/1/```


### **Response samples**
```
{
    "id": 0,
    "text": "string",
    "author": "string",
    "score": 1,
    "pub_date": "2019-08-24T14:15:22Z"
}
```

-----------------------------------------------------------------------------

- 🔷 Получить все комментарии на рецензию
- ```GET http://127.0.0.1:8000/api/v1/titles/1/reviews/1/comments/```

### **Response samples**
```
{
    "count": 11,
    "next": http://127.0.0.1:8000/api/v1/titles/1/reviews/1/comments/?page=3,
    "previous": http://127.0.0.1:8000/api/v1/titles/1/reviews/1/comments/,
    "results": [
        {
            "id": 6,
            "text": "string",
            "author": "username",
            "pub_date": "2022-11-23T12:41:20.607638Z"
        }
    ]
}
```

-----------------------------------------------------------------------------

- 🔷 Добавить свой комментарий на рецензию

- ```POST http://127.0.0.1:8000/api/v1/titles/1/reviews/```

### **Request samples**
```
{
    "text": "string"
}
```

### **Response samples**
```
{
    "id": 1,
    "text": "string",
    "author": "string",
    "pub_date": "2019-08-24T14:15:22Z"
}
```

-----------------------------------------------------------------------------

##  📌Разработчики проекта
👩‍💻 [SerafimaK](https://github.com/SerafimaK) В роли первого разработчика<br>
👨‍💻 [msk357](https://github.com/msk357) В роли второго разработчика<br>
👨‍💻 [Dazzy132](https://github.com/Dazzy132) В роли третьего разработчика (TeamLead)<br>


-----------------------------------------------------------------------------

## License

[BSD 3-Clause License](https://opensource.org/licenses/BSD-3-Clause)

Copyright (c) 2022 Yandex Praktikum