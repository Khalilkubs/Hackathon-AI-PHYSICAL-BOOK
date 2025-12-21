# Cross-Linking Guide for Physical AI Book

## Internal Links

Use relative paths to link between lessons in the book:

```markdown
[Link to another lesson](../chapter-2/lesson-2.md)
[Link to a lesson in another module](../../module-2/chapter-1/lesson-1.md)
```

## Navigation Links

Each lesson should include navigation links to the previous and next lessons:

```markdown
## Navigation

[← Previous Lesson](./lesson-1.md) | [Next Lesson →](./lesson-3.md)
```

## Module Links

For linking between modules:

```markdown
[Return to Module 1](../../module-1/intro.md)
[Continue to Module 3](../../module-3/intro.md)
```

## Cross-Module References

When referencing concepts from other modules:

```markdown
As discussed in [Module 2, Chapter 1](../../module-2/chapter-1/intro.md), ...
```