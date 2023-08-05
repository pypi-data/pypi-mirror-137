const _ = require('lodash');

class ReportCache {
    constructor() {
        this._cache = {};
    }

    cache(report) {
        if (!this._cache[report.request_id]) {
            this._cache[report.request_id] = report;
        } else {
            const mergeEvent = this._cache[report.request_id].events.concat(...report.events);
            this._cache[report.request_id].events = mergeEvent;
        }
    }

    flush() {
        const reports = [];
        for (let requestId in this._cache) {
            const report = this._cache[requestId];
            if (report.isClosed()) {
                reports.push(this._cache[report.request_id]);
                delete this._cache[requestId];
            }
        }
        return reports;
    }

    setClosed(id) {
        if (this._cache[id]) {
            this._cache[id].setClosed();
        }
    }
}

module.exports = new ReportCache();


