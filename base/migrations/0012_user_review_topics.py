# Generated by Django 4.2 on 2023-05-22 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_user_image_banner_alter_post_published_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='review_topics',
            field=models.ManyToManyField(blank=True, related_name='review_topics', to='base.posttopic'),
        ),
    ]
