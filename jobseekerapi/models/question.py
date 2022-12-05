from django.db import models

class Question(models.Model):
    """This class creates an instance a question. This class is only used in the context of an interviewPrep"""

    content = models.TextField(max_length=300)