from django.db import models
from surfaceintervalapi.utils import invalidate_multiple_cache_keys


class CacheInvalidationMixin(models.Model):
    class Meta:
        abstract = True

    def get_model_cache_keys(self):
        raise NotImplementedError("Subclasses must implement get_model_cache_keys()")

    def invalidate_model_cache(self):
        cache_keys = self.get_model_cache_keys()
        invalidate_multiple_cache_keys(cache_keys)

    def save(self, *args, **kwargs):
        self.invalidate_model_cache()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.invalidate_model_cache()
        super().delete(*args, **kwargs)
