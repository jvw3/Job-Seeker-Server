from django.db import models


class Job(models.Model):
    """This class creates an instance of a job. Only the title itself. All relevant information about unique jobs for the user is located in BoardJob."""

    title = models.CharField(max_length=100)