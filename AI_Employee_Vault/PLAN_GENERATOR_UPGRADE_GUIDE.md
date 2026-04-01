# Plan Generator Upgrade Guide
## Multi-Task-Type Support (Silver+ Tier)

**Date:** April 1, 2026  
**Status:** ✅ COMPLETE & VERIFIED  
**Compatibility:** Silver Tier and above

---

## Overview

The Plan Generator has been upgraded to **detect task types automatically** and generate **type-specific execution plans** with customized checklists.

### What This Means

Instead of generic "Review requirements → Do work → Get approval" steps, plans now include:

- **Email Tasks** → Email-specific steps (draft, verify recipients, send, etc.)
- **Social Media Tasks** → Content creation steps (research, draft, hashtags, etc.)
- **General Tasks** → Standard workflow steps (as before)

---

## How It Works

### 1. Task Type Detection

When a task file is analyzed, the Plan Generator reads its content and detects the task type:

```
Content Analysis:
├─ Contains "email" keyword? → Email Task
├─ Contains "post", "social", or "tweet"? → Social Media Task
└─ Otherwise → General Task
```

**Case-insensitive matching** on the entire task content.

### 2. Dynamic Plan Generation

Based on the detected type, the generator creates customized steps:

**Email Task Plan Example:**
```
## Step-by-Step Checklist

- [ ] Review email task requirements
- [ ] Draft email content and subject line
- [ ] Identify recipient(s) and verify email addresses
- [ ] Check for CC/BCC if applicable
- [ ] Review email for tone and completeness
- [ ] Verify all details are accurate
- [ ] Prepare email for sending
- [ ] Obtain approval from stakeholder
- [ ] Send email or move to Approved folder
- [ ] Document send timestamp and recipient confirmation
- [ ] Mark task as complete
```

**Social Media Task Plan Example:**
```
## Step-by-Step Checklist

- [ ] Review social media task requirements
- [ ] Research topic and gather content
- [ ] Draft post content and captions
- [ ] Select appropriate hashtags and mentions
- [ ] Add media (images, videos, links) if needed
- [ ] Review for brand consistency and tone
- [ ] Check for spelling, grammar, and clarity
- [ ] Preview post on target platform
- [ ] Obtain approval from stakeholder
- [ ] Schedule or publish post
- [ ] Monitor engagement and comments
- [ ] Mark task as complete
```

### 3. Enhanced Plan Template

Plans now include a **Task Type field**:

```markdown
# Plan: Your Task Title

**Created:** 2026-04-01T12:00:00.000000
**Status:** pending
**Priority:** Normal
**Task Type:** Email Task           ← NEW FIELD

## Objective
...

## Task Information
- **Original Task:** ...
- **From:** ...
- **Priority:** ...
- **Task Type:** Email Task         ← ALSO HERE
```

---

## Code Changes

### New Methods

#### `_detect_task_type(content)`
Analyzes content and returns one of:
- `'email_task'`
- `'social_media_task'`
- `'general_task'`

```python
def _detect_task_type(self, content):
    content_lower = content.lower()
    if 'email' in content_lower:
        return 'email_task'
    if 'post' in content_lower or 'social' in content_lower or 'tweet' in content_lower:
        return 'social_media_task'
    return 'general_task'
```

#### `_format_task_type(task_type)`
Converts machine-readable type to human-readable format:
- `'email_task'` → `'Email Task'`
- `'social_media_task'` → `'Social Media Task'`
- `'general_task'` → `'General Task'`

### Enhanced Methods

#### `_extract_task_info(content)` 
Now returns task_type in the dictionary:
```python
{
    'title': '...',
    'description': '...',
    'sender': '...',
    'priority': '...',
    'task_type': 'email_task'    # ← NEW
}
```

#### `_generate_steps(task_type, description)`
Now accepts `task_type` parameter and generates appropriate steps:
- Email tasks: 11 email-specific steps
- Social media tasks: 12 content creation steps
- General tasks: 10 standard workflow steps

#### `_generate_plan_content(task_info)`
Now includes task_type field in the generated plan and uses task_type for step generation.

#### `_create_plan(file_path, task_info)`
Now logs the detected task type when creating plans:
```
→ Plan created: PLAN_TASK_name.md
→ Task Type: Email Task
→ Status: pending
```

---

## Usage Examples

### Example 1: Email Task

**File:** `Needs_Action/TASK_send_newsletter.md`
```markdown
# Send Monthly Newsletter

## Task Description

Send our monthly newsletter to all subscribers with latest product updates.

**From:** Marketing Team  
**Priority:** Normal  

The email should include feature highlights and upcoming events.
```

**Generated Plan Will Include:**
- Task Type: Email Task
- Email-specific checklist (draft content, verify recipients, etc.)
- Steps for preparing email for sending

### Example 2: Social Media Task

**File:** `Needs_Action/TASK_twitter_campaign.md`
```markdown
# Launch Twitter Campaign

## Task Description

Create and post engaging tweets about our new feature with relevant hashtags.

**From:** Social Media  
**Priority:** High  

Post should drive traffic to announcement page.
```

**Generated Plan Will Include:**
- Task Type: Social Media Task
- Content creation steps (research, draft, hashtags, media, etc.)
- Steps for scheduling/publishing

### Example 3: General Task

**File:** `Needs_Action/TASK_code_review.md`
```markdown
# Code Review Process

## Task Description

Review pending pull requests and provide feedback.

**From:** Engineering  
**Priority:** Medium  

Focus on code quality and architecture.
```

**Generated Plan Will Include:**
- Task Type: General Task
- Standard workflow steps (review, analyze, document, etc.)
- Generic checklist suitable for any task

---

## Backward Compatibility

✅ **Fully backward compatible**

- Existing task files continue to work
- Old plans are unaffected
- Default behavior (general_task) for untyped tasks
- No breaking changes to API or file formats

---

## Benefits

### 1. Better Guidance
Users get specific, actionable steps for their task type instead of generic guidance.

### 2. Improved Quality
Task-specific checklists ensure all important steps are covered.

### 3. Faster Execution
Developers can follow optimized workflows for their specific task type.

### 4. Clear Classification
Task type is immediately visible in the plan document.

### 5. Easy Tracking
Task type information enables better reporting and analysis.

---

## Testing

The upgrade has been verified with three types of tasks:

```
✅ Email Task Detection
   Content: "Send a weekly email to customers"
   Detected: email_task
   Steps generated: 11 email-specific steps

✅ Social Media Task Detection  
   Content: "Create a Twitter post with hashtags"
   Detected: social_media_task
   Steps generated: 12 social media steps

✅ General Task Detection
   Content: "Optimize database queries"
   Detected: general_task
   Steps generated: 10 standard steps
```

---

## Implementation Details

### Detection Keywords

**Email Tasks:**
- "email" (case-insensitive)

**Social Media Tasks:**
- "post" (case-insensitive)
- "social" (case-insensitive)
- "tweet" (case-insensitive)

**General Tasks:**
- Default fallback for any other content

### Step Generation

Steps are customized based on the task type but maintain consistent structure:
- All steps use checkbox format: `- [ ]`
- All steps are action-oriented
- All steps progress logically from start to finish
- All include approval step
- All include completion step

### Type Display

Machine-readable types are converted to human-readable format:
- `email_task` → "Email Task"
- `social_media_task` → "Social Media Task"  
- `general_task` → "General Task"

---

## Configuration

No configuration needed. The detection is automatic and built-in.

To modify detection keywords or add new task types, edit the `_detect_task_type()` method in `scripts/plan_generator.py`.

---

## Future Enhancements

Potential upgrades:

### Platinum Tier (Potential)
- Machine learning-based task classification
- Custom task type definitions
- User-configurable detection keywords
- Task type-specific execution templates
- Analytics by task type

### Integration
- Task type reporting and metrics
- Workflow optimization by type
- Integration with other modules
- Template library for each task type

---

## Summary

**What Changed:**
- Added automatic task type detection (email, social media, general)
- Added dynamic step generation based on task type
- Enhanced plan template with task type field
- Improved plan logging with type information

**What Stayed the Same:**
- File structure and naming conventions
- Approval workflow
- General system architecture
- Silver Tier features and compatibility

**Result:**
Plans are now more targeted, specific, and actionable for each task type.

---

## Quick Reference

### For Task Creators

1. Create task files as usual in `Needs_Action/`
2. No special naming or format needed
3. Plan Generator automatically detects type
4. Check the generated plan to see the detected type
5. Follow the type-specific checklist

### For System Administrators

The upgrade requires no configuration or setup:
- All detection is automatic
- Backward compatible with existing tasks
- No database changes
- No new dependencies
- Works with all existing modules

### For Developers

New methods available in `PlanGenerator` class:
- `_detect_task_type(content)` - Detect task type
- `_format_task_type(task_type)` - Format for display
- Updated `_generate_steps()` - Now type-aware
- Updated `_extract_task_info()` - Now includes task_type
- Updated `_generate_plan_content()` - Now type-aware

---

*Plan Generator Upgrade - April 1, 2026*  
*Multi-Task-Type Support with Dynamic Step Generation*  
*Status: Production Ready ✅*
