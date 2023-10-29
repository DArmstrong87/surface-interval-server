from django.db import models


class CertificationCard(models.Model):
    diver = models.ForeignKey("Diver", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    date_issued = models.DateField()
    image_front_url = models.URLField()
    image_back_url = models.URLField()

    def __str__(self):
        return f"{self.pk} | {self.name} | {self.diver.user.first_name} {self.diver.user.last_name}"
