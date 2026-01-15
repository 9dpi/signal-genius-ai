# 🧪 QUICK TEST SCRIPT

## Railway URL
# Replace this with your actual Railway URL from dashboard
RAILWAY_URL="https://signal-genius-ai-production.up.railway.app"

## Test Commands

### Test 1: Health Check
echo "Testing /health endpoint..."
curl -X GET "$RAILWAY_URL/health" -H "Accept: application/json" -w "\n\nStatus Code: %{http_code}\nTime: %{time_total}s\n"

### Test 2: Root Endpoint
echo -e "\n\nTesting / endpoint..."
curl -X GET "$RAILWAY_URL/" -H "Accept: application/json" -w "\n\nStatus Code: %{http_code}\nTime: %{time_total}s\n"

### Test 3: Latest Signal
echo -e "\n\nTesting /api/v1/signal/latest endpoint..."
curl -X GET "$RAILWAY_URL/api/v1/signal/latest" -H "Accept: application/json" -w "\n\nStatus Code: %{http_code}\nTime: %{time_total}s\n"

## Expected Results:
# All should return:
# - Status Code: 200
# - Valid JSON response
# - Time: < 2 seconds
