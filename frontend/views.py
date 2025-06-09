from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from server.settings import USER_RELATIVE_PATH

@ensure_csrf_cookie
def index(request):
    prefix = USER_RELATIVE_PATH
    response = render(request, 'frontend/index.html')
    response.set_cookie('BASE_PREFIX', prefix, path='/', samesite='Lax')
    return response
