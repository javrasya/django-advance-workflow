from django.db import models
from daw.models import State
from daw.utils.fields import StateField


__author__ = 'ahmetdal'


class TestModel(models.Model):
    class Meta:
        db_table = "test_model"
        app_label = "tests"

    test_field = StateField()
