from south.modelsinspector import add_introspection_rules

__author__ = 'ahmetdal'

from externalpermission import *
from externalcontenttype import *
from state import *
from transition import *
from transitionapprovedefinition import *
from transitionapprovement import *

add_introspection_rules([], ["^daw\.utils\.fields\.StateField"])


