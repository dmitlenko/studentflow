from django import template
from ..models import ChatGroup

register = template.Library()

@register.filter
def other_participant(chat_group, current_user):
    if chat_group.private and chat_group.participants.count() == 2:
        participants = chat_group.participants.all()
        other_participant = participants.exclude(id=current_user.id).first()
        return other_participant
    else:
        return None