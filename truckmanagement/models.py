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
    
class Job(models.Model):
    driver = models.ForeignKey(trucker, on_delete=models.CASCADE)
    license_plate = models.ForeignKey(LicensePlate, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)  # store when the job was started

    def __str__(self):
        return f"{self.driver.firstname} {self.driver.lastname} - {self.license_plate.plate_number}"