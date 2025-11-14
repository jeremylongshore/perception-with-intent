#!/bin/bash
# Quick script to push Perception to GitHub
# Run this AFTER creating the GitHub repo

set -e

echo "========================================="
echo "Push Perception to GitHub"
echo "========================================="
echo ""

# Check if we're in the right directory
if [ ! -d "/home/jeremy/000-projects/perception/.git" ]; then
    echo "❌ Error: Not in perception directory"
    exit 1
fi

cd /home/jeremy/000-projects/perception

# Get GitHub username
echo "Enter your GitHub username:"
read GITHUB_USER

if [ -z "$GITHUB_USER" ]; then
    echo "❌ Error: GitHub username required"
    exit 1
fi

echo ""
echo "Using GitHub username: $GITHUB_USER"
echo ""

# Add remote (will fail if already exists, that's OK)
echo "Adding GitHub remote..."
git remote add origin "https://github.com/${GITHUB_USER}/perception.git" 2>/dev/null || echo "Remote already exists, continuing..."

# Verify remote
echo ""
echo "Current remotes:"
git remote -v

# Stage all files
echo ""
echo "Staging all files..."
git add -A

# Commit
echo ""
echo "Creating commit..."
git commit -m "feat: initial Perception implementation

Complete AI-powered news intelligence platform with:
- 8 specialized agents orchestrated via A2A Protocol
- Vertex AI Agent Engine deployment
- Firebase dashboard
- GitHub Actions CI/CD with WIF
- Comprehensive documentation and README

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>" || echo "Nothing to commit or already committed"

# Set main branch
git branch -M main

# Push to GitHub
echo ""
echo "Pushing to GitHub..."
git push -u origin main

echo ""
echo "========================================="
echo "✅ Complete!"
echo "========================================="
echo ""
echo "Your repo is now live at:"
echo "https://github.com/${GITHUB_USER}/perception"
echo ""
echo "Next steps:"
echo "1. Update README.md with your GitHub username"
echo "2. Set up WIF for GitHub Actions (see WIF-SETUP-GUIDE.md)"
echo "3. Deploy to production!"
