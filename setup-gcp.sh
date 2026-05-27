#!/bin/bash
# setup-gcp.sh — One-time GCP setup for the add-on

set -e
PROJECT_ID=$1
if [ -z "$PROJECT_ID" ]; then
  echo "Usage: ./setup-gcp.sh YOUR_PROJECT_ID"
  exit 1
fi

echo "Setting up GCP project: $PROJECT_ID"
gcloud config set project $PROJECT_ID

echo "Enabling required APIs..."
gcloud services enable \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  containerregistry.googleapis.com \
  dialogflow.googleapis.com \
  iamcredentials.googleapis.com \
  script.googleapis.com \
  gmail.googleapis.com \
  drive.googleapis.com

echo "Creating service account..."
gcloud iam service-accounts create cxas-addon-sa \
  --display-name "CXAS Addon Backend SA" || true

SA="cxas-addon-sa@$PROJECT_ID.iam.gserviceaccount.com"

echo "Granting roles..."
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member "serviceAccount:$SA" \
  --role "roles/dialogflow.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member "serviceAccount:$SA" \
  --role "roles/run.invoker"

echo "Allowing Apps Script (Google's service account) to invoke Cloud Run..."
# You'll need to add the Apps Script service account ARN after deploying.
# Reference: https://developers.google.com/workspace/add-ons/guides/alternate-runtimes

echo ""
echo "GCP setup complete for $PROJECT_ID"
echo "Next: run ./deploy.sh with PROJECT_ID=$PROJECT_ID"
