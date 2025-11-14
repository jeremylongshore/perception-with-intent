# GitHub Repository Setup for Perception

## Current Status

✅ Local repository exists with all code
❌ No remote repository configured yet
🎯 Need to create GitHub repo named "perception"

## Step-by-Step Instructions

### 1. Create GitHub Repository

Go to GitHub and create a new repository:
- **Repository name:** `perception`
- **Description:** "Executive-Level News Intelligence Without the Fluff"
- **Visibility:** ✅ **Public** (required for showcase)
- **DO NOT** initialize with README, .gitignore, or license (we already have these)

### 2. Connect Local Repo to GitHub

Once you create the repo, GitHub will show you commands. Use these:

```bash
cd /home/jeremy/000-projects/perception

# Add the remote (replace [your-username] with your GitHub username)
git remote add origin https://github.com/[your-username]/perception.git

# Or if you use SSH:
# git remote add origin git@github.com:[your-username]/perception.git

# Verify the remote was added
git remote -v
```

### 3. Push to GitHub

```bash
# Stage all files
git add -A

# Commit everything
git commit -m "feat: initial Perception implementation

Complete AI-powered news intelligence platform with:
- 8 specialized agents orchestrated via A2A Protocol
- Vertex AI Agent Engine deployment
- Firebase dashboard
- GitHub Actions CI/CD with WIF
- Comprehensive documentation and README

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"

# Push to GitHub
git branch -M main
git push -u origin main
```

### 4. Update README with Your Username

After pushing, update the README.md file to replace `[your-username]` with your actual GitHub username:

```bash
# Open in your editor
vim README.md  # or nano, or code

# Find and replace:
[your-username] → your-actual-username

# Commit the change
git add README.md
git commit -m "docs: update GitHub username in README"
git push
```

### 5. Set Up GitHub Actions Secrets (Optional for now)

If you want GitHub Actions to work, you'll need to:

1. Follow the `WIF-SETUP-GUIDE.md` to configure Workload Identity Federation
2. Update `.github/workflows/deploy.yml` with your WIF provider URL
3. Push the changes

But this can wait until after initial launch.

## Verification

After pushing, verify everything is there:

```bash
# Check remote
git remote -v

# Check branch
git branch -a

# Check latest commit
git log -1 --oneline
```

Your repo should now be live at:
`https://github.com/[your-username]/perception`

---

**Status:** Ready to create GitHub repo
**Next Action:** Create repo on GitHub, then run commands above
