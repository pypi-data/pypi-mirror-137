const _ = require('lodash');

const openRASP = require('./openRASP');
const ProtectOnceContext = require('../context');
const RegExpManager = require('../../utils/regex_manager');
const { SecurityActivity, Event, Report, ReportType } = require('../../reports/report');
const HeartbeatCache = require('../../reports/heartbeat_cache');
const RulesManager = require('../../rules/rules_manager');
const { RuntimeData, CommandData, XmlData, SsrfData, SsrfRedirectData } = require('../../runtime/runtime_data');
const { SQLData } = require('../../runtime/runtime_data');
const { FileData } = require('../../runtime/runtime_data');
const Logger = require('../../utils/logger');

function createSecurityActivity(inputData, result, context, options) {
    let reportType = setBlockOrAlert(options.runtimeData, options.shouldBlock);
    const request = inputData.data || {};
    let securityActivity = new SecurityActivity(request.poSessionId, "status", context.sourceIP, "200", context.method, context.path, "user");
    //Added Event for new implementation of Security Activity
    var event = new Event("rasp", request.poSessionId, (reportType == ReportType.REPORT_TYPE_BLOCK), result && result.confidence, new Date(),
        new Date(), result.name, "", result.message);
    securityActivity.addEvent(event);
    HeartbeatCache.cacheReport(securityActivity);
}
function setBlockOrAlert(runtimeData, shouldBlock) {
    let reportType = ReportType.REPORT_TYPE_ALERT;
    if (shouldBlock === true) {
        runtimeData.setBlock();
        reportType = ReportType.REPORT_TYPE_BLOCK;
    } else {
        runtimeData.setAlert();
    }
    return reportType;
}

function checkRegexp(data) {
    const runtimeData = new RuntimeData(data);
    const rule = RulesManager.getRule(runtimeData.context);

    if (!rule) {
        Logger.write(Logger.DEBUG && `RASP.checkRegexp: No rule found for id: ${runtimeData.context}`);
        return runtimeData;
    }

    const regExpressions = rule.regExps;
    let match = false;
    const args = runtimeData.args;
    for (let regExpId of regExpressions) {
        const regExp = RegExpManager.getRegExp(regExpId);

        // TODO: Use args from the rule instead of scanning all args
        for (let arg of args) {
            // FIXME: What about arguments which are other than string
            if (!_.isString(arg)) {
                continue;
            }

            if (arg.search(regExp) >= 0) {
                match = true;
                break;
            }
        }

        if (match === true) {
            break;
        }
    }

    if (match) {
        setBlockOrAlert(runtimeData, rule.shouldBlock);
        if (rule.shouldBlock === true) {
            runtimeData.message = 'ProtectOnce has blocked an attack'
        } else {
            runtimeData.message = 'ProtectOnce has detected an attack';
        }
        Logger.write(Logger.DEBUG && `RASP.checkRegexp: Attack found: ${runtimeData.message}`);
    }

    return runtimeData;
}

function detectSQLi(data) {
    const sqlData = new SQLData(data.data);

    const rule = RulesManager.getRule(data.context);
    if (!rule) {
        Logger.write(Logger.DEBUG && `RASP.detectSQLi: No rule found for id: ${data.context}`);
        return sqlData;
    }

    const context = ProtectOnceContext.get(sqlData.sessionId);
    const result = openRASP.detectSQLi(sqlData.query, sqlData.callStack, context);
    if (!result) {
        Logger.write(Logger.DEBUG && `RASP.detectSQLi: No attack found in query: ${sqlData.query}`);
        return sqlData;
    }

    createSecurityActivity(data, result, context, { runtimeData: sqlData, shouldBlock: rule.shouldBlock });
    Logger.write(Logger.DEBUG && `RASP.detectSQLi: Attack found in query: ${sqlData.query}`);
    return sqlData;
}

function executeLFI(lfiType, data, fileData) {

    const rule = RulesManager.getRule(data.context);
    if (!rule) {
        Logger.write(Logger.DEBUG && `RASP.executeLFI: No rule found for type: ${lfiType}, id: ${data.context}`);
        return fileData;
    }

    const context = ProtectOnceContext.get(fileData.sessionId);
    const result = openRASP.detectLFI(lfiType, fileData.source, fileData.dest, fileData.path, fileData.realpath, fileData.filename, fileData.stack, fileData.url, context);
    if (!result) {
        Logger.write(Logger.DEBUG && `RASP.executeLFI: No attack found in data: ${JSON.stringify(fileData)}`);
        return fileData;
    }
    createSecurityActivity(data, result, context, { runtimeData: fileData, shouldBlock: rule.shouldBlock });
    Logger.write(Logger.DEBUG && `RASP.executeLFI: Attack found in data: ${JSON.stringify(fileData)}`);
    return fileData;
}

function detectOpenFileLFI(data) {
    const fileData = new FileData(data.data);
    if (fileData.mode && fileData.mode.toLowerCase() === 'read') {
        return executeLFI('readFile', data, fileData);
    } else if (fileData.mode && fileData.mode.toLowerCase() === 'write') {
        return executeLFI('writeFile', data, fileData);
    }
}


function detectUploadFileLFI(data) {
    const fileData = new FileData(data.data);
    return executeLFI('fileUpload', data, fileData);
}

function detectDeleteFileLFI(data) {
    const fileData = new FileData(data.data);
    return executeLFI('deleteFile', data, fileData);
}

function detectRenameFileLFI(data) {
    const fileData = new FileData(data.data);
    return executeLFI('rename', data, fileData);
}


function detectListDirectoryLFI(data) {
    const fileData = new FileData(data.data);
    return executeLFI('directory', data, fileData);
}

function detectIncludeLFI(data) {
    const fileData = new FileData(data.data);
    return executeLFI('include', data, fileData);
}

function detectShellShock(data) {
    const commandData = new CommandData(data.data);

    const rule = RulesManager.getRule(data.context);
    if (!rule) {
        Logger.write(Logger.DEBUG && `RASP.detectShellShock: No rule found for id: ${data.context}`);
        return commandData;
    }

    const context = ProtectOnceContext.get(commandData.sessionId);
    const result = openRASP.detectShellShock(commandData.command, commandData.stack, context);
    if (!result) {
        Logger.write(Logger.DEBUG && `RASP.detectShellShock: No attack found for command: ${commandData.command}`);
        return commandData;
    }

    createSecurityActivity(data, result, context, { runtimeData: commandData, shouldBlock: rule.shouldBlock });
    Logger.write(Logger.DEBUG && `RASP.detectShellShock: Attack found for command: ${commandData.command}`);
    return commandData;
}


function preprocess_detectSsrf(data) {
    const param_url = new URL(decodeURIComponent(data.url));
    data.url = param_url.pathname;
    data.hostname = param_url.hostname;
    const ip = data.hostname.match(/\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b/);
    if (ip === null) {
        data.ip = [];
    }
    else {
        data.ip = ip;
    }
    if (!data.hostname && ip === null) {
        data.url = param_url.toString();
    }
    return data;
}


function detectSsrf(data) {
    data.data = preprocess_detectSsrf(data.data);
    const ssrfData = new SsrfData(data.data);

    const rule = RulesManager.getRule(data.context);
    if (!rule) {
        Logger.write(Logger.DEBUG && `RASP.detectSsrf: No rule found for id: ${data.context}`);
        return ssrfData;
    }

    const context = ProtectOnceContext.get(ssrfData.sessionId);
    const result = openRASP.detectSsrf(ssrfData.url, ssrfData.hostname, ssrfData.ip, ssrfData.origin_ip, ssrfData.origin_hostname, context);
    if (!result) {
        Logger.write(Logger.DEBUG && `RASP.detectSsrf: No attack found for data: ${JSON.stringify(ssrfData)}`);
        return ssrfData;
    }

    createSecurityActivity(data, result, context, { runtimeData: ssrfData, shouldBlock: rule.shouldBlock });
    Logger.write(Logger.DEBUG && `RASP.detectSsrf: Attack found for data: ${JSON.stringify(ssrfData)}`);
    return ssrfData;
}


function detectXxe(data) {
    const xmlData = new XmlData(data.data);

    const rule = RulesManager.getRule(data.context);
    if (!rule) {
        Logger.write(Logger.DEBUG && `RASP.detectXxe: No rule found for id: ${data.context}`);
        return xmlData;
    }

    const context = ProtectOnceContext.get(xmlData.sessionId);
    const result = openRASP.detectXxe(xmlData.entity, context);
    if (!result) {
        Logger.write(Logger.DEBUG && `RASP.detectXxe: No attack found for entity: ${xmlData.entity}`);
        return xmlData;
    }

    createSecurityActivity(data, result, context, { runtimeData: xmlData, shouldBlock: rule.shouldBlock });
    Logger.write(Logger.DEBUG && `RASP.detectXxe: Attack found for entity: ${xmlData.entity}`);
    return xmlData;
}


function detectSsrfRedirect(data) {
    const ssrfRedirectData = new SsrfRedirectData(data.data);

    const rule = RulesManager.getRule(data.context);
    if (!rule) {
        Logger.write(Logger.DEBUG && `RASP.detectSsrfRedirect: No rule found for id: ${data.context}`);
        return ssrfRedirectData;
    }

    const context = ProtectOnceContext.get(ssrfRedirectData.sessionId);
    const result = openRASP.detectSsrfRedirect(ssrfRedirectData.hostname, ssrfRedirectData.ip, ssrfRedirectData.url, ssrfRedirectData.url2, ssrfRedirectData.hostname2,
        ssrfRedirectData.ip2, ssrfRedirectData.port2, context);
    if (!result) {
        Logger.write(Logger.DEBUG && `RASP.detectSsrfRedirect: No attack found for data: ${JSON.stringify(ssrfRedirectData)}`);
        return ssrfRedirectData;
    }

    createSecurityActivity(data, result, context, { runtimeData: ssrfRedirectData, shouldBlock: rule.shouldBlock });
    Logger.write(Logger.DEBUG && `RASP.detectSsrfRedirect: Attack found for data: ${JSON.stringify(ssrfRedirectData)}`);
    return ssrfRedirectData;
}

module.exports = {
    checkRegexp: checkRegexp,
    detectSQLi: detectSQLi,
    detectOpenFileLFI: detectOpenFileLFI,
    detectUploadFileLFI: detectUploadFileLFI,
    detectDeleteFileLFI: detectDeleteFileLFI,
    detectRenameFileLFI: detectRenameFileLFI,
    detectListDirectoryLFI: detectListDirectoryLFI,
    detectIncludeLFI: detectIncludeLFI,
    detectShellShock: detectShellShock,
    detectSsrf: detectSsrf,
    detectXxe: detectXxe,
    detectSsrfRedirect: detectSsrfRedirect
}
