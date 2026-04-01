# Gold Tier Email Integration - Quick Start Guide

## Overview

Gold Tier adds **Email Task Support** to your AI Employee system. Create email tasks, get them approved, and watch them get logged (DRY RUN mode - no actual sends).

## Quick Start (5 minutes)

### 1. Start the Email Generator
```bash
python3 scripts/email_generator.py
```

You'll see:
```
EMAIL GENERATOR STARTED (GOLD TIER - DRY RUN MODE)
Watching directory: .../Needs_Action
✅ Generator is running. Waiting for email tasks...
```

### 2. Create an Email Task
Create file: `Needs_Action/EMAIL_hello_001.md`

```markdown
# Email: Send Hello

**To:** recipient@company.com
**Subject:** Hello from AI Employee!
**Priority:** Normal

## Email Body

Hi there,

This is an automated email from the AI Employee system.

Best regards,
Your AI Assistant
```

### 3. Watch It Get Detected
In your email generator terminal:
```
📧 Email task detected: EMAIL_hello_001.md
✅ Email approval created: EMAIL_APPROVAL_EMAIL_hello_001.json
→ To: recipient@company.com
→ Subject: Hello from AI Employee!
→ Mode: DRY RUN (will not actually send)
```

### 4. Review the Approval
```bash
cat Pending_Approval/EMAIL_APPROVAL_EMAIL_hello_001.json
```

You'll see all email details in JSON format.

### 5. Approve the Email
```bash
# Move to Approved folder to approve
mv Pending_Approval/EMAIL_APPROVAL_EMAIL_hello_001.json Approved/
```

### 6. Execute (Simulate Send)
```bash
python3 scripts/action_executor.py --once
```

Output:
```
🚀 Executing action: send_email
   [DRY RUN MODE] No actual action will be performed
   Recipient: recipient@company.com
   Subject: Hello from AI Employee!
   From: system@ai_employee_vault
   Full body:
      Hi there,
      
      This is an automated email from the AI Employee system.
      ...
   ✓ Action completed successfully
```

### 7. Check the Log
```bash
tail -30 Logs/action_executor_*.log
```

See the full email that was "sent"!

---

## Email Task Format

### Required Fields
```markdown
**To:** recipient@company.com
**Subject:** Email subject line

## Email Body
Your message here...
```

### Optional Fields
```markdown
**CC:** cc@company.com
**BCC:** bcc@company.com
**Priority:** Normal | High | Low
```

### Complete Example
```markdown
# Email: Welcome New Employee

**To:** newemployee@company.com
**Subject:** Welcome to the Team!
**CC:** manager@company.com
**BCC:** none
**Priority:** High

## Email Body

Dear New Employee,

Welcome aboard! We're excited to have you on the team.

Your onboarding checklist:
- [ ] IT setup and hardware
- [ ] Email configured
- [ ] Team introduction
- [ ] First project assignment

Let me know if you need anything!

Best,
HR Team
```

---

## File Naming

**Important:** Email tasks MUST start with `EMAIL_`

✅ Good:
- `EMAIL_welcome_001.md`
- `EMAIL_meeting_reminder.md`
- `EMAIL_new_user.md`

❌ Bad:
- `email_welcome_001.md` (lowercase)
- `WELCOME_001.md` (no EMAIL_ prefix)
- `EMAIL_welcome_001.txt` (wrong extension)

---

## Workflow Steps

```
1. Create file: Needs_Action/EMAIL_*.md
   ↓
2. Email Generator detects file
   ↓
3. Creates: Pending_Approval/EMAIL_APPROVAL_*.json
   ↓
4. YOU review and approve
   ↓
5. Move to: Approved/
   ↓
6. Action Executor simulates send
   ↓
7. Logs to: Logs/action_executor_*.log
   ↓
8. Moves to: Done/
```

---

## Running Everything Together

### Terminal 1: Plan Generator (Silver Tier)
```bash
python3 scripts/plan_generator.py
```

### Terminal 2: Approval Manager (Silver Tier)
```bash
python3 scripts/approval_manager.py
```

### Terminal 3: Email Generator (Gold Tier) ← NEW
```bash
python3 scripts/email_generator.py
```

### Terminal 4: Action Executor (All Tiers)
```bash
python3 scripts/action_executor.py
```

Now you have the complete AI Employee system running!

---

## DRY RUN Mode

**DRY RUN = Safe Testing Mode**

What happens:
- ✅ Email tasks are created and tracked
- ✅ Approval requests are generated
- ✅ Full email content is logged
- ❌ NO actual emails are sent
- ❌ Recipients never see messages

Why use it:
- Test email workflow safely
- Learn system without side effects
- Development and staging use
- Build confidence before real sends

---

## Checking Results

### See Generated Approvals
```bash
ls Pending_Approval/EMAIL_APPROVAL_*.json
```

### View Email Approval Details
```bash
cat Pending_Approval/EMAIL_APPROVAL_EMAIL_welcome_001.json
```

### Check Execution Logs
```bash
# Latest action executor log
tail -50 Logs/action_executor_*.log

# Search for email sends
grep "send_email" Logs/action_executor_*.log

# Search for specific recipient
grep "recipient@company.com" Logs/action_executor_*.log
```

### View Completed Tasks
```bash
ls Done/EMAIL_APPROVAL_*.json
```

---

## Troubleshooting

### "No approvals created"
1. Check filename: must start with `EMAIL_`
2. Check extension: must be `.md`
3. Check email generator is running
4. Wait a few seconds (polling interval)
5. Check log: `tail Logs/email_generator_*.log`

### "Invalid email: Missing X"
- Make sure you have `**To:**` field
- Make sure you have `**Subject:**` field
- Make sure you have `## Email Body` section

### "Email not executing"
- Check action executor is running
- Check file is in `Approved/` folder (not `Pending_Approval/`)
- Check JSON format is valid
- Run with `--once` flag manually

### Checking Logs
```bash
# Email generator log
ls -lt Logs/email_generator_*.log | head -1 | awk '{print $NF}' | xargs tail -50

# Action executor log
ls -lt Logs/action_executor_*.log | head -1 | awk '{print $NF}' | xargs tail -50
```

---

## Example Tasks

### 1. Welcome Email
```markdown
# Email: Welcome New Hire

**To:** newhire@company.com
**Subject:** Welcome to Company ABC!
**CC:** manager@company.com
**Priority:** High

## Email Body

Dear New Hire,

Welcome! We're thrilled to have you join our team.

Important info:
- First day: Monday, 9 AM in Building A
- Bring: ID and signed paperwork
- Questions: HR_Team@company.com

See you soon!

Human Resources
```

### 2. Meeting Reminder
```markdown
# Email: Team Meeting Reminder

**To:** team@company.com
**Subject:** Important: Team Sync Tomorrow 2 PM

## Email Body

Hi Team,

Reminder about tomorrow's team sync:
- Time: 2 PM
- Location: Conference Room B
- Topics: Q2 planning, project updates

See you there!
```

### 3. Status Update
```markdown
# Email: Project Status

**To:** stakeholders@company.com
**CC:** management@company.com
**Subject:** Project Update - 75% Complete
**Priority:** High

## Email Body

Project Status Update:

Current Progress: 75%

Completed:
- Design phase ✓
- Development phase ✓
- Initial testing ✓

Next Steps:
- UAT phase (next week)
- Final bug fixes
- Production deployment (week of April 15)

On track for schedule!
```

---

## Tips & Best Practices

### Tip 1: Test First
Create test emails to yourself before sending real ones.

### Tip 2: CC Approvers
CC your manager or approver so they see what was sent.

### Tip 3: Use Priorities
Mark urgent emails as `Priority: High`.

### Tip 4: Clear Subject Lines
Be specific: "Good: Project Kickoff Meeting Monday" vs "Bad: Meeting"

### Tip 5: Professional Body
Remember, these logs are auditable - write professional content.

### Tip 6: Check Logs
Always verify what was "sent" in the logs.

---

## Next Steps

1. ✅ Start email generator
2. ✅ Create EMAIL_*.md task
3. ✅ Review approval JSON
4. ✅ Move to Approved/
5. ✅ Run executor
6. ✅ Check logs

Then explore:
- Multiple emails at once
- Different priorities
- CC/BCC recipients
- Longer email content
- Integration with other components

---

## Need Help?

Check these files:
- `GOLD_COMPLETION_REPORT.md` - Full documentation
- `scripts/samples/EMAIL_sample_001.md` - Detailed examples
- `Logs/email_generator_*.log` - Debug info
- `Logs/action_executor_*.log` - Execution details

---

**Gold Tier Email Integration - Ready to use!**

Start by running the email generator and creating your first email task. Happy automating!
