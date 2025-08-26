#!/bin/bash
# Release script - auto bump, build, and publish

set -e

echo "🚀 Starting release process..."

# Auto-bump patch version
echo "📈 Bumping version..."
uv run bump2version patch

# Build package
echo "🔨 Building package..."
uv build

# Publish to PyPI
echo "📦 Publishing to PyPI..."
uv publish

echo "✅ Release complete!"
