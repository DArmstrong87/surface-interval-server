from django.db import models
from django.db.models import F, Case, When, Q, CharField
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
    def total_dives(self):
        return Dive.objects.filter(diver=self).count()

    @property
    def most_recent_dive(self):
        dive = Dive.objects.filter(diver=self).latest("date")
        return dive.date

    @property
    def deepest_dive(self):
        dive = Dive.objects.only("depth").filter(diver=self).order_by("-depth").first()
        return dive.depth

    @property
    def longest_dive(self):
        dive = Dive.objects.only("time").filter(diver=self).order_by("-time").first()
        return dive.time

    @property
    def most_logged_specialty(self):
        # Get diver's dive specialties
        # Annotate specialty
        dives_specialties = DiveSpecialty.objects.annotate(
            s_name=Case(
                When(Q(custom_specialty__isnull=False), then=F("custom_specialty__name")),
                default=F("specialty__name"),
                output_field=CharField(),
            )
        ).filter(dive__diver=self)

        # Get names only
        diver_dive_specialty_names = [ds["s_name"] for ds in dives_specialties.values("s_name")]
        # Get unique names
        unique_diver_dive_specialty_names = list(set(diver_dive_specialty_names))

        # Make dict of specialty_name: count for each specialty
        specialty_counts = {}
        for s_name in unique_diver_dive_specialty_names:
            specialty_types = [name for name in diver_dive_specialty_names if name == s_name]
            specialty_counts[s_name] = len(specialty_types)

        most_logged_specialty = max(specialty_counts, key=specialty_counts.get)

        # Return name and count of specialty
        return most_logged_specialty, specialty_counts[most_logged_specialty]

    @property
    def avg_air_consumption(self):
        dives = Dive.objects.filter(
            diver=self, start_pressure__isnull=False, end_pressure__isnull=False
        ).values()
        for dive in dives:
            air_consumption = get_air_consumption(dive, self.units)
            dive["air_consumption"] = air_consumption

        avg_air_consumption = sum([d["air_consumption"] for d in dives]) / len(dives)
        print(
            f"Average air consumption is {round(avg_air_consumption *  28.3168, 3)} liters per minute"
        )
        return avg_air_consumption

    def __str__(self):
        return f"{self.pk} | {self.user.first_name} {self.user.last_name}"
