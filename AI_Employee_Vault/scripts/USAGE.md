# Action Executor - Usage Guide

## TL;DR - Quick Start (2 minutes)

```bash
# 1. Create an approval file in Approved/
cp scripts/samples/send_email_example.json Approved/my_action.json

# 2. Run the executor
python3 scripts/action_executor.py --once

# 3. Check Done/ folder - file should be there!
ls Done/
```

## What This Does

The action executor is like an "approval processor" for your AI Employee system:

1. **You** place approval files in `Approved/`
2. **Script** reads and processes each file
3. **Script** simulates executing the action (send email, create user, etc.)
4. **Script** logs everything to a file
5. **Script** moves completed files to `Done/`

## Creating Approval Files

All approval files are simple JSON with these fields:

```json
{
  "action": "TYPE_OF_ACTION",
  "recipient": "who_it_affects",
  "subject": "what_to_do",
  "content": "details",
  "timestamp": "ISO_TIMESTAMP"
}
```

### Real-World Examples

**Example 1: Send an Email**
```json
{
  "action": "send_email",
  "recipient": "newemployee@company.com",
  "subject": "Welcome!",
  "content": "Your account is ready. Your username is newemployee.",
  "timestamp": "2026-03-31T14:30:00Z"
}
```

**Example 2: Create a User**
```json
{
  "action": "create_user",
  "recipient": "bob.jones@company.com",
  "subject": "Create user account",
  "content": "Create account with Manager role in Department: Engineering",
  "timestamp": "2026-03-31T15:00:00Z"
}
```

**Example 3: Update Database**
```json
{
  "action": "update_database",
  "recipient": "production_db",
  "subject": "Update user settings",
  "content": "Set onboarding_completed=true for user_id=12345",
  "timestamp": "2026-03-31T15:30:00Z"
}
```

## Running the Script

### Continuous Mode (keeps running)
```bash
python3 scripts/action_executor.py
# Ctrl+C to stop
```

### One-Time Mode (runs once and exits)
```bash
python3 scripts/action_executor.py --once
```

## How to Add Custom Actions

Edit `scripts/action_executor.py` and find the `simulate_action()` function:

```python
def simulate_action(action_data):
    action_type = action_data.get('action', 'unknown')
    
    # Add this:
    if action_type == 'send_slack_message':
        channel = action_data.get('recipient')
        message = action_data.get('content')
        logger.info(f"📨 Sending Slack message to {channel}")
        logger.info(f"   Message: {message}")
```

Then create approval files with:
```json
{
  "action": "send_slack_message",
  "recipient": "#engineering",
  "content": "Project X is complete!"
}
```

## Key Features

| Feature | How It Works |
|---------|-------------|
| **Duplicate Prevention** | `.processed_actions.json` tracks what's been done |
| **Logging** | Every action logged to `Logs/action_executor_DATE.log` |
| **File Organization** | Processed files moved from `Approved/` to `Done/` |
| **Simple** | Pure Python, no external dependencies |
| **Safe** | Never re-executes the same file twice |

## Folder Layout

```
AI_Employee_Vault/
├── Approved/                 ← Put files HERE
├── Done/                     ← Completed files go HERE
├── Logs/                     ← Log files stored HERE
├── scripts/
│   ├── action_executor.py   ← Main script
│   ├── README.md            ← Full documentation
│   ├── USAGE.md             ← This file
│   ├── sample_approval.json ← Quick test file
│   └── samples/
│       ├── send_email_example.json
│       ├── create_user_example.json
│       └── update_database_example.json
└── .processed_actions.json  ← Duplicate tracker
```

## Common Tasks

### Test the script
```bash
cp scripts/samples/send_email_example.json Approved/test.json
python3 scripts/action_executor.py --once
ls Done/  # Should contain test.json
```

### Run in background
```bash
nohup python3 scripts/action_executor.py > action_executor.log 2>&1 &
```

### Check recent logs
```bash
tail -f Logs/action_executor_*.log
```

### See what's been processed
```bash
cat .processed_actions.json | python3 -m json.tool
```

### Clear processed history (careful!)
```bash
rm .processed_actions.json
```

## Troubleshooting

**Q: Files in Approved/ aren't being processed?**
- Make sure script is running: `python3 scripts/action_executor.py`
- Check logs in `Logs/` folder
- Ensure JSON is valid: use `python3 -m json.tool your_file.json`

**Q: Same file keeps being processed?**
- Delete `.processed_actions.json` to reset tracker
- Or restart the script

**Q: Want to extend with real actions?**
- Edit `simulate_action()` function to call real APIs
- Example: replace logging with actual email sending
- Keep the logging lines for debugging!

## Next Steps

1. ✓ Run your first test with samples
2. ✓ Create your own approval files
3. ✓ Add custom action types for your needs
4. ✓ Integrate with your AI Employee workflow
