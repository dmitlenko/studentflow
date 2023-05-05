from django import template
from base.models import UserFollow

register = template.Library()

@register.filter('is_followed')
def is_followed(user, follower):
    return UserFollow.objects.filter(user=user, follower=follower).exists()