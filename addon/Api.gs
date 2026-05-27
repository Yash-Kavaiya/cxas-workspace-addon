// Api.gs — HTTP calls to the Cloud Run backend

function callBackend(path, method, payload) {
  var url = getBackendUrl() + path;
  var token = ScriptApp.getIdentityToken();

  var options = {
    method: method || 'GET',
    headers: {
      'Authorization': 'Bearer ' + token,
      'Content-Type': 'application/json'
    },
    muteHttpExceptions: true
  };

  if (payload && method !== 'GET') {
    options.payload = JSON.stringify(payload);
  }

  var response = UrlFetchApp.fetch(url, options);
  var code = response.getResponseCode();
  var body = response.getContentText();

  if (code >= 400) {
    throw new Error('Backend error ' + code + ': ' + body);
  }

  return JSON.parse(body);
}

function apiListAgents() {
  return callBackend('/agents/', 'GET');
}

function apiGetAgent(agentId) {
  return callBackend('/agents/' + agentId, 'GET');
}

function apiListVersions(agentId) {
  return callBackend('/agents/' + agentId + '/versions', 'GET');
}

function apiRunLint(agentConfig) {
  return callBackend('/lint/', 'POST', { agent_config: agentConfig });
}

function apiListEvals(agentId) {
  return callBackend('/evals/list/' + agentId, 'GET');
}

function apiRunSimulationEval(agentId, evalId) {
  return callBackend('/evals/simulation', 'POST', { agent_id: agentId, eval_id: evalId });
}

function apiListSessions(agentId) {
  return callBackend('/sessions/list/' + agentId, 'GET');
}

function apiGetTrace(agentId, sessionId) {
  return callBackend('/sessions/' + sessionId + '/trace?agent_id=' + agentId, 'GET');
}

function apiHealth() {
  return callBackend('/health', 'GET');
}
