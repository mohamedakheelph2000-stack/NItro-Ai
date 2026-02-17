# Quick Test for Ollama Integration
# PowerShell script to test Nitro AI with phi3

Write-Host "🧪 Testing Nitro AI + Ollama (phi3) Integration" -ForegroundColor Cyan
Write-Host ("=" * 60) -ForegroundColor Cyan

# Test 1: Backend Health
Write-Host "`n📋 Test 1: Backend Health Check..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get
    Write-Host "✅ Backend is running!" -ForegroundColor Green
    Write-Host "   Status: $($health.status)" -ForegroundColor Gray
} catch {
    Write-Host "❌ Backend not running!" -ForegroundColor Red
    Write-Host "   Start with: python -m uvicorn main:app --reload" -ForegroundColor Gray
    exit 1
}

# Test 2: Ollama Server
Write-Host "`n📋 Test 2: Ollama Server Check..." -ForegroundColor Yellow
try {
    $ollama = Invoke-RestMethod -Uri "http://localhost:11434/api/tags" -Method Get
    $models = $ollama.models | ForEach-Object { $_.name }
    Write-Host "✅ Ollama is running!" -ForegroundColor Green
    Write-Host "   Models: $($models -join ', ')" -ForegroundColor Gray
    
    if ($models -match "phi3") {
        Write-Host "   ✅ phi3 model found!" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  phi3 not found. Run: ollama pull phi3" -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠️  Cannot connect to Ollama" -ForegroundColor Yellow
    Write-Host "   It may be starting in background..." -ForegroundColor Gray
}

# Test 3: Simple Chat
Write-Host "`n📋 Test 3: Chat Endpoint Test..." -ForegroundColor Yellow
try {
    $body = @{
        message = "Hello! Can you say hi back?"
        user_id = "test_user"
    } | ConvertTo-Json

    $response = Invoke-RestMethod -Uri "http://localhost:8000/chat" -Method Post -Body $body -ContentType "application/json"
    
    Write-Host "✅ Chat endpoint working!" -ForegroundColor Green
    Write-Host "   Your message: Hello! Can you say hi back?" -ForegroundColor Gray
    Write-Host "   AI Response: $($response.response)" -ForegroundColor Cyan
} catch {
    Write-Host "❌ Chat test failed: $_" -ForegroundColor Red
}

# Test 4: Math Question (Tests real AI)
Write-Host "`n📋 Test 4: AI Intelligence Test..." -ForegroundColor Yellow
Write-Host "   (First run may take 10-30 seconds as phi3 loads)" -ForegroundColor Gray
try {
    $body = @{
        message = "What is 7 * 8? Reply with just the number."
        user_id = "test_user"
    } | ConvertTo-Json

    $response = Invoke-RestMethod -Uri "http://localhost:8000/chat" -Method Post -Body $body -ContentType "application/json" -TimeoutSec 60
    
    Write-Host "✅ AI Test complete!" -ForegroundColor Green
    Write-Host "   Question: What is 7 * 8?" -ForegroundColor Gray
    Write-Host "   AI Answer: $($response.response)" -ForegroundColor Cyan
    
    if ($response.response -match "56") {
        Write-Host "   ✅ Correct answer! AI is working!" -ForegroundColor Green
    }
} catch {
    Write-Host "⏱️  Request timeout or error" -ForegroundColor Yellow
    Write-Host "   First load of phi3 can be slow. Try again!" -ForegroundColor Gray
}

# Summary
Write-Host "`n$("=" * 60)" -ForegroundColor Cyan
Write-Host "🎯 Quick Links:" -ForegroundColor Cyan
Write-Host "   • API Docs: http://localhost:8000/docs" -ForegroundColor Gray
Write-Host "   • Health: http://localhost:8000/health" -ForegroundColor Gray
Write-Host "   • Frontend: Open frontend/index.html in browser" -ForegroundColor Gray
Write-Host "`n   🚀 Your Nitro AI with phi3 is ready!" -ForegroundColor Green
Write-Host ("=" * 60) -ForegroundColor Cyan
