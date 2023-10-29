from django.db import models


class Image(models.Model):
    diver = models.ForeignKey("Diver", on_delete=models.CASCADE)
    dive = models.ForeignKey("Dive", on_delete=models.CASCADE)
    url = models.URLField()
