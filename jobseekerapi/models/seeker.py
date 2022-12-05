from django.db import models
from django.contrib.auth.models import User

class Seeker(models.Model):
    """This class creates an instance of a Seeker (the application User) for JobSeeker Application"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    current_role = models.TextField()
    is_admin = models.BooleanField()
