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


var DawClient = function () {
}

DawClient.BEFORE_PROCESS = 'before_process';
DawClient.AFTER_PROCESS = 'after_process';
DawClient.WAITING_TRANSITION_PROCESSES = [];

DawClient.PROCESS_EVENTS = [];

DawClient.APPROVE = 'APPROVE';
DawClient.REJECT = 'REJECT';

DawClient.registerTransitionProcess = function (type, contentTypeId, objectId, field, nextStateId, callbackUri) {
    var currentState = DawClient.getCurrentState(contentTypeId, objectId, field);
    var filter = {contentTypeId: contentTypeId, objectId: objectId, field: field, currentStateId: currentState.id, nextStateId: nextStateId};
    var defaults = {type: type, callbackUri: callbackUri}
    if (nextStateId) {
        defaults['nextStateId'] = nextStateId
    }
    DawClient.WAITING_TRANSITION_PROCESSES.updateOrPush(filter, defaults);

}
DawClient.unRegisterTransitionProcess = function (contentTypeId, objectId, field, nextStateId) {
    var currentState = DawClient.getCurrentState(contentTypeId, objectId, field);
    DawClient.WAITING_TRANSITION_PROCESSES = DawClient.WAITING_TRANSITION_PROCESSES.removeElementBy({contentTypeId: contentTypeId, objectId: objectId, field: field, currentStateId: currentState.id, nextStateId: nextStateId})
}


DawClient.getTransitionProcesses = function (contentTypeId, objectId, field, nextStateId) {
    var currentState = DawClient.getCurrentState(contentTypeId, objectId, field);
    var filter = {contentTypeId: contentTypeId, objectId: objectId, field: field, currentStateId: currentState.id}
    if (nextStateId) {
        filter['nextStateId'] = nextStateId
    }
    return DawClient.WAITING_TRANSITION_PROCESSES.getElementsBy(filter)
}

DawClient.commitLastTransitionProcess = function (contentTypeId, objectId, field) {
    var result = $.grep(DawClient.WAITING_TRANSITION_PROCESSES.getElementsBy(
        {
            contentTypeId: contentTypeId,
            objectId: objectId,
            field: field
        }), function (e) {
        return e.date >= Math.max.apply(Math, DawClient.WAITING_TRANSITION_PROCESSES.map(function (o) {
            return o.date;
        }))
    });
    if (result.length) {
        var waitingTransitionProcess = result[0];
        DawClient.commitTransitionProcess.apply(undefined, [
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

DawClient.redirectUri = function (uri) {
    window.location = uri
}

DawClient.commitTransitionProcess = function (contentTypeId, objectId, field, currentStateId, nextStateId) {
    var waitingTransitionProcess = DawClient.getTransitionProcesses(contentTypeId, objectId, field, currentStateId, nextStateId);
    if (waitingTransitionProcess.length) {
        waitingTransitionProcess = waitingTransitionProcess[0]
        DawClient.processTransition.apply(undefined, [
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


DawClient.registerProcessCallBack = function (type, sourceStateId, destinationStateId, fn, contentTypeId, objectId, field) {
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
    DawClient.PROCESS_EVENTS.updateOrPush(filter, defaults);
}

DawClient.unRegisterProcessCallBack = function (type, sourceStateId, destinationStateId, contentTypeId, objectId, field) {
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
    DawClient.PROCESS_EVENTS = DawClient.PROCESS_EVENTS.removeElementBy(filter)

}


DawClient.getProcessCallBacks = function (type, sourceStateId, destinationStateId, contentTypeId, objectId, field) {
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
    return DawClient.PROCESS_EVENTS.getElementsBy(filter)
}


DawClient.invokeProcessCallback = function (type, currentStateId, nextStateId, contentTypeId, objectId, field, callback) {
    var processCallBacks = DawClient.getProcessCallBacks(type, currentStateId, nextStateId, contentTypeId, objectId, field)
    processCallBacks = processCallBacks.concat(DawClient.getProcessCallBacks(type, currentStateId, nextStateId, contentTypeId, null, null))
    processCallBacks = processCallBacks.concat(DawClient.getProcessCallBacks(type, currentStateId, nextStateId, null, null, null))
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


DawClient.getParameterizedUri = function (uri, args) {
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


DawClient.getAvailableStates = function (contentTypeId, objectId, field) {
    var uri = DawClient.getParameterizedUri(GETTING_AVAILABLE_STATES_URI, arguments)
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

DawClient.getCurrentState = function (contentTypeId, objectId, field) {
    var uri = DawClient.getParameterizedUri(GETTING_CURRENT_STATE_URI, arguments)
    var result = {};

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


DawClient.processTransition = function (type, callbackUri, contentTypeId, objectId, field, nextStateId, skipBeforeAction, currentStateId) {
    skipBeforeAction = typeof skipBeforeAction !== 'undefined' ? skipBeforeAction : false;
    currentStateId = typeof currentStateId !== 'undefined' ? currentStateId : DawClient.getCurrentState(contentTypeId, objectId, field).id;

    var uri = null;
    if (type == DawClient.APPROVE) {
        uri = APPROVE_TRANSITION_URI
    }
    else if (type == DawClient.REJECT) {
        uri = REJECT_TRANSITION_URI
    }
    uri = DawClient.getParameterizedUri(uri, Array.prototype.slice.call(arguments, 2))


    var anyInvocation = false;
    if (!skipBeforeAction) {
        var result = DawClient.invokeProcessCallback(DawClient.BEFORE_PROCESS, currentStateId, nextStateId, contentTypeId, objectId, field, function () {
            DawClient.commitLastTransitionProcess(contentTypeId, objectId, field)
        });
        anyInvocation = result[0]
    }
    if (!skipBeforeAction || !anyInvocation) {
        $.ajax({
                   type: "GET",
                   url: uri,
                   dataType: 'json',
                   success: function (data) {
                       DawClient.invokeProcessCallback(DawClient.AFTER_PROCESS, currentStateId, nextStateId, contentTypeId, objectId, field, function () {
                           DawClient.redirectUri(callbackUri)
                       })
                   },
                   error: function (err, data) {
                       console.log(arguments)
                       console.error(err)
                   }
               });
    } else {
        DawClient.registerTransitionProcess(DawClient.BEFORE_PROCESS, contentTypeId, objectId, field, nextStateId, callbackUri)
    }
}


DawClient.getStateByLabel = function (stateLabel) {
    var uri = DawClient.getParameterizedUri(GET_STATE_BY_LABEL_URI, arguments)
    var result = {};
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











