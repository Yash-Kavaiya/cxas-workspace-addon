# Google Workspace Marketplace — Listing Copy

## App Name
CX Agent Studio

## Short Description (max 100 chars)
Manage CX Agent Studio agents, run evals & lint checks inside Gmail, Drive and Sheets.

## Full Description (for Marketplace listing page)

**CX Agent Studio** brings the power of Google Cloud's Conversational AI platform directly into
your Google Workspace — without leaving Gmail, Drive, or Sheets.

Powered by the official [cxas-scrapi](https://github.com/GoogleCloudPlatform/cxas-scrapi) Python
library, this add-on lets conversational AI developers and CX engineers manage their agents,
run quality checks, and monitor sessions from the tools they already use every day.

### ✨ Key Features

**Agent Management**
- List and inspect all your CX Agent Studio agents
- View agent versions and configuration details
- Push agent configs directly from Drive JSON files

**Quality Assurance**
- Run `cxas lint` on any agent config — 60+ validation rules
- See lint violations highlighted inline, right in your sidebar
- Lint JSON files selected in Drive with one click

**Evaluation & Testing**
- Trigger Simulation Evals and view results without switching tabs
- Run Turn Evals against test cases stored in Sheets
- Browse recent eval results per agent

**Session Monitoring**
- List recent sessions for any agent
- View conversation traces inline
- Ideal for debugging live support agent flows

**Context-Aware Surfaces**
- Gmail: CX Agent Studio panel alongside every email
- Drive: Lint agent JSON configs on selection
- Sheets: Run evals from test case spreadsheets
- Docs: Quick agent reference panel

### 🔧 Setup
This add-on connects to a lightweight backend you deploy to your own Google Cloud Run project
(gen-ai-guru-gdg-pune or any GCP project). Your data never leaves your GCP environment.
Full setup takes under 10 minutes — step-by-step instructions are included in the Settings panel.

### 👨‍💻 Built for
- Conversational AI Engineers using CX Agent Studio / Dialogflow CX
- QA teams running agent evaluation pipelines
- Teams participating in the "30 Days of CX Agent Studio" program
- Google Cloud partners building customer service automation

### 📚 Resources
- cxas-scrapi docs: https://googlecloudplatform.github.io/cxas-scrapi/stable/
- GitHub: https://github.com/GoogleCloudPlatform/cxas-scrapi
- Follow @genai_guru for daily Conversational AI tips

---

## Category
Developer Tools

## Sub-category
Productivity

## Support URL
https://github.com/Yash-Kavaiya/cxas-workspace-addon/issues

## Homepage URL
https://github.com/Yash-Kavaiya/cxas-workspace-addon

## Privacy Policy URL
https://yash-kavaiya.github.io/cxas-workspace-addon/privacy-policy.html

## Terms of Service URL
https://yash-kavaiya.github.io/cxas-workspace-addon/terms-of-service.html

---

## OAuth Scope Justifications (required during consent screen setup)

| Scope | Justification |
|-------|--------------|
| gmail.readonly | Display CX Agent Studio actions panel alongside Gmail messages. No email content is stored or transmitted. |
| drive.readonly | Read user-selected JSON files to run cxas lint validation on agent configs. |
| spreadsheets.readonly | Read user-selected test case data from Sheets to run CX Agent Studio evaluations. |
| documents.readonly | Display agent context panel alongside Docs. |
| userinfo.email | Identify the user for personalised add-on display. |
| script.external_request | Call the user's own Cloud Run backend (cxas-scrapi API). No third-party servers. |
| script.storage | Persist user settings (backend URL, project ID) locally in Apps Script. |

---

## Screenshots Needed (1280x800 each)

1. Gmail sidebar showing agent list card
2. Drive sidebar showing lint result (passed/failed) for a JSON file
3. Sheets sidebar showing eval run results
4. Settings card with backend URL configuration
5. Agent detail card showing versions and quick actions

Generate screenshots after deploying by installing the add-on in test mode
(script.google.com -> Deploy -> Test deployments).
