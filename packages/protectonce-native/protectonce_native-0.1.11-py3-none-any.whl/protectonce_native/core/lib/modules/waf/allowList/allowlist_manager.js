const _ = require('lodash');
class AllowlistManager {
    constructor(allowList) {
        this.allowIP = new Set();
        this.allowParameter = new Set();
        this.allowPaths = new Set();
        this._setAllowList(allowList);
    }
    _setAllowList(allowList) {
        if (!_.isObject(allowList)) { return; }
        allowList = allowList.allowList || {};
        if (_.isArray(allowList.ipAddress)) {
            this.allowIP = new Set(allowList.ipAddress);
        }
        if (_.isArray(allowList.parameter)) {
            this.allowParameter = new Set(allowList.parameter.map(a => a.parameter));
        }
        if (_.isArray(allowList.path)) {
            this.allowPaths = new Set(allowList.path.map(a => a.path));
        }
    }

    shouldBypassRequest(request) {
        if (this._checkIpAllowList(request.sourceIP)) {
            return true;
        }
        return this._checkPathAllowList(request.path);
    }

    filterParameters(request) {
        let allowParameter = this.allowParameter;
        Object.keys(request.queryParams).forEach(function (key) {
            if (allowParameter.has(key)) {
                request.queryParams.pathParams[0] = request.queryParams.pathParams[0].replace(`${key}=${request.queryParams[key]}`, '');
                delete request.queryParams[key];
            }
        });
        return request.queryParams;
    }

    _checkIpAllowList(sourceIP) {
        return this.allowIP.has(sourceIP);
    }

    _checkPathAllowList(path) {
        return this.allowPaths.has(path);
    }
}
module.exports = AllowlistManager;