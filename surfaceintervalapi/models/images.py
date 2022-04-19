from django.db import models


class Images(models.Model):
    dive = models.ForeignKey('Dive', on_delete=models.CASCADE)
    url = models.URLField()