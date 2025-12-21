#!/bin/bash
# Deployment script for GitHub Pages

set -e

echo "Starting GitHub Pages deployment..."

# Check if we're in the right directory
if [ ! -d "Physical-Ai-Book" ]; then
    echo "Error: Physical-Ai-Book directory not found!"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "npm is not installed. Please install npm first."
    exit 1
fi

echo "Installing dependencies..."
cd Physical-Ai-Book
npm ci

echo "Building the website..."
npm run build

echo "Build completed successfully!"
echo "The built site is in the Physical-Ai-Book/build directory"
echo ""
echo "If you want to deploy manually to GitHub Pages, follow these steps:"
echo "1. Go to your GitHub repository settings"
echo "2. Navigate to Pages section"
echo "3. Select 'Deploy from a branch'"
echo "4. Choose 'gh-pages' branch and '/ (root)' folder"
echo ""
echo "For automatic deployment, the GitHub Actions workflow will handle it when you push to main branch."