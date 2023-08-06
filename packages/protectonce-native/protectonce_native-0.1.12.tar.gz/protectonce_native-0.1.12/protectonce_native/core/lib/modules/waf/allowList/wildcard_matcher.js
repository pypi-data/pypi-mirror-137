const BaseMatcher = require('./base_matcher');
const logger = require('../../../utils/logger');

class WildcardMatcher extends BaseMatcher {
  constructor(allowItem) {
    super();
    this._regEx = this._getRegEx(allowItem);
  }

  _getRegEx(allowItem) {
    if (allowItem.ipAddress) {
      return new RegExp(
        `${allowItem.ipAddress
          .replace(/\*/gm, '\\d{1,3}')
          .replace(/\./gm, '\\.')}`
      );
    }
    if (allowItem.path) {
      return new RegExp(`${allowItem.path.replace(/\*/gm, '[\\S]+')}`);
    }
    if (allowItem.parameter) {
      return new RegExp(`${allowItem.parameter.replace(/\*/gm, '[\\S]+')}`);
    }
    logger.write(logger.INFO && `Received invalid allowItem : ${JSON.stringify(allowItem)}.`);
    return undefined;
  }

  match(itemToMatch) {
    if (this._regEx) {
      return itemToMatch.match(this._regEx);
    }
    return false;
  }
}

module.exports = WildcardMatcher;