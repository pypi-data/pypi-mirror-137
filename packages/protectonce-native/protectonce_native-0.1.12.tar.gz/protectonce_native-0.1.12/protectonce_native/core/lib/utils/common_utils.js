const _ = require('lodash');

function toBoolean(value) {
    if (!value) {
        return false;
    }
    if (typeof value == 'number' || typeof value == 'boolean') {
        return !!value;
    }
    return _.replace(_.trim(value.toLowerCase()), /[""'']/ig, '') === 'true' ? true : false;
}

function isPromise(promise) {
    return !!promise && typeof promise.then === 'function'
}

_.mixin({
    'toBoolean': toBoolean,
    'isPromise': isPromise
});
