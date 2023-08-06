class HeartbeatCache {
  constructor() {
    this._cache = {
        reports: {},
        inventory: {}
    };
  }

  cacheInventory(inventory) {
      this._cache.inventory = inventory;
  }

  getInventory() {
      return this._cache.inventory;
  }

  cacheReport(report) {
    if (!this._cache.reports[report.request_id]) {
      this._cache.reports[report.request_id] = report;
    } else {
      const mergeEvent = this._cache.reports[report.request_id].events.concat(
        ...report.events
      );
      this._cache.reports[report.request_id].events = mergeEvent;
    }
  }

  flush() {
    const reports = [];
    for (let requestId in this._cache.reports) {
      const report = this._cache.reports[requestId];
      if (report.isClosed()) {
        reports.push(this._cache.reports[report.request_id]);
        delete this._cache.reports[requestId];
      }
    }
    const inventory = this._cache.inventory;
    this._cache.inventory = {};
    return {
        reports,
        inventory
    };
  }

  setClosed(id) {
    if (this._cache.reports[id]) {
      this._cache.reports[id].setClosed();
    }
  }
}

module.exports = new HeartbeatCache();
