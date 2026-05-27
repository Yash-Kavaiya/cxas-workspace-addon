#!/bin/bash
# setup-iam.sh — Create service account and grant IAM roles via REST API
# Run this in Cloud Shell or any machine with a valid gcloud auth token
set -e

PROJECT_ID="${1:-gen-ai-guru-gdg-pune}"
SA_NAME="cxas-addon-sa"
SA_EMAIL="${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"
TOKEN=$(gcloud auth print-access-token)

echo "=== Creating service account: $SA_EMAIL ==="
curl -sf -X POST \
  "https://iam.googleapis.com/v1/projects/${PROJECT_ID}/serviceAccounts" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"accountId\": \"${SA_NAME}\", \"serviceAccount\": {\"displayName\": \"CXAS Addon Backend\"}}" \
  && echo "Service account created." || echo "Already exists, continuing."

echo ""
echo "=== Granting roles ==="
for ROLE in roles/dialogflow.admin roles/run.invoker roles/secretmanager.secretAccessor; do
  curl -sf -X POST \
    "https://cloudresourcemanager.googleapis.com/v1/projects/${PROJECT_ID}:setIamPolicy" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"policy\": {\"bindings\": [{\"role\": \"${ROLE}\", \"members\": [\"serviceAccount:${SA_EMAIL}\"]}]}}" \
    > /dev/null && echo "Granted $ROLE"
done

echo ""
echo "=== Downloading key file ==="
curl -sf -X POST \
  "https://iam.googleapis.com/v1/projects/${PROJECT_ID}/serviceAccounts/${SA_EMAIL}/keys" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"privateKeyType":"TYPE_GOOGLE_CREDENTIALS_FILE","keyAlgorithm":"KEY_ALG_RSA_2048"}' \
  | python3 -c "import sys,json,base64; d=json.load(sys.stdin); open('cxas-addon-sa-key.json','wb').write(base64.b64decode(d['privateKeyData']))" \
  && echo "Key saved to: cxas-addon-sa-key.json"

echo ""
echo "Done. Next: run ./deploy-cloudrun.sh $PROJECT_ID"
