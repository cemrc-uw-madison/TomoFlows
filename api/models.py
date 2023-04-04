from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager

class User(AbstractUser):
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()
    email = models.EmailField("Email Address", unique=True)

    def __str__(self):
        return self.email
    
class Project(models.Model):
    name = models.CharField("Name", max_length=25, unique=True)
    description = models.CharField("Description", max_length=100)
    folder_path = models.CharField("Folder Path", max_length=200, unique=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    last_updated = models.DateTimeField("Last Updated", blank=True)
