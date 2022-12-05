from django.db import models


class Board(models.Model):
    """This class creates an instance of a (job) board"""

    seeker = models.ForeignKey("Seeker", on_delete=models.CASCADE)
    title = models.TextField()
    goal = models.TextField()
    requirements = models.TextField()