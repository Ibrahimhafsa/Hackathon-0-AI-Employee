#!/usr/bin/env python3
"""
Approval Manager for AI_Employee_Vault
Monitors Plans/ folder and creates approval requests for new plans
"""

import os
import sys
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

    log_file = log_dir / f"approval_manager_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

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
    logger.info("APPROVAL MANAGER STARTED")
    logger.info(f"Log file: {log_file}")
    logger.info("=" * 80)

    return logger


class ApprovalManager(FileSystemEventHandler):
    """Monitor Plans/ folder and create approval requests"""

    def __init__(self, logger, base_path):
        self.logger = logger
        self.base_path = base_path
        self.watch_dir = base_path / "Plans"
        self.approval_dir = base_path / "Pending_Approval"
        self.approved_dir = base_path / "Approved"
        self.rejected_dir = base_path / "Rejected"

        # Create directories
        self.approval_dir.mkdir(exist_ok=True)
        self.approved_dir.mkdir(exist_ok=True)
        self.rejected_dir.mkdir(exist_ok=True)

        self.processed_files = set()  # Track already-processed files
        self._load_existing_approvals()  # Load existing approvals on startup

    def _load_existing_approvals(self):
        """Load list of existing approvals to avoid recreating them"""
        if self.approval_dir.exists():
            for approval_file in self.approval_dir.glob("APPROVAL_*.md"):
                # Extract the original filename from approval filename
                original_name = approval_file.name.replace("APPROVAL_", "")
                self.processed_files.add(original_name)
                self.logger.debug(f"Loaded existing approval: {original_name}")

        # Also track approved and rejected plans
        if self.approved_dir.exists():
            for approved_file in self.approved_dir.glob("PLAN_*.md"):
                self.processed_files.add(approved_file.name)
                self.logger.debug(f"Loaded approved plan: {approved_file.name}")

        if self.rejected_dir.exists():
            for rejected_file in self.rejected_dir.glob("PLAN_*.md"):
                self.processed_files.add(rejected_file.name)
                self.logger.debug(f"Loaded rejected plan: {rejected_file.name}")

    def on_created(self, event):
        """Handle file creation events"""
        if event.is_directory:
            return

        file_path = Path(event.src_path)

        # Skip hidden files and non-plan files
        if file_path.name.startswith('.'):
            return

        # Only process PLAN_*.md files
        if not file_path.name.startswith('PLAN_') or file_path.suffix != '.md':
            return

        # Avoid processing the same file twice
        if file_path.name in self.processed_files:
            self.logger.debug(f"Approval already exists for: {file_path.name}")
            return

        self.logger.info(f"📋 New plan detected: {file_path.name}")
        self.processed_files.add(file_path.name)
        self._process_plan(file_path)

    def _read_plan_file(self, file_path):
        """Read and parse plan file"""
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            return content
        except Exception as e:
            self.logger.warning(f"⚠️  Could not read plan file: {str(e)}")
            return None

    def _extract_plan_info(self, content):
        """Extract plan information from file content"""
        plan_info = {
            'title': '',
            'objective': '',
            'priority': 'Normal',
            'status': 'pending'
        }

        # Extract title (first # heading)
        title_match = re.search(r'^# Plan: (.+)$', content, re.MULTILINE)
        if title_match:
            plan_info['title'] = title_match.group(1)

        # Extract objective
        obj_match = re.search(r'## Objective\n(.+?)(?=\n##|\Z)', content, re.DOTALL)
        if obj_match:
            plan_info['objective'] = obj_match.group(1).strip()

        # Extract priority
        priority_match = re.search(r'\*\*Priority:\*\*\s*(.+?)(?:\n|$)', content)
        if priority_match:
            plan_info['priority'] = priority_match.group(1).strip()

        # Extract status
        status_match = re.search(r'\*\*Status:\*\*\s*(.+?)(?:\n|$)', content)
        if status_match:
            plan_info['status'] = status_match.group(1).strip()

        return plan_info

    def _requires_approval(self, plan_info):
        """Determine if plan requires approval"""
        # All plans require approval in this workflow
        return True

    def _get_approval_reason(self, plan_info):
        """Generate approval reason based on plan details"""
        priority = plan_info['priority'].lower()

        if priority == 'high':
            return "High-priority plan requires management approval before execution"
        elif priority == 'critical':
            return "Critical-priority plan requires executive approval"
        else:
            return "Plan requires standard review and approval before proceeding"

    def _create_approval_request(self, file_path, plan_info):
        """Create an approval request file for the plan"""
        try:
            # Create approval filename
            approval_filename = f"APPROVAL_{file_path.name}"
            approval_file = self.approval_dir / approval_filename

            # Handle filename conflicts (shouldn't happen with our tracking)
            if approval_file.exists():
                self.logger.warning(f"Approval already exists: {approval_filename}")
                return

            # Generate approval content
            approval_content = self._generate_approval_content(file_path, plan_info)

            # Write approval file
            with open(approval_file, 'w') as f:
                f.write(approval_content)

            self.logger.info(f"   → Approval request created: {approval_filename}")
            self.logger.info(f"   → Reason: {self._get_approval_reason(plan_info)}")

        except Exception as e:
            self.logger.error(f"❌ Error creating approval: {str(e)}", exc_info=True)

    def _generate_approval_content(self, file_path, plan_info):
        """Generate approval request content"""
        title = plan_info['title']
        objective = plan_info['objective']
        priority = plan_info['priority']
        timestamp = datetime.now().isoformat()
        reason = self._get_approval_reason(plan_info)

        approval_content = f"""# Approval Request: {title}

**Created:** {timestamp}
**Status:** pending_approval
**Priority:** {priority}

## Plan Summary
**Plan File:** {file_path.name}
**Title:** {title}

### Objective
{objective}

## Approval Information

### Action Required
Review plan and approve or reject execution

### Reason for Approval
{reason}

### Priority Level
**Priority:** {priority}

## Instructions

### To Approve This Plan:
1. Review the plan details in `Plans/{file_path.name}`
2. Verify the objective and steps are appropriate
3. **Move** this file to the `Approved/` folder using the command:
   ```bash
   mv Pending_Approval/{Path(file_path.name).stem}.md Approved/{Path(file_path.name).stem}.md
   ```
   Or manually move it using your file manager

### To Reject This Plan:
1. If the plan has issues or is not suitable
2. **Move** this file to the `Rejected/` folder using the command:
   ```bash
   mv Pending_Approval/{Path(file_path.name).stem}.md Rejected/{Path(file_path.name).stem}.md
   ```
   Or manually move it using your file manager

### Decision Criteria
- [ ] Plan objective is clear and achievable
- [ ] Steps are logical and sequential
- [ ] Required resources are available
- [ ] No blocking dependencies identified
- [ ] Priority level is appropriate
- [ ] Plan aligns with organizational goals

## Related Files
- **Original Plan:** `Plans/{file_path.name}`
- **Original Task:** Locate in `Needs_Action/` folder

## Notes
- Review all details before making a decision
- Document any concerns or modifications needed
- Once moved to Approved/Rejected, execution will proceed accordingly

---
*Generated by Approval Manager*
"""
        return approval_content

    def _process_plan(self, file_path):
        """Process a new plan for approval"""
        try:
            # Wait for file to stabilize
            if not self._wait_for_file_stable(file_path, timeout=5):
                self.logger.warning(f"File not stable: {file_path.name}")
                return

            # Check if file still exists
            if not file_path.exists():
                self.logger.warning(f"File disappeared: {file_path.name}")
                return

            # Read plan file
            content = self._read_plan_file(file_path)
            if not content:
                return

            # Extract plan information
            plan_info = self._extract_plan_info(content)

            # Check if approval is needed
            if self._requires_approval(plan_info):
                self._create_approval_request(file_path, plan_info)
                self.logger.info(f"✅ Approval request created for: {file_path.name}")
            else:
                self.logger.info(f"ℹ️  No approval needed for: {file_path.name}")

        except Exception as e:
            self.logger.error(f"❌ Error processing plan: {str(e)}", exc_info=True)

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
    """Main function to run the approval manager"""
    # Get project base path
    base_path = Path(__file__).parent.parent
    watch_path = base_path / "Plans"

    # Setup logging
    logger = setup_logging()

    # Verify paths
    if not watch_path.exists():
        logger.error(f"Watch directory does not exist: {watch_path}")
        sys.exit(1)

    logger.info(f"Watching directory: {watch_path}")
    logger.info(f"Approval requests directory: {base_path / 'Pending_Approval'}")
    logger.info(f"Approved directory: {base_path / 'Approved'}")
    logger.info(f"Rejected directory: {base_path / 'Rejected'}")
    logger.info("ℹ️  Using PollingObserver (WSL-compatible, polls every 2 seconds)")

    # Create event handler and observer
    event_handler = ApprovalManager(logger, base_path)
    observer = PollingObserver(timeout=2)  # Poll every 2 seconds
    observer.schedule(event_handler, str(watch_path), recursive=False)

    # Start watching
    try:
        logger.info("Starting approval manager...")
        observer.start()
        logger.info("✅ Manager is running. Waiting for new plans...")
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
        logger.info("Approval manager shutdown complete")
        logger.info("=" * 80)


if __name__ == "__main__":
    main()
