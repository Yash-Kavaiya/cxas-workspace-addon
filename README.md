# CX Agent Studio — Google Workspace Add-on

A Google Workspace Add-on that brings CX Agent Studio (cxas-scrapi) capabilities
directly into Gmail, Drive, Sheets, and Docs.

## Features

- List & inspect CXAS agents from any Google Workspace surface
- Run cxas lint on agent configs (including Drive JSON files)
- Trigger simulation evals and view results inline
- Browse recent sessions and traces
- Context-aware Gmail card for CUJ-related workflows

## Architecture

Google Workspace Add-on (Apps Script)
  --> Cloud Run backend (Python + FastAPI + cxas-scrapi)
  --> CX Agent Studio / Dialogflow CX APIs

## Quick Start

### 1. GCP Setup (one-time)
    ./setup-gcp.sh YOUR_PROJECT_ID

### 2. Deploy Backend
    export PROJECT_ID=your-project-id
    ./deploy.sh

### 3. Push Apps Script Add-on
    cd addon
    clasp login
    clasp create --title "CX Agent Studio" --type standalone
    clasp push

### 4. Configure Add-on
    - Open script.google.com -> your project
    - Extensions -> Create new deployment -> Add-on
    - In the add-on Settings card, paste your Cloud Run URL + Project ID
<img width="1144" height="480" alt="image" src="https://github.com/user-attachments/assets/3b288bc8-95bf-4a79-a8cb-ce63f6617b70" />

### 5. Publish to Marketplace
    See docs/marketplace-publishing.md for the full checklist.

## Project Structure

    backend/          Cloud Run Python service (FastAPI + cxas-scrapi)
    addon/            Apps Script add-on (.gs files + appsscript.json)
    docs/             Publishing guide + screenshots
    deploy.sh         End-to-end deploy script
    setup-gcp.sh      One-time GCP IAM + API setup

## References

- cxas-scrapi docs: https://googlecloudplatform.github.io/cxas-scrapi/stable/
- GitHub: https://github.com/GoogleCloudPlatform/cxas-scrapi
- Workspace Add-ons: https://developers.google.com/workspace/add-ons/overview
- Marketplace Publishing: https://developers.google.com/workspace/marketplace/how-to-publish
