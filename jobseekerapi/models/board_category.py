from django.db import models

class BoardCategory(models.Model):
    """This class creates an instance of the many to many relationship between a (job) board and a category"""

    board = models.ForeignKey('Board', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)