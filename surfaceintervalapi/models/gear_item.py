from django.db import models
from django.utils import timezone
from typing import Optional, List
from datetime import date

from surfaceintervalapi.models.gear_item_service import GearItemService, GearItemServiceInterval
from surfaceintervalapi.models import GearDive


class GearItem(models.Model):
    diver = models.ForeignKey("Diver", on_delete=models.CASCADE)
    gear_type = models.ForeignKey("GearType", on_delete=models.SET_NULL, blank=True, null=True)
    custom_gear_type = models.ForeignKey(
        "CustomGearType", on_delete=models.SET_NULL, blank=True, null=True
    )
    name = models.CharField(max_length=255)

    @property
    def service_interval(self) -> Optional[GearItemServiceInterval]:
        try:
            return GearItemServiceInterval.objects.get(gear_item=self)
        except GearItemServiceInterval.DoesNotExist:
            return None

    @property
    def service_tracking(self) -> bool:
        return self.service_interval is not None

    def get_service_history(self) -> List[GearItemService]:
        return GearItemService.objects.filter(gear_item=self).order_by("-service_date")

    @property
    def service_history(self) -> List[GearItemService]:
        return self.get_service_history() if self.service_tracking else []

    @property
    def last_service_date(self) -> Optional[str]:
        item_service = self.get_service_history().first()
        return item_service.service_date if item_service else None

    @property
    def dive_count(self) -> Optional[int]:
        return GearDive.objects.filter(gear_item=self, dive__diver=self.diver).count()

    def _get_reference_date(self) -> Optional[date]:
        """
        Get the reference date for service calculations (last service or purchase date)
        If the gear item is tracking service, and the last service date is before the purchase date,
        then the reference date is the last service date, otherwise, the reference date is the purchase date.
        """
        if self.service_tracking:
            if self.last_service_date:
                return self.last_service_date
            else:
                return self.service_interval.purchase_date
        return None

    @property
    def dives_since_last_service(self) -> Optional[int]:
        if not self.service_interval:
            return None

        reference_date = self._get_reference_date()
        if not reference_date:
            return None

        return GearDive.objects.filter(
            gear_item=self, dive__diver=self.diver, dive__date__gte=reference_date
        ).count()

    def get_days_since_last_service(self, tz=None) -> Optional[int]:
        reference_date = self._get_reference_date()
        if not reference_date:
            return None

        current_date = timezone.now().date() if tz is None else timezone.now().astimezone(tz).date()
        return (current_date - reference_date).days

    def get_due_for_service_days(self, tz=None) -> Optional[int]:
        if not self.service_interval:
            return None

        days_since = self.get_days_since_last_service(tz=tz)
        if days_since is None:
            return None

        return days_since - self.service_interval.day_interval

    @property
    def due_for_service_dives(self) -> Optional[int]:
        if not self.service_interval or not self.service_interval.purchase_date:
            return None

        dives_since = self.dives_since_last_service
        if dives_since is None:
            return None

        return dives_since - self.service_interval.dive_interval

    def __str__(self):
        return f"{self.name}"
