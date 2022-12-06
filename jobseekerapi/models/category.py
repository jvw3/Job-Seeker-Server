from django.db import models


class Category(models.Model):
    """This class creates an instance of a category. Categories are only used in association with a (job) board."""

    name = models.CharField(max_length=30)