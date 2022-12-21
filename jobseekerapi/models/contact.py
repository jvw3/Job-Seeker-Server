from django.db import models

class Contact(models.Model):
    """This class creates an instance of a company. A company resource is only used in association with a BoardJob """

    name = models.CharField(max_length=80)
    current_role = models.CharField(max_length=150)
    current_company = models.CharField(max_length=150)
    last_contact = models.DateField()
    number_of_contacts = models.IntegerField()
    connection_level = models.IntegerField()
    linked_in = models.CharField(max_length=500)
    notes = models.CharField(max_length=500)
    seeker = models.ForeignKey("Seeker", on_delete=models.CASCADE, related_name="contacts")