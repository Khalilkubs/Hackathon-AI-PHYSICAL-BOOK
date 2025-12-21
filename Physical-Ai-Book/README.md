# Physical AI & Humanoid Robotics Book

This website is built using [Docusaurus 2](https://docusaurus.io/), a modern static website generator. It serves as a comprehensive educational resource on Physical AI & Humanoid Robotics.

## Project Overview

This is a comprehensive educational resource with modules covering various aspects of physical AI, robotics, and embodied intelligence systems:

1. **Module 1**: Fundamentals of Physical AI (ROS 2, sensing, actuation)
2. **Module 2**: Perception and Reasoning in Physical Systems (CV, navigation, planning)
3. **Module 3**: Advanced Physical AI Applications (HRI, edge AI, deployment)
4. **Module 4**: Vision-Language-Action (VLA) Models

## Installation

```
$ yarn
```

## Local Development

```
$ yarn start
```

This command starts a local development server and opens up a browser window. Most changes are reflected live without having to restart the server.

## Build

```
$ yarn build
```

This command generates static content into the `build` directory and can be served using any static contents hosting service.

## Deployment

### Vercel (Recommended)

This project is optimized for deployment on Vercel. For detailed instructions, see [VERCEL_DEPLOYMENT.md](./VERCEL_DEPLOYMENT.md).

1. Push your code to GitHub
2. Import the repository to Vercel
3. Configure:
   - Build Command: `npm run build`
   - Output Directory: `build`
   - Root Directory: `Physical-Ai-Book`
4. Deploy

### GitHub Pages

```
$ GIT_USER=<Your GitHub username> USE_SSH=true yarn deploy
```

If you are using GitHub pages for hosting, this command is a convenient way to build the website and push to the `gh-pages` branch.
