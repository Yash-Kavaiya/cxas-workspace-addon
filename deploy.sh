#!/bin/bash
# deploy.sh — Build and deploy the Cloud Run backend + push the Apps Script addon

set -e

PROJECT_ID=${PROJECT_ID:-"your-gcp-project-id"}
REGION=${REGION:-"us-central1"}
SERVICE_NAME="cxas-addon-backend"
IMAGE="gcr.io/$PROJECT_ID/$SERVICE_NAME"

echo "=== 1. Deploying Cloud Run backend ==="
cd backend
gcloud builds submit --tag $IMAGE
gcloud run deploy $SERVICE_NAME \
  --image $IMAGE \
  --region $REGION \
  --platform managed \
  --no-allow-unauthenticated \
  --set-env-vars "PROJECT_ID=$PROJECT_ID,LOCATION=$REGION" \
  --service-account "cxas-addon-sa@$PROJECT_ID.iam.gserviceaccount.com"

BACKEND_URL=$(gcloud run services describe $SERVICE_NAME --region $REGION --format 'value(status.url)')
echo "Backend deployed at: $BACKEND_URL"
cd ..

echo ""
echo "=== 2. Pushing Apps Script addon ==="
cd addon
# Install clasp if not present
npm list -g @google/clasp 2>/dev/null || npm install -g @google/clasp
clasp push
echo "Addon pushed to Apps Script."
cd ..

echo ""
echo "=== Done ==="
echo "Next: Open script.google.com, deploy as Add-on, then submit to Marketplace."
echo "Backend URL to paste in addon Settings: $BACKEND_URL"
