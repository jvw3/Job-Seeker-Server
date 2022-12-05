from django.db import models

class JobTag(models.Model):
    """This class creates an instance of the many to many relationship between a job and a tag"""

    board_job = models.ForeignKey('BoardJob', on_delete=models.CASCADE)
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE)