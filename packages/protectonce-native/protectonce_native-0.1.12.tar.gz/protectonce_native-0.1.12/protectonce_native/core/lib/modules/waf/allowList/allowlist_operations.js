const WildcardMatcher = require('./wildcard_matcher');
const ContainsMatcher = require('./contains_matcher');

class AllowlistOperations {
  constructor(allowIPs, allowPaths, allowParameters) {
    this._ipMatchers = allowIPs.map((allowItem) => this._getMatcher(allowItem));
    this._pathMatchers = allowPaths.map((allowItem) => this._getMatcher(allowItem));
    this._parameterMatchers = allowParameters.map((allowItem) => this._getMatcher(allowItem));
  }

  _getMatcher(allowItem) {
    if (allowItem.operator === 'wildcard') {
      return new WildcardMatcher(allowItem);
    }
    return new ContainsMatcher(allowItem);
  }

  checkIpAllowList(itemToCompare) {
    for (const matcher of this._ipMatchers) {
      if (itemToCompare && matcher.match(itemToCompare)) {
        return true;
      }
    }
    return false;
  }

  checkPathAllowList(itemToCompare) {
    for (const matcher of this._pathMatchers) {
      if (itemToCompare && matcher.match(itemToCompare)) {
        return true;
      }
    }
    return false;
  }

  _checkParameterAllowList(itemToCompare) {
    for (const matcher of this._parameterMatchers) {
      if (itemToCompare && matcher.match(itemToCompare)) {
        return true;
      }
    }
    return false;
  }

  filterParameters(request) {
    for (const key of Object.keys(request.queryParams)) {
      const isParamToBeFiltered = this._checkParameterAllowList(key);
      if (isParamToBeFiltered) {
        request.queryParams.pathParams[0] =
          request.queryParams.pathParams[0].replace(
            `${key}=${request.queryParams[key]}`,
            ''
          );
        delete request.queryParams[key];
      }
    }
    return request.queryParams;
  }
}

module.exports = AllowlistOperations;
