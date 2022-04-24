from django.db import models


class Custom_Gear_Type(models.Model):
    diver = models.ForeignKey('Diver', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return f'{self.pk} | {self.name} | {self.diver.user.first_name} {self.diver.user.last_name}'