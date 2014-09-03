from django.db import models
from daw.models.metaclasses.workflow_model_metaclass import WorkflowModelMetaclass

from daw.utils.fields import StateField


__author__ = 'ahmetdal'


class TestModel(models.Model):
    __metaclass__ = WorkflowModelMetaclass

    class Meta:
        db_table = "test_model"
        app_label = "tests"

    test_field = StateField()
