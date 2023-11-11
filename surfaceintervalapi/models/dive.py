from django.db import models

from surfaceintervalapi.models.favorite_dive import FavoriteDive
from surfaceintervalapi.models.dive_specialty import DiveSpecialty


class Dive(models.Model):
    diver = models.ForeignKey("Diver", on_delete=models.CASCADE)
    date = models.DateField()
    gear_set = models.ForeignKey("GearSet", on_delete=models.DO_NOTHING, null=True)
    location = models.CharField(max_length=255)
    site = models.CharField(max_length=255)
    water = models.CharField(max_length=6, choices=[("Salt", "salt"), ("Fresh", "fresh")])
    depth = models.IntegerField()
    time = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    start_pressure = models.IntegerField(blank=True, null=True)
    end_pressure = models.IntegerField(blank=True, null=True)
    tank_vol = models.FloatField(default=80, blank=True, null=True)

    @property
    def air_consumption(self):
        """
        Calculates air consumption in psi or bar per minute.
        Accounts for user's unit preferences.
        """
        air_consumed = None
        if (
            self.start_pressure is not None
            and self.end_pressure is not None
            and self.tank_vol is not None
        ):
            units = self.diver.units
            atm = 33 if units == "imperial" else 10
            bar_atm = (self.depth / atm) + 1
            psi_consumed = self.start_pressure - self.end_pressure
            working_pressure = self.start_pressure
            air_consumed = (self.tank_vol * psi_consumed) / working_pressure / self.time / bar_atm
            return round(air_consumed, 3)
        return None

    @property
    def favorite(self):
        return True if FavoriteDive.objects.filter(dive=self).exists() else False

    @property
    def specialties(self):
        dive_specialties = (
            DiveSpecialty.objects.only("specialty").filter(dive=self.id).values("specialty__name")
        )
        specialties = [ds["specialty__name"] for ds in dive_specialties]
        return specialties

    def __str__(self):
        return f"{self.pk} | {self.site} | {self.diver.user.first_name} {self.diver.user.last_name}"
