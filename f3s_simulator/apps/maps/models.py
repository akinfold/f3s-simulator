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
