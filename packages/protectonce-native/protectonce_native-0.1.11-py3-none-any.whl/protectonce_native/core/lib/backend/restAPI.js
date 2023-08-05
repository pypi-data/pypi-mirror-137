const https = require('https');
const Constants = require('../utils/constants');

const BackendConfig = require('./config');
const Token = require('./token');
const Logger = require('../utils/logger');

class RestAPI {
    constructor(path, data) {
        this._path = path;
        try {
            this._data = JSON.stringify(data);
        } catch (e) {
            this._data = '';
        }
    }

    get url() {
        return BackendConfig.endpoint;
    }

    get port() {
        return BackendConfig.port;
    }

    get postOptions() {
        const postOpts = {
            hostname: this.url,
            path: this._path,
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Content-Length': this._data.length,
                'Authorization': Token.authHeader
            }
        };

        if (this.port) {
            postOpts['port'] = this.port;
        }

        if (Token.refreshToken) {
            postOpts.headers[Constants.BACKEND_REST_API_REFRESH_TOKEN_HEADER] = Token.refreshToken
        }

        return postOpts;
    }

    post() {
        return new Promise((resolve, reject) => {
            Logger.write(Logger.DEBUG && `REST API: Sending request to: ${this.url}`);
            const that = this;
            const req = https.request(this.postOptions, res => {
                Logger.write(Logger.DEBUG && `REST API: url: ${that.url} returned status: ${res.statusCode}`);
                if (res.statusCode === Constants.APP_DELETE_STATUS_CODE) {
                    resolve({ 'data': '{}', 'statusCode': res.statusCode });
                    return;
                }

                let data = '';
                res.on('data', d => {
                    data += d.toString();
                })

                res.on('end', () => {
                    const responseObj = JSON.parse(data);
                    const authDetails = responseObj['authDetails'];
                    if (authDetails) {
                        Token.update(authDetails);
                    }
                    resolve({ 'data': JSON.stringify(responseObj), 'statusCode': res.statusCode });
                });
            })

            req.on('error', error => {
                // Error should be printed by caller to avoid duplicate prints
                reject(error);
            })

            req.write(this._data)
            req.end()
        });
    }
}

module.exports = RestAPI;
