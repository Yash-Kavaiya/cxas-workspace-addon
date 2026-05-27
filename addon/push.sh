#!/bin/bash
# push.sh — Authenticate clasp and push all add-on files
# Run ONCE interactively; paste the localhost:8888 URL when prompted.
set -e

CLASP=/home/yashk/.hermes/node/bin/clasp
ADDON_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "=== Step 1: clasp login ==="
echo "A browser URL will appear. Open it, authorize, then copy the"
echo "redirect URL (http://localhost:8888/?code=...) and paste it here."
echo ""

# Login via manual code exchange
$CLASP login --no-localhost

echo ""
echo "=== Step 2: Create Apps Script project ==="
cd "$ADDON_DIR"
$CLASP create --title "CX Agent Studio" --type standalone 2>/dev/null || true

echo ""
echo "=== Step 3: Push files ==="
$CLASP push --force

echo ""
SCRIPT_ID=$(cat .clasp.json | python3 -c "import sys,json; print(json.load(sys.stdin)['scriptId'])")
echo "=== Done! Script ID: $SCRIPT_ID ==="
echo "Open: https://script.google.com/d/$SCRIPT_ID/edit"
echo ""
echo "Next in the browser:"
echo "  1. Extensions > Test deployments > Install"
echo "  2. Open Gmail/Drive/Sheets - side panel shows CX Agent Studio"
echo "  3. Click Settings -> paste your Cloud Run URL + project ID"
