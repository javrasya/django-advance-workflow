from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from daw.models import Transition, State, TransitionApproveDefinition
from example_app.models import ExampleModel

__author__ = 'ahmetdal'

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        # DELETE
        ExampleModel.objects.all().delete()

        User.objects.filter(first_name="testUser1", last_name="testUser1", username="testUser1", email="testUser1@test.com", is_staff="True", is_active="True", is_superuser="False",
                            password="pbkdf2_sha256$12000$ep0RuU2mLSWv$5eF8YP5ABKCPSSFxhfXJW+yGZsUeCRq9jkTyeey6qfc=").delete()

        User.objects.filter(first_name="testUser2", last_name="testUser2", username="testUser2", email="testUser2@test.com", is_staff="True", is_active="True", is_superuser="False",
                            password="pbkdf2_sha256$12000$ep0RuU2mLSWv$5eF8YP5ABKCPSSFxhfXJW+yGZsUeCRq9jkTyeey6qfc=").delete()

        User.objects.filter(first_name="testUser3", last_name="testUser3", username="testUser3", email="testUser3@test.com", is_staff="True", is_active="True", is_superuser="False",
                            password="pbkdf2_sha256$12000$ep0RuU2mLSWv$5eF8YP5ABKCPSSFxhfXJW+yGZsUeCRq9jkTyeey6qfc=").delete()

        User.objects.filter(first_name="testUser4", last_name="testUser4", username="testUser4", email="testUser4@test.com", is_staff="True", is_active="True", is_superuser="False",
                            password="pbkdf2_sha256$12000$ep0RuU2mLSWv$5eF8YP5ABKCPSSFxhfXJW+yGZsUeCRq9jkTyeey6qfc=").delete()

        Permission.objects.filter(name='permission_1', content_type=ContentType.objects.get_for_model(Transition), codename='1').delete()
        Permission.objects.filter(name='permission_2', content_type=ContentType.objects.get_for_model(Transition), codename='2').delete()
        Permission.objects.filter(name='permission_3', content_type=ContentType.objects.get_for_model(Transition), codename='3').delete()
        Permission.objects.filter(name='permission_4', content_type=ContentType.objects.get_for_model(Transition), codename='4').delete()

        Transition.objects.all().delete()
        State.objects.all().delete()
        TransitionApproveDefinition.objects.all().delete()

        # INSERT

        permission1 = Permission.objects.create(name='permission_1', content_type=ContentType.objects.get_for_model(Transition), codename='1')
        permission2 = Permission.objects.create(name='permission_2', content_type=ContentType.objects.get_for_model(Transition), codename='2')
        permission3 = Permission.objects.create(name='permission_3', content_type=ContentType.objects.get_for_model(Transition), codename='3')
        permission4 = Permission.objects.create(name='permission_4', content_type=ContentType.objects.get_for_model(Transition), codename='4')

        user1 = User.objects.create(first_name="testUser1", last_name="testUser1", username="testUser1", email="testUser1@test.com", is_staff="True", is_active="True", is_superuser="False",
                                    password="pbkdf2_sha256$12000$ep0RuU2mLSWv$5eF8YP5ABKCPSSFxhfXJW+yGZsUeCRq9jkTyeey6qfc=")
        user1.user_permissions.add(permission1)

        user2 = User.objects.create(first_name="testUser2", last_name="testUser2", username="testUser2", email="testUser2@test.com", is_staff="True", is_active="True", is_superuser="False",
                                    password="pbkdf2_sha256$12000$ep0RuU2mLSWv$5eF8YP5ABKCPSSFxhfXJW+yGZsUeCRq9jkTyeey6qfc=")
        user2.user_permissions.add(permission2)

        user3 = User.objects.create(first_name="testUser3", last_name="testUser3", username="testUser3", email="testUser3@test.com", is_staff="True", is_active="True", is_superuser="False",
                                    password="pbkdf2_sha256$12000$ep0RuU2mLSWv$5eF8YP5ABKCPSSFxhfXJW+yGZsUeCRq9jkTyeey6qfc=")
        user3.user_permissions.add(permission3)

        user4 = User.objects.create(first_name="testUser4", last_name="testUser4", username="testUser4", email="testUser4@test.com", is_staff="True", is_active="True", is_superuser="False",
                                    password="pbkdf2_sha256$12000$ep0RuU2mLSWv$5eF8YP5ABKCPSSFxhfXJW+yGZsUeCRq9jkTyeey6qfc=")
        user4.user_permissions.add(permission4)

        state1 = State.objects.create(label='s1')
        state2 = State.objects.create(label='s2')
        state3 = State.objects.create(label='s3')
        state4 = State.objects.create(label='s4')
        state5 = State.objects.create(label='s5')
        state41 = State.objects.create(label='s4.1')
        state42 = State.objects.create(label='s4.2')
        state51 = State.objects.create(label='s5.1')
        state52 = State.objects.create(label='s5.2')

        transition1 = Transition.objects.create(content_type=ContentType.objects.get_for_model(ExampleModel), source_state=state1, destination_state=state2)
        transition2 = Transition.objects.create(content_type=ContentType.objects.get_for_model(ExampleModel), source_state=state2, destination_state=state3)
        transition3 = Transition.objects.create(content_type=ContentType.objects.get_for_model(ExampleModel), source_state=state3, destination_state=state4)
        transition4 = Transition.objects.create(content_type=ContentType.objects.get_for_model(ExampleModel), source_state=state3, destination_state=state5)
        transition5 = Transition.objects.create(content_type=ContentType.objects.get_for_model(ExampleModel), source_state=state4, destination_state=state41)
        transition6 = Transition.objects.create(content_type=ContentType.objects.get_for_model(ExampleModel), source_state=state4, destination_state=state42)
        transition7 = Transition.objects.create(content_type=ContentType.objects.get_for_model(ExampleModel), source_state=state5, destination_state=state51)
        transition8 = Transition.objects.create(content_type=ContentType.objects.get_for_model(ExampleModel), source_state=state5, destination_state=state52)

        transition_approve_definition1 = TransitionApproveDefinition.objects.create(transition=transition1, permission=permission1, order=0)
        transition_approve_definition2 = TransitionApproveDefinition.objects.create(transition=transition2, permission=permission2, order=0)
        transition_approve_definition3 = TransitionApproveDefinition.objects.create(transition=transition2, permission=permission3, order=1)
        transition_approve_definition4 = TransitionApproveDefinition.objects.create(transition=transition3, permission=permission4, order=0)
        transition_approve_definition5 = TransitionApproveDefinition.objects.create(transition=transition4, permission=permission4, order=0)
        transition_approve_definition6 = TransitionApproveDefinition.objects.create(transition=transition5, permission=permission4, order=0)
        transition_approve_definition7 = TransitionApproveDefinition.objects.create(transition=transition6, permission=permission4, order=0)
        transition_approve_definition8 = TransitionApproveDefinition.objects.create(transition=transition7, permission=permission4, order=0)
        transition_approve_definition9 = TransitionApproveDefinition.objects.create(transition=transition8, permission=permission4, order=0)

        ExampleModel(field1='field11', field2='field21', field3='field31', field4='field41').save()
        ExampleModel(field1='field12', field2='field22', field3='field32', field4='field42').save()






