from django.contrib.contenttypes.models import ContentType
from django.db import models

from daw.service.approvementservice import ApprovementService
from daw.utils.fields import StateField


__author__ = 'ahmetdal'

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        for model in models.get_models(include_auto_created=True):
            for field in model._meta.fields:
                if isinstance(field, StateField):
                    content_type = ContentType.objects.get_for_model(model)
                    for obj in model.objects.all():
                        ApprovementService.init_approvements(content_type.pk, obj.pk, field.name)







