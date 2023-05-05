from django import template
from base.models import UserFollow, Post

register = template.Library()

@register.filter('is_followed')
def is_followed(user, follower):
    return UserFollow.objects.filter(user=user, follower=follower).exists()

@register.filter('is_liked')
def is_liked(post, user):
    return post.likes.filter(id=user.id).exists()