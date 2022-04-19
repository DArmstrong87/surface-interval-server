from django.db import models


class Dive_Specialty(models.Model):
    dive = models.ForeignKey('Dive', on_delete=models.CASCADE)
    specialty = models.ForeignKey(
        'Specialty', on_delete=models.CASCADE, null=True, blank=True)
    custom_specialty = models.ForeignKey(
        'Custom_Specialty', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        specialty = self.specialty if self.specialty is not None else self.custom_specialty
        return f'{self.pk} | Dive: {self.dive.pk} | {specialty.name}'