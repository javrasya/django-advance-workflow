'use strict';

/**
 * Created by ahmetdal on 03/09/14.
 */



/*
 * required underscore
 * */
/*
 * There Uri's must be defined in base html as variable;
 *   GETTING_AVAILABLE_STATES_URI
 *   GETTING_CURRENT_STATE_URI
 *   APPROVE_TRANSITION_URI
 *   REJECT_TRANSITION_URI
 *
 * */

/*jshint indent: false */
/*jshint undef: false */

var updateOrPush = function (array, filter, defaults) {
    var results = $.grep(array, function (e) {
        var r = true;
        for (var k in filter) {
            if (e[k] !== filter[k]) {
                r = false;
            }
        }
        if (r) {
            for (k in defaults) {
                e[k] = defaults[k];
            }
        }
        return r;
    });

    if (!results.length) {
        array.push($.extend(filter, defaults));
    }
};

var removeElementBy = function (array, filter) {
    return $.grep(array, function (e) {
        var r = false;
        for (var k in filter) {
            if (e[k] !== filter[k]) {
                r = true;
            }
        }
        return r;
    });
};

var getElementsBy = function (array, filter) {
    return $.grep(array, function (e) {
        var r = true;
        for (var k in filter) {
            if (e[k] !== filter[k]) {
                r = false;
            }
        }
        return r;
    });
};


var DawClient = function () {
};

DawClient.BEFORE_PROCESS = 'before_process';
DawClient.AFTER_PROCESS = 'after_process';
DawClient.WAITING_TRANSITION_PROCESSES = [];

DawClient.PROCESS_CALLBACK_EVENTS = [];

DawClient.APPROVE = 'APPROVE';
DawClient.REJECT = 'REJECT';


DawClient.GETTING_AVAILABLE_STATES_URI = 'GETTING_AVAILABLE_STATES_URI';
DawClient.GETTING_CURRENT_STATE_URI = 'GETTING_CURRENT_STATE_URI';
DawClient.APPROVE_TRANSITION_URI = 'APPROVE_TRANSITION_URI';
DawClient.REJECT_TRANSITION_URI = 'REJECT_TRANSITION_URI';
DawClient.GET_STATE_BY_LABEL_URI = 'GET_STATE_BY_LABEL_URI';
DawClient.SKIP_TRANSITION_URI = 'SKIP_TRANSITION_URI';

DawClient.registerTransitionProcess = function (type, contentTypeId, objectId, field, nextStateId, callbackUri) {
    var currentState = DawClient.getCurrentState(contentTypeId, objectId, field);
    var filter = {contentTypeId: contentTypeId, objectId: objectId, field: field, currentStateId: currentState.id, nextStateId: nextStateId};
    var defaults = {type: type, callbackUri: callbackUri, date: new Date()};
    if (nextStateId) {
        defaults.nextStateId = nextStateId;
    }
    updateOrPush(DawClient.WAITING_TRANSITION_PROCESSES, filter, defaults);
};

DawClient.getTransitionProcesses = function (contentTypeId, objectId, field, nextStateId) {
    var currentState = DawClient.getCurrentState(contentTypeId, objectId, field);
    var filter = {contentTypeId: contentTypeId, objectId: objectId, field: field, currentStateId: currentState.id};
    if (nextStateId) {
        filter.nextStateId = nextStateId;
    }
    return getElementsBy(DawClient.WAITING_TRANSITION_PROCESSES, filter);
};


DawClient.unRegisterTransitionProcess = function (contentTypeId, objectId, field, nextStateId) {
    var currentState = DawClient.getCurrentState(contentTypeId, objectId, field);
    DawClient.WAITING_TRANSITION_PROCESSES = removeElementBy(DawClient.WAITING_TRANSITION_PROCESSES, {contentTypeId: contentTypeId, objectId: objectId, field: field, currentStateId: currentState.id, nextStateId: nextStateId});
};


DawClient.commitLastTransitionProcess = function (contentTypeId, objectId, field) {
    var waitingProcesses = DawClient.getTransitionProcesses(contentTypeId, objectId, field);

    var results = $.grep(waitingProcesses,
                         function (e) {
                             var maxDate = new Date(Math.max.apply(Math, waitingProcesses.map(
                                 function (o) {
                                     return o.date;
                                 })));
                             return e.date.getTime() >= maxDate.getTime();
                         });
    if (results.length) {
        var waitingTransitionProcess = results[0];
        DawClient.commitTransitionProcess.apply(undefined, [
            waitingTransitionProcess.contentTypeId,
            waitingTransitionProcess.objectId,
            waitingTransitionProcess.field,
            waitingTransitionProcess.currentStateId,
            waitingTransitionProcess.nextStateId
        ]);
    }
    else {
        throw 'No transition to be committed!';
    }
};

DawClient.commitTransitionProcess = function (contentTypeId, objectId, field, currentStateId, nextStateId) {
    var waitingTransitionProcess = DawClient.getTransitionProcesses(contentTypeId, objectId, field, nextStateId);
    if (waitingTransitionProcess.length) {
        waitingTransitionProcess = waitingTransitionProcess[0];
        DawClient.processTransition.apply(undefined, [
            waitingTransitionProcess.type,
            waitingTransitionProcess.callbackUri,
            waitingTransitionProcess.contentTypeId,
            waitingTransitionProcess.objectId,
            waitingTransitionProcess.field,
            waitingTransitionProcess.nextStateId,
            true,
            waitingTransitionProcess.currentStateId,
        ]);
    }
    else {
        throw 'No transition to be committed!';
    }
};


DawClient.redirectUri = function (uri) {
    window.location = uri;
};


DawClient.registerProcessCallBack = function (type, sourceStateId, destinationStateId, fn, contentTypeId, objectId, field) {
    var filter = {type: type, sourceStateId: sourceStateId, destinationStateId: destinationStateId};
    if (contentTypeId) {
        filter.contentTypeId = contentTypeId;
    }
    if (objectId) {
        filter.objectId = objectId;
    }
    if (field) {
        filter.field = field;
    }
    var defaults = {fn: fn};
    updateOrPush(DawClient.PROCESS_CALLBACK_EVENTS, filter, defaults);
};

DawClient.unRegisterProcessCallBack = function (type, sourceStateId, destinationStateId, contentTypeId, objectId, field) {
    var filter = {type: type, sourceStateId: sourceStateId, destinationStateId: destinationStateId};
    if (contentTypeId) {
        filter.contentTypeId = contentTypeId;
    }
    if (objectId) {
        filter.objectId = objectId;
    }
    if (field) {
        filter.field = field;
    }
    DawClient.PROCESS_CALLBACK_EVENTS = removeElementBy(DawClient.PROCESS_CALLBACK_EVENTS, filter);

};


DawClient.getProcessCallBacks = function (type, sourceStateId, destinationStateId, contentTypeId, objectId, field) {
    var filter = {type: type, sourceStateId: sourceStateId, destinationStateId: destinationStateId};

    if (contentTypeId) {
        filter.contentTypeId = contentTypeId;
    }
    if (objectId) {
        filter.objectId = objectId;
    }
    if (field) {
        filter.field = field;
    }
    return getElementsBy(DawClient.PROCESS_CALLBACK_EVENTS, filter);
};


DawClient.invokeProcessCallback = function (type, currentStateId, nextStateId, contentTypeId, objectId, field, callback) {
    var processCallBacks = DawClient.getProcessCallBacks(type, currentStateId, nextStateId, contentTypeId, objectId, field);
    processCallBacks = processCallBacks.concat(DawClient.getProcessCallBacks(type, currentStateId, nextStateId, contentTypeId, null, null));
    processCallBacks = processCallBacks.concat(DawClient.getProcessCallBacks(type, currentStateId, nextStateId, null, null, null));
    processCallBacks = _.uniq(processCallBacks, function (e) {
        return JSON.stringify(e);
    });
    var results = [];
    for (var i in processCallBacks) {
        var processCallBack = processCallBacks[i];
        if (processCallBack.fn) {
            results.push(processCallBack.fn.call(undefined, {
                type: type,
                currentStateId: currentStateId,
                nextStateId: nextStateId,
                contentTypeId: contentTypeId,
                objectId: objectId,
                field: field,
                callback: callback
            }));
        }

    }
    return [processCallBacks.length !== 0, results];
};


DawClient.getParameterizedUri = function (uri, args) {
    for (var i in args) {
        var argument = args[i];
        uri = uri.replace('$' + i, argument);
    }
    return uri;
};


/*
 *
 * CLIENT REST REQUESTS
 *
 * */


//noinspection JSCommentMatchesSignature
/**
 * Returns available states of the object given, as JSONArray.
 *
 * @param {number}  contentTypeId :ContentType id of the object that is processed.
 * @param {number}  objectId Object id of the object that is processed.
 * @param {string}  field :Field of the object that is processed.
 * @return {array} Desired states as json array.
 */

DawClient.getAvailableStates = function () {
    var uri = DawClient.getParameterizedUri(DawClient.GETTING_AVAILABLE_STATES_URI, arguments);
    var result = {};
    $.ajax(
        {
            type: 'GET',
            url: uri,
            dataType: 'json',
            async: false,
            success: function (data) {
                result = JSON.parse(data);
            },
            error: function (err) {
                throw err;
            }
        });
    return result;
};


//noinspection JSCommentMatchesSignature
/**
 * Returns current state the object is given.
 *
 * @param {number}  contentTypeId :ContentType id of the object that is processed.
 * @param {number}  objectId Object id of the object that is processed.
 * @param {string}  field :Field of the object that is processed.
 * @return {State} Desired state as dictionary.
 */
DawClient.getCurrentState = function () {
    var uri = DawClient.getParameterizedUri(DawClient.GETTING_CURRENT_STATE_URI, arguments);
    var result = {};

    $.ajax(
        {
            type: 'GET',
            url: uri,
            dataType: 'json',
            async: false,
            success: function (data) {
                result = data;
            },
            error: function (err) {
                throw err;
            }
        });
    return result;
};

//noinspection JSCommentMatchesSignature
/**
 * Returns state by given label as dictionary.
 *
 * @param {string} label The desired states label.
 * @return {State} Desired state as dictionary.
 */
DawClient.getStateByLabel = function () {
    var uri = DawClient.getParameterizedUri(DawClient.GET_STATE_BY_LABEL_URI, arguments);
    var result = {};
    $.ajax(
        {
            type: 'GET',
            url: uri,
            async: false,
            dataType: 'json',
            success: function (data) {
                result = data;
            },
            error: function (err) {
                throw err;
            }
        });
    return result;
};


/**
 * Workflow transition processor. Whenever you want to process any transition, just call this function with the required parameters.
 *
 * @param {string}  type :APPROVE or REJECT
 * @param {string}  callbackUri :redirecting url after the process is done
 * @param {number}  contentTypeId :ContentType id of the object that is processed.
 * @param {number}  objectId Object id of the object that is processed.
 * @param {string}  field :Field of the object that is processed.
 * @param {number}  nextStateId :Next state id of the object that is processed.
 * @param {boolean} skipBeforeAction :Command to ignore registered 'before callbacks'. (Optional)
 * @param {boolean} currentStateId :Current state id of the object that is processed. (Optional)
 */
DawClient.processTransition = function (type, callbackUri, contentTypeId, objectId, field, nextStateId, skipBeforeAction, currentStateId) {
    skipBeforeAction = typeof skipBeforeAction !== 'undefined' ? skipBeforeAction : false;
    currentStateId = typeof currentStateId !== 'undefined' ? currentStateId : DawClient.getCurrentState(contentTypeId, objectId, field).id;

    var uri = null;
    if (type === DawClient.APPROVE) {
        uri = DawClient.APPROVE_TRANSITION_URI;
    }
    else if (type === DawClient.REJECT) {
        uri = DawClient.REJECT_TRANSITION_URI;
    }
    uri = DawClient.getParameterizedUri(uri, Array.prototype.slice.call(arguments, 2));


    var anyInvocation = false;
    if (!skipBeforeAction) {
        DawClient.registerTransitionProcess(type, contentTypeId, objectId, field, nextStateId, callbackUri);
        var result = DawClient.invokeProcessCallback(DawClient.BEFORE_PROCESS, currentStateId, nextStateId, contentTypeId, objectId, field, function () {
            DawClient.commitLastTransitionProcess(contentTypeId, objectId, field);
        });
        anyInvocation = result[0];
    }
    if (skipBeforeAction || !anyInvocation) {
        $.ajax(
            {
                type: 'GET',
                url: uri,
                dataType: 'json',
                success: function () {
                    var result = DawClient.invokeProcessCallback(DawClient.AFTER_PROCESS, currentStateId, nextStateId, contentTypeId, objectId, field, function () {
                        DawClient.redirectUri(callbackUri);
                    });
                    var anyInvocation = result[0];
                    if (!anyInvocation) {
                        DawClient.redirectUri(callbackUri);
                    }
                },
                error: function (err) {
                    throw err;
                }
            });
        DawClient.unRegisterTransitionProcess(contentTypeId, objectId, field, nextStateId);
    }
};


DawClient.skipTransition = function (contentTypeId, objectId, field, destinationStateIds) {
    var uri = DawClient.getParameterizedUri(DawClient.SKIP_TRANSITION_URI, arguments);
    var postData = {
        destinationStateIds: destinationStateIds
    };
    var result = false;
    $.ajax(
        {
            type: 'POST',
            url: uri,
            dataType: 'json',
            data: JSON.stringify(postData),
            contentType: 'application/json',
            async: false,
            success: function () {
                result = true;
            },
            error: function (err) {
                throw err;
            }
        });

    return result;
};




