// Import Prism themes correctly for newer prism-react-renderer versions
const { themes } = require('prism-react-renderer');

const lightCodeTheme = themes.github;
const darkCodeTheme = themes.dracula;

/** @type {import('@docusaurus/types').DocusaurusConfig} */
(module.exports = {
  title: 'Physical AI & Humanoid Robotics Book',
  tagline: 'Embodied Artificial Intelligence Systems',
  url: 'https://your-github-username.github.io', // Replace with your GitHub Pages URL
  baseUrl: '/Hackathon-AI-PHYSICAL-BOOK/', // Replace with your repository name
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  favicon: 'img/favicon.ico',
  organizationName: 'your-github-username', // Replace with your GitHub username/organization
  projectName: 'Hackathon-AI-PHYSICAL-BOOK', // Replace with your repository name
  trailingSlash: false, // Recommended for GitHub Pages

  presets: [
    [
      '@docusaurus/preset-classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          editUrl: 'https://github.com/facebook/docusaurus/edit/main/website/',
        },
        blog: {
          showReadingTime: true,
          editUrl:
            'https://github.com/facebook/docusaurus/edit/main/website/blog/',
        },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      image: 'img/physical-ai-book-social-card.jpg',
      metadata: [
        { name: 'keywords', content: 'physical ai, robotics, embodied intelligence, sensors, actuators, ai systems' },
        { name: 'theme-color', content: '#12affa' },
      ],
      navbar: {
        title: 'Physical AI & Humanoid Robotics Book',
        logo: {
          alt: 'Physical AI Book Logo',
          src: 'img/logo.svg',
        },
        items: [
          { type: 'doc', docId: 'intro', position: 'left', label: 'Home' },
          { type: 'doc', docId: 'module-1/intro', position: 'left', label: 'Modules' },
          { to: '/blog', label: 'Blog', position: 'left' },
          {
            href: 'https://github.com/your-organization/physical-ai-book',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Physical AI & Humanoid Robotics Book',
            items: [
              { label: 'Introduction', to: '/docs/intro' },
              { label: 'Module 1: Fundamentals', to: '/docs/module-1/intro' },
              { label: 'Module 2: Perception & Reasoning', to: '/docs/module-2/intro' },
              { label: 'Module 3: Advanced Applications', to: '/docs/module-3/intro' },
              { label: 'Module 4: VLA Models', to: '/docs/module-4/intro' },
            ],
          },
          {
            title: 'Resources',
            items: [
              { label: 'Docusaurus', href: 'https://docusaurus.io' },
              { label: 'Physical AI Community', href: 'https://example.com/physical-ai-community' },
              { label: 'GitHub', href: 'https://github.com/your-organization/physical-ai-book' },
            ],
          },
          {
            title: 'Legal',
            items: [
              { label: 'Privacy Policy', href: '/privacy' },
              { label: 'Terms of Service', href: '/terms' },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Physical AI Book. Built with Docusaurus.`,
      },
      prism: {
        theme: lightCodeTheme,
        darkTheme: darkCodeTheme,
      },
    }),
});
