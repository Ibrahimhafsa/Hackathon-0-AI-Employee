# Email: Sample Email Task

## How to Use Email Tasks (Gold Tier)

Email tasks are simple to create! Follow this format:

### File Naming
- Start with `EMAIL_` prefix
- Use descriptive name (e.g., `EMAIL_welcome_001.md`)
- Save to `Needs_Action/` folder

### Required Fields
Each email must include:
- **To:** recipient email address
- **Subject:** email subject line
- **Email Body:** the message content

### Optional Fields
- **CC:** carbon copy recipients (comma-separated)
- **BCC:** blind carbon copy recipients (comma-separated)
- **Priority:** Normal, High, or Low

### Example Task

```markdown
# Email: Welcome Message

**To:** user@company.com
**Subject:** Welcome to Our Service!
**CC:** admin@company.com
**BCC:** none
**Priority:** Normal

## Email Body

Dear User,

Welcome! We're glad to have you.

Key information:
- Account created successfully
- Password reset link sent to your email
- Support team available 24/7

Best regards,
Support Team
```

## How It Works

1. **Create**: Place your email task file in `Needs_Action/`
2. **Detect**: Email Generator monitors and finds your file
3. **Approve**: An approval file is created in `Pending_Approval/`
4. **Review**: Open and review the email in the approval file
5. **Accept**: Move file to `Approved/` folder
6. **Execute**: Action Executor logs the email (DRY RUN - no actual send)
7. **Done**: File moves to `Done/` folder

## DRY RUN Mode

Gold Tier runs in **DRY RUN mode**, meaning:
- ✅ Emails are generated and logged
- ✅ Full email content is recorded
- ✅ Approval workflow is tested
- ❌ No actual emails are sent
- ❌ Recipients don't receive messages

This is perfect for testing and learning without sending real emails!

## Logs

All email processing is logged to `Logs/email_generator_*.log` and `Logs/action_executor_*.log`

View logs to see:
- Detected email tasks
- Generated approval requests
- Simulated email sends
- Full email content that was "sent"

---
Created for AI Employee Vault - Gold Tier Email Integration
