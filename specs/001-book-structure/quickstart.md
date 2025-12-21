# Quickstart: Physical AI Book Development

## Prerequisites
- Node.js (v18 or higher)
- npm or yarn package manager
- Git for version control
- Text editor or IDE

## Setup Instructions

1. **Install Docusaurus**:
   ```bash
   npm init docusaurus@latest docs-app classic
   ```

2. **Navigate to the project directory**:
   ```bash
   cd docs-app
   ```

3. **Install additional dependencies**:
   ```bash
   npm install @docusaurus/module-type-aliases @docusaurus/types
   ```

4. **Create the content structure**:
   ```bash
   mkdir -p docs/{module-1,module-2,module-3}/{chapter-1,chapter-2,chapter-3}
   ```

5. **Create the first lesson**:
   ```bash
   touch docs/module-1/chapter-1/lesson-1.md
   ```

## Content Creation Workflow

1. **Create a new lesson file** in the appropriate module/chapter directory
2. **Add Docusaurus frontmatter** at the top of each lesson file:
   ```markdown
   ---
   title: Lesson Title
   description: Brief description of the lesson
   sidebar_position: X
   ---
   ```
3. **Follow the 7-part lesson format**:
   - Learning Objectives
   - Prerequisites
   - Introduction
   - Core Content
   - Practical Exercise
   - Summary
   - Further Reading

## Running the Development Server

```bash
npm start
```

This command starts a local development server and opens the documentation site in your browser. Most changes are reflected live without having to restart the server.

## Building for Production

```bash
npm run build
```

This command generates static content in the `build` directory, which can be served using any static hosting service.

## Navigation Configuration

Update `sidebars.js` to reflect the module/chapter/lesson hierarchy:

```javascript
module.exports = {
  docs: [
    {
      type: 'category',
      label: 'Module 1: Fundamentals of Physical AI',
      items: [
        {
          type: 'category',
          label: 'Chapter 1.1: Introduction to Physical AI',
          items: ['module-1/chapter-1/lesson-1', 'module-1/chapter-1/lesson-2', 'module-1/chapter-1/lesson-3', 'module-1/chapter-1/lesson-4'],
        },
        // ... other chapters
      ],
    },
    // ... other modules
  ],
};
```

## Quality Checks

- Validate accessibility with `npm run serve` and test with accessibility tools
- Verify all practical exercises work as intended
- Ensure navigation works within 3 clicks maximum
- Check that all content follows the defined guidelines