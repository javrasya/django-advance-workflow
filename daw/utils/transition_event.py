from daw.utils.registry import Registry


__author__ = 'ahmetdal'


class TransitionEventRegistry(Registry):
    """
    Registry for Profile classes
    """
    name = "InformerRegistry"
    subdir = "profiles"
    classname = "informer"
    apps = ["etak.apps.informer"]
    exclude = ["highlight"]


    def get_transition_event(self, source, destination, when):
        return self.get('%s%s%s' % (source, destination, when))


transition_event_registry = TransitionEventRegistry()


class TransitionEventBase(type):
    """
    Metaclass for Profile. Register created Profile class
    with profile_registry
    """


    def __new__(cls, name, bases, attrs):
        m = type.__new__(cls, name, bases, attrs)
        m.scripts = {}
        if m.content_type and m.source and m.destination and m.when:
            transition_event_registry.register('%s%s%s' % (m.source, m.destination, m.when), m)
        return m


BEFORE = 0
AFTER = 1


class TransitionEvent:
    __metaclass__ = TransitionEventBase

    content_type = None
    source = '*'
    destination = None
    when = None

    def execute(self):
        pass

