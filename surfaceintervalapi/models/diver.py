from django.db import models
from django.contrib.auth.models import User

from surfaceintervalapi.models.dive import Dive


class Diver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_gear_set = models.ForeignKey('Gear_Set', null=True, blank=True, on_delete=models.DO_NOTHING, related_name='Gear_Set')
    units = models.CharField(max_length=255, choices=[('Metric', 'metric'), ('Imperial', 'imperial')])
    
    
    # Dynamic Properties:
    @property
    def total_dives(self):
        return Dive.objects.filter(diver=self).count()
    
    
    @property
    def most_recent_dive(self):
        dive = Dive.objects.filter(diver=self).latest('date')
        return dive.date
    
    
    @property
    def deepest_dive(self):
        dive = Dive.objects.filter(diver=self).values('depth').annotate(max_depth=models.Max('depth')).order_by('max_depth').first()
        return dive.depth


    @property
    def longest_dive(self):
        dive = Dive.objects.filter(diver=self).values('time').annotate(max_time=models.Max('time')).order_by('max_time').first()
        return dive.depth

    # most_logged_specialty
    # avg_air_consumption
    
    def __str__(self):
        return f'{self.pk} | {self.user.first_name} {self.user.last_name}'