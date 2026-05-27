#!/bin/bash
# cloudshell-quickstart.sh
# Run this in Google Cloud Shell (shell.cloud.google.com) for a zero-install deploy.
# It handles IAM, Cloud Run deploy, and clasp push in one shot.

set -e
PROJECT_ID="gen-ai-guru-gdg-pune"
REGION="us-central1"
SERVICE="cxas-addon-backend"
SA_EMAIL="cxas-addon-sa@${PROJECT_ID}.iam.gserviceaccount.com"

echo "================================================"
echo " CX Agent Studio Workspace Add-on — Quick Start"
echo " Project: $PROJECT_ID"
echo "================================================"
echo ""

gcloud config set project "$PROJECT_ID"

# 1. Enable APIs
echo "[1/6] Enabling APIs..."
gcloud services enable run.googleapis.com cloudbuild.googleapis.com   dialogflow.googleapis.com script.googleapis.com   appsmarket-component.googleapis.com --quiet

# 2. Service Account
echo "[2/6] Creating service account..."
gcloud iam service-accounts create cxas-addon-sa   --display-name "CXAS Addon Backend" 2>/dev/null || true

for ROLE in roles/dialogflow.admin roles/run.invoker roles/logging.logWriter; do
  gcloud projects add-iam-policy-binding "$PROJECT_ID"     --member "serviceAccount:$SA_EMAIL" --role "$ROLE" --quiet 2>/dev/null || true
done

# 3. Clone and deploy backend
echo "[3/6] Deploying Cloud Run backend..."
git clone https://github.com/GoogleCloudPlatform/cxas-scrapi /tmp/cxas-scrapi 2>/dev/null || true

# Copy our backend into a temp dir
mkdir -p /tmp/cxas-addon-deploy
cp -r ~/cxas-workspace-addon/backend /tmp/cxas-addon-deploy/

gcloud run deploy "$SERVICE"   --source /tmp/cxas-addon-deploy/backend   --region "$REGION"   --no-allow-unauthenticated   --service-account "$SA_EMAIL"   --set-env-vars "PROJECT_ID=${PROJECT_ID},LOCATION=${REGION}"   --memory 512Mi --cpu 1 --quiet

BACKEND_URL=$(gcloud run services describe "$SERVICE" --region "$REGION" --format 'value(status.url)')
echo "Backend URL: $BACKEND_URL"

# 4. Install clasp
echo "[4/6] Installing clasp..."
npm install -g @google/clasp --quiet 2>/dev/null || true

# 5. Push Apps Script
echo "[5/6] Pushing Apps Script add-on..."
cd ~/cxas-workspace-addon/addon
clasp login --no-localhost
clasp create --title "CX Agent Studio" --type standalone 2>/dev/null || true
clasp push --force

SCRIPT_ID=$(cat .clasp.json | python3 -c "import sys,json; print(json.load(sys.stdin)['scriptId'])")

# 6. Summary
echo ""
echo "================================================"
echo " DEPLOYMENT COMPLETE"
echo "================================================"
echo " Backend URL : $BACKEND_URL"
echo " Script ID   : $SCRIPT_ID"
echo " Edit add-on : https://script.google.com/d/$SCRIPT_ID/edit"
echo ""
echo " Final steps:"
echo "  1. script.google.com -> Deploy -> New Deployment -> Add-on"
echo "  2. In Gmail/Drive/Sheets sidebar -> Settings"
echo "     Backend URL : $BACKEND_URL"
echo "     Project ID  : $PROJECT_ID"
echo "  3. Marketplace: console.cloud.google.com/apis/api/appsmarket-component.googleapis.com"
echo "================================================"
