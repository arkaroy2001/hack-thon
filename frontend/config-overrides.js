const path = require('path');

module.exports = function override(config, env) {
    // New config, e.g. config.plugins.push...
    if (config.resolve) {
        config.resolve.extensions.push('.ts', '.tsx');
      } else {
        config.resolve = {
          extensions: ['.js', '.json', '.ts', '.tsx'],
        };
      }

    return config;
}