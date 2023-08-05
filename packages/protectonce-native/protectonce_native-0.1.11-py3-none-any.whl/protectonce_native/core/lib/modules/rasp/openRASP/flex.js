'use strict';

const poNative = require('@protectonce/native');

global.tokenize = function (query, type) {
    const result = []
    const arr = poNative.flex_tokenize(query, type) || []
    for (let i = 0; i < arr.length; i += 2) {
        const start = arr[i]
        const stop = arr[i + 1]
        const text = query.substring(start, stop)
        result.push({ start, stop, text })
    }
    return result
}