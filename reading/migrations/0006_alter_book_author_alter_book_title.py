# Generated by Django 5.1.3 on 2024-12-13 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reading', '0005_alter_book_cover'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.CharField(max_length=75),
        ),
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(max_length=75),
        ),
    ]
