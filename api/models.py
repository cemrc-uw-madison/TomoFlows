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
    
class Task(models.Model):
    name = models.CharField("Name",  max_length=25, unique=True)
    description = models.CharField("Description", max_length=100)
    
class ProjectTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    parameters = models.TextField("Parameters", null=True, blank=True)
    
class Run(models.Model):
    project_task = models.ForeignKey(ProjectTask, on_delete=models.CASCADE)
    status = models.CharField("Status", max_length=7, null=True, blank=True) # CREATED, RUNNING, SUCCESS, FAILED
    start_time = models.DateTimeField("Start Time", null=True, blank=True)
    end_time = models.DateTimeField("End Time", null=True, blank=True)
    logs = models.TextField("Logs", null=True, blank=True)
    errors = models.TextField("Errors", null=True, blank=True)
