#!/usr/bin/env python3
"""
Email Generator for AI_Employee_Vault - Gold Tier
Monitors Needs_Action/ folder and creates email approval requests
DRY RUN MODE: No actual emails sent, only logged and approved
"""

import os
import sys
import json
import logging
import time
import re
from pathlib import Path
from datetime import datetime
from watchdog.observers.polling import PollingObserver
from watchdog.events import FileSystemEventHandler


# Setup logging
def setup_logging():
    """Configure logging to file and console"""
    log_dir = Path(__file__).parent.parent / "Logs"
    log_dir.mkdir(exist_ok=True)

    log_file = log_dir / f"email_generator_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )

    logger = logging.getLogger(__name__)
    logger.info("=" * 80)
    logger.info("EMAIL GENERATOR STARTED (GOLD TIER - DRY RUN MODE)")
    logger.info(f"Log file: {log_file}")
    logger.info("=" * 80)

    return logger


class EmailGenerator(FileSystemEventHandler):
    """Monitor Needs_Action/ folder and generate email approval requests"""

    def __init__(self, logger, base_path):
        self.logger = logger
        self.base_path = base_path
        self.watch_dir = base_path / "Needs_Action"
        self.approval_dir = base_path / "Pending_Approval"
        self.approval_dir.mkdir(exist_ok=True)
        self.processed_files = set()
        self._load_existing_emails()

    def _load_existing_emails(self):
        """Load list of existing email approvals to avoid recreating them"""
        if self.approval_dir.exists():
            for approval_file in self.approval_dir.glob("EMAIL_APPROVAL_*.json"):
                # Extract the original filename from approval filename
                # EMAIL_APPROVAL_EMAIL_task_001.json -> EMAIL_task_001.md
                match = re.search(r'EMAIL_APPROVAL_(.+)\.json', approval_file.name)
                if match:
                    original_name = match.group(1) + ".md"
                    self.processed_files.add(original_name)
                    self.logger.debug(f"Loaded existing email approval: {original_name}")

    def on_created(self, event):
        """Handle file creation events"""
        if event.is_directory:
            return

        file_path = Path(event.src_path)

        # Skip hidden files and metadata files
        if file_path.name.startswith('.') or '_metadata.md' in file_path.name:
            return

        # Only process .md files that start with EMAIL_
        if not file_path.name.startswith('EMAIL_') or file_path.suffix != '.md':
            return

        # Avoid processing the same file twice
        if file_path.name in self.processed_files:
            self.logger.debug(f"Email approval already exists for: {file_path.name}")
            return

        self.logger.info(f"📧 Email task detected: {file_path.name}")
        self.processed_files.add(file_path.name)
        self._generate_email_approval(file_path)

    def _read_task_file(self, file_path):
        """Read and parse task file"""
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            return content
        except Exception as e:
            self.logger.warning(f"⚠️  Could not read task file: {str(e)}")
            return None

    def _extract_email_info(self, content):
        """Extract email information from file content"""
        email_info = {
            'to': '',
            'subject': '',
            'body': '',
            'from': 'AI_Employee_Vault',
            'cc': '',
            'bcc': '',
            'priority': 'Normal'
        }

        # Extract recipient (To:)
        to_match = re.search(r'\*\*To:\*\*\s*(.+?)(?:\n|$)', content)
        if to_match:
            email_info['to'] = to_match.group(1).strip()

        # Extract subject
        subject_match = re.search(r'\*\*Subject:\*\*\s*(.+?)(?:\n|$)', content)
        if subject_match:
            email_info['subject'] = subject_match.group(1).strip()

        # Extract body
        body_match = re.search(r'## Email Body\n(.+?)(?=\n##|\*\*|\Z)', content, re.DOTALL)
        if body_match:
            email_info['body'] = body_match.group(1).strip()
        else:
            # Fallback: look for any content after Subject
            body_match = re.search(r'\*\*Subject:\*\*.*?\n(.+?)(?:\n##|\Z)', content, re.DOTALL)
            if body_match:
                email_info['body'] = body_match.group(1).strip()

        # Extract CC
        cc_match = re.search(r'\*\*CC:\*\*\s*(.+?)(?:\n|$)', content)
        if cc_match:
            cc_value = cc_match.group(1).strip()
            if cc_value.lower() != 'none' and cc_value:
                email_info['cc'] = cc_value

        # Extract BCC
        bcc_match = re.search(r'\*\*BCC:\*\*\s*(.+?)(?:\n|$)', content)
        if bcc_match:
            bcc_value = bcc_match.group(1).strip()
            if bcc_value.lower() != 'none' and bcc_value:
                email_info['bcc'] = bcc_value

        # Extract priority
        priority_match = re.search(r'\*\*Priority:\*\*\s*(.+?)(?:\n|$)', content)
        if priority_match:
            email_info['priority'] = priority_match.group(1).strip()

        return email_info

    def _validate_email_info(self, email_info):
        """Validate that email has required fields"""
        if not email_info['to']:
            return False, "Missing recipient (To:)"
        if not email_info['subject']:
            return False, "Missing subject"
        if not email_info['body']:
            return False, "Missing email body"
        return True, "Valid"

    def _create_email_approval(self, file_path, email_info):
        """Create an email approval request JSON file"""
        try:
            # Validate email info
            is_valid, message = self._validate_email_info(email_info)
            if not is_valid:
                self.logger.error(f"   ❌ Invalid email: {message}")
                return False

            # Create approval filename
            # EMAIL_task_001.md -> EMAIL_APPROVAL_EMAIL_task_001.json
            approval_filename = f"EMAIL_APPROVAL_{file_path.stem}.json"
            approval_file = self.approval_dir / approval_filename

            # Ensure no conflicts
            if approval_file.exists():
                self.logger.warning(f"Email approval already exists: {approval_filename}")
                return False

            # Create approval data
            approval_data = {
                'action': 'send_email',
                'type': 'email',
                'recipient': email_info['to'],
                'to': email_info['to'],
                'cc': email_info['cc'],
                'bcc': email_info['bcc'],
                'subject': email_info['subject'],
                'body': email_info['body'],
                'from': email_info['from'],
                'priority': email_info['priority'],
                'created_at': datetime.now().isoformat(),
                'dry_run': True,
                'mode': 'DRY_RUN'
            }

            # Write approval file
            with open(approval_file, 'w') as f:
                json.dump(approval_data, f, indent=2)

            self.logger.info(f"   ✅ Email approval created: {approval_filename}")
            self.logger.info(f"   → To: {email_info['to']}")
            self.logger.info(f"   → Subject: {email_info['subject']}")
            self.logger.info(f"   → Mode: DRY RUN (will not actually send)")

            return True

        except Exception as e:
            self.logger.error(f"❌ Error creating email approval: {str(e)}", exc_info=True)
            return False

    def _generate_email_approval(self, file_path):
        """Generate email approval for a task"""
        try:
            # Wait for file to stabilize
            if not self._wait_for_file_stable(file_path, timeout=5):
                self.logger.warning(f"File not stable: {file_path.name}")
                return

            # Check if file still exists
            if not file_path.exists():
                self.logger.warning(f"File disappeared: {file_path.name}")
                return

            # Read task file
            content = self._read_task_file(file_path)
            if not content:
                return

            # Extract email information
            email_info = self._extract_email_info(content)

            # Create email approval
            if self._create_email_approval(file_path, email_info):
                self.logger.info(f"✅ Email approval generated for: {file_path.name}")
            else:
                self.logger.error(f"❌ Failed to generate email approval for: {file_path.name}")

        except Exception as e:
            self.logger.error(f"❌ Error processing email task: {str(e)}", exc_info=True)

    def _wait_for_file_stable(self, file_path, timeout=5, check_interval=0.5):
        """Wait for file size to stabilize (indicates write is complete)"""
        try:
            elapsed = 0
            last_size = None

            while elapsed < timeout:
                try:
                    current_size = file_path.stat().st_size

                    if last_size is not None and last_size == current_size:
                        return True

                    last_size = current_size
                    time.sleep(check_interval)
                    elapsed += check_interval

                except (OSError, FileNotFoundError):
                    return False

            return True

        except Exception as e:
            self.logger.warning(f"Error checking file stability: {e}")
            return True


def main():
    """Main function to run the email generator"""
    # Get project base path
    base_path = Path(__file__).parent.parent
    watch_path = base_path / "Needs_Action"

    # Setup logging
    logger = setup_logging()

    # Verify paths
    if not watch_path.exists():
        logger.error(f"Watch directory does not exist: {watch_path}")
        sys.exit(1)

    logger.info(f"Watching directory: {watch_path}")
    logger.info(f"Output directory: {base_path / 'Pending_Approval'}")
    logger.info("ℹ️  Using PollingObserver (WSL-compatible, polls every 2 seconds)")
    logger.info("ℹ️  DRY RUN MODE: Emails will be logged but not actually sent")

    # Create event handler and observer
    event_handler = EmailGenerator(logger, base_path)
    observer = PollingObserver(timeout=2)  # Poll every 2 seconds
    observer.schedule(event_handler, str(watch_path), recursive=False)

    # Start watching
    try:
        logger.info("Starting email generator...")
        observer.start()
        logger.info("✅ Generator is running. Waiting for email tasks...")
        logger.info("=" * 80)

        # Keep the observer running
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        logger.info("\n⛔ Shutdown signal received (Ctrl+C)")
        observer.stop()
        logger.info("Observer stopped")

    finally:
        observer.join()
        logger.info("Email generator shutdown complete")
        logger.info("=" * 80)


if __name__ == "__main__":
    main()
