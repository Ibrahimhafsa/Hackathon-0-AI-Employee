# SKILL: Basic Vault Operations

**Tier**: Bronze
**Version**: 1.0
**Last Updated**: 2026-03-27

## Overview
Core operations for managing the AI Employee vault. These are fundamental actions required for daily task management and workflow organization.

---

## 1. List All Files in Needs_Action Folder

### Purpose
Display all pending tasks and items requiring action.

### Steps
1. Navigate to the `Needs_Action` folder in your vault
2. View all .md files in the folder
3. Note the filename and any metadata

### Expected Output
A list of all markdown files that contain tasks waiting to be processed.

### Example
```
Needs_Action/
  - task_client_email.md
  - task_budget_review.md
  - task_approve_invoice.md
```

---

## 2. Read Any .md File Content

### Purpose
Display the full content of a markdown file to review its details.

### Steps
1. Identify the file path (e.g., `Needs_Action/task_name.md`)
2. Open the file in your editor or vault viewer
3. Read the complete content line by line
4. Note any important information, dates, amounts, or decisions needed

### Expected Output
Full markdown content with all headings, checkboxes, and text visible.

### Example
```
# Task: Client Email Response
Status: Pending
Priority: High
Content: Detailed task information...
```

---

## 3. Create a New Plan.md File with Checkboxes

### Purpose
Create a structured plan document with trackable action items.

### Steps
1. Navigate to the `Plans` folder
2. Create a new file named `Plan_[description]_[date].md`
3. Add the following structure:
   ```markdown
   # Plan: [Plan Name]

   **Created**: [Date]
   **Status**: Active

   ## Objectives
   - [Main goal 1]
   - [Main goal 2]

   ## Action Items
   - [ ] Task 1
   - [ ] Task 2
   - [ ] Task 3

   ## Timeline
   - [Milestone 1]: [Date]
   - [Milestone 2]: [Date]
   ```
4. Save the file

### Expected Output
A new .md file in the Plans folder with checkbox-based action items ready to track.

---

## 4. Move Files from Needs_Action to Done Folder

### Purpose
Archive completed tasks and maintain a record of finished work.

### Steps
1. Identify the completed task file in `Needs_Action` folder
2. Ensure the file is finalized and no further action is needed
3. Move the file from `Needs_Action/` to `Done/` folder
4. Optionally add a completion note (date, outcome)
5. Verify the file is no longer in `Needs_Action`

### Expected Output
The file is now located in the `Done` folder and removed from `Needs_Action`.

### Example
```
Before:  Needs_Action/task_email.md
After:   Done/task_email.md
```

---

## Success Criteria
✓ Can list all items in Needs_Action
✓ Can read any .md file content completely
✓ Can create a Plan.md with proper checkbox syntax
✓ Can move completed tasks to Done folder

## Notes
- Always verify operations are complete before marking tasks as done
- Keep file names descriptive and date-stamped when relevant
- Maintain the folder structure consistently
