from django.db import models


class GearItemServiceInterval(models.Model):
    gear_item = models.ForeignKey("GearItem", on_delete=models.CASCADE)
    purchase_date = models.DateField(blank=True, null=True)
    dives = models.IntegerField()
    days = models.IntegerField()

class GearItemService(models.Model):
    gear_item = models.ForeignKey("GearItem", on_delete=models.CASCADE)
    service_date = models.DateField()
