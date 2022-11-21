# Generated by Django 3.2.16 on 2022-11-20 17:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='category',
            field=models.ForeignKey(blank=True, help_text='Выберите категорию произведения', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='category', to='reviews.category', verbose_name='Категория произведения'),
        ),
    ]
