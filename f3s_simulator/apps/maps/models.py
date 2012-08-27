# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _
from f3s_simulator.libs.models import CommonModel

class Map(CommonModel):
    """
    Top level abstraction representing simulation initial state.
    Some kind of level in terms of game dev.
    """
    name = models.CharField(_('name'), max_length=255, help_text=_('Map name'), unique=True)
    author = models.ForeignKey(User, related_name='maps')
    description = models.CharField(_('description'), max_length=1024, blank=True, default='',
        help_text=_('Map description'))

    def __unicode__(self):
        return self.name



class Environment(CommonModel):
    """
    Abstraction representing global values such as air temperature, wind direction and speed, etc.
    Environment changes in time, so each game contains own sequence of environment snapshots.
    """
    map = models.OneToOneField(Map)
    air_temp = models.FloatField(_('air temperature'), default=0)
    wind_speed = models.FloatField(_('wind speed'), default=0)
    wind_direction = models.IntegerField(_('wind direction'), default=0)

    def __unicode__(self):
        return '%s environment' % self.map.name



class Flammable(CommonModel):
    """
    Flammable object on the map.
    """
    map = models.ForeignKey(Map, related_name='flammables')
    name = models.CharField(_('name'), max_length=32, blank=True)
    polygon = models.PolygonField(_('polygon'))

    objects = models.GeoManager()

    def __unicode__(self):
        return '%s on % map' % (self.name, self.map.name)



class Reservoir(CommonModel):
    """
    Water reservoir on the map.
    """
    map = models.ForeignKey(Map, related_name='reservoirs')
    name = models.CharField(_('reservoir name'), max_length=32, blank=True)
    polygon = models.PolygonField(_('polygon'))

    objects = models.GeoManager()
    