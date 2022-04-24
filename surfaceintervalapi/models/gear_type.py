from django.db import models


class Gear_Type(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    