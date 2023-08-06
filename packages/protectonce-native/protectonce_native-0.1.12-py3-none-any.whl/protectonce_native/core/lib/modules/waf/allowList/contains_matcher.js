const BaseMatcher = require('./base_matcher');
const logger = require('../../../utils/logger');

class ContainsMatcher extends BaseMatcher {
  constructor(allowItem) {
    super();
    this._stringToMatchWith = this._getAttributeValueByType(allowItem);
  }

  _getAttributeValueByType(allowItem) {
    if (allowItem.ipAddress) {
      return allowItem.ipAddress;
    }
    if (allowItem.path) {
      return allowItem.path;
    }
    if (allowItem.parameter) {
      return allowItem.parameter;
    }
    logger.write(logger.INFO && `Received invalid allowItem : ${JSON.stringify(allowItem)}.`);
    return undefined;
  }

  match(stringToMatch) {
    if (this._stringToMatchWith) {
      return stringToMatch.includes(this._stringToMatchWith);
    }
    return false;
  }
}

module.exports = ContainsMatcher;