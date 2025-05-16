from django.db.models.signals import post_save
from django.dispatch import receiver
from surfaceintervalapi.models import Dive, GearDive


@receiver(post_save, sender=Dive)
def create_gear_dive(sender, instance, created, **kwargs):
    """
    When a dive is saved, ensure Gear Item usage is created
    through GearDive.
    """

    if created:
        gear_items = instance.get_dive_gear_items()
        for gear_item in gear_items:
            GearDive.objects.create(gear_item=gear_item, dive=instance)
            print(f"Gear {gear_item.name} used on {instance.date}")
