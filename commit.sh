#!/bin/bash
# Commit script for Perception

cd /home/jeremy/000-projects/perception || exit 1

echo "========================================="
echo "Perception - Git Commit & Push"
echo "========================================="

# Make scripts executable
chmod +x scripts/*.sh 2>/dev/null || true

# Check git status
echo ""
echo "Git Status:"
git status --short

# Stage all files
echo ""
echo "Staging all files..."
git add -A

# Commit with message
echo ""
echo "Creating commit..."
git commit -m "feat: complete Perception agent system implementation

- Created world-class README with badges and comprehensive documentation
- Implemented 8 specialized AI agents with A2A protocol orchestration
- Added complete tool implementations for all agents
- Set up GitHub Actions for WIF deployment (keyless auth)
- Created deployment scripts and Makefile for development
- Added Dockerfile and deployment configuration
- Configured RSS sources and environment templates
- Established Progressive Hardening development workflow
- Added WIF setup guide for secure cloud deployments
- Implemented telemetry and observability infrastructure

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"

# Push to origin
echo ""
echo "Pushing to origin main..."
git push origin main

echo ""
echo "========================================="
echo "✅ Complete!"
echo "========================================="
