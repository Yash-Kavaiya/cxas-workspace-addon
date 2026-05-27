# Google Workspace Marketplace — Publishing Checklist

## Pre-requisites

- [ ] GCP project with billing enabled
- [ ] OAuth consent screen configured (External, In Production)
- [ ] Privacy Policy URL (required — must be publicly accessible)
- [ ] Terms of Service URL
- [ ] Homepage / Support URL
- [ ] App icon: 128x128 PNG
- [ ] Screenshots: minimum 3, size 1280x800

## Step 1 — OAuth Consent Screen

1. Go to: console.cloud.google.com/apis/credentials/consent
2. User Type: External
3. App name: "CX Agent Studio"
4. User support email: your email
5. Add scopes:
   - gmail.readonly
   - drive.readonly
   - script.external_request
   - userinfo.email
   - spreadsheets.readonly
   - documents.readonly
   - script.storage
6. Add test users during development
7. Submit for verification (required for 100+ users or sensitive scopes)

## Step 2 — Enable Workspace Marketplace SDK

1. Go to: console.cloud.google.com/apis/library
2. Search: "Google Workspace Marketplace SDK"
3. Enable it
4. Go to: console.cloud.google.com/apis/api/appsmarket-component.googleapis.com/googleapps_sdk
5. Fill App Configuration:
   - App name, description
   - App icons (128x128, 32x32)
   - App category: Productivity or Developer Tools
   - Terms of service URL
   - Privacy policy URL

## Step 3 — Apps Script Deployment

1. script.google.com -> your project
2. Deploy -> New Deployment
3. Type: Add-on
4. Description: version notes
5. Copy Deployment ID

## Step 4 — Marketplace Listing

1. In SDK config: add the Deployment ID from Step 3
2. Fill store listing:
   - Short description (max 100 chars)
   - Full description (markdown supported)
   - Screenshots (1280x800, at least 3)
3. Set visibility: Public
4. Submit for review

## Step 5 — Review Process

- Google reviews take 3-7 business days (first publish)
- Updates to existing listings are faster
- You'll receive email notification on approval/rejection
- Common rejection reasons:
  - Privacy policy not accessible
  - Scopes not justified in description
  - Screenshots don't match functionality

## Useful Links

- Marketplace SDK: https://console.cloud.google.com/apis/api/appsmarket-component.googleapis.com
- Publishing guide: https://developers.google.com/workspace/marketplace/how-to-publish
- OAuth verification: https://support.google.com/cloud/answer/9110914
- Add-on overview: https://developers.google.com/workspace/add-ons/overview
