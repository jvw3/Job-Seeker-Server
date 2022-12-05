from django.db import models


class BoardJob(models.Model):
    """This class creates an instance a job ON a board"""


    job = models.ForeignKey("Job", on_delete=models.CASCADE)
    company = models.ForeignKey("Company", on_delete=models.CASCADE)
    prep = models.ForeignKey("InterviewPrep", on_delete=models.CASCADE)
    has_interviewed = models.BooleanField()
    interview_rounds = models.IntegerField()
    salary_rating = models.PositiveIntegerField(default=0, validators=[])
    location_rating = models.PositiveIntegerField(default=0, validators=[])
    culture_rating = models.PositiveIntegerField(default=0, validators=[])
    leadership_rating = models.PositiveIntegerField(default=0, validators=[])
    team_rating = models.PositiveIntegerField(default=0, validators=[])
    job_score = models.IntegerField()