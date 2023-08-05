const _ = require('lodash');

const { WAFEvent, ReportType, SecurityActivity } = require('../reports/report');
const ReportCache = require('../reports/reports_cache');

function createSecurityActivity(data) {
    if (!_.isString(data.data.poSessionId)) {
        return;
    }

    const securityActivity = new SecurityActivity(data.data.poSessionId, '', data.data.sourceIP, '', '', data.data.path);
    ReportCache.cache(securityActivity);
}

function generateWafEvents(data) {
    const findings = data.data.findings;
    if (!_.isArray(findings) || findings.length === 0) {
        return { 'action': 'none' };
    }

    const poSessionId = data.data.poSessionId;
    const securityActivity = new SecurityActivity(poSessionId);
    let blocked = false;
    for (let finding of findings) {
        blocked = blocked || finding.action === ReportType.REPORT_TYPE_BLOCK;
        const event = new WAFEvent(poSessionId, (finding.action === ReportType.REPORT_TYPE_BLOCK), finding.flowName);
        securityActivity.addEvent(event);
    }

    ReportCache.cache(securityActivity);

    if (blocked) {
        return { 'action': 'abort' };
    }

    return { 'action': 'none' };
}

module.exports = {
    createSecurityActivity: createSecurityActivity,
    generateWafEvents: generateWafEvents
};
