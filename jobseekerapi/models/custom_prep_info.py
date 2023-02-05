from django.db import models
import uuid

class CustomPrepInfo(models.Model):
    """This class creates an instance of a Custom prep info. This is customized content that the user can add to their interview prep sheet."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    prep = models.ForeignKey("InterviewPrep", on_delete=models.CASCADE, related_name="custom_preps")
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=300)
    content = models.TextField(max_length=10000)