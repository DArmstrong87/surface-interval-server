from django.db import models
from surfaceintervalapi.models import CacheInvalidationMixin
from surfaceintervalapi.utils import get_cache_key


class CustomGearType(CacheInvalidationMixin, models.Model):
    diver = models.ForeignKey("Diver", on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.pk} | {self.name} | {self.diver.user.first_name} {self.diver.user.last_name}"

    def get_model_cache_keys(self) -> list[str]:
        return [get_cache_key(self.diver.user.id, "custom_gear_types")]
