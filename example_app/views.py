from django.shortcuts import render_to_response

# Create your views here.
from django.template import RequestContext
from example_app.models.example_model import ExampleModel


def on_approval_objects(request):
    context = {
        'cls': ExampleModel,
        'cls_meta': ExampleModel._meta,
        'state_field': 'state',
        'list_displays': ['field1', 'field3', 'state']
    }
    return render_to_response(
        'on_approval_objects_view.html', context,
        context_instance=RequestContext(request),
    )


def process_buttons(request):
    context = {
        'cls': ExampleModel,
        'state_field': 'state',
        'objects': ExampleModel.objects.all(),
    }
    return render_to_response(
        'process_buttons_view.html', context,
        context_instance=RequestContext(request),
    )