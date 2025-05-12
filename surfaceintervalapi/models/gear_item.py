from django.db import models
from django.utils import timezone

from surfaceintervalapi.models.dive import Dive
from surfaceintervalapi.models.gear_item_service import GearItemService, GearItemServiceInterval


class GearItem(models.Model):
    diver = models.ForeignKey("Diver", on_delete=models.CASCADE)
    gear_type = models.ForeignKey("GearType", on_delete=models.SET_NULL, blank=True, null=True)
    custom_gear_type = models.ForeignKey(
        "CustomGearType", on_delete=models.SET_NULL, blank=True, null=True
    )
    name = models.CharField(max_length=255)

    def service_interval(self):
        try:
            return GearItemServiceInterval.objects.get(gear_item=self)
        except GearItemServiceInterval.DoesNotExist:
            return None

    @property
    def last_service_date(self) -> str | None:
        item_service = (
            GearItemService.objects.filter(gear_item=self).order_by("service_date").first()
        )
        return None if item_service is None else item_service.service_date

    # Calculate dives or days since last service date.
    @property
    def dives_since_last_service(self) -> int:
        if self.service_interval() is None:
            return None

        count = 0
        dives = []
        last_service_date = self.last_service_date
        purchase_date = self.service_interval().purchase_date

        # If no service date, get dives since purchase date.
        if last_service_date is None and purchase_date is not None:
            dives = Dive.objects.only("gear_set").filter(diver=self.diver, date__gte=purchase_date)

        # Get dives since last_service_date
        if last_service_date:
            dives = Dive.objects.only("gear_set").filter(
                diver=self.diver, date__gte=last_service_date
            )

        for dive in dives:
            if dive.gear_set and self in dive.gear_set.gear_items.all():
                count += 1

        return count

    @property
    def days_since_last_service(self) -> int | None:
        days = None
        if self.last_service_date is not None:
            days = (timezone.now().date() - self.last_service_date).days
        elif self.service_interval() is not None:
            days = (timezone.now().date() - self.service_interval().purchase_date).days
        return days

    @property
    def due_for_service_days(self) -> tuple[bool, int]:
        service_interval = self.service_interval()
        days_since_last_service = self.days_since_last_service()
        if service_interval is None or days_since_last_service is None:
            return None

        days_past_due_service = days_since_last_service - service_interval.days

        return days_past_due_service

    @property
    def due_for_service_dives(self) -> int | None:
        days = None
        service_interval = self.service_interval()
        dives_since_last_service = self.dives_since_last_service
        if (
            service_interval is None
            or dives_since_last_service is None
            or service_interval.purchase_date is None
        ):
            return days

        gear_type_name = self.gear_type.name
        custom_gear_type_name = self.custom_gear_type.name if self.custom_gear_type else None

        items_to_service_every_100_dives = ["BCD", "Tank", "Regulator", "Octopus"]

        if (
            gear_type_name in items_to_service_every_100_dives
            or custom_gear_type_name in items_to_service_every_100_dives
        ):
            days_since = self.dives_since_last_service
            days = days_since - 100
        return days

    def __str__(self):
        return f"{self.name}"
