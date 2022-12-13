from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class BoardJob(models.Model):
    """This class creates an instance a job ON a board"""


    job = models.ForeignKey("Job", on_delete=models.CASCADE)
    custom_job = models.CharField(max_length=100)
    company = models.ForeignKey("Company", on_delete=models.CASCADE)
    custom_company = models.CharField(max_length=100)
    has_applied = models.BooleanField()
    has_interviewed = models.BooleanField()
    interview_rounds = models.IntegerField(null=True, blank=True)
    received_offer = models.BooleanField()
    salary = models.IntegerField()
    location = models.CharField(max_length=70)
    salary_rating = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(10)])
    location_rating = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(10)])
    culture_rating = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(10)])
    leadership_rating = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(10)])
    team_rating = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(10)])
    job_score = models.IntegerField(null=True, blank=True)
    board = models.ForeignKey("Board", on_delete=models.CASCADE, related_name="jobs")
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    tags = models.ManyToManyField("Tag", through="BoardJobTag", related_name='tags')