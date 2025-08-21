#!/bin/bash

# CRM System Consolidation Verification Script

echo "🔍 CRM System Consolidation Verification"
echo "========================================"

# Initialize counters
PASSED=0
FAILED=0

check_item() {
    local description="$1"
    local condition="$2"
    
    if eval "$condition"; then
        echo "✅ $description"
        ((PASSED++))
    else
        echo "❌ $description"
        ((FAILED++))
    fi
}

echo "📋 Configuration Files:"
check_item "Docker Compose configuration exists" "[ -f 'docker-compose.yml' ]"
check_item "Dockerfile exists and properly configured" "[ -f 'Dockerfile' ] && grep -q '8083' Dockerfile"
check_item "Environment file exists" "[ -f '.env' ]"
check_item "Entrypoint script exists and executable" "[ -x 'entrypoint.sh' ]"
check_item "Docker ignore file exists" "[ -f '.dockerignore' ]"

echo ""
echo "📊 Dataset Management:"
check_item "Data directory structure exists" "[ -d 'data' ] && [ -d 'data/datasets' ]"
check_item "Primary customer dataset exists" "[ -f 'data/datasets/complete_customer_dataset_20250820_035231.csv' ]"
check_item "Secondary datasets exist" "[ -f 'data/datasets/customers_export_20250730_071955_updated.csv' ]"
check_item "Dataset management script exists" "[ -x 'manage_datasets.py' ]"

DATASET_COUNT=$(ls data/datasets/*.csv 2>/dev/null | wc -l)
check_item "All 5 datasets present" "[ $DATASET_COUNT -eq 5 ]"

echo ""
echo "🚀 Deployment Scripts:"
check_item "Main launch script exists and executable" "[ -x 'start_crm_8083.sh' ]"
check_item "Launch script configured for port 8083" "grep -q '8083' start_crm_8083.sh"

echo ""
echo "🏗️ Project Structure:"
check_item "Django project directory exists" "[ -d 'crm_project' ]"
check_item "Django manage.py exists" "[ -f 'crm_project/manage.py' ]"
check_item "Requirements file exists" "[ -f 'requirements.txt' ]"
check_item "Log directory exists" "[ -d 'logs' ]"
check_item "Media directory exists" "[ -d 'media' ]"
check_item "Static directory exists" "[ -d 'static' ]"

echo ""
echo "📖 Documentation:"
check_item "Consolidation summary exists" "[ -f 'CONSOLIDATION_SUMMARY.md' ]"
check_item "README exists" "[ -f 'README.md' ]"

echo ""
echo "🔧 Docker Configuration Validation:"
if command -v docker-compose &> /dev/null; then
    if docker-compose config &> /dev/null; then
        echo "✅ Docker Compose configuration is valid"
        ((PASSED++))
    else
        echo "❌ Docker Compose configuration has errors"
        ((FAILED++))
    fi
else
    echo "⚠️  Docker Compose not available for validation"
fi

echo ""
echo "📊 Dataset Statistics:"
if [ -d "data/datasets" ]; then
    TOTAL_SIZE=$(du -sh data/datasets/ | cut -f1)
    echo "📁 Dataset directory size: $TOTAL_SIZE"
    
    echo "📋 Dataset files:"
    for file in data/datasets/*.csv; do
        if [ -f "$file" ]; then
            SIZE=$(du -h "$file" | cut -f1)
            LINES=$(wc -l < "$file" 2>/dev/null || echo "unknown")
            echo "   - $(basename "$file"): $SIZE ($LINES lines)"
        fi
    done
fi

echo ""
echo "🎯 Port Configuration Check:"
DOCKER_COMPOSE_PORT=$(grep -o "8083:8083" docker-compose.yml | head -1)
DOCKERFILE_PORT=$(grep -o "8083" Dockerfile | head -1)
ENV_PORT=$(grep "PORT=8083" .env | head -1)

if [ "$DOCKER_COMPOSE_PORT" = "8083:8083" ]; then
    echo "✅ Docker Compose configured for port 8083"
    ((PASSED++))
else
    echo "❌ Docker Compose port configuration missing"
    ((FAILED++))
fi

if [ "$DOCKERFILE_PORT" = "8083" ]; then
    echo "✅ Dockerfile configured for port 8083"
    ((PASSED++))
else
    echo "❌ Dockerfile port configuration missing"
    ((FAILED++))
fi

echo ""
echo "🏁 Consolidation Summary:"
echo "========================="
echo "✅ Passed checks: $PASSED"
echo "❌ Failed checks: $FAILED"
TOTAL=$((PASSED + FAILED))
PERCENTAGE=$((PASSED * 100 / TOTAL))
echo "📈 Success rate: $PERCENTAGE%"

if [ $FAILED -eq 0 ]; then
    echo ""
    echo "🎉 CONSOLIDATION SUCCESSFUL!"
    echo "Your CRM system is ready for deployment on port 8083"
    echo ""
    echo "🚀 Quick Start:"
    echo "   ./start_crm_8083.sh"
    echo ""
    echo "🌐 Once running, access at:"
    echo "   http://localhost:8083/"
    exit 0
else
    echo ""
    echo "⚠️  CONSOLIDATION INCOMPLETE"
    echo "Please address the failed checks before deployment"
    exit 1
fi