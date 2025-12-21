# GitHub Pages Deployment for Physical AI & Humanoid Robotics Textbook

This guide explains how to deploy the Docusaurus-based textbook to GitHub Pages.

## Automatic Deployment with GitHub Actions

The repository is configured with a GitHub Actions workflow that automatically deploys the site when changes are pushed to the `main` branch.

### Setup Steps:

1. **Enable GitHub Pages in your repository:**
   - Go to your repository on GitHub
   - Click on the "Settings" tab
   - In the left sidebar, click on "Pages"
   - Under "Source", select "Deploy from a branch"
   - Choose "gh-pages" as the branch and "/" as the folder
   - Click "Save"

2. **The workflow will automatically:**
   - Checkout your repository
   - Setup Node.js environment
   - Install dependencies
   - Build the Docusaurus site
   - Deploy the built site to the `gh-pages` branch

### Workflow Configuration

The deployment workflow is defined in `.github/workflows/deploy.yml` and runs on:
- Push to the `main` branch
- Pull requests to the `main` branch

## Manual Deployment

If you prefer to deploy manually, you can use the provided script:

```bash
chmod +x scripts/deploy_to_github_pages.sh
./scripts/deploy_to_github_pages.sh
```

This script will:
1. Install dependencies using npm
2. Build the Docusaurus site
3. Prepare the built site in the `Physical-Ai-Book/build` directory

## Configuration

The deployment is configured in `Physical-Ai-Book/docusaurus.config.js`:

```javascript
{
  url: 'https://your-github-username.github.io', // Replace with your GitHub Pages URL
  baseUrl: '/Hackathon-AI-PHYSICAL-BOOK/', // Replace with your repository name
  organizationName: 'your-github-username', // Replace with your GitHub username/organization
  projectName: 'Hackathon-AI-PHYSICAL-BOOK', // Replace with your repository name
}
```

**Important:** Before deploying, make sure to update these values with your actual GitHub username and repository name.

## Custom Domain (Optional)

If you want to use a custom domain:

1. Add a `CNAME` file in the `static` directory (`Physical-Ai-Book/static/CNAME`)
2. Add your domain name to this file (e.g., `myroboticsbook.com`)
3. Configure your DNS settings to point to GitHub Pages

## Troubleshooting

1. **Site not updating:** Make sure the workflow completed successfully in the Actions tab
2. **Incorrect URL:** Verify the `url` and `baseUrl` in `docusaurus.config.js` match your repository
3. **Build errors:** Check the Action logs for specific error messages
4. **Content not showing:** Ensure all markdown files are in the correct directory structure

## Verification

After deployment, your site will be available at:
`https://<your-github-username>.github.io/<repository-name>/`

For this repository, it would be:
`https://<your-github-username>.github.io/Hackathon-AI-PHYSICAL-BOOK/`