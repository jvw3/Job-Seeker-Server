from django.db import models
import uuid

class InterviewPrep(models.Model):
    """This class creates an instance of an Interview Prep sheet"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seeker = models.ForeignKey("Seeker", on_delete=models.CASCADE)
    company_info = models.TextField(max_length=5000)
    questions = models.ManyToManyField("Question", through="PrepQuestion", related_name="questions")