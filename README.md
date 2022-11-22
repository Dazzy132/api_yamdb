<h2 align="center">Командный проект Api_yamdb</h2>

-----------------------------------------------------------------------------

## Описание проекта:

Проект YaMDb служит для сбора рецензий и оценок реальных пользователей на
различные произведения. Публиковать отзывы могут только зарегистрированные
пользователи прошедшие аутентификацию по JWT токену. Пользователи могут так же
делиться своим мнением на рецензии других пользователей. Контент на сайте
модерируется пользователями с группами (модератор, администратор).

-----------------------------------------------------------------------------

### Инструменты разработки:

**Стек:**

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

### Немного примеров работы с API проекта

-----------------------------------------------------------------------------

- Регистрация на проекте. Сообщение с кодом будет отправлено на почту

```
POST http://127.0.0.1:8000/api/v1/auth/signup/
```

-----------------------------------------------------------------------------

- Получение токена для работы на проекте. Требуется ввести код с почты

```
POST http://127.0.0.1:8000/api/v1/auth/token/
```

-----------------------------------------------------------------------------

- Изменение своего профиля

```
POST http://127.0.0.1:8000/api/v1/users/me/
```

-----------------------------------------------------------------------------

- Получить список всех произведений

```
GET http://127.0.0.1:8000/api/v1/titles/
```

-----------------------------------------------------------------------------

- Получить конкретное произведение по его идентификатору

```
GET http://127.0.0.1:8000/api/v1/titles/1/
```

-----------------------------------------------------------------------------

- Получить все рецензии на произведение

```
GET http://127.0.0.1:8000/api/v1/titles/1/reviews/
```

-----------------------------------------------------------------------------

- Добавить свою рецензию на произведение

```
POST http://127.0.0.1:8000/api/v1/titles/1/reviews/
```

-----------------------------------------------------------------------------

- Получить конкретную рецензию на произведение

```
GET http://127.0.0.1:8000/api/v1/titles/1/reviews/1/
```

-----------------------------------------------------------------------------

- Получить все комментарии на рецензию

```
GET http://127.0.0.1:8000/api/v1/titles/1/reviews/1/comments/
```

-----------------------------------------------------------------------------

- Добавить свой комментарий на рецензию

```
POST http://127.0.0.1:8000/api/v1/titles/1/reviews/
```

-----------------------------------------------------------------------------

## License

[BSD 3-Clause License](https://opensource.org/licenses/BSD-3-Clause)

Copyright (c) 2022 Yandex Praktikum - **Команда 32**