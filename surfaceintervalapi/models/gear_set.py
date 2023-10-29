from django.db import models

# from django.contrib.postgres.fields import ArrayField


class GearSet(models.Model):
    diver = models.ForeignKey("Diver", on_delete=models.CASCADE)
    name = models.CharField(max_length=50, default="GearSet")
    bcd = models.ForeignKey(
        "GearItem",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"gear_type__name": "BCD"},
        related_name="BCD",
    )
    regulator = models.ForeignKey(
        "GearItem",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"gear_type__name": "Regulator"},
        related_name="Regulator",
    )
    octopus = models.ForeignKey(
        "GearItem",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"gear_type__name": "Octopus"},
        related_name="Octopus",
    )
    mask = models.ForeignKey(
        "GearItem",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"gear_type__name": "Mask"},
        related_name="Mask",
    )
    fins = models.ForeignKey(
        "GearItem",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"gear_type__name": "Fins"},
        related_name="Fins",
    )
    boots = models.ForeignKey(
        "GearItem",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"gear_type__name": "Boots"},
        related_name="Boots",
    )
    computer = models.ForeignKey(
        "GearItem",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"gear_type__name": "Computer"},
        related_name="Computer",
    )
    exposure_suit = models.ForeignKey(
        "GearItem",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"gear_type__name": "Exposure suit"},
        related_name="Exposure_Suit",
    )
    weights = models.IntegerField(blank=True, null=True)
    tank = models.ForeignKey(
        "GearItem",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"gear_type__name": "Tank"},
    )
    # additional_gear = ArrayField(base_field=models.IntegerField, blank=True)

    def __str__(self):
        return f"{self.pk} | {self.name} by {self.diver.user.first_name}"
