#!/usr/bin/env python3
"""
Simple MCP-like action executor script.
Monitors the Approved/ folder and processes approval files.
"""

import os
import json
import time
import shutil
import logging
from datetime import datetime
from pathlib import Path

# Configuration
APPROVED_FOLDER = "Approved"
DONE_FOLDER = "Done"
LOGS_FOLDER = "Logs"
PROCESSED_LOG = ".processed_actions.json"

# Setup logging
log_filename = os.path.join(LOGS_FOLDER, f"action_executor_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def load_processed_files():
    """Load set of already processed files to avoid duplicates."""
    if os.path.exists(PROCESSED_LOG):
        try:
            with open(PROCESSED_LOG, 'r') as f:
                data = json.load(f)
                return set(data.get('processed', []))
        except Exception as e:
            logger.warning(f"Could not load processed log: {e}")
    return set()


def save_processed_files(processed_set):
    """Save processed files to prevent re-execution."""
    try:
        with open(PROCESSED_LOG, 'w') as f:
            json.dump({'processed': list(processed_set)}, f, indent=2)
    except Exception as e:
        logger.error(f"Could not save processed log: {e}")


def read_approval_file(filepath):
    """Read and parse approval file."""
    try:
        with open(filepath, 'r') as f:
            if filepath.endswith('.json'):
                return json.load(f)
            else:
                return {'content': f.read(), 'type': 'text'}
    except Exception as e:
        logger.error(f"Error reading file {filepath}: {e}")
        return None


def simulate_action(action_data):
    """Simulate performing the action (e.g., sending email, creating user, etc)."""
    action_type = action_data.get('action', 'unknown')
    recipient = action_data.get('recipient', 'N/A')
    subject = action_data.get('subject', 'No subject')
    content = action_data.get('content', 'No content')
    mode = action_data.get('mode', 'NORMAL')

    logger.info(f"🚀 Executing action: {action_type}")
    if mode == 'DRY_RUN':
        logger.info(f"   [DRY RUN MODE] No actual action will be performed")
    logger.info(f"   Recipient: {recipient}")
    logger.info(f"   Subject: {subject}")
    logger.info(f"   Content preview: {content[:100]}...")

    # Simulate different actions
    if action_type == 'send_email':
        logger.info(f"   ✉️  {'[DRY RUN] Would send' if mode == 'DRY_RUN' else 'Sending'} email to {recipient}")
        # Enhanced email logging
        body = action_data.get('body', content)
        cc = action_data.get('cc', '')
        bcc = action_data.get('bcc', '')
        email_from = action_data.get('from', 'system@ai_employee_vault')
        priority = action_data.get('priority', 'Normal')

        logger.info(f"      From: {email_from}")
        if cc:
            logger.info(f"      CC: {cc}")
        if bcc:
            logger.info(f"      BCC: {bcc}")
        logger.info(f"      Priority: {priority}")
        logger.info(f"      Full body:\n{_format_email_body(body)}")
    elif action_type == 'create_user':
        logger.info(f"   👤 Simulating user creation for: {recipient}")
    elif action_type == 'update_database':
        logger.info(f"   🗄️  Simulating database update: {subject}")
    else:
        logger.info(f"   ⚙️  Simulating generic action: {subject}")

    # Success simulation
    logger.info(f"   ✓ Action completed successfully")
    return True


def _format_email_body(body):
    """Format email body for logging with proper indentation."""
    lines = body.split('\n')
    formatted = '\n'.join(f"         {line}" for line in lines)
    return formatted


def process_file(filename, approved_path):
    """Process a single approval file."""
    logger.info(f"\n{'='*60}")
    logger.info(f"Processing: {filename}")
    logger.info(f"{'='*60}")

    # Read the approval file
    action_data = read_approval_file(approved_path)
    if not action_data:
        logger.error(f"Failed to read approval file: {filename}")
        return False

    logger.info(f"File content loaded: {json.dumps(action_data, indent=2)}")

    # Simulate performing the action
    try:
        success = simulate_action(action_data)
        if not success:
            logger.error(f"Action failed for {filename}")
            return False
    except Exception as e:
        logger.error(f"Exception during action simulation: {e}")
        return False

    # Move file to Done/ folder
    try:
        done_path = os.path.join(DONE_FOLDER, filename)
        shutil.move(approved_path, done_path)
        logger.info(f"✓ Moved to Done/: {filename}")
        return True
    except Exception as e:
        logger.error(f"Failed to move file to Done/: {e}")
        return False


def monitor_folder(poll_interval=2, single_run=False):
    """Monitor Approved/ folder for new files."""
    logger.info("Starting action executor...")
    logger.info(f"Monitoring: {APPROVED_FOLDER}/")
    logger.info(f"Processed files log: {PROCESSED_LOG}")

    # Load previously processed files
    processed_files = load_processed_files()
    logger.info(f"Loaded {len(processed_files)} previously processed files")

    # Ensure folders exist
    os.makedirs(APPROVED_FOLDER, exist_ok=True)
    os.makedirs(DONE_FOLDER, exist_ok=True)
    os.makedirs(LOGS_FOLDER, exist_ok=True)

    try:
        iteration = 0
        while True:
            iteration += 1
            logger.debug(f"[Iteration {iteration}] Checking for new files...")

            # Get list of files in Approved/
            try:
                files = os.listdir(APPROVED_FOLDER)
            except FileNotFoundError:
                logger.warning(f"{APPROVED_FOLDER} folder not found")
                files = []

            # Filter out hidden/metadata files
            files = [f for f in files if not f.startswith('.') and os.path.isfile(os.path.join(APPROVED_FOLDER, f))]

            if files:
                logger.info(f"Found {len(files)} file(s) in Approved/")

            # Process new files
            for filename in files:
                if filename not in processed_files:
                    approved_path = os.path.join(APPROVED_FOLDER, filename)

                    # Process the file
                    if process_file(filename, approved_path):
                        processed_files.add(filename)
                        save_processed_files(processed_files)
                        logger.info(f"✓ Successfully processed and logged: {filename}\n")
                    else:
                        logger.warning(f"⚠ Failed to process: {filename}\n")
                else:
                    logger.debug(f"Skipping already processed file: {filename}")

            # Exit if single run mode
            if single_run:
                break

            # Wait before next check
            time.sleep(poll_interval)

    except KeyboardInterrupt:
        logger.info("\nShutting down...")
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
    finally:
        logger.info("Action executor stopped")


if __name__ == "__main__":
    import sys

    # Support --once flag for single run
    single_run = "--once" in sys.argv

    if single_run:
        logger.info("Running in single-pass mode (--once)")
        monitor_folder(single_run=True)
    else:
        logger.info("Running in continuous monitoring mode (Ctrl+C to stop)")
        monitor_folder()
