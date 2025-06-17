from django.db import models
from surfaceintervalapi.models import CacheInvalidationMixin
from surfaceintervalapi.utils import get_cache_key


class GearSet(CacheInvalidationMixin, models.Model):
    diver = models.ForeignKey("Diver", on_delete=models.CASCADE)
    name = models.CharField(max_length=50, default="GearSet")
    gear_items = models.ManyToManyField("GearItem", related_name="gear_sets")
    weight = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.pk} | {self.name} by {self.diver.user.first_name}"

    def get_model_cache_keys(self) -> list[str]:
        gear_sets_cache_key = get_cache_key(self.diver.user.id, "gear_sets")
        gear_set_cache_key = get_cache_key(self.diver.user.id, "gear_set", self.pk)
        return [gear_sets_cache_key, gear_set_cache_key]
