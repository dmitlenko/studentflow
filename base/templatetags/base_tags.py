from django import template
from base.models import UserFollow, Post
from django.template.loader import render_to_string

register = template.Library()

@register.filter('is_followed')
def is_followed(user, follower):
    return UserFollow.objects.filter(user=user, follower=follower).exists()

@register.filter('is_liked')
def is_liked(post, user):
    return post.likes.filter(id=user.id).exists()

@register.filter('post_card')
def post_card(post, prefix=''):
    return render_to_string('base/items/post_card.html', {'post': post, 'prefix':prefix})

@register.filter('followers')
def followers(user):
    return UserFollow.objects.filter(user=user).count()

@register.filter('following')
def followers(user):
    return UserFollow.objects.filter(follower=user).count()