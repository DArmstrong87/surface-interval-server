from django.db import models


class GearDive(models.Model):
    """
    For tracking gear use in order to determine service.
    If a GearItem or Dive is deleted, the Gear usage or GearDive is deleted as well.

    GearSets may change and an item may be removed from the set entirely.
    This model ensures the gear item is always tied to a Dive, even when GearSets change.
    """

    gear_item = models.ForeignKey("GearItem", on_delete=models.CASCADE)
    dive = models.ForeignKey("Dive", on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.gear_item.name} | {self.dive.date}"
