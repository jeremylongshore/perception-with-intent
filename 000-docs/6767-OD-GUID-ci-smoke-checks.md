# CI Smoke Checks - No GCP Required

**Version:** 1.0
**Date:** 2025-11-14
**Purpose:** Validate code quality and structure without requiring GCP credentials

---

## Overview

The **CI Smoke Tests** workflow (`.github/workflows/ci-smoke.yml`) performs comprehensive validation of all Perception components **without requiring GCP authentication**.

This allows:
- ✅ Fast feedback on PRs
- ✅ Local development verification
- ✅ Pre-deployment confidence
- ✅ Works even when GCP credentials are not configured

---

## Workflow Triggers

**File:** `.github/workflows/ci-smoke.yml`

**Triggers:**
- `pull_request` → main
- `push` → main
- `workflow_dispatch` (manual)

**Runtime:** ~3-5 minutes
**No GCP credentials required:** ✅

---

## Test Jobs

### 1. Python Smoke Tests (`python-smoke`)

**Purpose:** Validate MCP service Python code

**Actions:**
1. Set up Python 3.12
2. Create virtual environment
3. Install MCP service dependencies (`app/mcp_service/requirements.txt`)
4. Compile MCP service (syntax check)
5. Test MCP service imports
6. Validate uvicorn can start (--help)
7. Run MCP unit tests (if they exist)

**Commands:**
```bash
# Compile all Python files
python -m compileall app/mcp_service -q

# Test imports
python -c "from app.mcp_service.main import app; print('✅ MCP service imports OK')"

# Validate uvicorn
cd app/mcp_service && uvicorn main:app --help

# Run tests
pytest tests/mcp_service -v
```

**Pass Criteria:**
- ✅ All Python files compile without syntax errors
- ✅ MCP service imports successfully
- ✅ uvicorn recognizes the FastAPI app
- ✅ Unit tests pass (if present)

---

### 2. Agent Configuration Smoke Tests (`agent-smoke`)

**Purpose:** Validate all 8 agent configurations

**Actions:**
1. Verify all 8 agent YAML files exist
2. Verify all 8 agent tools modules exist
3. Compile agent tools (syntax check)
4. Validate `agent_engine_app.py` exists and compiles
5. Test `agent_engine_app.py` imports
6. Validate YAML syntax (basic)

**Expected Files:**

**Agent YAMLs:**
- `app/perception_agent/agents/agent_0_orchestrator.yaml`
- `app/perception_agent/agents/agent_1_source_harvester.yaml`
- `app/perception_agent/agents/agent_2_topic_manager.yaml`
- `app/perception_agent/agents/agent_3_relevance_ranking.yaml`
- `app/perception_agent/agents/agent_4_brief_writer.yaml`
- `app/perception_agent/agents/agent_5_alert_anomaly.yaml`
- `app/perception_agent/agents/agent_6_validator.yaml`
- `app/perception_agent/agents/agent_7_storage_manager.yaml`

**Agent Tools:**
- `app/perception_agent/tools/agent_0_tools.py` through `agent_7_tools.py`

**Commands:**
```bash
# Compile agent tools
python -m compileall app/perception_agent/tools -q

# Validate agent_engine_app.py
cd app && python -c "import agent_engine_app; print('✅ agent_engine_app imports OK')"

# Validate YAML syntax
pip install pyyaml
python -c "
import yaml
from pathlib import Path

for yaml_file in Path('app/perception_agent/agents').glob('*.yaml'):
    with open(yaml_file) as f:
        yaml.safe_load(f)
    print(f'✅ {yaml_file.name} is valid YAML')
"
```

**Pass Criteria:**
- ✅ All 8 agent YAML configs present
- ✅ All 8 agent tools modules present
- ✅ All Python files compile
- ✅ `agent_engine_app.py` imports successfully
- ✅ All YAML files are valid syntax

---

### 3. Dashboard Smoke Tests (`dashboard-smoke`)

**Purpose:** Validate React dashboard build

**Actions:**
1. Set up Node.js 20
2. Install dashboard dependencies
3. TypeScript type checking
4. Build dashboard (production build)
5. Verify build artifacts exist

**Commands:**
```bash
cd dashboard

# Install dependencies
npm ci

# TypeScript check
npx tsc --noEmit

# Build
npm run build

# Verify artifacts
ls -lh dist/index.html
```

**Pass Criteria:**
- ✅ Dependencies install successfully
- ✅ No TypeScript errors
- ✅ Build completes without errors
- ✅ `dashboard/dist/index.html` exists

---

### 4. Data Source Smoke Tests (`data-source-smoke`)

**Purpose:** Validate RSS feeds CSV structure

**Actions:**
1. Verify `data/initial_feeds.csv` exists
2. Validate CSV structure (required columns)
3. Count feeds

**Required CSV Columns:**
- `source_id`
- `name`
- `type`
- `url`
- `category`
- `enabled`

**Commands:**
```bash
# Verify file exists
ls -lh data/initial_feeds.csv

# Validate structure
python3 -c "
import csv

required_columns = ['source_id', 'name', 'type', 'url', 'category', 'enabled']

with open('data/initial_feeds.csv') as f:
    reader = csv.DictReader(f)
    headers = reader.fieldnames

    if headers != required_columns:
        print(f'❌ CSV headers mismatch')
        sys.exit(1)

    row_count = sum(1 for row in reader)
    print(f'✅ CSV structure valid ({row_count} feeds)')
"
```

**Pass Criteria:**
- ✅ CSV file exists
- ✅ Headers match required columns
- ✅ At least 1 feed present

---

### 5. Summary Job (`summary`)

**Purpose:** Report overall smoke test status

**Actions:**
1. Collect results from all jobs
2. Generate summary table
3. Exit with failure if any job failed

**Output Format:**
```
## Smoke Test Results

| Component | Status |
|-----------|--------|
| Python/MCP Service | ✅ Pass |
| Agent Configs | ✅ Pass |
| Dashboard | ✅ Pass |
| Data Sources | ✅ Pass |
```

---

## Running Locally

### Run All Smoke Tests Locally

```bash
# 1. Python/MCP smoke tests
cd /home/jeremy/000-projects/perception
python3 -m venv .venv
source .venv/bin/activate
pip install -r app/mcp_service/requirements.txt
python -m compileall app/mcp_service -q
python -c "from app.mcp_service.main import app; print('✅ MCP OK')"
cd app/mcp_service && uvicorn main:app --help

# 2. Agent smoke tests
python -m compileall app/perception_agent/tools -q
cd app && python -c "import agent_engine_app; print('✅ Agents OK')"

# 3. Dashboard smoke tests
cd dashboard
npm ci
npx tsc --noEmit
npm run build
ls -lh dist/index.html

# 4. Data source smoke tests
python3 -c "
import csv
with open('data/initial_feeds.csv') as f:
    reader = csv.DictReader(f)
    print(f'✅ CSV OK ({sum(1 for row in reader)} feeds)')
"
```

### Run Individual Components

**MCP Service Only:**
```bash
source .venv/bin/activate
python -m compileall app/mcp_service -q && echo "✅ MCP compiles"
```

**Agents Only:**
```bash
python -m compileall app/perception_agent -q && echo "✅ Agents compile"
```

**Dashboard Only:**
```bash
cd dashboard && npm run build && echo "✅ Dashboard builds"
```

---

## Makefile Targets (Future)

Add to root `Makefile`:

```makefile
.PHONY: smoke-test smoke-python smoke-agents smoke-dashboard

smoke-test: smoke-python smoke-agents smoke-dashboard
	@echo "✅ All smoke tests passed"

smoke-python:
	python -m compileall app/mcp_service -q
	python -c "from app.mcp_service.main import app"
	@echo "✅ Python smoke tests passed"

smoke-agents:
	python -m compileall app/perception_agent -q
	cd app && python -c "import agent_engine_app"
	@echo "✅ Agent smoke tests passed"

smoke-dashboard:
	cd dashboard && npm run build > /dev/null
	@echo "✅ Dashboard smoke test passed"
```

**Usage:**
```bash
make smoke-test        # Run all smoke tests
make smoke-python      # Python only
make smoke-agents      # Agents only
make smoke-dashboard   # Dashboard only
```

---

## Integration with CI

### Automatic Execution

The smoke test workflow runs **automatically** on:
- Every push to `main`
- Every pull request to `main`

### Manual Execution

Trigger manually via GitHub Actions UI:
1. Go to https://github.com/{owner}/{repo}/actions
2. Select "CI Smoke Tests"
3. Click "Run workflow"
4. Select branch
5. Click "Run workflow"

### Pull Request Status Checks

When configured as a required status check:
- ✅ PR can only merge if smoke tests pass
- ❌ PR blocked if smoke tests fail

**Configure in GitHub:**
1. Settings → Branches → Branch protection rules
2. Select `main` branch
3. Check "Require status checks to pass before merging"
4. Select "CI Smoke Tests / summary"

---

## Common Failures & Fixes

### Python Syntax Error

**Symptom:** `SyntaxError` in compile step

**Fix:**
```bash
# Find problematic file
python -m py_compile app/mcp_service/main.py

# Fix syntax and re-test
```

### Import Error

**Symptom:** `ModuleNotFoundError` when testing imports

**Fix:**
```bash
# Ensure all dependencies are installed
pip install -r app/mcp_service/requirements.txt

# Check for missing __init__.py files
find app -type d -exec test ! -f {}/__init__.py \; -print
```

### YAML Syntax Error

**Symptom:** `yaml.scanner.ScannerError` in YAML validation

**Fix:**
```bash
# Use yamllint to find issues
pip install yamllint
yamllint app/perception_agent/agents/*.yaml

# Common issues:
# - Tabs instead of spaces
# - Incorrect indentation
# - Missing quotes around special characters
```

### Dashboard Build Failure

**Symptom:** TypeScript errors or build fails

**Fix:**
```bash
cd dashboard

# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install

# Check for TypeScript errors
npx tsc --noEmit

# Fix errors and rebuild
npm run build
```

### CSV Structure Invalid

**Symptom:** CSV validation fails

**Fix:**
```bash
# Check CSV headers
head -1 data/initial_feeds.csv

# Expected:
# source_id,name,type,url,category,enabled

# Fix headers if mismatched
```

---

## Performance Benchmarks

| Job | Expected Runtime | Acceptable Max |
|-----|------------------|----------------|
| python-smoke | ~30s | 1min |
| agent-smoke | ~20s | 45s |
| dashboard-smoke | ~2min | 4min |
| data-source-smoke | ~5s | 15s |
| **Total** | **~3min** | **6min** |

**Optimization Tips:**
- Use `npm ci` instead of `npm install` (faster, deterministic)
- Cache Node.js dependencies in GitHub Actions
- Use Python virtual environment caching
- Skip unnecessary steps if files haven't changed

---

## Comparison: Smoke Tests vs Full CI

| Aspect | Smoke Tests | Full CI (test.yml) |
|--------|-------------|-------------------|
| **GCP Required** | ❌ No | ❌ No |
| **Run Time** | ~3min | ~5min |
| **Coverage** | Syntax, imports, builds | + Unit tests, coverage |
| **Pytest** | Optional (if tests exist) | Required |
| **Linting** | Basic compile | Full (flake8, black, mypy) |
| **Deployment** | ❌ Never deploys | ❌ Never deploys |

**Use Cases:**
- **Smoke Tests:** Quick validation before/after code changes
- **Full CI:** Comprehensive quality checks before merge

---

## Next Steps

1. **Add Unit Tests**
   - Create `tests/mcp_service/` directory
   - Write pytest tests for MCP routers
   - Smoke tests will automatically run them

2. **Add Integration Tests**
   - Create `tests/integration/` directory
   - Test Agent → MCP communication
   - Test full workflow end-to-end

3. **Add Makefile**
   - Implement smoke test targets
   - Make local testing easier

4. **Configure as Required Check**
   - Add to branch protection
   - Block merges on failure

---

**Last Updated:** 2025-11-14
**Status:** Smoke test workflow created and ready
**Next:** Run workflow to verify all tests pass
