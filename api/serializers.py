from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from api.models import User, Project


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
        fields = ['id', 'name', 'description', 'folder_path', 'owner', 'last_updated']
