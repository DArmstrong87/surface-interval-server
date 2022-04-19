from django.db import models



class Favorite_Dive(models.Model):
    diver = models.ForeignKey('Diver', on_delete=models.CASCADE)
    dive = models.ForeignKey('Dive', on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.pk} | Dive: {self.dive.pk} | {self.diver.user.first_name} {self.diver.user.last_name}'