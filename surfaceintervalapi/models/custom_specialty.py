from django.db import models
from surfaceintervalapi.models import CacheInvalidationMixin
from surfaceintervalapi.utils import get_cache_key


class CustomSpecialty(CacheInvalidationMixin, models.Model):
    diver = models.ForeignKey("Diver", on_delete=models.CASCADE)
    name = models.CharField(max_length=25)

    def __str__(self):
        return f"{self.pk} | {self.name} | {self.diver.user.first_name} {self.diver.user.last_name}"

    def get_model_cache_keys(self) -> list[str]:
        custom_specialties_key = get_cache_key(self.diver.user.id, "custom_specialties")
        custom_specialty_key = get_cache_key(self.diver.user.id, "custom_specialty", self.pk)
        return [custom_specialties_key, custom_specialty_key]
