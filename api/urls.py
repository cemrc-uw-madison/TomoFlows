from django.urls import path, include
from allauth.account.views import confirm_email
# from django.conf.urls import url
from django.contrib import admin
from .views import Ping, Protected, ProjectList, ProjectDetail, TaskList, TaskDetail, ProjectTaskList, ProjectTaskDetail

urlpatterns = [
    path('ping', Ping),
    path('protected', Protected),
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/register/', include('dj_rest_auth.registration.urls')),
    path('projects', ProjectList),
    path('projects/<int:id>', ProjectDetail),
    path('tasks', TaskList),
    path('tasks/<int:id>', TaskDetail),
    path('project-tasks', ProjectTaskList),
    path('project-tasks/<int:id>', ProjectTaskDetail),
    # url(r'^account/', include('allauth.urls')),
    # url(r'^confirm-email/(?P<key>.+)/$', confirm_email, name='account_confirm_email'),
]
