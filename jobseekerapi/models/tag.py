from django.db import models


class Tag(models.Model):
    """This class creates an instance of a tag."""

    name = models.TextField(max_length=30)