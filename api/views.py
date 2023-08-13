from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from django.conf import settings
from datetime import datetime
import os
import json
import threading
import pytz
from api.models import User, Project, Task, ProjectTask, Run
from api.serializers import UserSerializer, ProjectSerializer, TaskSerializer, ProjectTaskSerializer, RunSerializer
from api.taskwrapper import task_handler
from django.utils.timezone import now
from server.settings import DISK_MANAGER
VERIFICATION_CODE = "12345"

def generate_project_identifer(name, email, first_created):
    return name.lower().replace(' ', '-') + '-' + email.lower().replace(' ', '-') + '-' + first_created.strftime("%m:%d:%Y-%H:%M:%S").lower().replace(' ', '-')

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
            serializer.validated_data['last_updated'] = datetime.now().replace(tzinfo=pytz.utc)
            name = serializer.validated_data['name']
            first_created = now()
            project_identifer = name.lower().replace(' ', '-') + '-' + request.user.email.lower().replace(' ', '-') + '-' + first_created.strftime("%m:%d:%Y-%H:%M:%S").lower().replace(' ', '-')
            path = os.path.join(settings.BASE_DIR, "data", project_identifer)
            serializer.validated_data['folder_path'] = path
            serializer.save()
            DISK_MANAGER.create_project(project_identifer)
            # TODO: manager could create folders + serialize metadata.

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # TODO: return error handlding page
        print("invalid data")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((permissions.IsAuthenticated,))
def ProjectDetail(request, id):
    """
    GET, PUT, DELETE /api/projects/<int:id>
    """
    try:
        project = Project.objects.get(pk=id)
        project_identifier = generate_project_identifer(project.name, request.user.email, project.first_created)
    except Project.DoesNotExist:
        return Response({"detail": "Project not found with given id"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = ProjectSerializer(project)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.validated_data['last_updated'] = datetime.now().replace(tzinfo=pytz.utc)
            new_project_name = serializer.validated_data['name']
            new_project_description = serializer.validated_data['description']
            DISK_MANAGER.update_project(project_identifier, new_project_name, new_project_description)
            serializer.save()
            return Response(serializer.data)
        # TODO: error handling page
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        DISK_MANAGER.delete_project(project_identifier)
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
        data = serializer.data
        for i in range(len(data)):
            if data[i]["parameter_fields"] is not None:
                data[i]["parameter_fields"] = json.loads(data[i]["parameter_fields"])
        return Response(serializer.data)

    elif request.method == 'POST':
        if request.data.get("verification_code", "0") != VERIFICATION_CODE:
            return Response({"detail": "Incorrect verification code"}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            if 'parameter_fields' in serializer.validated_data:
                try:
                    json.loads(serializer.validated_data['parameter_fields'])
                except json.decoder.JSONDecodeError:
                    serializer.validated_data['parameter_fields'] = json.dumps([])
            else:
                serializer.validated_data['parameter_fields'] = json.dumps([])
            serializer.save()
            data = serializer.data
            print(data)
            data["parameter_fields"] = json.loads(data["parameter_fields"])
            return Response(data, status=status.HTTP_201_CREATED)
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
        data = serializer.data
        data["parameter_fields"] = json.loads(data["parameter_fields"])
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            if 'parameter_fields' in serializer.validated_data:
                try:
                    json.loads(serializer.validated_data['parameter_fields'])
                except json.decoder.JSONDecodeError:
                    serializer.validated_data['parameter_fields'] = json.dumps({})
            else:
                serializer.validated_data['parameter_fields'] = json.dumps({})
            serializer.save()
            data = serializer.data
            data["parameter_fields"] = json.loads(data["parameter_fields"])
            return Response(data)
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
        for i in range(len(data)):
            if data[i]["parameter_values"] is not None:
                data[i]["parameter_values"] = json.loads(data[i]["parameter_values"])
            try:
                run = Run.objects.get(project_task_id=data[i]["id"])
                run_serialized = RunSerializer(run)
                data[i]["run"] = run_serialized.data
                del data[i]["run"]["project_task"]
                data[i]["run"]["logs"] = json.loads(data[i]["run"]["logs"])
                data[i]["run"]["errors"] = json.loads(data[i]["run"]["errors"])
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
            if 'parameter_values' in serializer.validated_data:
                try:
                    json.loads(serializer.validated_data['parameter_values'])
                except json.decoder.JSONDecodeError:
                    serializer.validated_data['parameter_values'] = json.dumps([])
            else:
                serializer.validated_data['parameter_values'] = json.dumps([])
            serializer.save()

            # TODO: manager could create folders + serialize metadata.

            data = serializer.data
            data["parameter_values"] = json.loads(data["parameter_values"])
            run = Run.objects.create(project_task_id=data["id"], status="CREATED", logs="[]", errors="[]")
            run.project_task.project.last_updated = datetime.now().replace(tzinfo=pytz.utc)
            run.project_task.project.save()
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
        data["parameter_values"] = json.loads(data["parameter_values"])
        try:
            run = Run.objects.get(project_task_id=data["id"])
            run_serialized = RunSerializer(run)
            data["run"] = run_serialized.data
            del data["run"]["project_task"]
            data["run"]["logs"] = json.loads(data["run"]["logs"])
            data["run"]["errors"] = json.loads(data["run"]["errors"])
        except Run.DoesNotExist:
            data["run"] = None
        return Response(data)
    elif request.method == 'PUT':
        serializer = ProjectTaskSerializer(project_task, data=request.data)
        if serializer.is_valid():
            if 'parameter_values' in serializer.validated_data:
                try:
                    json.loads(serializer.validated_data['parameter_values'])
                except json.decoder.JSONDecodeError:
                    serializer.validated_data['parameter_values'] = json.dumps([])
            else:
                serializer.validated_data['parameter_values'] = json.dumps([])
            serializer.save()
            data = serializer.data
            data["parameter_values"] = json.loads(data["parameter_values"])
            project_task.project.last_updated = datetime.now().replace(tzinfo=pytz.utc)
            project_task.project.save()
            try:
                run = Run.objects.get(project_task_id=data["id"])
                run_serialized = RunSerializer(run)
                data["run"] = run_serialized.data
                del data["run"]["project_task"]
                data["run"]["logs"] = json.loads(data["run"]["logs"])
                data["run"]["errors"] = json.loads(data["run"]["errors"])
            except Run.DoesNotExist:
                data["run"] = None
            return Response(data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        project_task.project.last_updated = datetime.now().replace(tzinfo=pytz.utc)
        project_task.project.save()
        project_task.delete()
        return Response({"detail": "ProjectTask deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def RunProjectTask(request, id):
    """
    GET /api/run-project-task/<int:id>
    """
    try:
        project_task = ProjectTask.objects.get(pk=id)
        run = Run.objects.get(project_task=project_task)
    except ProjectTask.DoesNotExist:
        return Response({"detail": "ProjectTask not found with given id"}, status=status.HTTP_404_NOT_FOUND)
    
    if run.status == "RUNNING":
        return Response({"detail": "Task already running"}, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'GET':
        starter = threading.Thread(target=start_task, name=f"StartTask-{id}", args=[id])
        starter.start()
        run.status = "RUNNING"
        run.start_time = datetime.now().replace(tzinfo=pytz.utc)
        run.save()
        run.project_task.project.last_updated = datetime.now().replace(tzinfo=pytz.utc)
        run.project_task.project.save()
        serializer = ProjectTaskSerializer(project_task)
        data = serializer.data
        data["parameter_values"] = json.loads(data["parameter_values"])
        data["run"] = RunSerializer(run).data
        data["run"]["logs"] = json.loads(data["run"]["logs"])
        data["run"]["errors"] = json.loads(data["run"]["errors"])
        del data["run"]["project_task"]
        return Response(data)

def start_task(project_task_id):
    project_task = ProjectTask.objects.get(pk=project_task_id)
    run = Run.objects.get(project_task=project_task)
    task_handler(project_task, run)
    
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
