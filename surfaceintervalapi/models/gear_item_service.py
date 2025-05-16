from django.db import models


class GearItemServiceInterval(models.Model):
    gear_item = models.ForeignKey("GearItem", on_delete=models.CASCADE)
    purchase_date = models.DateField(blank=True, null=True)
    dive_interval = models.IntegerField()
    day_interval = models.IntegerField()

    def __str__(self):
        return f"{self.gear_item.name} | Service after {self.dive_interval} dives or {self.day_interval} days."


class GearItemService(models.Model):
    gear_item = models.ForeignKey("GearItem", on_delete=models.CASCADE)
    service_date = models.DateField()

    def __str__(self):
        return f"{self.gear_item.name} | {self.service_date}"
