from django.db import models

class CustomPrepInfo(models.Model):
    """This class creates an instance of a Custom prep info. This is customized content that the user can add to their interview prep sheet."""

    interview_prep_id = models.ForeignKey("InterviewPrep", on_delete=models.CASCADE)
    title = models.TextField(max_length=50)
    description = models.TextField(max_length=300)
    content = models.TextField(max_length=10000)