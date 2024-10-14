from django import template
from base.models import UserFollow, Post
from django.template.loader import render_to_string
from base.utils import themes_list

register = template.Library()

@register.filter('is_followed')
def is_followed(user, follower):
    return UserFollow.objects.filter(user=user, follower=follower).exists()

@register.filter('is_liked')
def is_liked(post, user):
    return post.likes.filter(id=user.id).exists()

@register.filter('followers')
def followers(user):
    return UserFollow.objects.filter(user=user)

@register.filter('following')
def following(user):
    return UserFollow.objects.filter(follower=user)

@register.filter('followers_count')
def followers_count(user):
    return followers(user).count()

@register.filter('following_count')
def following_count(user):
    return following(user).count()

@register.filter('percent')
def percent(value, max):
    return int((value / max) * 100)

@register.filter
def valid_theme(theme_name):
    return theme_name in themes_list()

@register.filter
def get_themes_list(dummy):
    return themes_list()

@register.filter
def user_in(user, manytomany):
    return user in manytomany.all()