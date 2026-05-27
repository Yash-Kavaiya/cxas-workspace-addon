// Code.gs — Main entry points for all add-on surfaces

// ─── Homepage (all surfaces) ────────────────────────────────────────────────

function onHomepage(e) {
  if (!isConfigured()) return buildNotConfiguredCard();
  return buildDashboardCard();
}

function onSheetsHomepage(e) {
  return onHomepage(e);
}

function onDocsHomepage(e) {
  return onHomepage(e);
}

function buildDashboardCard() {
  var card = CardService.newCardBuilder()
    .setHeader(
      CardService.newCardHeader()
        .setTitle('CX Agent Studio')
        .setSubtitle('Project: ' + getConfig('PROJECT_ID'))
        .setImageUrl('https://storage.googleapis.com/cxas-addon-assets/icon128.png')
        .setImageStyle(CardService.ImageStyle.CIRCLE)
    );

  var quickActions = CardService.newCardSection().setHeader('Quick Actions');
  quickActions.addWidget(
    CardService.newTextButton().setText('📋 List Agents')
      .setOnClickAction(CardService.newAction().setFunctionName('showAgentList'))
  );
  quickActions.addWidget(
    CardService.newTextButton().setText('🔍 Run Lint')
      .setOnClickAction(CardService.newAction().setFunctionName('promptLint'))
  );
  quickActions.addWidget(
    CardService.newTextButton().setText('🧪 Run Eval')
      .setOnClickAction(CardService.newAction().setFunctionName('promptEval'))
  );
  quickActions.addWidget(
    CardService.newTextButton().setText('📊 Recent Sessions')
      .setOnClickAction(CardService.newAction().setFunctionName('promptSessions'))
  );
  quickActions.addWidget(
    CardService.newTextButton().setText('📈 Export KPIs to Sheets')
      .setOnClickAction(CardService.newAction().setFunctionName('promptKpiExport'))
  );
  card.addSection(quickActions);

  var footer = CardService.newCardSection().setHeader('Resources');
  footer.addWidget(
    CardService.newTextButton().setText('📖 cxas-scrapi Docs')
      .setOpenLink(CardService.newOpenLink()
        .setUrl('https://googlecloudplatform.github.io/cxas-scrapi/stable/')
        .setOpenAs(CardService.OpenAs.OVERLAY))
  );
  footer.addWidget(
    CardService.newTextButton().setText('⚙️ Settings')
      .setOnClickAction(CardService.newAction().setFunctionName('openSettings'))
  );
  card.addSection(footer);
  return card.build();
}

// ─── Gmail Contextual Trigger ────────────────────────────────────────────────

function onGmailMessage(e) {
  if (!isConfigured()) return [buildNotConfiguredCard()];
  var card = CardService.newCardBuilder()
    .setHeader(
      CardService.newCardHeader()
        .setTitle('CX Agent Studio')
        .setSubtitle('Gmail Integration')
    );

  var section = CardService.newCardSection().setHeader('Actions');
  section.addWidget(CardService.newTextParagraph()
    .setText('Use this email as context for CX Agent Studio workflows.'));
  section.addWidget(
    CardService.newTextButton().setText('📋 List Agents')
      .setOnClickAction(CardService.newAction().setFunctionName('showAgentList'))
  );
  section.addWidget(
    CardService.newTextButton().setText('🔍 Run Lint on Project')
      .setOnClickAction(CardService.newAction().setFunctionName('promptLint'))
  );
  card.addSection(section);
  return [card.build()];
}

// ─── Drive Contextual Trigger ─────────────────────────────────────────────────

function onDriveItemSelected(e) {
  if (!isConfigured()) return [buildNotConfiguredCard()];
  var items = e.drive.selectedItems || [];
  var card = CardService.newCardBuilder()
    .setHeader(CardService.newCardHeader()
      .setTitle('CX Agent Studio')
      .setSubtitle(items.length + ' file(s) selected'));

  var section = CardService.newCardSection().setHeader('Actions');
  if (items.length > 0 && items[0].mimeType === 'application/json') {
    section.addWidget(CardService.newTextParagraph()
      .setText('JSON file detected. Run cxas lint on this agent config?'));
    section.addWidget(
      CardService.newTextButton().setText('🔍 Lint This File')
        .setOnClickAction(CardService.newAction()
          .setFunctionName('lintDriveFile')
          .setParameters({ fileId: items[0].id, fileName: items[0].title }))
    );
  } else {
    section.addWidget(CardService.newTextParagraph()
      .setText('Select a JSON agent config file to lint it.'));
  }
  section.addWidget(
    CardService.newTextButton().setText('📋 All Agents')
      .setOnClickAction(CardService.newAction().setFunctionName('showAgentList'))
  );
  card.addSection(section);
  return [card.build()];
}

// ─── Action handlers ──────────────────────────────────────────────────────────

function openSettings(e) {
  return CardService.newActionResponseBuilder()
    .setNavigation(CardService.newNavigation().pushCard(buildSettingsCard()))
    .build();
}

function saveSettings(e) {
  var form = e.formInputs;
  if (form.backend_url) setConfig('BACKEND_URL', form.backend_url[0]);
  if (form.project_id)  setConfig('PROJECT_ID', form.project_id[0]);
  if (form.location)    setConfig('LOCATION', form.location[0]);
  return CardService.newActionResponseBuilder()
    .setNotification(CardService.newNotification().setText('Settings saved!'))
    .setNavigation(CardService.newNavigation().popCard())
    .build();
}

function testConnection(e) {
  try {
    var result = apiHealth();
    return CardService.newActionResponseBuilder()
      .setNotification(CardService.newNotification()
        .setText('Connected! Status: ' + result.status))
      .build();
  } catch (err) {
    return CardService.newActionResponseBuilder()
      .setNotification(CardService.newNotification()
        .setText('Connection failed: ' + err.message))
      .build();
  }
}

function showAgentList(e) {
  try {
    var data = apiListAgents();
    var agents = data.agents || [];
    return CardService.newActionResponseBuilder()
      .setNavigation(CardService.newNavigation()
        .pushCard(buildAgentListCard(agents)))
      .build();
  } catch (err) {
    return CardService.newActionResponseBuilder()
      .setNavigation(CardService.newNavigation()
        .pushCard(buildErrorCard(err.message)))
      .build();
  }
}

function showAgentDetails(e) {
  var agentId = e.parameters.agentId;
  try {
    var data = apiGetAgent(agentId);
    return CardService.newActionResponseBuilder()
      .setNavigation(CardService.newNavigation()
        .pushCard(buildAgentDetailCard(data.agent, agentId)))
      .build();
  } catch (err) {
    return CardService.newActionResponseBuilder()
      .setNavigation(CardService.newNavigation()
        .pushCard(buildErrorCard(err.message)))
      .build();
  }
}

function promptLint(e) {
  var card = CardService.newCardBuilder()
    .setHeader(CardService.newCardHeader().setTitle('Run Lint'));
  var section = CardService.newCardSection();
  section.addWidget(CardService.newTextInput()
    .setFieldName('agent_id_lint')
    .setTitle('Agent ID')
    .setHint('Enter the agent ID to lint'));
  section.addWidget(CardService.newTextButton()
    .setText('Run Lint')
    .setOnClickAction(CardService.newAction().setFunctionName('runLintForAgent')));
  card.addSection(section);
  return CardService.newActionResponseBuilder()
    .setNavigation(CardService.newNavigation().pushCard(card.build()))
    .build();
}

function runLintForAgent(e) {
  var agentId = (e.parameters && e.parameters.agentId)
    || (e.formInputs && e.formInputs.agent_id_lint && e.formInputs.agent_id_lint[0]);
  if (!agentId) {
    return CardService.newActionResponseBuilder()
      .setNotification(CardService.newNotification().setText('No agent ID provided'))
      .build();
  }
  try {
    var result = apiRunLint(null);
    return CardService.newActionResponseBuilder()
      .setNavigation(CardService.newNavigation()
        .pushCard(buildLintResultCard(result, agentId)))
      .build();
  } catch (err) {
    return CardService.newActionResponseBuilder()
      .setNavigation(CardService.newNavigation()
        .pushCard(buildErrorCard(err.message)))
      .build();
  }
}

function lintDriveFile(e) {
  var fileId = e.parameters.fileId;
  var fileName = e.parameters.fileName;
  try {
    var file = DriveApp.getFileById(fileId);
    var content = file.getBlob().getDataAsString();
    var agentConfig = JSON.parse(content);
    var result = apiRunLint(agentConfig);
    return CardService.newActionResponseBuilder()
      .setNavigation(CardService.newNavigation()
        .pushCard(buildLintResultCard(result, fileName)))
      .build();
  } catch (err) {
    return CardService.newActionResponseBuilder()
      .setNavigation(CardService.newNavigation()
        .pushCard(buildErrorCard(err.message)))
      .build();
  }
}

function promptEval(e) {
  var card = CardService.newCardBuilder()
    .setHeader(CardService.newCardHeader().setTitle('Run Simulation Eval'));
  var section = CardService.newCardSection();
  section.addWidget(CardService.newTextInput()
    .setFieldName('agent_id_eval').setTitle('Agent ID'));
  section.addWidget(CardService.newTextInput()
    .setFieldName('eval_id').setTitle('Eval ID').setHint('Optional'));
  section.addWidget(CardService.newTextButton()
    .setText('Run Eval')
    .setOnClickAction(CardService.newAction().setFunctionName('runEvalSubmit')));
  card.addSection(section);
  return CardService.newActionResponseBuilder()
    .setNavigation(CardService.newNavigation().pushCard(card.build()))
    .build();
}

function runEvalSubmit(e) {
  var agentId = e.formInputs.agent_id_eval && e.formInputs.agent_id_eval[0];
  var evalId = e.formInputs.eval_id && e.formInputs.eval_id[0];
  try {
    var result = apiRunSimulationEval(agentId, evalId);
    var card = CardService.newCardBuilder()
      .setHeader(CardService.newCardHeader().setTitle('Eval Result'));
    var section = CardService.newCardSection();
    section.addWidget(CardService.newTextParagraph()
      .setText('Status: ' + result.status));
    section.addWidget(CardService.newTextParagraph()
      .setText(JSON.stringify(result.result, null, 2).substring(0, 800)));
    card.addSection(section);
    return CardService.newActionResponseBuilder()
      .setNavigation(CardService.newNavigation().pushCard(card.build()))
      .build();
  } catch (err) {
    return CardService.newActionResponseBuilder()
      .setNavigation(CardService.newNavigation()
        .pushCard(buildErrorCard(err.message)))
      .build();
  }
}

function promptSessions(e) {
  var card = CardService.newCardBuilder()
    .setHeader(CardService.newCardHeader().setTitle('Recent Sessions'));
  var section = CardService.newCardSection();
  section.addWidget(CardService.newTextInput()
    .setFieldName('agent_id_sessions').setTitle('Agent ID'));
  section.addWidget(CardService.newTextButton()
    .setText('Fetch Sessions')
    .setOnClickAction(CardService.newAction().setFunctionName('listSessionsSubmit')));
  card.addSection(section);
  return CardService.newActionResponseBuilder()
    .setNavigation(CardService.newNavigation().pushCard(card.build()))
    .build();
}

function listSessionsForAgent(e) {
  var agentId = e.parameters.agentId;
  try {
    var data = apiListSessions(agentId);
    var sessions = data.sessions || [];
    var card = CardService.newCardBuilder()
      .setHeader(CardService.newCardHeader()
        .setTitle('Sessions (' + sessions.length + ')'));
    var section = CardService.newCardSection();
    sessions.slice(0, 10).forEach(function(s) {
      var sid = s.name ? s.name.split('/').pop() : JSON.stringify(s);
      section.addWidget(CardService.newDecoratedText().setText(sid));
    });
    card.addSection(section);
    return CardService.newActionResponseBuilder()
      .setNavigation(CardService.newNavigation().pushCard(card.build()))
      .build();
  } catch (err) {
    return CardService.newActionResponseBuilder()
      .setNavigation(CardService.newNavigation()
        .pushCard(buildErrorCard(err.message)))
      .build();
  }
}

function listSessionsSubmit(e) {
  var agentId = e.formInputs.agent_id_sessions && e.formInputs.agent_id_sessions[0];
  return listSessionsForAgent({ parameters: { agentId: agentId } });
}

// ─── KPI Export ───────────────────────────────────────────────────────────────

function promptKpiExport(e) {
  return CardService.newActionResponseBuilder()
    .setNavigation(CardService.newNavigation().pushCard(buildKpiExportCard()))
    .build();
}

function submitKpiExport(e) {
  var form = e.formInputs || {};
  var spreadsheetId = (form.kpi_spreadsheet_id && form.kpi_spreadsheet_id[0]) || '';
  var sheetName     = (form.kpi_sheet_name      && form.kpi_sheet_name[0])     || 'KPIs';
  var metrics       = (form.kpi_metrics         && form.kpi_metrics[0])        || 'all';
  var aggregateBy   = (form.kpi_aggregate_by    && form.kpi_aggregate_by[0])   || '';
  var dateRange     = (form.kpi_date_range      && form.kpi_date_range[0])     || '';
  var filter        = (form.kpi_filter          && form.kpi_filter[0])         || '';
  var spreadTitle   = (form.kpi_spreadsheet_title && form.kpi_spreadsheet_title[0]) || 'CXAS KPI Dashboard';

  try {
    var payload = {
      project_id:         getConfig('PROJECT_ID'),
      location:           getConfig('LOCATION') || 'us-central1',
      sheet_name:         sheetName,
      metrics:            metrics,
      append:             true,
    };
    if (aggregateBy) payload.aggregate_by = aggregateBy;
    if (dateRange)   payload.date_range   = dateRange;
    if (filter)      payload.filter       = filter;

    var endpoint, result;
    if (spreadsheetId) {
      payload.spreadsheet_id = spreadsheetId;
      result = callBackend('/kpis/export', 'POST', payload);
    } else {
      payload.spreadsheet_title = spreadTitle;
      result = callBackend('/kpis/create-and-export', 'POST', payload);
    }

    return CardService.newActionResponseBuilder()
      .setNavigation(CardService.newNavigation().pushCard(buildKpiResultCard(result)))
      .build();
  } catch (err) {
    return CardService.newActionResponseBuilder()
      .setNavigation(CardService.newNavigation().pushCard(buildErrorCard(err.message)))
      .build();
  }
}
