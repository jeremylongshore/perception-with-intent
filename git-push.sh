#!/bin/bash
cd /home/jeremy/000-projects/perception

echo "=== Pushing Perception to GitHub ==="
echo ""

# Make scripts executable
chmod +x scripts/*.sh 2>/dev/null || true
chmod +x *.sh 2>/dev/null || true

# Check remote
echo "Checking remote..."
git remote -v

# Stage everything
echo ""
echo "Staging files..."
git add -A

# Show what will be committed
echo ""
echo "Files to commit:"
git status --short

# Commit
echo ""
echo "Committing..."
git commit -m "feat: complete Perception agent system implementation

Complete AI-powered news intelligence platform with:
- 8 specialized agents orchestrated via A2A Protocol
- Vertex AI Agent Engine deployment architecture
- Firebase dashboard integration
- GitHub Actions CI/CD with WIF (keyless auth)
- Comprehensive world-class documentation
- Progressive Hardening development workflow
- Complete tool implementations for all agents
- RSS source configuration (15 feeds)
- Deployment scripts and Makefile
- WIF setup guide for secure deployments

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"

# Push
echo ""
echo "Pushing to GitHub..."
git push -u origin main

echo ""
echo "=== Done! ==="
