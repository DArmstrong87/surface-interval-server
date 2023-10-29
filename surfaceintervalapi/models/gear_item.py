from django.db import models
from django.utils import timezone

from surfaceintervalapi.models.dive import Dive


class GearItem(models.Model):
    diver = models.ForeignKey("Diver", on_delete=models.CASCADE)
    gear_type = models.ForeignKey("GearType", on_delete=models.SET_NULL, blank=True, null=True)
    custom_gear_type = models.ForeignKey(
        "CustomGearType", on_delete=models.SET_NULL, blank=True, null=True
    )
    name = models.CharField(max_length=200)
    purchase_date = models.DateField(blank=True, null=True)
    last_serviced = models.DateField(blank=True, null=True)

    # If an item was recently serviced, calculate dives or days since that date.
    @property
    def dives_since_last_service(self):
        count = 0

        if self.last_serviced is None and self.purchase_date:
            dives = Dive.objects.only("gear_set").filter(
                diver=self.diver, date__gte=self.purchase_date
            )
        elif self.last_serviced:
            dives = Dive.objects.only("gear_set").filter(
                diver=self.diver, date__gte=self.last_serviced
            )
        else:
            pass

        if self.purchase_date:
            for dive in dives:
                bcd = dive.gear_set.bcd
                regulator = dive.gear_set.regulator
                octopus = dive.gear_set.octopus
                tank = dive.gear_set.tank
                if self in [bcd, regulator, octopus, tank]:
                    count += 1

        return count

    @property
    def days_since_last_service(self):
        if self.last_serviced is not None:
            days = (timezone.now().date() - self.last_serviced).days
            return days
        else:
            return None

    @property
    def due_for_service_days(self):
        if self.purchase_date is not None and self.days_since_last_service is not None:
            gear_type = self.gear_type.name

            if gear_type in ["BCD", "Tank", "Regulator", "Octopus"]:
                dives_since = self.days_since_last_service
                dives = dives_since - 365
                return dives
            else:
                return None
        else:
            return None

    @property
    def due_for_service_dives(self):
        if self.purchase_date is not None:
            gear_type = self.gear_type.name

            if gear_type in ["BCD", "Tank", "Regulator", "Octopus"]:
                days_since = self.dives_since_last_service
                days = days_since - 100
                return days
            else:
                return None
        else:
            return None

    def __str__(self):
        return f"{self.pk} | {self.name}"
