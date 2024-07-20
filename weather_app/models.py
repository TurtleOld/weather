from django.db import models


class CityCount(models.Model):
    city = models.CharField(max_length=100)
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.city
