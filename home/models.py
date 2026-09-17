from django.db import models


class SiteSetting(models.Model):
    cafe_name = models.CharField(max_length=100, default='Selin Coffee')
    tagline = models.CharField(
        max_length=200,
        default='A little cup of happiness.'
    )
    description = models.TextField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=255, blank=True)
    instagram = models.URLField(blank=True)

    def __str__(self):
        return self.cafe_name