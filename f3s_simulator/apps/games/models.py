# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _
from f3s_simulator.apps.maps.models import Map
from f3s_simulator.libs.models import CommonModel

class Game(CommonModel):
    """
    Fire simulation. In terms of game dev - game.
    """
    map = models.ForeignKey(Map, related_name='games')
    owner = models.ForeignKey(User, related_name='created_games')
    players = models.ManyToManyField(User, related_name='played_games')