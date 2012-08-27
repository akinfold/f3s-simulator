# -*- coding: utf-8 -*-
from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _
from f3s_simulator.apps.games.models import Step, Map
from f3s_simulator.libs.models import CommonModel


class Environment(CommonModel):
    """
    Abstraction representing global values such as air temperature, wind direction and speed, etc.
    Environment changes in time, so each game contains own sequence of environment snapshots.
    """
    map = models.OneToOneField(Map)
    step = models.OneToOneField(Step, blank=True, null=True)
    air_temp = models.FloatField(_('air temperature'), default=0)
    wind_speed = models.FloatField(_('wind speed'), default=0)
    wind_direction = models.IntegerField(_('wind direction'), default=0)
    rainfall = models.IntegerField(_('rainfall'), default=0)

    def __unicode__(self):
        return '%s environment' % self.map.name



class FlammableType(CommonModel):
    """
    Flammable material type.
    """
    name = models.CharField(_('name'), max_length=32, unique=True)
    colour = models.CharField(_('display colour'), max)

    def __unicode__(self):
        return self.name



class Flammable(CommonModel):
    """
    Flammable object on the map.
    """
    type = models.ForeignKey(FlammableType, related_name='flammables')
    map = models.ForeignKey(Map, related_name='flammables')
    name = models.CharField(_('name'), max_length=32, blank=True)
    polygon = models.PolygonField(_('polygon'))

    objects = models.GeoManager()

    def __unicode__(self):
        return '%s on %s map' % (self.name, self.map.name)



class Reservoir(CommonModel):
    """
    Water reservoir on the map.
    """
    map = models.ForeignKey(Map, related_name='reservoirs')
    name = models.CharField(_('reservoir name'), max_length=32, blank=True)
    polygon = models.PolygonField(_('polygon'))

    objects = models.GeoManager()

    def __unicode__(self):
        return '%s on % map' % (self.name, self.map.name)



class Burnout(CommonModel):
    """
    Territory damaged by fire.

    On each step burnouts polygons recalculates, then checks for intersection.
    Intersected burnouts merges into new burnout.
    All fires linked to merged burnouts should be relinked to new burnout.
    """
    map = models.ForeignKey(Map, related_name='burnouts')
    step = models.ForeignKey(Step, related_name='burnouts', blank=True, null=True)
    name = models.CharField(_('burnout name'), max_length=32, blank=True)
    child = models.ForeignKey('self', related_name='parents', blank=True, null=True)
    polygon = models.PolygonField(_('polygon'))

    def __unicode__(self):
        return '%s on % map' % (self.name, self.map.name)



class Fire(CommonModel):
    """
    Burning area of the wildfire.

    On each step fires polygons recalculates, then checks for intersection.
    Intersected fires merges into new fire.
    """
    map = models.ForeignKey(Map, related_name='fires')
    step = models.ForeignKey(Step, related_name='fires', blank=True, null=True)
    burnout = models.ForeignKey(Burnout, related_name='fires')
    name = models.CharField(_('burnout name'), max_length=32, blank=True)
    child = models.ForeignKey('self', related_name='parents', blank=True, null=True)
    polygon = models.PolygonField(_('polygon'))

    def __unicode__(self):
        return '%s on % map' % (self.name, self.map.name)