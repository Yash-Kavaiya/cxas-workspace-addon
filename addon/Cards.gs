// Cards.gs — Reusable card builders

function buildHeader(title, subtitle) {
  return CardService.newCardHeader()
    .setTitle(title)
    .setSubtitle(subtitle || 'CX Agent Studio')
    .setImageUrl('https://storage.googleapis.com/cxas-addon-assets/icon128.png')
    .setImageStyle(CardService.ImageStyle.CIRCLE);
}

function buildErrorCard(message) {
  return CardService.newCardBuilder()
    .setHeader(buildHeader('Error', 'CX Agent Studio'))
    .addSection(
      CardService.newCardSection()
        .addWidget(CardService.newDecoratedText()
          .setText(message)
          .setStartIcon(CardService.newIconImage().setIcon(CardService.Icon.NONE)))
    ).build();
}

function buildNotConfiguredCard() {
  var section = CardService.newCardSection()
    .setHeader('Setup Required')
    .addWidget(CardService.newTextParagraph()
      .setText('Configure your backend URL and GCP Project ID to get started.'))
    .addWidget(CardService.newTextButton()
      .setText('Open Settings')
      .setOnClickAction(CardService.newAction().setFunctionName('openSettings')));
  return CardService.newCardBuilder()
    .setHeader(buildHeader('CX Agent Studio', 'Setup'))
    .addSection(section)
    .build();
}

function buildAgentListCard(agents) {
  var card = CardService.newCardBuilder()
    .setHeader(buildHeader('Agents (' + agents.length + ')', getConfig('PROJECT_ID')));

  var section = CardService.newCardSection().setHeader('Your Agents');
  agents.forEach(function(agent) {
    var name = agent.displayName || agent.name || 'Unnamed';
    var agentId = agent.name ? agent.name.split('/').pop() : '';
    section.addWidget(
      CardService.newDecoratedText()
        .setTopLabel(agentId)
        .setText(name)
        .setButton(
          CardService.newTextButton()
            .setText('Details')
            .setOnClickAction(
              CardService.newAction()
                .setFunctionName('showAgentDetails')
                .setParameters({ agentId: agentId })
            )
        )
    );
  });

  card.addSection(section);
  card.addSection(
    CardService.newCardSection()
      .addWidget(CardService.newTextButton()
        .setText('Refresh')
        .setOnClickAction(CardService.newAction().setFunctionName('showAgentList')))
  );
  return card.build();
}

function buildAgentDetailCard(agent, agentId) {
  var card = CardService.newCardBuilder()
    .setHeader(buildHeader(agent.displayName || agentId, 'Agent Details'));

  var infoSection = CardService.newCardSection().setHeader('Info');
  infoSection.addWidget(CardService.newKeyValue().setTopLabel('Agent ID').setContent(agentId));
  if (agent.defaultLanguageCode) {
    infoSection.addWidget(CardService.newKeyValue().setTopLabel('Language').setContent(agent.defaultLanguageCode));
  }
  if (agent.timeZone) {
    infoSection.addWidget(CardService.newKeyValue().setTopLabel('Timezone').setContent(agent.timeZone));
  }
  card.addSection(infoSection);

  var actionsSection = CardService.newCardSection().setHeader('Actions');
  actionsSection.addWidget(
    CardService.newTextButton().setText('Run Lint')
      .setOnClickAction(CardService.newAction().setFunctionName('runLintForAgent')
        .setParameters({ agentId: agentId }))
  );
  actionsSection.addWidget(
    CardService.newTextButton().setText('List Evals')
      .setOnClickAction(CardService.newAction().setFunctionName('listEvalsForAgent')
        .setParameters({ agentId: agentId }))
  );
  actionsSection.addWidget(
    CardService.newTextButton().setText('Recent Sessions')
      .setOnClickAction(CardService.newAction().setFunctionName('listSessionsForAgent')
        .setParameters({ agentId: agentId }))
  );
  card.addSection(actionsSection);
  return card.build();
}

function buildLintResultCard(result, agentId) {
  var passed = result.passed;
  var card = CardService.newCardBuilder()
    .setHeader(buildHeader('Lint: ' + (passed ? 'PASSED' : 'FAILED'), agentId));

  var summary = CardService.newCardSection().setHeader('Summary');
  summary.addWidget(CardService.newKeyValue()
    .setTopLabel('Status')
    .setContent(passed ? '✅ All rules passed' : '❌ Violations found'));
  summary.addWidget(CardService.newKeyValue()
    .setTopLabel('Violations')
    .setContent(String(result.violations ? result.violations.length : 0)));
  card.addSection(summary);

  if (result.violations && result.violations.length > 0) {
    var violSection = CardService.newCardSection().setHeader('Violations');
    result.violations.slice(0, 10).forEach(function(v) {
      violSection.addWidget(CardService.newTextParagraph().setText('• ' + v));
    });
    card.addSection(violSection);
  }
  return card.build();
}

function buildSettingsCard() {
  var card = CardService.newCardBuilder()
    .setHeader(buildHeader('Settings', 'CX Agent Studio'));

  var section = CardService.newCardSection().setHeader('Backend Configuration');
  section.addWidget(
    CardService.newTextInput()
      .setFieldName('backend_url')
      .setTitle('Cloud Run Backend URL')
      .setValue(getConfig('BACKEND_URL'))
      .setHint('https://your-service-xxxxx-uc.a.run.app')
  );
  section.addWidget(
    CardService.newTextInput()
      .setFieldName('project_id')
      .setTitle('GCP Project ID')
      .setValue(getConfig('PROJECT_ID'))
  );
  section.addWidget(
    CardService.newTextInput()
      .setFieldName('location')
      .setTitle('Location')
      .setValue(getConfig('LOCATION') || 'us-central1')
  );
  section.addWidget(
    CardService.newTextButton()
      .setText('Save Settings')
      .setOnClickAction(CardService.newAction().setFunctionName('saveSettings'))
  );
  card.addSection(section);

  var testSection = CardService.newCardSection().setHeader('Test Connection');
  testSection.addWidget(
    CardService.newTextButton()
      .setText('Test Backend Health')
      .setOnClickAction(CardService.newAction().setFunctionName('testConnection'))
  );
  card.addSection(testSection);
  return card.build();
}
