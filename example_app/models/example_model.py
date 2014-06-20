from django.db import models
from django.utils.translation import ugettext_lazy as _
from daw.utils.fields import StateField

__author__ = 'ahmetdal'


class ExampleModel(models.Model):
    class Meta:
        verbose_name = _("Example Model")
        verbose_name_plural = _("Example Models")
        db_table = "example_app_example_model"
        app_label = "example_app"


    field1 = models.CharField(_('Field 1'), max_length=50, null=True, blank=True)
    field2 = models.CharField(_('Field 2'), max_length=50, null=True, blank=True)
    field3 = models.CharField(_('Field 3'), max_length=50, null=True, blank=True)
    field4 = models.CharField(_('Field 4'), max_length=50, null=True, blank=True)
    state = StateField()








