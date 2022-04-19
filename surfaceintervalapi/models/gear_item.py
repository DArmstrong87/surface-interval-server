from django.db import models
from django.utils import timezone

from surfaceintervalapi.models.dive import Dive


class Gear_Item(models.Model):
    diver = models.ForeignKey('Diver', on_delete=models.CASCADE)
    gear_type = models.ForeignKey('Gear_Type', on_delete= models.SET_NULL, blank=True, null=True)
    custom_gear_type = models.ForeignKey('Custom_Gear_Type', on_delete= models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=200)
    purchase_date = models.DateField(blank=True, null=True)
    last_serviced = models.DateField(blank=True, null=True)
    
    
    # If an item was recently serviced, get next dives or days since that date.
    
    def dives_since_last_service(self):
        if self.last_serviced is None:
            dives = Dive.objects.filter(diver=self.diver, date__gte=self.purchase_date).count()
        else:
            dives = Dive.objects.filter(diver=self.diver, date__gte=self.last_serviced).count()
            
        return dives


    def days_since_last_service(self):
        days = (timezone.now() - self.date).days
        return days
    
    
    def get_service_interval(self):
        if self.purchase_date is not None:
            g_type = self.gear_type.name
            interval = 10 if g_type == 'BCD' else (20 if g_type == 'Regulator' or g_type == 'Octopus' else 30)
            # TODO Figure out dive intervals.
            return interval
        else:
            return None


    def due_for_service_days(self):
        if self.purchase_date is not None:
            days_since = self.days_since_last_service
            day_difference = days_since - 365
            return day_difference
        else:
            return None

    def __str__(self):
        return f'{self.pk} | {self.name}'
    