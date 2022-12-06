from django.db import models


class Board(models.Model):
    """This class creates an instance of a (job) board"""

    seeker = models.ForeignKey("Seeker", on_delete=models.CASCADE, related_name="boards")
    title = models.CharField(max_length=50)
    goal = models.CharField(max_length=200)
    requirements = models.TextField(max_length=400)
    categories = models.ManyToManyField("Category", through="BoardCategory", related_name='categories')
