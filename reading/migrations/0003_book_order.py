# Generated by Django 5.1.3 on 2024-12-13 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reading', '0002_book_book_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='order',
            field=models.PositiveSmallIntegerField(default=1),
            preserve_default=False,
        ),
    ]
