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

var BEFORE_PROCESS = 'before_process';
var AFTER_PROCESS = 'after_process';
var WAITING_TRANSITION_PROCESSES = [];

var PROCESS_EVENTS = [];

var APPROVE = 'APPROVE';
var REJECT = 'REJECT';

Array.prototype.updateOrPush = function (filter, defaults) {
    var results = $.grep(this, function (e) {
        var r = true
        for (k in filter) {
            if (e[k] != filter[k]) {
                r = false
            }
        }
        if (r) {
            for (k in defaults) {
                e[k] = defaults[k]
            }
        }
        return r
    });

    if (!results.length) {
        this.push($.extend(filter, defaults))
    }
};

Array.prototype.removeElementBy = function (filter) {
    return $.grep(this, function (e) {
        var r = false;
        for (k in filter) {
            if (e[k] != filter[k]) {
                r = true
            }
        }
        return r
    });
};

Array.prototype.getElementsBy = function (filter) {
    return $.grep(this, function (e) {
        var r = true;
        for (k in filter) {
            if (e[k] != filter[k]) {
                r = false
            }
        }
        return r
    });
};


function registerTransitionProcess(type, contentTypeId, objectId, field, nextStateId, callbackUri) {
    var currentState = getCurrentState(contentTypeId, objectId, field);
    var filter = {contentTypeId: contentTypeId, objectId: objectId, field: field, currentStateId: currentState.id, nextStateId: nextStateId};
    var defaults = {type: type, callbackUri: callbackUri}
    if (nextStateId) {
        defaults['nextStateId'] = nextStateId
    }
    WAITING_TRANSITION_PROCESSES.updateOrPush(filter, defaults);

}
function unRegisterTransitionProcess(contentTypeId, objectId, field, nextStateId) {
    var currentState = getCurrentState(contentTypeId, objectId, field);
    WAITING_TRANSITION_PROCESSES = WAITING_TRANSITION_PROCESSES.removeElementBy({contentTypeId: contentTypeId, objectId: objectId, field: field, currentStateId: currentState.id, nextStateId: nextStateId})
}


function getTransitionProcesses(contentTypeId, objectId, field, nextStateId) {
    var currentState = getCurrentState(contentTypeId, objectId, field);
    var filter = {contentTypeId: contentTypeId, objectId: objectId, field: field, currentStateId: currentState.id}
    if (nextStateId) {
        filter['nextStateId'] = nextStateId
    }
    return WAITING_TRANSITION_PROCESSES.getElementsBy(filter)
}

function commitLastTransitionProcess(contentTypeId, objectId, field) {
    var result = $.grep(WAITING_TRANSITION_PROCESSES.getElementsBy(
        {
            contentTypeId: contentTypeId,
            objectId: objectId,
            field: field
        }), function (e) {
        return e.date >= Math.max.apply(Math, WAITING_TRANSITION_PROCESSES.map(function (o) {
            return o.date;
        }))
    });
    if (result.length) {
        var waitingTransitionProcess = result[0];
        commitTransitionProcess.apply(undefined, [
            waitingTransitionProcess.type,
            waitingTransitionProcess.contentTypeId,
            waitingTransitionProcess.objectId,
            waitingTransitionProcess.field,
            waitingTransitionProcess.callbackUri,
            waitingTransitionProcess.currentStateId,
            waitingTransitionProcess.nextStateId
        ])
    }
}

function redirectUri(uri) {
    window.location = uri
}

function commitTransitionProcess(contentTypeId, objectId, field, currentStateId, nextStateId) {
    var waitingTransitionProcess = getTransitionProcesses(contentTypeId, objectId, field, currentStateId, nextStateId);
    if (waitingTransitionProcess.length) {
        waitingTransitionProcess = waitingTransitionProcess[0]
        processTransition.apply(undefined, [
            waitingTransitionProcess.type,
            waitingTransitionProcess.callbackUri,
            waitingTransitionProcess.contentTypeId,
            waitingTransitionProcess.objectId,
            waitingTransitionProcess.field,
            waitingTransitionProcess.currentStateId,
            waitingTransitionProcess.nextStateId,
            true
        ])
    }
    else {
        console.error('No transition to be committed!')
    }
}


function registerProcessCallBack(type, sourceStateId, destinationStateId, fn, contentTypeId, objectId, field) {
    var filter = {type: type, sourceStateId: sourceStateId, destinationStateId: destinationStateId}
    if (contentTypeId) {
        filter['contentTypeId'] = contentTypeId;
    }
    if (objectId) {
        filter['objectId'] = objectId;
    }
    if (field) {
        filter['field'] = field;
    }
    var defaults = {type: type, fn: fn};
    PROCESS_EVENTS.updateOrPush(filter, defaults);
}

function unRegisterProcessCallBack(type, sourceStateId, destinationStateId, contentTypeId, objectId, field) {
    var filter = {type: type, sourceStateId: sourceStateId, destinationStateId: destinationStateId}
    if (contentTypeId) {
        filter['contentTypeId'] = contentTypeId;
    }
    if (objectId) {
        filter['objectId'] = objectId;
    }
    if (field) {
        filter['field'] = field;
    }
    PROCESS_EVENTS = PROCESS_EVENTS.removeElementBy(filter)

}


function getProcessCallBacks(type, sourceStateId, destinationStateId, contentTypeId, objectId, field) {
    var filter = {type: type, sourceStateId: sourceStateId, destinationStateId: destinationStateId}

    if (contentTypeId) {
        filter['contentTypeId'] = contentTypeId;
    }
    if (objectId) {
        filter['objectId'] = objectId;
    }
    if (field) {
        filter['field'] = field;
    }
    return PROCESS_EVENTS.getElementsBy(filter)
}


function invokeProcessCallback(type, currentStateId, nextStateId, contentTypeId, objectId, field, callback) {
    var processCallBacks = getProcessCallBacks(type, currentStateId, nextStateId, contentTypeId, objectId, field)
    processCallBacks = processCallBacks.concat(getProcessCallBacks(type, currentStateId, nextStateId, contentTypeId, null, null))
    processCallBacks = processCallBacks.concat(getProcessCallBacks(type, currentStateId, nextStateId, null, null, null))
    var results = [];
    if (processCallBacks.length) {
        for (i in processCallBacks) {
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
                }))
            }

        }
    }
    return [processCallBacks.length != 0, results]
}


function getParameterizedUri(uri, args) {
    for (i in args) {
        var argument = args[i]
        uri = uri.replace('$' + i, argument)
    }
    return uri;
}

/*
 *
 * CLIENT REST REQUESTS
 *
 * */


function getAvailableStates(contentTypeId, objectId, field) {
    var uri = getParameterizedUri(GETTING_AVAILABLE_STATES_URI, arguments)
    //TODO: do ajax request;
    $.ajax({
               type: "GET",
               url: uri,
               dataType: "application/json",
               async: false,
               success: function (data) {
                   return JSON.parse(data)
               },
               error: function (err) {
                   console.error(err)
               }
           });
}

function getCurrentState(contentTypeId, objectId, field) {
    var uri = getParameterizedUri(GETTING_CURRENT_STATE_URI, arguments)
    var result;

    $.ajax({
               type: "GET",
               url: uri,
               dataType: "json",
               async: false,
               success: function (data) {
                   result = data
               },
               error: function (err) {
                   console.error(err)
               }
           });
    return result;
}


function processTransition(type, callbackUri, contentTypeId, objectId, field, nextStateId, skipBeforeAction, currentStateId) {
    skipBeforeAction = typeof skipBeforeAction !== 'undefined' ? skipBeforeAction : false;
    currentStateId = typeof currentStateId !== 'undefined' ? currentStateId : getCurrentState(contentTypeId, objectId, field).id;

    var uri = null;
    if (type == APPROVE) {
        uri = APPROVE_TRANSITION_URI
    }
    else if (type == REJECT) {
        uri = REJECT_TRANSITION_URI
    }
    uri = getParameterizedUri(uri, Array.prototype.slice.call(arguments, 2))


    var anyInvocation = false;
    if (!skipBeforeAction) {
        var result = invokeProcessCallback(BEFORE_PROCESS, currentStateId, nextStateId, contentTypeId, objectId, field, function () {
            commitLastTransitionProcess(contentTypeId, objectId, field)
        });
        anyInvocation = result[0]
    }
    if (!skipBeforeAction || !anyInvocation) {
        $.ajax({
                   type: "GET",
                   url: uri,
                   dataType: 'json',
                   success: function (data) {
                       invokeProcessCallback(AFTER_PROCESS, currentStateId, nextStateId, contentTypeId, objectId, field, function () {
                           redirectUri(callbackUri)
                       })
                   },
                   error: function (err, data) {
                       console.log(arguments)
                       console.error(err)
                   }
               });
    } else {
        registerTransitionProcess(BEFORE_PROCESS, contentTypeId, objectId, field, nextStateId, callbackUri)
    }
}


function getStateByLabel(stateLabel) {
    var uri = getParameterizedUri(GET_STATE_BY_LABEL_URI, arguments)
    var result;
    $.ajax({
               type: "GET",
               url: uri,
               async: false,
               dataType: 'json',
               success: function (data) {
                   result = data
               },
               error: function (err) {
                   console.error(err)
               }
           });
    return result;
}











