from django.contrib import admin

from daw.forms import ContentTypeForm, PermissionForm, TransitionApproveDefinitionForm
from daw.models.state import State
from daw.models.externalcontenttype import ExternalContentType
from daw.models.externalpermission import ExternalPermission
from daw.models.transition import Transition
from daw.models.transitionapprovedefinition import TransitionApproveDefinition
from daw.models.transitionapprovement import TransitionApprovement


class ExternalPermissionAdmin(admin.ModelAdmin):
    list_display = ["name", "content_type"]
    list_filter = ["name", "content_type"]

    form = PermissionForm


class ExternalContentTypeAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_filter = ["name"]

    form = ContentTypeForm


class StateAdmin(admin.ModelAdmin):
    list_display = ["label", "description"]
    list_filter = ["label", "description"]


class TransitionAdmin(admin.ModelAdmin):
    list_display = ["content_type", "source_state", "destination_state"]
    list_filter = ["content_type", "source_state", "destination_state"]


class TransitionApproveDefinitionAdmin(admin.ModelAdmin):
    list_display = ["transition", "permission", "order"]
    list_filter = ["transition", "permission", "order"]

    form = TransitionApproveDefinitionForm


class TransitionApprovementAdmin(admin.ModelAdmin):
    list_display = ["approve_definition", "content_type", "object_pk", "transactioner", "transaction_date", "skip", "status"]
    list_filter = ["approve_definition", "content_type", "object_pk", "transactioner", "transaction_date", "skip", "status"]


admin.site.register(ExternalContentType, ExternalContentTypeAdmin)
admin.site.register(ExternalPermission, ExternalPermissionAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(Transition, TransitionAdmin)
admin.site.register(TransitionApproveDefinition, TransitionApproveDefinitionAdmin)
admin.site.register(TransitionApprovement, TransitionApprovementAdmin)