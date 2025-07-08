# AI Development Tips and Guidelines

This comprehensive guide consolidates best practices, token management strategies, and operational protocols for AI assistants working with the Sales Commissions App codebase.

## Table of Contents
1. [Token Management](#token-management)
2. [Code Modification Best Practices](#code-modification-best-practices)
3. [File Handling Tips](#file-handling-tips)
4. [Task Planning and Decomposition](#task-planning-and-decomposition)
5. [Manual Code Replacement Protocol](#manual-code-replacement-protocol)
6. [General Development Guidelines](#general-development-guidelines)

---

## Token Management

### Core Operating Parameters
When working with AI models, especially Gemini, be aware of token constraints:
- **Input Context Window**: 1,000,000 tokens
- **Maximum Output Generation**: 65,536 tokens

### Mandatory Pre-Task Analysis
Before executing any complex request:

1. **Output Estimation**: Internally estimate the number of tokens your planned response will require
2. **Constraint Checking**: Compare your estimated output against the hard token limit

### Response Strategy Protocol

**Strategy A: Direct Response (Estimate < Limit)**
- If estimated output is safely within the token limit, proceed with generating the full response

**Strategy B: Task Decomposition (Estimate > Limit)**
- If estimated output approaches or exceeds the limit:
  1. Halt execution immediately
  2. Decompose the task into smaller, logical sub-tasks
  3. Present a step-by-step plan to the user
  4. Await explicit user approval before proceeding

### Example of Proper Task Decomposition
```
User Request: "Create a full-stack web application..."

Correct Response:
"This is a large request that will exceed my output limit. I've broken it down into:
1. Project Scaffolding & Environment Setup
2. Database Schema
3. Backend API (Node.js/Express)
4. Frontend Core Components (React)
5. State Management & API Integration

Please approve to begin with Part 1."
```

---

## Code Modification Best Practices

### Efficiency Guidelines
- **Be efficient with token usage**: When using CLI tools, only send small, relevant code snippets instead of entire files
- **Edit with caution**: Always verify changes before applying them
- **Create micro-steps**: Evaluate tasks and create detailed steps to avoid system lock-ups

### Handling Output Truncation
**Issue**: When using `read_file`, output can be truncated, preventing full content visibility.

**Solution**:
1. **Increase `limit` parameter**: Use `limit = 1000` or more for large files
2. **Verify `old_string`**: Always verify against full, untruncated content before replacements
3. **Include context**: For replace operations, include at least 3 lines before and after in `old_string`

---

## File Handling Tips

### Reading Files
- Always increase the limit parameter when reading large files or critical sections
- Verify that you have the complete content before performing operations
- Check for truncation indicators like "[File content truncated...]"

### Writing and Editing
- Never create files unless absolutely necessary
- Always prefer editing existing files over creating new ones
- Verify exact matches including all whitespace and line breaks

---

## Task Planning and Decomposition

### When to Decompose Tasks
Decompose complex requests when they involve:
- Multiple file modifications
- Large code generation requirements
- Multi-step analysis or refactoring
- Any operation that might exceed token limits

### Decomposition Best Practices
1. Break down into logical, independent sub-tasks
2. Each sub-task output must be well within token limits
3. Present clear, numbered steps to the user
4. Wait for explicit approval before proceeding

---

## Manual Code Replacement Protocol

When automated diff/patch tools fail, follow this multi-step process:

### Step 1: State the Action Clearly
Begin by stating: "Find and Delete", "Find and Replace", or "Paste New Code"

### Step 2: Provide Code to be Found/Deleted
- Provide the *exact* block of code to find
- Include all whitespace and formatting

### Step 3: Provide New Code
- Provide the complete new block of code
- Maintain consistent formatting

### Step 4: Clarify Placement and Spacing
- Explicitly state where to paste (e.g., "in the exact same spot")
- Specify if blank lines are needed

### Example Interaction
```
"To fix this, we'll need to manually replace a function.

### Step 1: Find and Delete
Please find and delete this entire function from `your_file.py`:

```python
def old_buggy_function():
    # old, buggy logic
    return False
```

### Step 2: Paste New Code
In the exact same spot where you deleted the old function, paste:

```python
def new_function_with_fix():
    # new, corrected logic
    return True
```

No extra blank line is needed."
```

---

## General Development Guidelines

### Code Quality
1. Always maintain consistent indentation and formatting
2. Preserve existing code style conventions
3. Include appropriate error handling
4. Add comments for complex logic

### Communication
1. Be clear and concise in explanations
2. Provide context for all changes
3. Explain the reasoning behind modifications
4. Alert users to potential issues or considerations

### Testing and Verification
1. Suggest testing approaches after modifications
2. Identify potential edge cases
3. Recommend verification steps
4. Highlight any breaking changes

### Documentation
1. Update relevant documentation when making changes
2. Keep README files current
3. Document new features or significant modifications
4. Maintain clear commit messages

---

## Quick Reference Checklist

Before starting any task:
- [ ] Estimate token requirements
- [ ] Check if task needs decomposition
- [ ] Verify file read limits are sufficient
- [ ] Plan the approach with micro-steps

During development:
- [ ] Use efficient token management
- [ ] Verify exact string matches for replacements
- [ ] Include sufficient context in operations
- [ ] Edit existing files rather than creating new ones

After completion:
- [ ] Verify all changes are correct
- [ ] Check for any truncated operations
- [ ] Ensure consistent formatting
- [ ] Document significant changes

---

## Tips for Common Scenarios

### Large File Modifications
- Read with increased limits first
- Break into smaller, focused edits
- Verify each change independently

### Multi-File Refactoring
- Create a clear plan upfront
- Process files systematically
- Track progress explicitly

### Complex Feature Implementation
- Decompose into logical components
- Implement incrementally
- Test each component separately

### Bug Fixes
- Understand the full context first
- Make minimal necessary changes
- Preserve existing functionality

---

This guide should be referenced regularly to ensure efficient and effective AI-assisted development on the Sales Commissions App project.