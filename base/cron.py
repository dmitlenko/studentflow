from datetime import datetime
from .models import Post


def man_unpin_posts():
    objects = Post.objects.filter(pinned=True, date_unpinned__isnull=False)
    for obj in objects:
        if obj.date_unpinned <= datetime.now():
            obj.pinned = False
            obj.save()


def man_pin_posts():
    objects = Post.objects.filter(pinned=False, date_pinned__isnull=False)
    for obj in objects:
        if obj.date_pinned <= datetime.now():
            obj.pinned = True
            obj.save()


def man_archive_posts():
    objects = Post.opbjects.filter(archived=False, date_archived__isnull=False)
    for obj in objects:
        if obj.date_archived <= datetime.now():
            obj.archived = True
            obj.save()


def man_publish_posts():
    objects = Post.opbjects.filter(published=False, date_published__isnull=False)
    for obj in objects:
        if obj.date_published <= datetime.now():
            obj.published = True
            obj.save()