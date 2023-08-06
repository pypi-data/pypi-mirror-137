const _ = require('lodash');
const { Route, Api, Inventory } = require('../reports/inventory');
const HeartbeatCache = require('../reports/heartbeat_cache');
const Logger = require('../utils/logger');
function storeRoute(inputData) {
  try {
    const { data } = inputData;
    const trimmedPath = data.path.replace(/^\/+|\/+$/g, '');
    const supportedMethods = data.methods.filter((method) => supportedHttpMethods().includes(method));
    let inventory = HeartbeatCache.getInventory();
    if (inventory && inventory.api && _.isArray(inventory.api.routes)) {
      const existingRoute = inventory.api.routes.find(
        (route) => route.path === trimmedPath
      );
      if (existingRoute) {
        existingRoute.addMethods(supportedMethods);
      } else {
        inventory.api.addRoute(new Route(trimmedPath, supportedMethods));
      }
    } else {
      inventory = new Inventory(new Api([new Route(trimmedPath, supportedMethods)]));
    }

    HeartbeatCache.cacheInventory(inventory);
  } catch (error) {
    Logger.write(Logger.ERROR && `api.StoreRoute: Failed to store route: ${error}`);
  }
}

function supportedHttpMethods() {
  return [
    'GET',
    'PUT',
    'POST',
    'DELETE',
    'PATCH',
    'HEAD',
    'OPTIONS',
    'CONNECT',
    'TRACE'
  ];
}

module.exports = {
  storeRoute
};
