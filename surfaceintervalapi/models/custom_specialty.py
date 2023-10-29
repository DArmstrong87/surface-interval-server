from django.db import models


class CustomSpecialty(models.Model):
    diver = models.ForeignKey("Diver", on_delete=models.CASCADE)
    name = models.CharField(max_length=25)

    def __str__(self):
        return f"{self.pk} | {self.name} | {self.diver.user.first_name} {self.diver.user.last_name}"
