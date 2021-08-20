from django.db import models


class TouristAttraction(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)
    selected = models.BooleanField(default=False)

    def __str__(self):
        return self.name