// Config.gs — Store and retrieve user settings via PropertiesService

var CONFIG_KEYS = {
  BACKEND_URL: 'CXAS_BACKEND_URL',
  PROJECT_ID: 'CXAS_PROJECT_ID',
  AGENT_ID: 'CXAS_AGENT_ID',
  LOCATION: 'CXAS_LOCATION'
};

function getConfig(key) {
  return PropertiesService.getUserProperties().getProperty(CONFIG_KEYS[key]) || '';
}

function setConfig(key, value) {
  PropertiesService.getUserProperties().setProperty(CONFIG_KEYS[key], value);
}

function getBackendUrl() {
  var url = getConfig('BACKEND_URL');
  if (!url) throw new Error('Backend URL not configured. Open Settings to configure.');
  return url.replace(/\/$/, '');
}

function isConfigured() {
  return !!(getConfig('BACKEND_URL') && getConfig('PROJECT_ID'));
}