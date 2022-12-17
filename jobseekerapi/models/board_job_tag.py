from django.db import models


class BoardJobTag(models.Model):
    """This class creates an instance of a category. Categories are only used in association with a (job) board."""

    board_job = models.ForeignKey('BoardJob', on_delete=models.CASCADE)
    tag = models.ForeignKey("Tag", on_delete=models.CASCADE)