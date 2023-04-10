from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from django.conf import settings
from datetime import datetime
import os
from api.models import Project
from api.serializers import ProjectSerializer


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def Ping(request):
    """
    GET /api/ping
    """
    return Response({'message':'API is up and running!'})

@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def Protected(request):
    """
    GET /api/protected
    """
    return Response({'message':'This is a protected endpoint'})

@api_view(['GET', 'POST'])
@permission_classes((permissions.IsAuthenticated,))
def ProjectList(request):
    """
    GET, POST /api/projects
    """
    if request.method == 'GET':
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data[::-1])

    elif request.method == 'POST':
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['owner'] = request.user
            serializer.validated_data['last_updated'] = datetime.now()
            name = serializer.validated_data['name']
            path = os.path.join(settings.BASE_DIR, "data", name.lower().replace(' ', '-'))
            serializer.validated_data['folder_path'] = path
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((permissions.IsAuthenticated,))
def ProjectDetail(request, id):
    """
    GET, PUT, DELETE /api/projects/<int:id>
    """
    try:
        project = Project.objects.get(pk=id)
    except Project.DoesNotExist:
        return Response({"detail": "Project not found with given id"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = ProjectSerializer(project)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.validated_data['last_updated'] = datetime.now()
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        project.delete()
        return Response({"detail": "Project deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
