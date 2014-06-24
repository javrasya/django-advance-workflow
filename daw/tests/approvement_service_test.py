from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from mock import MagicMock
from daw.tests import TestModel

from daw.utils import middleware
from daw.models import TransitionApprovement, State
from daw.service.approvementservice import ApprovementService
from daw.tests.base_test import BaseTestCase


__author__ = 'ahmetdal'


class ApprovementServiceTest(BaseTestCase):
    fixtures = ['daw/fixtures/approvement_service_test.json']


    def test_get_approvements_object_waiting_for_approval_without_skip(self):
        middleware.get_user = MagicMock(return_value=User.objects.get(pk=2001))
        approvements = ApprovementService.get_approvements_object_waiting_for_approval(TestModel.objects.get(pk=5001), [TestModel.objects.get(pk=5001).test_field], include_user=False)
        self.assertEqual(1, approvements.count())
        approvements = ApprovementService.get_approvements_object_waiting_for_approval(TestModel.objects.get(pk=5001), [TestModel.objects.get(pk=5001).test_field], include_user=True)
        self.assertEqual(1, approvements.count())

        middleware.get_user = MagicMock(return_value=User.objects.get(pk=2002))
        approvements = ApprovementService.get_approvements_object_waiting_for_approval(TestModel.objects.get(pk=5001), [TestModel.objects.get(pk=5001).test_field], include_user=False)
        self.assertEqual(1, approvements.count())
        approvements = ApprovementService.get_approvements_object_waiting_for_approval(TestModel.objects.get(pk=5001), [TestModel.objects.get(pk=5001).test_field], include_user=True)
        self.assertEqual(0, approvements.count())

        middleware.get_user = MagicMock(return_value=User.objects.get(pk=2003))
        approvements = ApprovementService.get_approvements_object_waiting_for_approval(TestModel.objects.get(pk=5001), [TestModel.objects.get(pk=5001).test_field], include_user=False)
        self.assertEqual(1, approvements.count())
        approvements = ApprovementService.get_approvements_object_waiting_for_approval(TestModel.objects.get(pk=5001), [TestModel.objects.get(pk=5001).test_field], include_user=True)
        self.assertEqual(0, approvements.count())

        middleware.get_user = MagicMock(return_value=User.objects.get(pk=2004))
        approvements = ApprovementService.get_approvements_object_waiting_for_approval(TestModel.objects.get(pk=5001), [TestModel.objects.get(pk=5001).test_field], include_user=False)
        self.assertEqual(1, approvements.count())
        approvements = ApprovementService.get_approvements_object_waiting_for_approval(TestModel.objects.get(pk=5001), [TestModel.objects.get(pk=5001).test_field], include_user=True)
        self.assertEqual(0, approvements.count())

    def test_get_approvements_object_waiting_for_approval_with_skip(self):
        middleware.get_user = MagicMock(return_value=User.objects.get(pk=2001))

        approvements = ApprovementService.get_approvements_object_waiting_for_approval(TestModel.objects.get(pk=5002), [TestModel.objects.get(pk=5002).test_field], include_user=False)
        self.assertEqual(1, approvements.count())
        self.assertEqual(State.objects.get(label='s2'), approvements[0].approve_definition.transition.destination_state)
        approvements = ApprovementService.get_approvements_object_waiting_for_approval(TestModel.objects.get(pk=5002), [TestModel.objects.get(pk=5002).test_field], include_user=True)
        self.assertEqual(1, approvements.count())
        self.assertEqual(State.objects.get(label='s2'), approvements[0].approve_definition.transition.destination_state)

        TransitionApprovement.objects.filter(
            content_type=ContentType.objects.get_for_model(TestModel),
            object_pk=5002,
            approve_definition__transition__destination_state=State.objects.get(label='s2')
        ).update(skip=True)

        approvements = ApprovementService.get_approvements_object_waiting_for_approval(TestModel.objects.get(pk=5002), [TestModel.objects.get(pk=5002).test_field], include_user=False)
        self.assertEqual(1, approvements.count())
        self.assertEqual(State.objects.get(label='s3'), approvements[0].approve_definition.transition.destination_state)
        approvements = ApprovementService.get_approvements_object_waiting_for_approval(TestModel.objects.get(pk=5002), [TestModel.objects.get(pk=5002).test_field], include_user=True)
        self.assertEqual(1, approvements.count())
        self.assertEqual(State.objects.get(label='s3'), approvements[0].approve_definition.transition.destination_state)

        TransitionApprovement.objects.filter(
            content_type=ContentType.objects.get_for_model(TestModel),
            object_pk=5002,
            approve_definition__transition__destination_state=State.objects.get(label='s3')
        ).update(skip=True)

        approvements = ApprovementService.get_approvements_object_waiting_for_approval(TestModel.objects.get(pk=5002), [TestModel.objects.get(pk=5002).test_field], include_user=False)
        self.assertEqual(2, approvements.count())
        self.assertEqual(State.objects.get(label='s4'), approvements[0].approve_definition.transition.destination_state)
        self.assertEqual(State.objects.get(label='s5'), approvements[1].approve_definition.transition.destination_state)
        approvements = ApprovementService.get_approvements_object_waiting_for_approval(TestModel.objects.get(pk=5002), [TestModel.objects.get(pk=5002).test_field], include_user=True)
        self.assertEqual(2, approvements.count())
        self.assertEqual(State.objects.get(label='s4'), approvements[0].approve_definition.transition.destination_state)
        self.assertEqual(State.objects.get(label='s5'), approvements[1].approve_definition.transition.destination_state)

        TransitionApprovement.objects.filter(
            content_type=ContentType.objects.get_for_model(TestModel),
            object_pk=5002,
            approve_definition__transition__destination_state=State.objects.get(label='s4')
        ).update(skip=True)

        approvements = ApprovementService.get_approvements_object_waiting_for_approval(TestModel.objects.get(pk=5002), [TestModel.objects.get(pk=5002).test_field], include_user=False)
        self.assertEqual(1, approvements.count())
        self.assertEqual(State.objects.get(label='s5'), approvements[0].approve_definition.transition.destination_state)
        approvements = ApprovementService.get_approvements_object_waiting_for_approval(TestModel.objects.get(pk=5002), [TestModel.objects.get(pk=5002).test_field], include_user=True)
        self.assertEqual(1, approvements.count())
        self.assertEqual(State.objects.get(label='s5'), approvements[0].approve_definition.transition.destination_state)

        TransitionApprovement.objects.filter(
            content_type=ContentType.objects.get_for_model(TestModel),
            object_pk=5002,
            approve_definition__transition__destination_state=State.objects.get(label='s4')
        ).update(skip=False)
        TransitionApprovement.objects.filter(
            content_type=ContentType.objects.get_for_model(TestModel),
            object_pk=5002,
            approve_definition__transition__destination_state=State.objects.get(label='s5')
        ).update(skip=True)

        approvements = ApprovementService.get_approvements_object_waiting_for_approval(TestModel.objects.get(pk=5002), [TestModel.objects.get(pk=5002).test_field], include_user=False)
        self.assertEqual(1, approvements.count())
        self.assertEqual(State.objects.get(label='s4'), approvements[0].approve_definition.transition.destination_state)
        approvements = ApprovementService.get_approvements_object_waiting_for_approval(TestModel.objects.get(pk=5002), [TestModel.objects.get(pk=5002).test_field], include_user=True)
        self.assertEqual(1, approvements.count())
        self.assertEqual(State.objects.get(label='s4'), approvements[0].approve_definition.transition.destination_state)

        TransitionApprovement.objects.filter(
            content_type=ContentType.objects.get_for_model(TestModel),
            object_pk=5002,
            approve_definition__transition__destination_state__in=State.objects.filter(label__in=['s4', 's5'])
        ).update(skip=True)

        approvements = ApprovementService.get_approvements_object_waiting_for_approval(TestModel.objects.get(pk=5002), [TestModel.objects.get(pk=5002).test_field], include_user=False)
        self.assertEqual(4, approvements.count())
        self.assertEqual(State.objects.get(label='s4.1'), approvements[0].approve_definition.transition.destination_state)
        self.assertEqual(State.objects.get(label='s4.2'), approvements[1].approve_definition.transition.destination_state)
        self.assertEqual(State.objects.get(label='s5.1'), approvements[2].approve_definition.transition.destination_state)
        self.assertEqual(State.objects.get(label='s5.2'), approvements[3].approve_definition.transition.destination_state)
        approvements = ApprovementService.get_approvements_object_waiting_for_approval(TestModel.objects.get(pk=5002), [TestModel.objects.get(pk=5002).test_field], include_user=True)
        self.assertEqual(4, approvements.count())
        self.assertEqual(State.objects.get(label='s4.1'), approvements[0].approve_definition.transition.destination_state)
        self.assertEqual(State.objects.get(label='s4.2'), approvements[1].approve_definition.transition.destination_state)
        self.assertEqual(State.objects.get(label='s5.1'), approvements[2].approve_definition.transition.destination_state)
        self.assertEqual(State.objects.get(label='s5.2'), approvements[3].approve_definition.transition.destination_state)

        TransitionApprovement.objects.filter(
            content_type=ContentType.objects.get_for_model(TestModel),
            object_pk=5002,
            approve_definition__transition__destination_state__in=State.objects.filter(label__in=['s4.1', 's5.1'])
        ).update(skip=True)

        approvements = ApprovementService.get_approvements_object_waiting_for_approval(TestModel.objects.get(pk=5002), [TestModel.objects.get(pk=5002).test_field], include_user=False)
        self.assertEqual(2, approvements.count())
        self.assertEqual(State.objects.get(label='s4.2'), approvements[0].approve_definition.transition.destination_state)
        self.assertEqual(State.objects.get(label='s5.2'), approvements[1].approve_definition.transition.destination_state)
        approvements = ApprovementService.get_approvements_object_waiting_for_approval(TestModel.objects.get(pk=5002), [TestModel.objects.get(pk=5002).test_field], include_user=True)
        self.assertEqual(2, approvements.count())
        self.assertEqual(State.objects.get(label='s4.2'), approvements[0].approve_definition.transition.destination_state)
        self.assertEqual(State.objects.get(label='s5.2'), approvements[1].approve_definition.transition.destination_state)












