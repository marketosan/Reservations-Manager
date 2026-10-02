from django.db import models


class Property(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=255, blank=True)
    ical_url = models.URLField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Reservation(models.Model):
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name="reservations"
    )
    uid = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    summary = models.CharField(max_length=255, blank=True)
    synced_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("property", "uid")

    def __str__(self):
        return f"{self.property.name}: {self.start_date} to {self.end_date}"
