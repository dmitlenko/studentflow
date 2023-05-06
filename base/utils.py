import re

from django.core.exceptions import ValidationError
from django.db.models import Q
from datetime import datetime

def extract_parameters(input_string):
    pattern = r'(\w+):"([^"]*)"'
    matches = re.findall(pattern, input_string)
    parameters = {}

    for match in matches:
        parameter_name = match[0]
        parameter_value = match[1]
        parameters[parameter_name] = parameter_value
    remaining_text = re.sub(pattern, '', input_string).strip()

    return parameters, remaining_text


def fail_safe_date(date_string, default=None):
    try:
        return datetime.strptime(date_string, "%d.%m.%Y").date()
    except:
        return default


def search_posts(posts, query_string):
    if not query_string:
        return posts

    params, search = extract_parameters(query_string)

    topic = params.get('topic')
    author = params.get('author')
    pinned = params.get('pinned')
    after = fail_safe_date(params.get('after'))
    before = fail_safe_date(params.get('before'))

    if after:
        posts = posts.filter(date_created__gte=after)
    if before:
        posts = posts.filter(date_created__lte=before)
    if pinned:
        posts = posts.filter(pinned=pinned)
    if topic:
        posts = posts.filter(topic__name__icontains=topic)
    if author:
        posts = posts.filter(author__username__icontains=author)
    if search:
        posts = posts.filter(Q(title__icontains=search) | Q(body__icontains=search))

    return posts


def validate_file_size(fieldfile_obj):
        filesize = fieldfile_obj.file.size
        megabyte_limit = 5.0
        if filesize > megabyte_limit*1024*1024:
            raise ValidationError("Max file size is %sMB" % str(megabyte_limit))