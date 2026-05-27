#!/bin/bash
# deploy-cloudrun.sh — Deploy backend to Cloud Run using 'gcloud run deploy --source'
# Requires: gcloud auth login, billing enabled on gen-ai-guru-gdg-pune
set -e

PROJECT_ID="${1:-gen-ai-guru-gdg-pune}"
REGION="us-central1"
SERVICE="cxas-addon-backend"
SA_EMAIL="cxas-addon-sa@${PROJECT_ID}.iam.gserviceaccount.com"

echo "=== Deploying $SERVICE to Cloud Run ==="
echo "Project : $PROJECT_ID"
echo "Region  : $REGION"
echo ""

gcloud config set project "$PROJECT_ID"

# --source . uses Cloud Build automatically, no Docker needed locally
gcloud run deploy "$SERVICE" \
  --source ./backend \
  --region "$REGION" \
  --platform managed \
  --no-allow-unauthenticated \
  --service-account "$SA_EMAIL" \
  --set-env-vars "PROJECT_ID=${PROJECT_ID},LOCATION=${REGION}" \
  --memory 512Mi \
  --cpu 1 \
  --timeout 300 \
  --max-instances 10 \
  --project "$PROJECT_ID"

echo ""
BACKEND_URL=$(gcloud run services describe "$SERVICE" \
  --region "$REGION" --format 'value(status.url)' --project "$PROJECT_ID")
echo "=== Backend live at: $BACKEND_URL ==="
echo ""
echo "Next steps:"
echo "  1. Copy this URL: $BACKEND_URL"
echo "  2. cd addon && clasp push"
echo "  3. Open script.google.com -> Extensions -> Test deployments"
echo "  4. In the addon Settings card, paste: $BACKEND_URL"
echo "  5. Set Project ID: $PROJECT_ID"
