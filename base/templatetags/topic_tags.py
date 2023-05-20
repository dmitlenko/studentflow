from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def without_topic(query, topic):
    if not query.replace(',', ''):
        return '?topic'
    res = [item for item in query.split(',') if item != topic]
    return f'?topic={",".join(res)}'


@register.filter
@stringfilter
def with_topic(query, topic):
    arr = query.split(',') if query else []
    arr.append(topic)

    return f'?topic={",".join(arr)}'


@register.simple_tag
def show_if_topic(query, topics):
    topics = [topic.name for topic in topics]
    if query:
        query = query.split(',')

        for topic in query:
            if topic in topics:
                return 'show'
    return ''