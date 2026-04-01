# Action Executor - MCP-like Script

A simple Python script that monitors the `Approved/` folder and processes approval files, simulating actions like sending emails or creating users.

## Features

✓ **File Monitoring** - Continuously watches the `Approved/` folder for new files
✓ **Action Simulation** - Simulates performing actions (emails, user creation, etc.)
✓ **Duplicate Prevention** - Tracks processed files to avoid re-execution
✓ **Logging** - Comprehensive logging to both console and file
✓ **File Organization** - Moves processed files to `Done/` folder
✓ **Simple & Beginner-Friendly** - Clean code, easy to understand and extend

## Quick Start

### Run in continuous monitoring mode:
```bash
python3 scripts/action_executor.py
```

### Run once and exit:
```bash
python3 scripts/action_executor.py --once
```

## Approval File Format

Create JSON files in the `Approved/` folder with this structure:

```json
{
  "action": "send_email",
  "recipient": "user@company.com",
  "subject": "Email Subject",
  "content": "Email body content",
  "timestamp": "2026-03-31T10:30:00Z"
}
```

### Supported Actions

- `send_email` - Simulate sending an email
- `create_user` - Simulate creating a new user
- `update_database` - Simulate database updates
- Any custom action type (will be logged with a generic message)

## Folder Structure

```
AI_Employee_Vault/
├── Approved/           # ← Put approval files here
├── Done/               # ← Processed files moved here
├── Logs/               # ← Log files stored here
└── scripts/
    ├── action_executor.py
    ├── sample_approval.json
    └── README.md
```

## How It Works

1. **Monitor** - Script checks `Approved/` folder every 2 seconds
2. **Read** - Loads JSON approval file
3. **Execute** - Simulates the action and logs details
4. **Move** - Transfers file to `Done/` folder
5. **Track** - Records processed file in `.processed_actions.json` to prevent duplicates

## Testing

Test with the sample file:

```bash
# Copy sample to Approved folder
cp scripts/sample_approval.json Approved/

# Run once
python3 scripts/action_executor.py --once
```

## Log Files

- **Console Output** - Real-time processing details
- **File Logs** - Stored in `Logs/action_executor_YYYYMMDD_HHMMSS.log`
- **Processed Tracker** - `.processed_actions.json` tracks completed files

## Example Output

```
2026-03-31 10:30:45,123 - INFO - Starting action executor...
2026-03-31 10:30:45,124 - INFO - Monitoring: Approved/
2026-03-31 10:30:45,125 - INFO - Found 1 file(s) in Approved/
2026-03-31 10:30:45,126 - INFO - ============================================================
2026-03-31 10:30:45,127 - INFO - Processing: sample_approval.json
2026-03-31 10:30:45,128 - INFO - 🚀 Executing action: send_email
2026-03-31 10:30:45,129 - INFO -    Recipient: john.doe@company.com
2026-03-31 10:30:45,130 - INFO -    ✉️  Simulating email to john.doe@company.com
2026-03-31 10:30:45,131 - INFO -    ✓ Action completed successfully
2026-03-31 10:30:45,132 - INFO - ✓ Moved to Done/: sample_approval.json
```

## Customization

To add custom actions, modify the `simulate_action()` function:

```python
def simulate_action(action_data):
    action_type = action_data.get('action', 'unknown')
    
    if action_type == 'my_custom_action':
        logger.info(f"Executing custom action...")
        # Add your logic here
```

## Notes

- Script uses JSON for approval files (easy to parse and read)
- Duplicate prevention uses file names - ensure unique filenames
- Polling interval is 2 seconds (can be adjusted)
- Press Ctrl+C to gracefully stop monitoring
