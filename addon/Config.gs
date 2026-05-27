// Config.gs - Store and retrieve user settings via PropertiesService

// Default values (used if user has not configured via Settings card)
var DEFAULTS = {
  BACKEND_URL: 'https://cxas-addon-backend-wc5dzwjbtq-uc.a.run.app',
  PROJECT_ID:  'gen-ai-guru-gdg-pune',
  AGENT_ID:    '',
  LOCATION:    'us'
};

/**
 * Get a config value from UserProperties, falling back to the default.
 * @param {string} key - one of 'BACKEND_URL', 'PROJECT_ID', 'AGENT_ID', 'LOCATION'
 */
function getConfig(key) {
  var stored = PropertiesService.getUserProperties().getProperty(key);
  return stored || DEFAULTS[key] || '';
}

/**
 * Persist a config value to UserProperties.
 * @param {string} key
 * @param {string} value
 */
function setConfig(key, value) {
  if (!key || typeof key !== 'string') throw new Error('setConfig: key must be a non-empty string');
  PropertiesService.getUserProperties().setProperty(key, value);
}

/**
 * Returns the backend URL with no trailing slash.
 */
function getBackendUrl() {
  var url = getConfig('BACKEND_URL');
  if (!url) throw new Error('Backend URL not configured. Open Settings to configure.');
  return url.replace(/\/$/, '');
}

/**
 * True if both BACKEND_URL and PROJECT_ID are set (either stored or default).
 */
function isConfigured() {
  return !!(getConfig('BACKEND_URL') && getConfig('PROJECT_ID'));
}

/**
 * Reset all settings to defaults.
 */
function resetConfig() {
  PropertiesService.getUserProperties().deleteAllProperties();
}
