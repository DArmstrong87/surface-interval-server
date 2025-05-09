from django.db import models
from django.db.models import F, Case, When, Q, CharField, Count
from django.contrib.auth.models import User
from surfaceintervalapi.utils import get_air_consumption

from surfaceintervalapi.models.dive import Dive, DiveSpecialty


class Diver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_gear_set = models.ForeignKey(
        "GearSet", null=True, blank=True, on_delete=models.DO_NOTHING, related_name="GearSet"
    )
    units = models.CharField(
        max_length=255, choices=[("Metric", "metric"), ("Imperial", "imperial")]
    )

    # Dynamic Properties:
    @property
    def total_dives(self) -> int:
        return Dive.objects.filter(diver=self).count()

    @property
    def most_recent_dive(self) -> str:
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
        print(most_logged_specialty)

        # Return name and count of specialty
        return most_logged_specialty

    @property
    def avg_air_consumption(self) -> float | None:
        dives = Dive.objects.filter(
            diver=self, start_pressure__isnull=False, end_pressure__isnull=False
        ).values()
        for dive in dives:
            air_consumption = get_air_consumption(dive, self.units)
            dive["air_consumption"] = air_consumption

        avg_air_consumption = None
        if dives:
            avg_air_consumption = sum([d["air_consumption"] for d in dives]) / len(dives)
            print(
                f"Average air consumption is {round(avg_air_consumption *  28.3168, 3)} liters per minute"
            )
        return avg_air_consumption

    def __str__(self):
        return f"{self.pk} | {self.user.first_name} {self.user.last_name}"
