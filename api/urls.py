from django.urls import path, include
from allauth.account.views import confirm_email
# from django.conf.urls import url
from django.contrib import admin
from .views import Ping, Protected

urlpatterns = [
    path('ping', Ping),
    path('protected', Protected),
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/signup/', include('dj_rest_auth.registration.urls')),
    # url(r'^account/', include('allauth.urls')),
    # url(r'^confirm-email/(?P<key>.+)/$', confirm_email, name='account_confirm_email'),
]
