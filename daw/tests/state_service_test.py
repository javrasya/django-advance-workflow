from django.contrib.auth.models import User
from mock import MagicMock

from daw.utils import middleware
from daw.tests.models import State, TestModel
from daw.service.state_service import StateService
from daw.tests import BaseTestCase


__author__ = 'ahmetdal'


class StateServiceTest(BaseTestCase):
    fixtures = ['daw/fixtures/approvement_service_test.json']


    def test_get_available_states(self):
        middleware.get_user = MagicMock(return_value=User.objects.get(pk=2002))
        obj = TestModel.objects.get(pk=5001)
        available_states = StateService.get_available_states(obj, 'test_field', include_user=False)
        self.assertEqual(1, available_states.count())
        self.assertEqual(State.objects.get(label='s2'), available_states[0])
        available_states = StateService.get_available_states(obj, 'test_field', include_user=True)
        self.assertEqual(0, available_states.count())
        available_states = StateService.get_available_states(obj, 'test_field')
        self.assertEqual(0, available_states.count())

        middleware.get_user = MagicMock(return_value=User.objects.get(pk=2003))
        obj = TestModel.objects.get(pk=5001)
        available_states = StateService.get_available_states(obj, 'test_field', include_user=False)
        self.assertEqual(1, available_states.count())
        self.assertEqual(State.objects.get(label='s2'), available_states[0])
        available_states = StateService.get_available_states(obj, 'test_field', include_user=True)
        self.assertEqual(0, available_states.count())
        available_states = StateService.get_available_states(obj, 'test_field')
        self.assertEqual(0, available_states.count())

        middleware.get_user = MagicMock(return_value=User.objects.get(pk=2004))
        obj = TestModel.objects.get(pk=5001)
        available_states = StateService.get_available_states(obj, 'test_field', include_user=False)
        self.assertEqual(1, available_states.count())
        self.assertEqual(State.objects.get(label='s2'), available_states[0])
        available_states = StateService.get_available_states(obj, 'test_field', include_user=True)
        self.assertEqual(0, available_states.count())
        available_states = StateService.get_available_states(obj, 'test_field')
        self.assertEqual(0, available_states.count())

        middleware.get_user = MagicMock(return_value=User.objects.get(pk=2001))
        obj = TestModel.objects.get(pk=5001)
        available_states = StateService.get_available_states(obj, 'test_field', include_user=False)
        self.assertEqual(1, available_states.count())
        self.assertEqual(State.objects.get(label='s2'), available_states[0])
        available_states = StateService.get_available_states(obj, 'test_field', include_user=True)
        self.assertEqual(1, available_states.count())
        self.assertEqual(State.objects.get(label='s2'), available_states[0])

        available_states = StateService.get_available_states(obj, 'test_field')
        self.assertEqual(1, available_states.count())
        self.assertEqual(State.objects.get(label='s2'), available_states[0])





