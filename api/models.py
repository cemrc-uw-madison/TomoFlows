from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from .managers import UserManager

class User(AbstractUser):
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    email = models.EmailField(_('email address'), unique=True)    
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.email
