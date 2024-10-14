from rest_framework import serializers, exceptions
from dj_rest_auth.registration.serializers import RegisterSerializer
from api.models import User, Project, Task, ProjectTask, Run
from dj_rest_auth.serializers import LoginSerializer

class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'labName', 'institutionName', 'date_joined']

class CustomLoginSerializer(LoginSerializer):
    def _validate_created(self, email):
        if email:
            try:
                user = User.objects.get(email=email)
                if not user.created and not user.is_superuser:
                    return None
                else:
                    return user
            except:
                raise exceptions.ValidationError("User does not exist")
            
    def validate(self, attrs):
        user = self._validate_created(attrs.get("email"))
        if not user:
            raise exceptions.ValidationError("Request is pending, please contact the admin")
        return super().validate(attrs)

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
        fields = ['id', 'project_task', 'status', 'start_time', 'end_time', 'logs', 'errors', 'output_files']
