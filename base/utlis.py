import re
from .models import Post
from django.db.models import Q

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


def search_posts(posts, query_string):
    if not query_string:
        return posts

    params, search = extract_parameters(query_string)

    topic = params.get('topic')
    author = params.get('author')
    pinned = params.get('pinned')

    if pinned:
        posts = posts.filter(pinned=pinned)
    if topic:
        posts = posts.filter(topic__name__icontains=topic)
    if author:
        posts = posts.filter(author__username__icontains=author)
    if search:
        posts = posts.filter(Q(title__icontains=search) | Q(body__icontains=search))

    return posts