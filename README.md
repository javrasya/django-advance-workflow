# [Django Advance Workflow](https://bitbucket.org/ahmetdal/django-advance-workflow/)[![Build Status](https://travis-ci.org/javrasya/django-advance-workflow.svg?branch=master)](https://travis-ci.org/javrasya/django-advance-workflow)

Django Advance Workflow is a open source workflow mechanism can be embed into Python-DJango Project which support on the fly changes on every item in workflow instead of hardcoding states and transitions.

Main goal of developing this framework is **to be able to edit any workflow item on the fly.** This means, all elements in workflow like states, transitions, user authorizations(permission), even specific objects worflow items are editable. To do this, all data about the workflow item is persisted into DB. **Hence, they can be change without touching the code.**

There is ordering aprovments for a transition in DAW is supported. DAW also provides skipping specific transition of a specific objects.

DAW has javascript client, which you can do some DAW actions. It also provides hooking before and after transition. This means, anything custom can be done before the transition approved. This makes user more flexible.

It is created and maintained by [Ahmet DAL](https://twitter.com/ceahmetdal).

## Installation
`pip install git+https://ahmetdal@bitbucket.org/ahmetdal/django-advance-workflow.git`

## Usage
	INSTALLED_APPS = (
	    '...',
	    'daw',
	    '...'
	)
We need to include the DAW models in our database;
Required `south` for django version less than 1.7
 
	python manage.py migrate	
	
**DAW** provides an admin interface that you can reach through your application to define your workflow items like states, transitions, permissions etc. 

To have it, it is needed to add DAW admin url definition into your urls.py.

		
		urlpatterns = patterns('',
								... 
								url(r'^admin/', include(admin.site.urls)),
								url(r'^daw/', include('daw.urls')),
								...
								)	

You can now see it on;

		/admin/daw/state/
		

DAW provides a model state field and it must be used. Here is a model example;

		from daw.utils.fields import StateField
		from daw.models.metaclasses.workflow_model_metaclass import WorkflowModelMetaclass
		
		class MyModel(...)
			__metaclass__ = WorkflowModelMetaclass
			....
			state = StateField(verbose_name='Approval State')
			....

You must edit metaclass of the model and give **WorkflowModelMetaclass**, otherwise, DAW can't generate workflow items of the object on its creation.

Now, we need to do some definition through the admin interface;

1. Define your extra permission if you have.
2. Define your states.
3. Define your state transitions.
4. Define your state transition approve definition which indicates the authorization.

We are now ready to workflowing :)

Whenever an object of MyModel is inserted, its path will be described in DAW sytem.

###DAW Models:

####States: 
Indicates states in your state machine. This model is used by user.

####Transitions: 
These are transition between your states. **There must be only one initial state** which is in a transition as destionation state but no source state to make DAW find it on object creation. This model is used by user.

####Transition Approve Definitions: 
These are approvement definition of transitions that describes which user permission will be allowed to approve the transition. An order can also be given to permission for a transition. This means, If you want to order approvement for a transition, you can define it. Assume **s1** and **s2** are our states and there is a transition defined between them and we have two Transition Approve Definition on this transition. They shall be **permission1** and **permission2**. If you want object is on approval first permission1 and after it is approved by permission1, then it is on approval the second permission which is permission2, you can do it with DAW by defining order in this model. This model is used by user.

####Transition Approvements
On every model creation, DAW will generate for all transition approve definition of the creation object. This is not definition. This is a path that the object get through. So we can also edit per objects Transition Approvements. This model is used by DAW not by user. Do not touch this model until you don't need specific objects item editing like skiping.


###DAW Javascript Client:
There are some action you can do on DAW with this javascript library. Here are some of them;
* Getting a state by label
* Getting current state of an object
* Getting available next states of an object
* Process Transition (Approve or Reject)
* Skip Transition

There is most significant functionality in this library which is hooking before and after a transition process. You can have custom callback function before or after the transition. Here is its usage;

		<script src="/path_to_your_js/daw_client.js" type="text/javascript"></script>
	    <script type="text/javascript">
	        DawClient.GETTING_CURRENT_STATE_URI = "{% url 'daw.views.get_current_state' '$0' '$1' '$2'%}".replace(/%24/g, '$');
	        DawClient.APPROVE_TRANSITION_URI = "{% url 'daw.views.approve_transition_view' '$0' '$1' '$2' '$3' %}".replace(/%24/g, '$');
	        DawClient.REJECT_TRANSITION_URI = "{% url 'daw.views.reject_transition_view' '$0' '$1' '$2' '$3' %}".replace(/%24/g, '$');
	        DawClient.GET_STATE_BY_LABEL_URI = "{% url 'daw.views.get_state_by_label' '$0' %}".replace(/%24/g, '$');
	        DawClient.SKIP_TRANSITION_URI = "{% url 'daw.views.skip_transition' '$0' '$1' '$2' %}".replace(/%24/g, '$');

	        DawClient.registerProcessCallBack(DawClient.BEFORE_PROCESS, DawClient.getStateByLabel('s1').id, DawClient.getStateByLabel('s2').id, function (data) {
	            alert('Before Done!');
	            data.callback();
	        });
	        DawClient.registerProcessCallBack(DawClient.AFTER_PROCESS, DawClient.getStateByLabel('s1').id, DawClient.getStateByLabel('s2').id, function (data) {
	            alert('After Done!');
	            data.callback();
	        });
    </script>

First of all, we must define some urls for DAW javascript client. At the top of our script consists of the definitions.

There is a registration you see under the definition. With this piece of code, we told the javascript client, "When you are processing the transition has source state **s1** and destionation state **s2**, just call my callback function before you do it". My callback function will alert "Before Done!" text. We also registered for after processes as you see. 

On this registration t**here is a few things are very imporant**. DAW dispatchs a function to your custom callback function which you have to invoke it at the end of your callback function. If you don't, DAW javascript client won't complete your transition processes. DAW is letting you complete of transition process. This must be like this. Because, DAW can't now know, when did you callback function really ended. You might want to pass the transition completion function to another function. This is like this because of this reason. So, you don't have to do your things in one block. You have the transition process completion callback function. Invoke it whenever you want. 

It is not important same as AFTER_PROCESSES registration. If you invoke the function that is sent by DAW to your custom after callback, the page will be refreshed. You don't have to invoke it. But otherwise, you will have to handle the after transition processes somehow. It is under your control.

A json is sent to your custom callback function by DAW Javascript client. The json contains;

*	**contentTypeId** :		Content type id of the processed object.
*	**objectId**:				Object id of the processed object.
* 	**field**:				State field name of the processed object.
*  **callback**:				Callback function which you must invoke at the end of your custom callback function.