# -*- coding: utf-8 -*-
__author__ = 'ahmetdal'

from django.dispatch import Signal

pre_transition = Signal(providing_args=['instance', 'name', 'source', 'target'])
post_transition = Signal(providing_args=['instance', 'name', 'source', 'target'])
