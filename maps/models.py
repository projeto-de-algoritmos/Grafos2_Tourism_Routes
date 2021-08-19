from django.db import models

# Create your models here.
class TouristAttraction(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)

    def __str__(self):
        return self.name