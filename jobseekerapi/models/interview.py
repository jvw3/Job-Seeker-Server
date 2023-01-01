from django.db import models

class Interview(models.Model):
    """This class creates an instance of an interview"""

    seeker = models.ForeignKey("Seeker", on_delete=models.CASCADE, related_name="interviews")
    board_job = models.ForeignKey("BoardJob", on_delete=models.CASCADE, related_name="interviews")
    prep = models.OneToOneField("InterviewPrep", on_delete=models.CASCADE, related_name="interview", null=True, blank=True)
    date = models.DateTimeField()
    is_complete = models.BooleanField()
    interview_feedback = models.TextField(max_length=10000, blank=True)