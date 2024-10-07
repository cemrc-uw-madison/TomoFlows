from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from django.conf import settings
from datetime import datetime
from django.utils.timezone import now
import os
import json
import threading
import pytz
from api.models import User, Project, Task, ProjectTask, Run, OneTimePassword
from api.serializers import UserSerializer, ProjectSerializer, TaskSerializer, ProjectTaskSerializer, RunSerializer
from api.taskwrapper import task_handler
import scripts.program.scripts_constants as CONSTANTS
from django.db.models import Q

@api_view(['GET', 'PUT'])
@permission_classes((permissions.IsAuthenticated,))
def UserDetail(request):
    """
    GET, PUT /api/user
    """
    try:
        user = User.objects.get(pk=request.user.id)
    except User.DoesNotExist:
        return Response({"detail": "User not found with given id"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)
    elif request.method == 'PUT':
        data = dict(request.data)
        if 'email' in data:
            del data['email']
        data['email'] = request.user.email
        serializer = UserSerializer(user, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def IsAdmin(request):
    """
    GET /api/is-admin
    """
    try:
        if request.method == 'GET':
            email = request.GET.get("email")
            isAdmin = User.objects.get(email=email).is_staff
            return Response(isAdmin)
        else:
            return Response({"message": "missing user email!"})
    except Exception as err:
        return Response({"message": f"Unexpected {err=}, {type(err)=}"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def RequestAccount(request):
    """
    POST /api/request-account
    :payload {email, labName, institutionName}
    Disable account created from dj-rest-auth
    """
    try:
        if request.method == 'POST':
            email = request.data.get("email")
            labName = request.data.get("labName")
            institutionName = request.data.get("institutionName")
            if not email or not labName or not institutionName:
                return Response({"message": "missing user info!"}, status=status.HTTP_400_BAD_REQUEST)
            try:
                password = request.data.get("password")
                createdUser = User.objects.get(email=email)
                tempPassword = OneTimePassword.objects.create(user=createdUser, temp_password=password)
                tempPassword.save()
            except User.DoesNotExist:
                return Response({"message": "User not found with given email"}, status=status.HTTP_404_NOT_FOUND)
            if createdUser.is_active == False and createdUser.created == False:
                return Response({"message": "There is already an request related to this account"}, status=status.HTTP_400_BAD_REQUEST) 
            createdUser.is_active = False
            createdUser.labName = labName
            createdUser.institutionName = institutionName
            createdUser.save()
            return Response({"message": "request made successfully!"}, status=status.HTTP_200_OK)
    except Exception as err:
        return Response({"message": f"Unexpected {err=}, {type(err)=}"})

@api_view(['GET', 'POST', 'DELETE'])
@permission_classes((permissions.IsAuthenticated, permissions.IsAdminUser, ))
def CreateAccount(request):
    """
    GET /api/create-account
    """
    try:
        if request.method == 'GET':
            pendingCond = Q(is_active=False) & Q(created=False)
            pendingUser = User.objects.filter(pendingCond)
            serializer = UserSerializer(pendingUser, many=True)
            return Response(serializer.data[::-1])
        elif request.method == 'POST':
            email = request.data.get("email")
            pendingUser = User.objects.get(email=email)
            pendingUser.is_active = True
            pendingUser.created = True
            pendingUser.save()
            oneTimePassword = OneTimePassword.objects.get(user=pendingUser)
            password = oneTimePassword.temp_password
            return Response({"message": "account got approved", "password": password})
        elif request.method == 'DELETE':
            email = request.query_params["email"]
            pendingUser = User.objects.get(email=email)
            pendingUser.delete()
            return Response({"message": "account got rejected"})
    except Exception as err:
        return Response({"message": f"Unexpected {err=}, {type(err)=}"})



