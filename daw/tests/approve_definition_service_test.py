from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import connections, connection
from django.db.models import Q
from mock import MagicMock
from daw.models.state import State
from daw.models.transition import Transition
from daw.models.transitionapprovedefinition import TransitionApproveDefinition, TransitionApproveDefinitionManager
from daw.service.approvedefinitionservice import ApproveDefinitionService

from daw.tests import TestModel

from daw.models import TransitionApprovement
from daw.tests.base_test import BaseTestCase


__author__ = 'ahmetdal'


class ApproveDefinitionServiceTest(BaseTestCase):
    fixtures = ['daw/fixtures/approve_definition_service_test.json']


    def test_apply_new_approve_definition(self):
        ct = ContentType.objects.get_for_model(TestModel)
        self.assertEqual(1, TransitionApprovement.objects.filter(object_pk=5001, content_type=ct).count())

        transition = Transition.objects.create(content_type=ct, source_state=State.objects.get(pk=3002), destination_state=State.objects.get(pk=3003))

        cursor = connection.cursor()
        cursor.execute('''
        INSERT INTO %(transition_approve_definition_table)s('transition_id','permission_id','order')
        VALUES (%(transition_id)s,1001,0)

        ''' % {'transition_approve_definition_table': TransitionApproveDefinition._meta.db_table, 'transition_id': transition.pk})

        transition_approve_definition = TransitionApproveDefinition.objects.get(~Q(pk=6001))

        self.assertEqual(1, TransitionApprovement.objects.filter(object_pk=5001, content_type=ct).count())

        ApproveDefinitionService.apply_new_approve_definition(transition_approve_definition)

        self.assertEqual(2, TransitionApprovement.objects.filter(object_pk=5001, content_type=ct).count())

        transition_approve_definition.save()

        self.assertEqual(2, TransitionApprovement.objects.filter(object_pk=5001, content_type=ct).count())














