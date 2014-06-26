__autor__ = 'ahmetdal'

from django.conf import settings


CONTENT_TYPE_EXTERNAL_APP_LABEL = hasattr(settings, 'CONTENT_TYPE_EXTERNAL_APP_LABEL') and settings.CONTENT_TYPE_EXTERNAL_APP_LABEL or 'external'

DAW_LOAD_AS_BUILT_IN = hasattr(settings, 'DAW_LOAD_AS_BUILT_IN') and settings.DAW_LOAD_AS_BUILT_IN or True

if DAW_LOAD_AS_BUILT_IN:
    from django.template.loader import add_to_builtins

    add_to_builtins('daw.templatetags.on_approval_objects')
    add_to_builtins('daw.templatetags.process_button_modals')
    add_to_builtins('daw.templatetags.process_buttons')
    add_to_builtins('daw.templatetags.content_type_filter')
