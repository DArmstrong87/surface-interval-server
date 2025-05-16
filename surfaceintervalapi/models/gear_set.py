from django.db import models

# from django.contrib.postgres.fields import ArrayField


class GearSet(models.Model):
    diver = models.ForeignKey("Diver", on_delete=models.CASCADE)
    name = models.CharField(max_length=50, default="GearSet")
    gear_items = models.ManyToManyField("GearItem", related_name="gear_sets")
    weight = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.pk} | {self.name} by {self.diver.user.first_name}"
