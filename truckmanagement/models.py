from django.db import models

class trucker(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100, default = "Unknown")
    role = models.CharField(max_length=100, default = "Unknown")
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

class LicensePlate(models.Model):
    state = models.CharField(max_length=100)
    plate_number = models.CharField(max_length=20)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.state} - {self.plate_number}"