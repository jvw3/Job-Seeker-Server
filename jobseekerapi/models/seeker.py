from django.db import models
from django.contrib.auth.models import User

class Seeker(models.Model):
    """This class creates an instance of a Seeker (the application User) for JobSeeker Application"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=5000)
    current_role = models.CharField(max_length=100)
    elevator_pitch = models.TextField(max_length=1000, null=True, blank=True)
    is_admin = models.BooleanField()

    @property
    def full_name(self):
        return f'{self.user.first_name}{self.user.last_name}'

    @property
    def username(self):
        return f'{self.user.username}'