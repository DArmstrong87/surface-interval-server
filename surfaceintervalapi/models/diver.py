from django.db import models
from django.db.models import F, Case, When, Q, CharField, Count
from django.contrib.auth.models import User
from surfaceintervalapi.utils import get_air_consumption_cu_ft_min, get_average_air_consumption
from django.forms.models import model_to_dict
from surfaceintervalapi.utils import get_dive_air_consumption

from surfaceintervalapi.models.dive import Dive, DiveSpecialty
from surfaceintervalapi.utils import invalidate_cache


class Diver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_gear_set = models.ForeignKey(
        "GearSet", null=True, blank=True, on_delete=models.DO_NOTHING, related_name="GearSet"
    )
    units = models.CharField(
        max_length=255, choices=[("Metric", "metric"), ("Imperial", "imperial")]
    )

    def save(self, *args, **kwargs):
        key = f"user:{self.user.id}:diver"
        invalidate_cache(key)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        key = f"user:{self.user.id}:diver"
        invalidate_cache(key)
        super().delete(*args, **kwargs)

    # Dynamic Properties:
    @property
    def total_dives(self) -> int:
        return Dive.objects.filter(diver=self).count()

    @property
    def most_recent_dive(self) -> str | None:
        dive = Dive.objects.filter(diver=self).latest("date")
        return dive.date

    @property
    def deepest_dive(self) -> int | None:
        dive = Dive.objects.only("depth").filter(diver=self).order_by("-depth").first()
        if dive:
            return dive.depth
        return None

    @property
    def longest_dive(self) -> int | None:
        dive = Dive.objects.only("time").filter(diver=self).order_by("-time").first()
        if dive:
            return dive.time
        return None

    @property
    def shortest_dive(self) -> int | None:
        dive = Dive.objects.only("time").filter(diver=self).order_by("time").first()
        if dive:
            return dive.time
        return None

    @property
    def most_logged_specialty(self) -> dict[str | None, int | None]:
        # Get diver's dive specialties
        # Annotate specialty
        dives_specialties = DiveSpecialty.objects.annotate(
            specialty_name=Case(
                When(Q(custom_specialty__isnull=False), then=F("custom_specialty__name")),
                default=F("specialty__name"),
                output_field=CharField(),
            )
        ).filter(dive__diver=self)

        # Count the number of occurrences of each specialty
        specialty_counts = (
            dives_specialties.values("specialty_name")  # Group by specialty name
            .annotate(count=Count("specialty_name"))
            .order_by("-count")  # Count the occurrences of each specialty
        )

        # Get the specialty with the max count
        most_logged_specialty = specialty_counts.first()

        # Return name and count of specialty
        return most_logged_specialty

    @property
    def air_consumption(self) -> dict | None:
        dives = Dive.objects.filter(
            diver=self, start_pressure__isnull=False, end_pressure__isnull=False
        )

        if dives.count() == 0:
            return None

        dives_with_pressure_logged = [dive for dive in dives if dive.air_consumption is not None]
        least_efficient_dive = max(dives_with_pressure_logged, key=lambda x: x.air_consumption)
        most_efficient_dive = min(dives_with_pressure_logged, key=lambda x: x.air_consumption)
        print("min_dive", least_efficient_dive.air_consumption, most_efficient_dive.air_consumption)

        dives = dives.values()

        for dive in dives:
            air_consumption = get_air_consumption_cu_ft_min(dive, self.units)
            dive["air_consumption"] = air_consumption

        most_efficient_dive = model_to_dict(most_efficient_dive)
        most_efficient_dive_air_consumption = get_dive_air_consumption(
            most_efficient_dive, self.units
        )

        least_efficient_dive = model_to_dict(least_efficient_dive)
        least_efficient_dive_air_consumption = get_dive_air_consumption(
            least_efficient_dive, self.units
        )

        avg_air_consumption = get_average_air_consumption(dives)

        air_consumption = {
            "most_efficient": most_efficient_dive_air_consumption,
            "least_efficient": least_efficient_dive_air_consumption,
            "average": avg_air_consumption,
        }

        print("AIR", air_consumption)

        return air_consumption

    def __str__(self):
        return f"{self.pk} | {self.user.first_name} {self.user.last_name}"
