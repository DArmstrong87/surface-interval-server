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
    def last_service_date(self):
        try:
            return GearItemService.objects.filter(gear_item=self).order_by("service_date").first().service_date
        except GearItemService.DoesNotExist:
            return None

    # Calculate dives or days since last service date.
    @property
    def dives_since_last_service(self):

        service_interval = self.service_interval()
        if service_interval is None:
            return None

        print(service_interval)

        count = None
        dives = []
        last_service_date = self.last_service_date
        purchase_date = service_interval.purchase_date

        # If no service date, get dives since purchase date.
        if last_service_date is None and purchase_date is not None:
            dives = Dive.objects.only("gear_set").filter(
                diver=self.diver, date__gte=purchase_date
            )
        # Get dives since last_service_date
        if last_service_date:
            dives = Dive.objects.only("gear_set").filter(
                diver=self.diver, date__gte=last_service_date
            )

        for dive in dives:
            if dive.gear_set and dive.gear_item == self:
                count += 1

        return count

    def days_since_last_service(self):
        item_service = GearItemService.objects.filter(gear_item=self).order_by("service_date").first()
        if item_service is not None:
            days = (timezone.now().date() - item_service.service_date).days
            return days
        else:
            return None

    @property
    def due_for_service_days(self) -> tuple[bool, int]:
        service_interval = self.service_interval()
        if service_interval is None:
            return None

        days_since_last_service = self.days_since_last_service()
        days_past_due_service = days_since_last_service - service_interval.days

        return days_past_due_service


    @property
    def due_for_service_dives(self):
        service_interval = self.service_interval()
        if service_interval is None:
            return None
        
        dives_past_due_service = self.dives_since_last_service - service_interval.dives

        return dives_past_due_service



    def __str__(self):
        return f"{self.pk} | {self.name}"
