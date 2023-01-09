from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class PriorityRank(models.Model):
    """This class creates an instance of a priority rank for a board"""

    board = models.ForeignKey("Board", on_delete=models.CASCADE, related_name="priorities")
    name = models.CharField(max_length=20)
    rank_value = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])
