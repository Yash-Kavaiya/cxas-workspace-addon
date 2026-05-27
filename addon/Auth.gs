// Auth.gs — OAuth2 service for calling Cloud Run backend

function getOAuthService() {
  var clientId = PropertiesService.getScriptProperties().getProperty('CLIENT_ID');
  var clientSecret = PropertiesService.getScriptProperties().getProperty('CLIENT_SECRET');
  return OAuth2.createService('CloudRun')
    .setAuthorizationBaseUrl('https://accounts.google.com/o/oauth2/auth')
    .setTokenUrl('https://oauth2.googleapis.com/token')
    .setClientId(clientId)
    .setClientSecret(clientSecret)
    .setScope('https://www.googleapis.com/auth/cloud-platform')
    .setCallbackFunction('authCallback')
    .setPropertyStore(PropertiesService.getUserProperties())
    .setCache(CacheService.getUserCache());
}

function authCallback(request) {
  var service = getOAuthService();
  var authorized = service.handleCallback(request);
  if (authorized) {
    return HtmlService.createHtmlOutput('<p>Authorization successful! You can close this tab.</p>');
  } else {
    return HtmlService.createHtmlOutput('<p>Authorization failed. Please try again.</p>');
  }
}

function getIdToken() {
  // For Cloud Run: use identity token (OIDC), not access token
  var backendUrl = getBackendUrl();
  var serviceAccountToken = ScriptApp.getIdentityToken();
  return serviceAccountToken;
}
