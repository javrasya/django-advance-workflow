from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from mock import MagicMock

from daw.utils import middleware
from daw.models import TransitionApprovement
from daw.service.objectservice import ObjectService
from daw.service.stateservice import StateService
from daw.tests import BaseTestCase, TestModel


__author__ = 'ahmetdal'


class ObjectServiceTest(BaseTestCase):
    fixtures = ['daw/fixtures/approvement_service_test.json']


    def test_init(self):
        test_obj = TestModel.objects.get(pk=5001)
        initial_state = StateService.get_init_state(ContentType.objects.get_for_model(test_obj))

        self.assertEqual(initial_state, test_obj.test_field)
        self.assertEqual(18, TransitionApprovement.objects.count())

    def test_get_objects_waiting_for_approval_for_user(self):
        middleware.get_user = MagicMock(return_value=User.objects.get(pk=2001))
        on_approval_objects = ObjectService.get_objects_waiting_for_approval(ContentType.objects.get_for_model(TestModel), 'test_field')
        self.assertEqual(2, on_approval_objects.count())
        self.assertEqual(5001, on_approval_objects[0].pk)

        middleware.get_user = MagicMock(return_value=User.objects.get(pk=2002))
        on_approval_objects = ObjectService.get_objects_waiting_for_approval(ContentType.objects.get_for_model(TestModel), 'test_field')
        self.assertEqual(0, on_approval_objects.count())

        middleware.get_user = MagicMock(return_value=User.objects.get(pk=2003))
        on_approval_objects = ObjectService.get_objects_waiting_for_approval(ContentType.objects.get_for_model(TestModel), 'test_field')
        self.assertEqual(0, on_approval_objects.count())

        middleware.get_user = MagicMock(return_value=User.objects.get(pk=2004))
        on_approval_objects = ObjectService.get_objects_waiting_for_approval(ContentType.objects.get_for_model(TestModel), 'test_field')
        self.assertEqual(0, on_approval_objects.count())











