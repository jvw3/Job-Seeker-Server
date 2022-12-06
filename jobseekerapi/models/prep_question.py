from django.db import models


class PrepQuestion(models.Model):
    """This class creates an instance of the many to many relationship between an interviewPrep and a question"""

    prep = models.ForeignKey("InterviewPrep", on_delete=models.CASCADE)
    question = models.ForeignKey("Question", on_delete=models.CASCADE)