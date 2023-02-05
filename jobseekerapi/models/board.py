from django.db import models
from .priority_rank import PriorityRank
import uuid

class Board(models.Model):
    """This class creates an instance of a (job) board"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seeker = models.ForeignKey("Seeker", on_delete=models.CASCADE, related_name="boards")
    title = models.CharField(max_length=50)
    goal = models.CharField(max_length=200)
    requirements = models.TextField(max_length=400)
    date_started = models.DateField()
    date_ended = models.DateField(null=True, blank=True, default=None)
    is_active = models.BooleanField()
    categories = models.ManyToManyField("Category", through="BoardCategory", related_name='categories')

    @property
    def board_application_count(self):
        all_jobs = self.jobs.all()
        interview_count = 0
        for job in all_jobs:
            if job.has_applied == True:
                interview_count += 1
        return interview_count

    @property
    def board_offer_count(self):
        all_jobs = self.jobs.all()
        offer_count = 0
        for job in all_jobs:
            if job.received_offer == True:
                offer_count += 1
        return offer_count

    @property
    def board_completed_interview_count(self):
        all_jobs = self.jobs.all()
        interview_count = 0
        for job in all_jobs:
            all_interviews = job.interviews.all()
            for interview in all_interviews:
                if interview.is_complete == True:
                    interview_count += 1
        return interview_count

    @property
    def board_offer_count(self):
        all_jobs = self.jobs.all()
        offer_count = 0
        for job in all_jobs:
            if job.received_offer == True:
                    offer_count += 1
        return offer_count

    # @property
    # def ordered_priorities(self):
    #     board_priorities = PriorityRank.objects.filter(board=self.id)
    #     board_priorities = board_priorities.objects.values_list('board_priorities', flat=True)
    #     updated_priorities = board_priorities.order_by("rank_value")
    #     return updated_priorities
