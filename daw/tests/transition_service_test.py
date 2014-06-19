from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from mock import MagicMock

from daw.utils import middleware
from daw.models import State, TransitionApprovement, APPROVED
from daw.service.transition_service import TransitionService
from daw.tests import BaseTestCase, TestModel


__author__ = 'ahmetdal'


class TransitionServiceTest(BaseTestCase):
    fixtures = ['daw/fixtures/approvement_service_test.json']


    def test_approve_transition(self):
        # ####################
        # STATE 1 - STATE 2
        # Only User1(2001) can approve and after his approve state must be changed to STATE 2
        # ###################

        # Approved by user has no required permission for this transition
        middleware.get_user = MagicMock(return_value=User.objects.get(pk=2002))
        obj = TestModel.objects.get(pk=5001)

        try:
            TransitionService.approve_transition(obj, 'test_field')
            self.fail('Exception was expected')
        except Exception, e:
            self.assertEqual(e.message, 'There is no available state for destination for the user.')

        middleware.get_user = MagicMock(return_value=User.objects.get(pk=2002))
        obj = TestModel.objects.get(pk=5001)

        try:
            TransitionService.reject_transition(obj, 'test_field')
            self.fail('Exception was expected')
        except Exception, e:
            self.assertEqual(e.message, 'There is no available state for destination for the user.')


        # Approved by user has no required permission for this transition
        middleware.get_user = MagicMock(return_value=User.objects.get(pk=2003))
        obj = TestModel.objects.get(pk=5001)

        try:
            TransitionService.approve_transition(obj, 'test_field')
            self.fail('Exception was expected')
        except Exception, e:
            self.assertEqual(e.message, 'There is no available state for destination for the user.')

        middleware.get_user = MagicMock(return_value=User.objects.get(pk=2003))
        obj = TestModel.objects.get(pk=5001)

        try:
            TransitionService.reject_transition(obj, 'test_field')
            self.fail('Exception was expected')
        except Exception, e:
            self.assertEqual(e.message, 'There is no available state for destination for the user.')


        # Approved by user has no required permission for this transition
        middleware.get_user = MagicMock(return_value=User.objects.get(pk=2004))
        obj = TestModel.objects.get(pk=5001)

        try:
            TransitionService.approve_transition(obj, 'test_field')
            self.fail('Exception was expected')
        except Exception, e:
            self.assertEqual(e.message, 'There is no available state for destination for the user.')

        middleware.get_user = MagicMock(return_value=User.objects.get(pk=2004))
        obj = TestModel.objects.get(pk=5001)

        try:
            TransitionService.reject_transition(obj, 'test_field')
            self.fail('Exception was expected')
        except Exception, e:
            self.assertEqual(e.message, 'There is no available state for destination for the user.')

        # Approved by user has required permission for this transition
        middleware.get_user = MagicMock(return_value=User.objects.get(pk=2001))
        obj = TestModel.objects.get(pk=5001)

        self.assertEqual(State.objects.get(label='s1'), obj.test_field)

        TransitionService.approve_transition(obj, 'test_field')

        obj = TestModel.objects.get(pk=5001)
        self.assertEqual(State.objects.get(label='s2'), obj.test_field)

        approvements = TransitionApprovement.objects.filter(
            content_type=ContentType.objects.get_for_model(obj),
            object_pk=obj.pk,
            status=APPROVED,
            approve_definition__transition__source_state__label='s1',
            approve_definition__transition__destination_state__label='s2'
        )
        self.assertEqual(1, approvements.count())
        self.assertIsNotNone(approvements[0].transactioner)
        self.assertEqual(User.objects.get(pk=2001), approvements[0].transactioner)
        self.assertIsNotNone(approvements[0].transaction_date)

        try:
            TransitionService.approve_transition(obj, 'test_field')
            self.fail('Exception was expected')
        except Exception, e:
            self.assertEqual(e.message, 'There is no available state for destination for the user.')


        # ####################
        # STATE 2 - STATE 3
        # User2(2002) is first approver and User3(2003) is second approver. This must be done with turn. After approvement is done, state is gonna be changed to STATE 3
        # ####################

        # Approved by user has no required permission for this transition
        middleware.get_user = MagicMock(return_value=User.objects.get(pk=2001))
        obj = TestModel.objects.get(pk=5001)
        try:
            TransitionService.approve_transition(obj, 'test_field')
            self.fail('Exception was expected')
        except Exception, e:
            self.assertEqual(e.message, 'There is no available state for destination for the user.')

        # Approved by user has no required permission for this transition
        middleware.get_user = MagicMock(return_value=User.objects.get(pk=2004))
        obj = TestModel.objects.get(pk=5001)
        try:
            TransitionService.approve_transition(obj, 'test_field')
            self.fail('Exception was expected')
        except Exception, e:
            self.assertEqual(e.message, 'There is no available state for destination for the user.')

        # Turn is User2(2002)s, not User3(2003)s. After User2(2002) approved, User3(2003) can approve.
        middleware.get_user = MagicMock(return_value=User.objects.get(pk=2003))
        obj = TestModel.objects.get(pk=5001)
        try:
            TransitionService.approve_transition(obj, 'test_field')
            self.fail('Exception was expected')
        except Exception, e:
            self.assertEqual(e.message, 'There is no available state for destination for the user.')


        # Approved by two user has required permission for this transition to get next state (order is user2(2002),user3(2003)).
        middleware.get_user = MagicMock(return_value=User.objects.get(pk=2002))
        obj = TestModel.objects.get(pk=5001)

        self.assertEqual(State.objects.get(label='s2'), obj.test_field)

        TransitionService.approve_transition(obj, 'test_field')

        obj = TestModel.objects.get(pk=5001)
        self.assertEqual(State.objects.get(label='s2'), obj.test_field)

        approvements = TransitionApprovement.objects.filter(
            content_type=ContentType.objects.get_for_model(obj),
            object_pk=obj.pk,
            status=APPROVED,
            approve_definition__transition__source_state__label='s2',
            approve_definition__transition__destination_state__label='s3'
        )
        self.assertEqual(1, approvements.count())
        self.assertIsNotNone(approvements[0].transactioner)
        self.assertEqual(User.objects.get(pk=2002), approvements[0].transactioner)
        self.assertIsNotNone(approvements[0].transaction_date)

        try:
            TransitionService.approve_transition(obj, 'test_field')
            self.fail('Exception was expected')
        except Exception, e:
            self.assertEqual(e.message, 'There is no available state for destination for the user.')

        middleware.get_user = MagicMock(return_value=User.objects.get(pk=2003))
        obj = TestModel.objects.get(pk=5001)

        self.assertEqual(State.objects.get(label='s2'), obj.test_field)

        TransitionService.approve_transition(obj, 'test_field')

        obj = TestModel.objects.get(pk=5001)
        self.assertEqual(State.objects.get(label='s3'), obj.test_field)

        approvements = TransitionApprovement.objects.filter(
            content_type=ContentType.objects.get_for_model(obj),
            object_pk=obj.pk,
            status=APPROVED,
            approve_definition__transition__source_state__label='s2',
            approve_definition__transition__destination_state__label='s3'
        )
        self.assertEqual(2, approvements.count())
        self.assertIsNotNone(approvements[0].transactioner)
        self.assertIsNotNone(approvements[1].transactioner)
        self.assertEqual(User.objects.get(pk=2002), approvements[0].transactioner)
        self.assertEqual(User.objects.get(pk=2003), approvements[1].transactioner)
        self.assertIsNotNone(approvements[0].transaction_date)
        self.assertIsNotNone(approvements[1].transaction_date)

        try:
            TransitionService.approve_transition(obj, 'test_field')
            self.fail('Exception was expected')
        except Exception, e:
            self.assertEqual(e.message, 'There is no available state for destination for the user.')



        # ####################
        # STATE 3 - STATE 4 or STATE 5
        # Only User4(2004) can approve by giving the exact next state and after his approve with his state must be changed to STATE 4 or STATE 5
        # ###################

        # Approved by user has no required permission for this transition
        middleware.get_user = MagicMock(return_value=User.objects.get(pk=2001))
        obj = TestModel.objects.get(pk=5001)
        try:
            TransitionService.approve_transition(obj, 'test_field')
            self.fail('Exception was expected')
        except Exception, e:
            self.assertEqual(e.message, 'There is no available state for destination for the user.')

        # Approved by user has no required permission for this transition
        middleware.get_user = MagicMock(return_value=User.objects.get(pk=2002))
        obj = TestModel.objects.get(pk=5001)
        try:
            TransitionService.approve_transition(obj, 'test_field')
            self.fail('Exception was expected')
        except Exception, e:
            self.assertEqual(e.message, 'There is no available state for destination for the user.')

        # Approved by user has no required permission for this transition
        middleware.get_user = MagicMock(return_value=User.objects.get(pk=2003))
        obj = TestModel.objects.get(pk=5001)
        try:
            TransitionService.approve_transition(obj, 'test_field')
            self.fail('Exception was expected')
        except Exception, e:
            self.assertEqual(e.message, 'There is no available state for destination for the user.')


        # There are STATE 4 and STATE 5 as next. State must be given to switch
        middleware.get_user = MagicMock(return_value=User.objects.get(pk=2004))
        obj = TestModel.objects.get(pk=5001)
        try:
            TransitionService.approve_transition(obj, 'test_field')
            self.fail('Exception was expected')
        except Exception, e:
            self.assertEqual(e.message, 'State must be given when there are multiple states for destination')


        # There are STATE 4 and STATE 5 as next. State among STATE 4 and STATE 5 must be given to switch, not other state
        middleware.get_user = MagicMock(return_value=User.objects.get(pk=2004))
        obj = TestModel.objects.get(pk=5001)
        try:
            TransitionService.approve_transition(obj, 'test_field', state=State.objects.get(label='s3'))
            self.fail('Exception was expected')
        except Exception, e:
            self.assertEqual(e.message,
                             "Invalid state is given(%s). Valid states is(are) %s" % (
                                 State.objects.get(label='s3').__unicode__(), ','.join([ast.__unicode__() for ast in State.objects.filter(label__in=['s4', 's5'])])))




        # There are STATE 4 and STATE 5 as next. After one of them is given to approvement, the state must be switch to it immediately.
        middleware.get_user = MagicMock(return_value=User.objects.get(pk=2004))
        obj = TestModel.objects.get(pk=5001)
        self.assertEqual(State.objects.get(label='s3'), obj.test_field)

        TransitionService.approve_transition(obj, 'test_field', state=State.objects.get(label='s5'))

        obj = TestModel.objects.get(pk=5001)
        self.assertEqual(State.objects.get(label='s5'), obj.test_field)

        approvements = TransitionApprovement.objects.filter(
            content_type=ContentType.objects.get_for_model(obj),
            object_pk=obj.pk,
            status=APPROVED,
            approve_definition__transition__source_state__label='s3',
            approve_definition__transition__destination_state__label='s5'
        )
        self.assertEqual(1, approvements.count())
        self.assertIsNotNone(approvements[0].transactioner)
        self.assertEqual(User.objects.get(pk=2004), approvements[0].transactioner)
        self.assertIsNotNone(approvements[0].transaction_date)













