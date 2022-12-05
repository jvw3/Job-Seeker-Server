from django.db import models

class Interview(models.Model):
    """This class creates an instance of an interview"""

    board_job = models.ForeignKey("BoardJob", on_delete=models.CASCADE)
    date = models.DateTimeField()
    is_complete = models.BooleanField()
    interview_feedback = models.TextField(max_length=10000)