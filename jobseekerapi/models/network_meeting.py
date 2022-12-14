from django.db import models

class NetworkMeeting(models.Model):
    """This class creates an instance of a company. A company resource is only used in association with a BoardJob """

    contact = models.ForeignKey("Contact", on_delete=models.CASCADE, related_name="meetings")
    description = models.CharField(max_length=500)
    meeting_date = models.DateTimeField()
    notes = models.TextField(max_length=10000, blank=True)
    is_complete = models.BooleanField()
    meeting_type = models.ForeignKey("MeetingType", on_delete=models.CASCADE)