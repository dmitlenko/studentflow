# Generated by Django 4.2 on 2023-05-08 15:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_post_arhived_post_date_archive_post_date_pinned_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='arhived',
            new_name='archived',
        ),
    ]
