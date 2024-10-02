from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager
from django.utils.timezone import now

class User(AbstractUser):
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()
    email = models.EmailField("Email Address", unique=True)
    labName = models.CharField(default="Unknown", max_length=50)
    institutionName = models.CharField(default="Unknown", max_length=50)
    created = models.BooleanField(default=False)
    def __str__(self):
        return self.email

class Project(models.Model):
    name = models.CharField("Name", max_length=25, unique=True)
    description = models.CharField("Description", max_length=100)
    folder_path = models.CharField("Folder Path", max_length=200, unique=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    first_created = models.DateTimeField("First Created", default=now)
    last_updated = models.DateTimeField("Last Updated", blank=True)
    
class Task(models.Model):
    name = models.CharField("Name",  max_length=25, unique=True)
    description = models.CharField("Description", max_length=100)
    parameter_fields = models.TextField("Parameter Fields", null=True, blank=True)
    
class ProjectTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    parameter_values = models.TextField("Parameter Values", null=True, blank=True)
    
class Run(models.Model):
    project_task = models.ForeignKey(ProjectTask, on_delete=models.CASCADE)
    status = models.CharField("Status", max_length=7, null=True, blank=True) # CREATED, RUNNING, SUCCESS, FAILED
    start_time = models.DateTimeField("Start Time", null=True, blank=True)
    end_time = models.DateTimeField("End Time", null=True, blank=True)
    logs = models.TextField("Logs", null=True, blank=True)
    errors = models.TextField("Errors", null=True, blank=True)
    output_files = models.TextField("Output Files", null=True, blank=True)

class OneTimePassword(models.Model):
    user_email = models.EmailField("Email Address", unique=True)
    temp_password = models.CharField(null=True, max_length=20)

class ProjectUser(models.Model):
    project = models.ForeignKey(Project, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    read_permission = models.BooleanField(default=False)
    write_permission = models.BooleanField(default=False)