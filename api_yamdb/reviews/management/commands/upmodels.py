from django.core.management.base import BaseCommand, CommandError
import csv
import os

from api_yamdb.settings import BASE_DIR
from reviews.models import Categories, Title, Genres


class Command(BaseCommand):
    help = 'upgrade model data from csv'

    def handle(self, *args, **options):
        """Функция добавляет данные для всех моделей"""
        Command.category_update()
        Command.genre_update()
        Command.title_update()
        # Command.genre_title()
        # Command.comments_update()
        # Command.reviews_update()
        # Command.users_update()

    def title_update():
        """Добавление данных для модели Title"""  
        with open(os.path.join(BASE_DIR, 'static/data/titles.csv'), encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                id = row['id']
                name = row['name']
                year = row['year']
                category_id = row['category']
                title = Title(id=id, name=name, year=year, category_id=category_id)
                title.save()

    def category_update():
        """Добавление данных для модели Categories"""  
        with open(os.path.join(BASE_DIR, 'static/data/category.csv'), encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                id = row['id']
                name = row['name']
                slug = row['slug']
                category = Categories(id=id, name=name, slug=slug)
                category.save()

    def genre_update():
        """Добавление данных для модели Genres"""  
        with open(os.path.join(BASE_DIR, 'static/data/genre.csv'), encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                id = row['id']
                name = row['name']
                slug = row['slug']
                genre = Genres(id=id, name=name, slug=slug)
                genre.save()

    # функция genre_title не работает, жду ответа наставника
    """def genre_title():
        with open(os.path.join(BASE_DIR, 'static/data/genre_title.csv'), encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                title_id = row['title_id']
                genre_id = row['genre_id']
                title = Title(id=title_id, genre_id=genre_id)
                title.save()"""

    # def comments_update():
        # Добавление данных для модели Comment"""  
       # with open(os.path.join(BASE_DIR, 'static/data/comments.csv'), encoding='utf-8') as csv_file:
            # csv_reader = csv.DictReader(csv_file, delimiter=',')
            # for row in csv_reader:
                # id = row['id']
                # review_id = row['review_id']
                # text = row['text']
                # author_id = row['author']
                # pub_date = row['pub_date']
                # comments = Comment(id=id, review_id=review_id, text=text, author_id=author_id, pub_date=pub_date)
                # comments.save()

    # def reviews_update():
        # Добавление данных для модели Review"""  
        # with open(os.path.join(BASE_DIR, 'static/data/review.csv'), encoding='utf-8') as csv_file:
            # csv_reader = csv.DictReader(csv_file, delimiter=',')
            # for row in csv_reader:
                # id = row['id']
                # title_id = row['title_id']
                # text = row['text']
                # author_id = row['author']
                # score = row['score']
                # pub_date = row['pub_date']
                # reviews = Review(id=id, title_id=title_id, text=text, author_id=author_id,score=score, pub_date=pub_date)
                # reviews.save()

    # def users_update():
        # Добавление данных для модели User"""
        # with open(os.path.join(BASE_DIR, 'static/data/users.csv'), encoding='utf-8') as csv_file:
            # csv_reader = csv.DictReader(csv_file, delimiter=',')
            # for row in csv_reader:
                # id = row['id']
                # username = row['username']
                # email = row['email']
                # role = row['role']
                # bio = row['bio']
                # first_name = row['first_name']
                # last_name = row['last_name']
                # users = User(id=id, username=username, email=email, role=role, bio=bio, first_name=first_name, last_name=last_name)
                # users.save()
