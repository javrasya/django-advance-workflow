__autor__ = 'ahmetdal'

from django.conf import settings

DAW_LOAD_AS_BUILT_IN = hasattr(settings, 'DAW_LOAD_AS_BUILT_IN') and settings.DAW_LOAD_AS_BUILT_IN or True

if DAW_LOAD_AS_BUILT_IN:
    from django.template.loader import add_to_builtins

    add_to_builtins('daw.templatetags.on_approval_objects')
    add_to_builtins('daw.templatetags.process_button_modals')
    add_to_builtins('daw.templatetags.process_buttons')
