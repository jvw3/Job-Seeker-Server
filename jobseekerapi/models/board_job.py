from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class BoardJob(models.Model):
    """This class creates an instance a job ON a board"""


    job = models.ForeignKey("Job", on_delete=models.CASCADE)
    company = models.ForeignKey("Company", on_delete=models.CASCADE)
    has_interviewed = models.BooleanField()
    interview_rounds = models.IntegerField(null=True, blank=True)
    salary_rating = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(10)])
    location_rating = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(10)])
    culture_rating = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(10)])
    leadership_rating = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(10)])
    team_rating = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(10)])
    job_score = models.IntegerField(null=True, blank=True)
    board = models.ForeignKey("Board", on_delete=models.CASCADE, related_name="jobs")