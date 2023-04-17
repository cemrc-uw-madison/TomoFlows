from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from django.conf import settings
from datetime import datetime
import os
import json
from api.models import Project, Task, ProjectTask, Run
from api.serializers import ProjectSerializer, TaskSerializer, ProjectTaskSerializer, RunSerializer


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

@api_view(['GET', 'POST'])
@permission_classes((permissions.IsAuthenticated,))
def TaskList(request):
    """
    GET, POST /api/tasks
    """
    if request.method == 'GET':
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((permissions.IsAuthenticated,))
def TaskDetail(request, id):
    """
    GET, PUT, DELETE /api/tasks/<int:id>
    """
    try:
        task = Task.objects.get(pk=id)
    except Task.DoesNotExist:
        return Response({"detail": "Task not found with given id"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = TaskSerializer(task)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        task.delete()
        return Response({"detail": "Task deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
@permission_classes((permissions.IsAuthenticated,))
def ProjectTaskList(request):
    """
    GET, POST /api/project-tasks
    """
    if request.method == 'GET':
        project_id = request.query_params.get("project_id", "0")
    elif request.method == 'POST':
        project_id = request.data.get("project_id", "0")
    
    try:
        project = Project.objects.get(pk=project_id)
    except Project.DoesNotExist:
        return Response({"detail": "Project not found with given id"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        project_tasks = ProjectTask.objects.filter(project=project)
        serializer = ProjectTaskSerializer(project_tasks, many=True)
        data = serializer.data
        print(data[0]["parameters"])
        for i in range(len(data)):
            if data[i]["parameters"] is not None:
                data[i]["parameters"] = json.loads(data[i]["parameters"])
            try:
                run = Run.objects.get(project_task_id=data[i]["id"])
                run_serialized = RunSerializer(run)
                data[i]["run"] = run_serialized.data
                del data[i]["run"]["project_task"]
            except Run.DoesNotExist:
                data[i]["run"] = None
            
        return Response(data)

    elif request.method == 'POST':
        task_id = request.data.get("task_id", "0")
        try:
            task = Task.objects.get(pk=task_id)
        except Task.DoesNotExist:
            return Response({"detail": "Task not found with given id"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProjectTaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['project'] = project
            serializer.validated_data['task'] = task
            serializer.validated_data['parameters'] = json.dumps({})
            serializer.save()
            data = serializer.data
            data["parameters"] = json.loads(data["parameters"])
            run = Run.objects.create(project_task_id=data["id"], status="CREATED")
            run_serialized = RunSerializer(run)
            data["run"] = run_serialized.data
            del data["run"]["project_task"]
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((permissions.IsAuthenticated,))
def ProjectTaskDetail(request, id):
    """
    GET, PUT, DELETE /api/project-tasks/<int:id>
    """
    try:
        project_task = ProjectTask.objects.get(pk=id)
    except ProjectTask.DoesNotExist:
        return Response({"detail": "ProjectTask not found with given id"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = ProjectTaskSerializer(project_task)
        data = serializer.data
        data["parameters"] = json.loads(data["parameters"])
        try:
            run = Run.objects.get(project_task_id=data["id"])
            run_serialized = RunSerializer(run)
            data["run"] = run_serialized.data
            del data["run"]["project_task"]
        except Run.DoesNotExist:
            data["run"] = None
        return Response(data)
    elif request.method == 'PUT':
        serializer = ProjectTaskSerializer(project_task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            data["parameters"] = json.loads(data["parameters"])
            try:
                run = Run.objects.get(project_task_id=data["id"])
                run_serialized = RunSerializer(run)
                data["run"] = run_serialized.data
                del data["run"]["project_task"]
            except Run.DoesNotExist:
                data["run"] = None
            return Response(data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        project_task.delete()
        return Response({"detail": "ProjectTask deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
