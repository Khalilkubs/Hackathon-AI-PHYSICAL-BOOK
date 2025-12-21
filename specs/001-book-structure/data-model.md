# Data Model: Physical AI Book

## Entity: Module
- **Fields**:
  - id: string (e.g., "module-1", "module-2", "module-3")
  - title: string (e.g., "Fundamentals of Physical AI")
  - description: string (brief overview of the module content)
  - chapters: array of Chapter entities
  - order: integer (1-3 for sequence)
- **Validation rules**:
  - title is required and non-empty
  - description is required and 10-200 characters
  - must contain exactly 3 chapters
  - order must be 1-3
- **Relationships**:
  - Contains 3 Chapter entities
  - Related to other modules via cross-references

## Entity: Chapter
- **Fields**:
  - id: string (e.g., "chapter-1-1", "chapter-2-3")
  - title: string (e.g., "Introduction to Physical AI")
  - description: string (brief overview of the chapter content)
  - lessons: array of Lesson entities
  - moduleId: string (reference to parent Module)
  - order: integer (1-3 for sequence within module)
- **Validation rules**:
  - title is required and non-empty
  - description is required and 10-200 characters
  - must contain exactly 4 lessons
  - order must be 1-3
  - moduleId must reference a valid Module
- **Relationships**:
  - Belongs to 1 Module entity
  - Contains 4 Lesson entities
  - Related to other chapters via cross-references

## Entity: Lesson
- **Fields**:
  - id: string (e.g., "lesson-1-1-1", "lesson-3-2-4")
  - title: string (e.g., "What is Physical AI?")
  - description: string (brief overview of the lesson content)
  - content: string (Markdown formatted lesson content)
  - learningObjectives: array of strings (measurable learning goals)
  - prerequisites: array of strings (required knowledge/skills)
  - coreContent: string (main educational content)
  - practicalExercise: string (hands-on activity)
  - summary: string (key takeaways)
  - furtherReading: array of strings (additional resources)
  - chapterId: string (reference to parent Chapter)
  - order: integer (1-4 for sequence within chapter)
- **Validation rules**:
  - title is required and non-empty
  - description is required and 10-100 characters
  - all content sections are required
  - learningObjectives must contain 1-5 items
  - prerequisites may be empty
  - practicalExercise is required (for hands-on learning)
  - chapterId must reference a valid Chapter
  - order must be 1-4
- **Relationships**:
  - Belongs to 1 Chapter entity
  - Related to other lessons via cross-references
  - May reference external resources

## Entity: DocusaurusConfig
- **Fields**:
  - sidebarItems: array of navigation objects
  - versioning: boolean (whether to enable versioning)
  - search: boolean (whether to enable search)
  - themeConfig: object (navigation, footer, etc.)
- **Validation rules**:
  - sidebarItems must match the module/chapter/lesson hierarchy
  - versioning should be enabled for educational content
  - search must be enabled for documentation
- **Relationships**:
  - Configures navigation for all Module, Chapter, and Lesson entities