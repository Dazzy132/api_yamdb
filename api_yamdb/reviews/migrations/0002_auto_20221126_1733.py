# Generated by Django 2.2.16 on 2022-11-26 14:33

import reviews.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.PositiveSmallIntegerField(validators=[reviews.validators.validate_year], verbose_name='Год создания произведения'),
        ),
    ]
