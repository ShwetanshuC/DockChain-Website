from django.db import models

class trucker(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100, default = "Unknown")
    role = models.CharField(max_length=100, default = "Unknown")
    organization = models.CharField(max_length=100, default = "Unknown")
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
    port_location = models.CharField(max_length=50, default='Unknown')
    job_type = models.CharField(choices=[('HYBRID', 'Hybrid'), ('PICKUP', 'Pickup'), ('DELIVERY', 'Delivery')], default='PICKUP', max_length=10)
    cargo_id = models.CharField(max_length=50, default='Unknown')
    description = models.TextField(max_length=30, blank=True, default='Unknown')
    status = models.CharField(max_length=10, default='Pending')  # e.g., Pending, Approved, Denied, InProgress, SecurityCleared, CargoPickedUp, Completed
    timestamp = models.DateTimeField(auto_now_add=True)  # store when the job was started
    approval_timestamp = models.DateTimeField(null=True)  # store when the job was approved
    target_timestamp = models.DateTimeField(null=True)  # store when the job is expected to be completed
    completed_timestamp = models.DateTimeField(null=True)
    def __str__(self):
        return f"{self.driver.firstname} {self.driver.lastname} - {self.license_plate.plate_number}. {self.status}"