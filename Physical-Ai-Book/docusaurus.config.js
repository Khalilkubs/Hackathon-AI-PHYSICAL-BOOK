const { themes } = require('prism-react-renderer');

const lightCodeTheme = themes.github;
const darkCodeTheme = themes.dracula;

/** @type {import('@docusaurus/types').DocusaurusConfig} */
(module.exports = {
  title: 'Physical AI & Humanoid Robotics Book',
  tagline: 'Embodied Artificial Intelligence Systems',
  url: 'https://hackathon-ai-physical-book-1ojs.vercel.app', // Replace with your Vercel URL
  baseUrl: '/', // Root path for Vercel
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  favicon: 'img/favicon.ico',
  organizationName: 'Khalilkubs',
  projectName: 'Hackathon-AI-PHYSICAL-BOOK',
  trailingSlash: false,

  presets: [
    [
      '@docusaurus/preset-classic',
      ({
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          editUrl: 'https://github.com/Khalilkubs/Hackathon-AI-PHYSICAL-BOOK/edit/001-book-structure/Physical-Ai-Book/',
        },
        blog: {
          showReadingTime: true,
          editUrl: 'https://github.com/Khalilkubs/Hackathon-AI-PHYSICAL-BOOK/edit/001-book-structure/Physical-Ai-Book/blog/',
        },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
  ],

  themeConfig: {
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
          href: 'https://github.com/Khalilkubs/Hackathon-AI-PHYSICAL-BOOK',
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
            { label: 'GitHub', href: 'https://github.com/Khalilkubs/Hackathon-AI-PHYSICAL-BOOK' },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Physical AI Book. Built with Docusaurus.`,
    },
    prism: {
      theme: lightCodeTheme,
      darkTheme: darkCodeTheme,
    },
  },
});
