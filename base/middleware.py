from django.http import HttpResponse
from rest_framework.authtoken.models import Token

class TokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'token' not in request.COOKIES:
            response = HttpResponse()
            token, created = Token.objects.get_or_create(user=request.user)
            response.set_cookie('token', token.key)
        else:
            # Token cookie already exists, continue with the request
            response = self.get_response(request)

        response.set_cookie('user_id', request.user.id)
        
        return response