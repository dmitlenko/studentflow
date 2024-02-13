from django.http import HttpResponse
from rest_framework.authtoken.models import Token

class TokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if response.cookies.get('token') and response.cookies.get('user_id') == request.user.id:
            return response
        
        if request.user.is_authenticated:
            token, created = Token.objects.get_or_create(user=request.user)
            response.set_cookie('token', token.key)
            response.set_cookie('user_id', request.user.id)
            
        return response