const _ = require('lodash');
const uuid = require('uuid');
const ProtectOnceContext = require('./context');
const Logger = require('../utils/logger');
const HeartbeatCache = require('../reports/heartbeat_cache');

function createSession() {
    // TODO: This is a stopgap implementation of session id
    const sessionId = uuid.v4();
    ProtectOnceContext.create(sessionId, {});

    Logger.write(Logger.DEBUG && `httpServer: Session created with session id: ${sessionId}`);
    return sessionId;
}

/**
 * Releases the stored http session, this should be called when a request is completed
 * @param  {Object} sessionData The incoming data is of the form:
 *          @param {Object} data This holds following field:
 *              @param {String} poSessionId
 */
function releaseSession(sessionData) {
    try {
        ProtectOnceContext.release(sessionData.data.poSessionId);
        Logger.write(Logger.DEBUG && `httpServer: Releasing data for session id: ${sessionData.data.poSessionId}`);
    } catch (e) {
        Logger.write(Logger.INFO && `httpServer: Failed to release data: ${e}`);
    }
}

/**
 * Stores the http request info in the session context
 * @param  {Object} requestData The incoming data is of the form:
 *          @param {Object} data This holds http request object of the form:
 *              @param {Object} queryParams
 *              @param {Object} headers
 *              @param {String} method
 *              @param {String} path
 *              @param {String} sourceIP
 *              @param {String} poSessionId
 */
function storeHttpRequestInfo(requestData) {
    try {
        ProtectOnceContext.update(requestData.data.poSessionId, requestData.data);
        Logger.write(Logger.DEBUG && `httpServer: Updated request info for session id: ${requestData.data.poSessionId}`);
    } catch (e) {
        Logger.write(Logger.INFO && `httpServer: Failed to store session data: ${e}`);
    }
}

function storeHttpRequestData(requestData) {
    try {
        ProtectOnceContext.update(requestData.data.poSessionId, requestData.data);
        Logger.write(Logger.DEBUG && `httpServer: Updated body for session id: ${requestData.data.poSessionId}`);
    } catch (e) {
        Logger.write(Logger.INFO && `httpServer: Failed to store session data: ${e}`);
    }
}

function getHttpRequestData(requestData) {
    try {
        const requestInfo = ProtectOnceContext.get(requestData.data);
        Logger.write(Logger.DEBUG && `httpServer: Get request info from session: ${JSON.stringify(requestInfo)}`);
        return requestInfo;
    } catch (e) {
        Logger.write(Logger.INFO && `httpServer: Get request info failed: ${e}`);
    }
}

function closeHttpRequest(requestData) {
    try {
        if (!_.isString(requestData.data)) {
            return true;
        }

        const requestInfo = ProtectOnceContext.get(requestData.data);
        Logger.write(Logger.DEBUG && `httpServer: closing request for request: ${JSON.stringify(requestInfo.poSessionId)}`);
        HeartbeatCache.setClosed(requestInfo.poSessionId);
        return requestInfo;
    } catch (e) {
        Logger.write(Logger.INFO && `httpServer: Get request info failed: ${e}`);
    }
}

module.exports = {
    createSession: createSession,
    releaseSession: releaseSession,
    storeHttpRequestInfo: storeHttpRequestInfo,
    storeHttpRequestData: storeHttpRequestData,
    getHttpRequestData: getHttpRequestData,
    closeHttpRequest: closeHttpRequest
};
