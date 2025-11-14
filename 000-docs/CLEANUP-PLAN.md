# Directory Cleanup Plan
## Transition to New Project

**Created:** 2025-11-11
**Purpose:** Clean slate preparation for new project
**Archive Reference:** `000-docs/ARCHIVE-2025-11-11-PRE-NEW-PROJECT.md`
**Source Snapshot:** `000-docs/archive/iam1-legacy-2025-11-11.tar.gz`

---

## Current Status

### Completed ✅
- [x] **Archive created** - Complete audit saved to `ARCHIVE-2025-11-11-PRE-NEW-PROJECT.md`
- [x] **Directory renamed** - `claudes-docs/` → `000-docs/`
- [x] **User manuals directory created** - `000-usermanuals/` ready

### Directory Overview

```
intent-agent-model-jvp-base/
├── 000-docs/                    # ✅ KEEP - Documentation archive
│   ├── ARCHIVE-2025-11-11-PRE-NEW-PROJECT.md  # Complete audit
│   ├── 000-INDEX.md
│   └── ... (7 other docs)
├── 000-usermanuals/             # ✅ NEW - User manual directory
├── .github/                     # 🔄 DECIDE - CI/CD workflows
├── app/                         # 🗑️ DELETE - Old IAM1 code
├── data_ingestion/              # 🗑️ DELETE - Old pipeline
├── deployment/                  # 🔄 DECIDE - Terraform configs
├── docs/                        # 🗑️ DELETE - GitHub Pages site
├── notebooks/                   # 🗑️ DELETE - Old notebooks
├── slack-webhook/               # 🗑️ DELETE - Old integration
├── tests/                       # 🗑️ DELETE - Old test suite
├── .venv/                       # 🗑️ DELETE - Virtual environment
├── DEPLOYMENT_GUIDE.md          # 🗑️ DELETE - Old guide
├── deployment_metadata.json     # ⚠️ BACKUP FIRST - Live deployment ID
├── GEMINI.md                    # 🗑️ DELETE - Old docs
├── Makefile                     # 🗑️ DELETE - Old automation
├── pyproject.toml               # 🗑️ DELETE - Old dependencies
├── README.md                    # 🗑️ DELETE - Old README
└── uv.lock                      # 🗑️ DELETE - Old lock file
```

---

## Cleanup Recommendations

### Phase 1: Critical Backups ⚠️

**BEFORE DELETING ANYTHING:**

```bash
# 1. Backup deployment metadata (contains live Vertex AI Agent Engine ID)
cp deployment_metadata.json 000-docs/BACKUP-deployment_metadata.json

# 2. Check for any uncommitted Git changes
git status

# 3. Ensure archive is complete
cat 000-docs/ARCHIVE-2025-11-11-PRE-NEW-PROJECT.md | wc -l  # Should be 700+ lines
# 4. Verify source snapshot archive exists (~>400MB compressed)
ls -lh 000-docs/archive/iam1-legacy-2025-11-11.tar.gz
```

**CRITICAL: Deployed Agent Engine**
```json
{
  "remote_agent_engine_id": "projects/205354194989/locations/us-central1/reasoningEngines/5828234061910376448",
  "deployment_timestamp": "2025-11-09T15:34:23.310165"
}
```

**Decision Required:**
- **Keep running?** - Leave deployed, just archive the ID
- **Tear down?** - Use Terraform to destroy resources first
- **Unknown?** - Check Vertex AI console before deleting

---

### Phase 2: Safe Deletions 🗑️

**These can be safely deleted (all archived):**

```bash
# Remove old code directories
rm -rf app/
rm -rf data_ingestion/
rm -rf notebooks/
rm -rf slack-webhook/
rm -rf tests/
rm -rf docs/

# Remove old configuration files
rm -f DEPLOYMENT_GUIDE.md
rm -f GEMINI.md
rm -f Makefile
rm -f pyproject.toml
rm -f README.md
rm -f uv.lock

# Remove virtual environment
rm -rf .venv/

# After backing up deployment metadata:
rm -f deployment_metadata.json
```

---

### Phase 3: Conditional Cleanup 🔄

#### `.github/` - CI/CD Workflows

**Decision Options:**

**Option A: Keep Structure, Clear Content**
```bash
# Keep directory structure for new CI/CD, but clear old workflows
rm -rf .github/workflows/*
rm -rf .github/ISSUE_TEMPLATE/*
rm -rf .github/PULL_REQUEST_TEMPLATE/*
rm -f .github/pull_request_template.md

# Keep .github/ directory itself for future use
```

**Option B: Complete Removal**
```bash
# Start completely fresh
rm -rf .github/
```

**Recommendation:** Option A - Keep structure, useful for new project CI/CD

---

#### `deployment/` - Terraform Infrastructure

**Decision Options:**

**Option A: Keep Terraform (If reusing GCP infrastructure pattern)**
```bash
# Keep deployment/ directory if new project will use similar Terraform setup
# Just update terraform files for new project
```

**Option B: Archive and Delete**
```bash
# Move to archive if not reusing
mv deployment/ 000-docs/archived-terraform/
```

**Option C: Complete Removal**
```bash
# Delete if starting fresh infrastructure
rm -rf deployment/
```

**Recommendation:**
- If new project uses Google Cloud → Keep and modify
- If different cloud/no infrastructure → Delete
- If unsure → Option B (archive first)

**WARNING:** If Terraform state has **live resources**, destroy first:
```bash
cd deployment/terraform/
terraform destroy  # Review carefully before confirming
cd ../..
```

---

### Phase 4: Git Cleanup 🔄

**Options:**

**Option A: Keep Git History**
```bash
# Keep .git/ directory, commit cleanup
git add -A
git commit -m "Archive IAM JVP Base template history, prepare for new project"
```

**Option B: Fresh Git Repository**
```bash
# Remove old history, start fresh
rm -rf .git/
git init
git add 000-docs/ 000-usermanuals/ .gitignore
git commit -m "Initial commit - New project"
```

**Recommendation:** Option A if you want history, Option B for truly clean slate

---

## Execution Plan

### Quick Clean (Safe for Most Cases)

```bash
#!/bin/bash
# Execute from project root

# 1. Backup critical data
cp deployment_metadata.json 000-docs/BACKUP-deployment_metadata.json

# 2. Remove code directories
rm -rf app/ data_ingestion/ notebooks/ slack-webhook/ tests/ docs/ .venv/

# 3. Remove old config files
rm -f DEPLOYMENT_GUIDE.md GEMINI.md Makefile pyproject.toml README.md uv.lock deployment_metadata.json

# 4. Clear CI/CD workflows (keep structure)
rm -rf .github/workflows/*
rm -rf .github/ISSUE_TEMPLATE/*
rm -rf .github/PULL_REQUEST_TEMPLATE/*
rm -f .github/pull_request_template.md

# 5. Decision point - deployment/
# CHOOSE ONE:
# rm -rf deployment/                    # Delete completely
# mv deployment/ 000-docs/archived-tf/  # Archive
# (or keep deployment/ for reuse)

# 6. Verify what remains
ls -la
```

---

### Thorough Clean (Complete Fresh Start)

```bash
#!/bin/bash
# Execute from project root

# 1. Backup critical data
cp deployment_metadata.json 000-docs/BACKUP-deployment_metadata.json

# 2. Check for live Terraform resources
cd deployment/terraform/
terraform plan  # Review what's deployed
# terraform destroy  # ONLY if you want to tear down live resources
cd ../..

# 3. Remove ALL old content
rm -rf app/ data_ingestion/ deployment/ docs/ notebooks/ slack-webhook/ tests/ .venv/ .github/

# 4. Remove ALL old config files
rm -f DEPLOYMENT_GUIDE.md GEMINI.md Makefile pyproject.toml README.md uv.lock deployment_metadata.json

# 5. Keep only archive and new directories
# Remaining: 000-docs/, 000-usermanuals/, .git/, .gitignore

# 6. Optional: Fresh git
# rm -rf .git/
# git init

# 7. Verify clean slate
ls -la
```

---

## New Project Structure (After Cleanup)

### Minimal Clean State
```
intent-agent-model-jvp-base/
├── .git/                        # Git repository (optional)
├── .gitignore                   # Git ignore patterns
├── 000-docs/                    # Documentation archive
│   ├── ARCHIVE-2025-11-11-PRE-NEW-PROJECT.md
│   ├── CLEANUP-PLAN.md
│   └── ... (old docs for reference)
└── 000-usermanuals/             # User manual directory (empty, ready)
```

### Ready for New Project
```
intent-agent-model-jvp-base/
├── .git/                        # Version control
├── .gitignore                   # Ignore patterns
├── 000-docs/                    # Project documentation
│   ├── ARCHIVE-2025-11-11-PRE-NEW-PROJECT.md
│   ├── 001-PP-ARCH-[new-project-architecture].md
│   └── ...
├── 000-usermanuals/             # User manuals
│   ├── 001-[manual-name].md
│   └── ...
├── README.md                    # New project README
├── pyproject.toml               # New dependencies
└── [new-project-files]/         # Your new project structure
```

---

## Verification Checklist

### Before Cleanup
- [ ] Archive document exists and is complete (700+ lines)
- [ ] `deployment_metadata.json` backed up to `000-docs/`
- [ ] Git status checked (no uncommitted critical changes)
- [ ] Terraform state checked (know what's deployed)
- [ ] Decision made on live GCP resources (keep/destroy)
- [ ] Decision made on Git history (keep/fresh)
- [ ] Decision made on Terraform configs (keep/archive/delete)

### After Cleanup
- [ ] `000-docs/` directory exists with archive
- [ ] `000-usermanuals/` directory exists (empty)
- [ ] All old code removed (`app/`, `tests/`, etc.)
- [ ] All old config removed (Makefile, pyproject.toml, etc.)
- [ ] `.venv/` removed
- [ ] `.github/` handled per decision (cleared or removed)
- [ ] `deployment/` handled per decision (kept/archived/removed)
- [ ] `.gitignore` still present
- [ ] Git repository in desired state
- [ ] Directory is clean slate for new project

### Final Verification
```bash
# Should show minimal structure
ls -la

# Should show only archive and new dirs in project
find . -maxdepth 1 -type d

# Should be no Python files in root or immediate subdirs
find . -maxdepth 2 -name "*.py"  # Should return nothing or very minimal

# Should be no old config files
ls *.toml *.lock Makefile 2>/dev/null  # Should return nothing
```

---

## Recommendations by Use Case

### Use Case 1: Reusing Google Cloud Infrastructure Pattern
**Keep:**
- `deployment/` (modify for new project)
- `.github/` structure (update workflows)
- `.gitignore` (update for new project)
- Git history

**Delete:**
- All code (`app/`, `tests/`, etc.)
- All old configs
- `.venv/`

**Result:** Infrastructure template ready for new agent project

---

### Use Case 2: Completely Different Project (Non-Agent)
**Keep:**
- `000-docs/` (archive only)
- `000-usermanuals/`
- `.gitignore` (heavily modify)

**Delete:**
- Everything else

**Result:** Clean slate with only documentation archive

---

### Use Case 3: New Agent Project (Different Framework)
**Keep:**
- `000-docs/` (reference patterns)
- `000-usermanuals/`
- `.github/` structure (CI/CD useful)
- `.gitignore` (Python patterns still relevant)

**Delete:**
- All code and Terraform
- Old configs

**Result:** Fresh start with useful CI/CD and reference docs

---

## Quick Commands

### Check What Would Be Deleted
```bash
# Dry run - see what would be removed
ls -ld app data_ingestion deployment docs notebooks slack-webhook tests .venv
ls -l *.md *.toml *.lock Makefile 2>/dev/null
```

### Safe Minimal Clean
```bash
# Removes obvious old files, keeps potentially useful infrastructure
cp deployment_metadata.json 000-docs/BACKUP-deployment_metadata.json
rm -rf app/ data_ingestion/ notebooks/ slack-webhook/ tests/ docs/ .venv/
rm -f DEPLOYMENT_GUIDE.md GEMINI.md Makefile pyproject.toml README.md uv.lock deployment_metadata.json
rm -rf .github/workflows/* .github/ISSUE_TEMPLATE/* .github/PULL_REQUEST_TEMPLATE/*
```

### Aggressive Clean
```bash
# Removes everything except archive and .git
cp deployment_metadata.json 000-docs/BACKUP-deployment_metadata.json
rm -rf app/ data_ingestion/ deployment/ docs/ notebooks/ slack-webhook/ tests/ .venv/ .github/
rm -f DEPLOYMENT_GUIDE.md GEMINI.md Makefile pyproject.toml README.md uv.lock deployment_metadata.json
```

---

## Important Notes

1. **Deployment Metadata** - Contains live Vertex AI Agent Engine ID. If that agent is still running, keep this ID somewhere safe for potential teardown later.

2. **Terraform State** - If `deployment/terraform/` has state files with live resources, destroying them requires `terraform destroy`. Don't just delete the directory.

3. **Git History** - 8 commits exist. If you want to preserve history of the IAM1 template work, keep `.git/`. Otherwise, fresh start is fine.

4. **GitHub Pages** - The `docs/index.html` is deployed to GitHub Pages. If that site should stay live, don't delete the repository or update GH Pages settings.

5. **Archive Completeness** - The `ARCHIVE-2025-11-11-PRE-NEW-PROJECT.md` contains:
   - Complete file tree
   - All code summaries (1,623 lines documented)
   - Deployment information
   - Architecture diagrams
   - Technology stack details
   - Business model documentation

---

## Next Steps

1. **Review this plan** and decide on cleanup level
2. **Execute backup commands** (deployment_metadata.json)
3. **Check Terraform** for live resources
4. **Execute cleanup** per chosen level
5. **Verify clean state** with checklist
6. **Begin new project** setup

---

**Created By:** Claude Code
**Reference:** `ARCHIVE-2025-11-11-PRE-NEW-PROJECT.md`
**Status:** Ready for execution

---
