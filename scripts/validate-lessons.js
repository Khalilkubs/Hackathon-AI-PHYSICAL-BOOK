#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// Configuration
const DOCS_DIR = './docs';
const MODULES = ['module-1', 'module-2', 'module-3'];
const CHAPTERS = ['chapter-1', 'chapter-2', 'chapter-3'];
const LESSONS_PER_CHAPTER = 4;

// Expected lesson structure
const EXPECTED_SECTIONS = [
  '## Learning Objectives',
  '## Prerequisites',
  '## Introduction',
  '## Core Content',
  '## Practical Exercise',
  '## Summary',
  '## Further Reading'
];

function validateLesson(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const lines = content.split('\n');

    // Check if required sections exist
    const missingSections = [];
    for (const section of EXPECTED_SECTIONS) {
      if (!content.includes(section)) {
        missingSections.push(section);
      }
    }

    // Check for frontmatter
    const hasFrontmatter = content.startsWith('---');
    if (!hasFrontmatter) {
      missingSections.push('frontmatter (--- title/description ---)');
    }

    if (missingSections.length > 0) {
      console.log(`❌ ${filePath} is missing: ${missingSections.join(', ')}`);
      return false;
    }

    console.log(`✅ ${filePath} is valid`);
    return true;
  } catch (error) {
    console.error(`Error reading ${filePath}:`, error.message);
    return false;
  }
}

function validateStructure() {
  console.log('Validating Physical AI Book structure...\n');

  let totalLessons = 0;
  let validLessons = 0;

  for (const module of MODULES) {
    const modulePath = path.join(DOCS_DIR, module);

    for (const chapter of CHAPTERS) {
      const chapterPath = path.join(modulePath, chapter);

      if (!fs.existsSync(chapterPath)) {
        console.log(`❌ Chapter directory missing: ${chapterPath}`);
        continue;
      }

      for (let lessonNum = 1; lessonNum <= LESSONS_PER_CHAPTER; lessonNum++) {
        const lessonPath = path.join(chapterPath, `lesson-${lessonNum}.md`);
        totalLessons++;

        if (fs.existsSync(lessonPath)) {
          if (validateLesson(lessonPath)) {
            validLessons++;
          }
        } else {
          console.log(`❌ Lesson file missing: ${lessonPath}`);
        }
      }
    }
  }

  console.log(`\nValidation Summary:`);
  console.log(`Total lessons: ${totalLessons}`);
  console.log(`Valid lessons: ${validLessons}`);
  console.log(`Missing/invalid: ${totalLessons - validLessons}`);

  if (validLessons === totalLessons) {
    console.log('🎉 All lessons are valid!');
    return true;
  } else {
    console.log('❌ Some lessons need attention.');
    return false;
  }
}

// Run validation
const isValid = validateStructure();
process.exit(isValid ? 0 : 1);