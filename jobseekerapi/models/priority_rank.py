from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class PriorityRank(models.Model):
    """This class creates an instance of a priority rank for a board"""

    board = models.ForeignKey("Board", on_delete=models.CASCADE)
    salary = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])
    location = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])
    culture = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])
    leadership = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])
    team = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])