const os = require('os');
const coreVersion = require('../../package.json').version;

// TODO: read applicationId and agentId from config
const applicationId = "1234567890_sql_injection";
const agentId = "1abd5b6f-028f-48df-87fb-9ad1d8e6d331";

class Config {
    set runtimeInfo(runtimeInfo) {
        this._agentRuntimeVersion = runtimeInfo.version || '';
        this._runtime = runtimeInfo.runtime || '';
        this._runtimeVersion = runtimeInfo.runtimeVersion || '';
        this._bom = runtimeInfo.bom || [];
    }

    get info() {
        const info = {
            "os": os.platform(),
            "osVersion": os.release(),
            "agentCoreVersion": coreVersion,
            "timestamp": Date.now(),
            "applicationId": applicationId,
            "agentId": agentId
        };

        info['agentRuntimeVersion'] = this._agentRuntimeVersion;
        info['agentCoreVersion'] = coreVersion;
        info['runtime'] = this._runtime;
        info['runtimeVersion'] = this._runtimeVersion;
        info['bom'] = this._bom;

        return info;
    }

    get syncInterval() {
        // TODO: Read this from rule or config
        return 20000; // 20 secs
    }
}

module.exports = new Config();
