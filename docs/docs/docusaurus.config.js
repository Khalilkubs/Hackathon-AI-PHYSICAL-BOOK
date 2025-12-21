const lightCodeTheme = require('prism-react-renderer/themes/github');
const darkCodeTheme = require('prism-react-renderer/themes/dracula');

// With JSDoc @type annotations, IDEs can provide config autocompletion
/** @type {import('@docusaurus/types').DocusaurusConfig} */
(module.exports = {
  title: 'Physical AI & Humanoid Robotics Book',
  tagline: 'Embodied Artificial Intelligence Systems',
  url: 'https://your-physical-ai-book.com',
  baseUrl: '/',
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  favicon: 'img/favicon.ico',
  organizationName: 'your-organization', // Usually your GitHub org/user name.
  projectName: 'physical-ai-book', // Usually your repo name.

  presets: [
    [
      '@docusaurus/preset-classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          // Please change this to your repo.
          editUrl: 'https://github.com/facebook/docusaurus/edit/main/website/',
        },
        blog: {
          showReadingTime: true,
          // Please change this to your repo.
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
      image: 'img/physical-ai-book-social-card.jpg', // For social media cards
      metadata: [
        {name: 'keywords', content: 'physical ai, robotics, embodied intelligence, sensors, actuators, ai systems'},
        {name: 'theme-color', content: '#12affa'},
      ],
      navbar: {
        title: 'Physical AI Book',
        logo: {
          alt: 'Physical AI Book Logo',
          src: 'img/logo.svg',
        },
        items: [
          {
            type: 'doc',
            docId: 'intro',
            position: 'left',
            label: 'Home',
          },
          {
            type: 'doc',
            docId: 'module-1/intro',
            position: 'left',
            label: 'Modules',
          },
          {to: '/blog', label: 'Blog', position: 'left'},
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
            title: 'Physical AI Book',
            items: [
              {
                label: 'Introduction',
                to: '/docs/intro',
              },
              {
                label: 'Module 1: Fundamentals',
                to: '/docs/module-1/intro',
              },
              {
                label: 'Module 2: Perception & Reasoning',
                to: '/docs/module-2/intro',
              },
              {
                label: 'Module 3: Advanced Applications',
                to: '/docs/module-3/intro',
              },
              {
                label: 'Module 4: VLA Models',
                to: '/docs/module-4/intro',
              },
            ],
          },
          {
            title: 'Resources',
            items: [
              {
                label: 'Docusaurus',
                href: 'https://docusaurus.io',
              },
              {
                label: 'Physical AI Community',
                href: 'https://example.com/physical-ai-community',
              },
              {
                label: 'GitHub',
                href: 'https://github.com/your-organization/physical-ai-book',
              },
            ],
          },
          {
            title: 'Legal',
            items: [
              {
                label: 'Privacy Policy',
                href: '/privacy',
              },
              {
                label: 'Terms of Service',
                href: '/terms',
              },
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
