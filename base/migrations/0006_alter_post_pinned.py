# Generated by Django 4.2 on 2023-05-07 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_post_published'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='pinned',
            field=models.BooleanField(default=False, verbose_name='Закріпити'),
        ),
    ]
