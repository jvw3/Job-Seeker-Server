from django.db import models


class MeetingType(models.Model):
    """This class creates an instance of a meeting type. meeting types are only used in association with a network meeting"""

    name = models.CharField(max_length=100)