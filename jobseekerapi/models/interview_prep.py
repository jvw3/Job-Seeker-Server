from django.db import models


class InterviewPrep(models.Model):
    """This class creates an instance of an Interview Prep sheet"""

    seeker = models.ForeignKey("Seeker", on_delete=models.CASCADE)
    company_info = models.TextField(max_length=5000)
    elevator_pitch = models.TextField(max_length=500)