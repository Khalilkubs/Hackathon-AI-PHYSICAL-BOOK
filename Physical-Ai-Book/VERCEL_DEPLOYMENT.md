# AI Physical Book - Vercel Deployment Guide

This repository contains the Physical AI & Humanoid Robotics Book, a comprehensive educational resource built with Docusaurus. This guide will help you deploy the project to Vercel.

## Project Overview

This is a Docusaurus-based documentation website focused on Physical AI & Humanoid Robotics. The project is structured as a comprehensive educational resource with modules covering various aspects of physical AI, robotics, and embodied intelligence systems.

## Deployment to Vercel

### Prerequisites

- A GitHub repository containing this code
- A Vercel account (https://vercel.com)

### Deployment Steps

1. **Push your code to GitHub**
   - Make sure all changes are committed and pushed to your GitHub repository

2. **Import to Vercel**
   - Go to https://vercel.com/dashboard
   - Click "New Project"
   - Select your GitHub repository
   - Click "Import"

3. **Configure the project**
   - Framework Preset: Auto-detected (Docusaurus)
   - Build Command: `npm run build`
   - Output Directory: `build`
   - Root Directory: `Physical-Ai-Book`
   - Environment Variables (optional):
     - NODE_VERSION: `18.x` or `20.x`

4. **Deploy**
   - Click "Deploy" to start the deployment process

### Post-Deployment Steps

1. **Update Docusaurus Configuration**
   After deployment, update the `docusaurus.config.js` file with your actual Vercel URL:

   ```js
   url: 'https://your-project-name.vercel.app', // Replace with your actual Vercel URL
   ```

2. **Custom Domain (Optional)**
   - Go to your project settings in Vercel
   - Navigate to "Domains" section
   - Add your custom domain if desired

## Project Structure

- `/docs` - Educational content organized by modules
- `/src` - Custom source code (components, CSS, pages)
- `/blog` - Blog posts directory
- `/static` - Static assets (images, etc.)
- `docusaurus.config.js` - Docusaurus configuration
- `sidebars.js` - Navigation structure
- `vercel.json` - Vercel deployment configuration

## Module Structure

The content is organized into 4 comprehensive modules:

1. **Module 1**: Fundamentals of Physical AI (ROS 2, sensing, actuation)
2. **Module 2**: Perception and Reasoning in Physical Systems (CV, navigation, planning)
3. **Module 3**: Advanced Physical AI Applications (HRI, edge AI, deployment)
4. **Module 4**: Vision-Language-Action (VLA) Models

## Development

To run the project locally:

```bash
# Install dependencies
npm install

# Start development server
npm run start

# Build for production
npm run build
```

## Troubleshooting

### Common Issues

1. **Build fails on Vercel**
   - Ensure `vercel.json` is properly configured
   - Check that the output directory is set to `build`
   - Verify Node.js version compatibility

2. **Broken links after deployment**
   - Make sure all module intro files exist
   - Verify that `baseUrl` is set correctly for Vercel deployment

3. **Images not loading**
   - Ensure images are placed in the `/static/img` directory
   - Use relative paths in markdown files

## Additional Notes

- The project is configured to work with both GitHub Pages and Vercel
- For GitHub Pages deployment, change `baseUrl` back to `/repository-name/`
- For Vercel deployment, use `baseUrl: '/'`
- The project uses Docusaurus v3.9.2