from django.db import models

class Company(models.Model):
    """This class creates an instance of a company. A company resource is only used in association with a BoardJob """

    name = models.CharField(max_length=80)