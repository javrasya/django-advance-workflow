# -*- coding: utf-8 -*-

import os
import sys

__author__ = 'ahmetdal'

class Registry(object):
    """
    Abstract module loader/registry
    """
    name = "Registry"  # Registry name
    subdir = "directory"  # Restrict to directory
    classname = "Class"  # Auto-register class
    apps = None  # Restrict to a list of application
    exclude = []  # List of excluded modules
    exclude_daemons = []  # List of excluded daemons

    def __init__(self):
        self.classes = {}
        # Detect daemon name
        _, self.daemon_name = os.path.split(sys.argv[0])
        if self.daemon_name.endswith(".py"):
            self.daemon_name = self.daemon_name[:-3]
        if self.daemon_name == "manage":
            self.daemon_name = sys.argv[1]
            #
        self.is_registered = self.daemon_name in self.exclude_daemons


    def register(self, name, module):
        """
        Should be called within metaclass' __new__ method
        """
        if name is None:
            return
        self.classes[name] = module

    def __getitem__(self, name):
        return self.classes[name]

    def __contains__(self, item):
        return item in self.classes

    @property
    def choices(self):
        """
        For model field's choices=
        """
        return [(x, x) for x in sorted(self.classes.keys())]


import logging




class TransitionChangeRegistry(Registry):
    """
    Registry for Profile classes
    """
    name = "TransitionChangeRegistry"


transition_change_registry = TransitionChangeRegistry()


class TransitionChangeBase(type):
    """
    Metaclass for Profile. Register created Profile class
    with profile_registry
    """

    def __new__(cls, name, bases, attrs):
        m = type.__new__(cls, name, bases, attrs)
        transition_change_registry.register(m.name, m)
        return m


class TransitionChange:
    logger = logging.getLogger('informer')

    __metaclass__ = TransitionChangeBase
    name = None
    when = None
