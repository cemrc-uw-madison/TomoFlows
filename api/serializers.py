from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from api.models import User, Project, Task, ProjectTask, Run


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name']

class RegistrationSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

    def custom_signup(self, request, user):
        user.first_name = self.validated_data.get('first_name', '')
        user.last_name = self.validated_data.get('last_name', '')
        user.save(update_fields=['first_name', 'last_name'])
        
class ProjectSerializer(serializers.ModelSerializer):
    owner = UserSerializer(required=False)
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'folder_path', 'owner', 'last_updated', 'first_created']
    
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'parameter_fields']
    
class ProjectTaskSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(required=False)
    task = TaskSerializer(required=False)
    class Meta:
        model = ProjectTask
        fields = ['id', 'project', 'task', 'parameter_values']
        
class RunSerializer(serializers.ModelSerializer):
    project_task = ProjectTaskSerializer(required=False)
    class Meta:
        model = Run
        fields = ['id', 'project_task', 'status', 'start_time', 'end_time', 'logs', 'errors']
