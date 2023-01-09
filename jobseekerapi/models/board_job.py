from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from .board import Board
from .priority_rank import PriorityRank


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
    work_status = models.CharField(max_length=50)
    salary_rating = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(10)])
    location_rating = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(10)])
    culture_rating = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(10)])
    leadership_rating = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(10)])
    team_rating = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(10)])
    board = models.ForeignKey("Board", on_delete=models.CASCADE, related_name="jobs")
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    tags = models.ManyToManyField("Tag", through="BoardJobTag", related_name='tags')


    @property
    def job_score(self):
        board = self.board
        ranks = PriorityRank.objects.filter(board=board.id)

        final_score = 0
        for priority_rank in ranks:
            if priority_rank.rank_value == 1:
                if priority_rank.name in "salary_rating":
                    adjusted_salary_score = self.salary_rating * 0.4
                    final_score += adjusted_salary_score
                
                elif priority_rank.name in "location_rating":
                    adjusted_location_score = self.location_rating * 0.4
                    final_score += adjusted_location_score
                
                elif priority_rank.name in "culture_rating":
                    adjusted_culture_score = self.culture_rating * 0.4
                    final_score += adjusted_culture_score
                
                elif priority_rank.name in "leadership_rating":
                    adjusted_leadership_score = self.leadership_rating * 0.4
                    final_score += adjusted_leadership_score
                
                elif priority_rank.name in "team_rating":
                    adjusted_team_score = self.team_rating * 0.4
                    final_score += adjusted_team_score



            elif priority_rank.rank_value == 2:
                if priority_rank.name in "salary_rating":
                    adjusted_salary_score = self.salary_rating * 0.3
                    final_score += adjusted_salary_score
                
                elif priority_rank.name in "location_rating":
                    adjusted_location_score = self.location_rating * 0.3
                    final_score += adjusted_location_score
                
                elif priority_rank.name in "culture_rating":
                    adjusted_culture_score = self.culture_rating * 0.3
                    final_score += adjusted_culture_score
                
                elif priority_rank.name in "leadership_rating":
                    adjusted_leadership_score = self.leadership_rating * 0.3
                    final_score += adjusted_leadership_score
                
                elif priority_rank.name in "team_rating":
                    adjusted_team_score = self.team_rating * 0.3
                    final_score += adjusted_team_score

            
            
            elif priority_rank.rank_value == 3:
                if priority_rank.name in "salary_rating":
                    adjusted_salary_score = self.salary_rating * 0.15
                    final_score += adjusted_salary_score
                
                elif priority_rank.name in "location_rating":
                    adjusted_location_score = self.location_rating * 0.15
                    final_score += adjusted_location_score
                
                elif priority_rank.name in "culture_rating":
                    adjusted_culture_score = self.culture_rating * 0.15
                    final_score += adjusted_culture_score
                
                elif priority_rank.name in "leadership_rating":
                    adjusted_leadership_score = self.leadership_rating * 0.15
                    final_score += adjusted_leadership_score
                
                elif priority_rank.name in "team_rating":
                    adjusted_team_score = self.team_rating * 0.15
                    final_score += adjusted_team_score




            elif priority_rank.rank_value == 4:
                if priority_rank.name in "salary_rating":
                    adjusted_salary_score = self.salary_rating * 0.10
                    final_score += adjusted_salary_score
                
                elif priority_rank.name in "location_rating":
                    adjusted_location_score = self.location_rating * 0.10
                    final_score += adjusted_location_score
                
                elif priority_rank.name in "culture_rating":
                    adjusted_culture_score = self.culture_rating * 0.10
                    final_score += adjusted_culture_score
                
                elif priority_rank.name in "leadership_rating":
                    adjusted_leadership_score = self.leadership_rating * 0.10
                    final_score += adjusted_leadership_score
                
                elif priority_rank.name in "team_rating":
                    adjusted_team_score = self.team_rating * 0.10
                    final_score += adjusted_team_score





            elif priority_rank.rank_value == 5:
                if priority_rank.name in "salary_rating":
                    adjusted_salary_score = self.salary_rating * 0.05
                    final_score += adjusted_salary_score
                
                elif priority_rank.name in "location_rating":
                    adjusted_location_score = self.location_rating * 0.05
                    final_score += adjusted_location_score
                
                elif priority_rank.name in "culture_rating":
                    adjusted_culture_score = self.culture_rating * 0.05
                    final_score += adjusted_culture_score
                
                elif priority_rank.name in "leadership_rating":
                    adjusted_leadership_score = self.leadership_rating * 0.05
                    final_score += adjusted_leadership_score
                
                elif priority_rank.name in "team_rating":
                    adjusted_team_score = self.team_rating * 0.05
                    final_score += adjusted_team_score
                

        return format(final_score, '.1f')