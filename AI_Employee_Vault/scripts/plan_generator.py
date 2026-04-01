#!/usr/bin/env python3
"""
Plan Generator for AI_Employee_Vault
Monitors Needs_Action/ folder and creates plans for new tasks
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

    log_file = log_dir / f"plan_generator_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

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
    logger.info("PLAN GENERATOR STARTED")
    logger.info(f"Log file: {log_file}")
    logger.info("=" * 80)

    return logger


class PlanGenerator(FileSystemEventHandler):
    """Monitor Needs_Action/ folder and generate plans for new tasks"""

    def __init__(self, logger, base_path):
        self.logger = logger
        self.base_path = base_path
        self.watch_dir = base_path / "Needs_Action"
        self.plans_dir = base_path / "Plans"
        self.plans_dir.mkdir(exist_ok=True)
        self.processed_files = set()  # Track already-processed files
        self._load_existing_plans()  # Load existing plans on startup

    def _load_existing_plans(self):
        """Load list of existing plans to avoid recreating them"""
        if self.plans_dir.exists():
            for plan_file in self.plans_dir.glob("PLAN_*.md"):
                # Extract the original filename from plan filename
                # PLAN_TASK_dummy_001.md -> TASK_dummy_001.md
                original_name = plan_file.name.replace("PLAN_", "")
                self.processed_files.add(original_name)
                self.logger.debug(f"Loaded existing plan: {original_name}")

    def on_created(self, event):
        """Handle file creation events"""
        if event.is_directory:
            return

        file_path = Path(event.src_path)

        # Skip hidden files, metadata files, and plan files
        if file_path.name.startswith('.') or '_metadata.md' in file_path.name:
            return

        # Only process .md files
        if file_path.suffix != '.md':
            return

        # Avoid processing the same file twice
        if file_path.name in self.processed_files:
            self.logger.debug(f"Plan already exists for: {file_path.name}")
            return

        self.logger.info(f"📋 New task detected: {file_path.name}")
        self.processed_files.add(file_path.name)
        self._generate_plan(file_path)

    def _read_task_file(self, file_path):
        """Read and parse task file"""
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            return content
        except Exception as e:
            self.logger.warning(f"⚠️  Could not read task file: {str(e)}")
            return None

    def _extract_task_info(self, content):
        """Extract task information from file content"""
        task_info = {
            'title': '',
            'description': '',
            'sender': '',
            'priority': 'Normal'
        }

        # Extract title (first # heading)
        title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
        if title_match:
            task_info['title'] = title_match.group(1)

        # Extract task description
        desc_match = re.search(r'## Task Description\n(.+?)(?=\n##|\Z)', content, re.DOTALL)
        if desc_match:
            task_info['description'] = desc_match.group(1).strip()

        # Extract sender
        sender_match = re.search(r'\*\*From:\*\*\s*(.+?)(?:\n|$)', content)
        if sender_match:
            task_info['sender'] = sender_match.group(1).strip()

        # Extract priority
        priority_match = re.search(r'\*\*Priority:\*\*\s*(.+?)(?:\n|$)', content)
        if priority_match:
            task_info['priority'] = priority_match.group(1).strip()

        return task_info

    def _create_plan(self, file_path, task_info):
        """Create a plan file based on task information"""
        try:
            # Create plan filename
            plan_filename = f"PLAN_{file_path.name}"
            plan_file = self.plans_dir / plan_filename

            # Handle filename conflicts (shouldn't happen with our tracking)
            if plan_file.exists():
                self.logger.warning(f"Plan already exists: {plan_filename}")
                return

            # Generate plan content
            plan_content = self._generate_plan_content(task_info)

            # Write plan file
            with open(plan_file, 'w') as f:
                f.write(plan_content)

            self.logger.info(f"   → Plan created: {plan_filename}")
            self.logger.info(f"   → Status: pending")

        except Exception as e:
            self.logger.error(f"❌ Error creating plan: {str(e)}", exc_info=True)

    def _generate_plan_content(self, task_info):
        """Generate plan content with checklist"""
        title = task_info['title']
        description = task_info['description']
        sender = task_info['sender']
        priority = task_info['priority']
        timestamp = datetime.now().isoformat()

        # Generate step-by-step checklist based on task description
        steps = self._generate_steps(description)

        plan_content = f"""# Plan: {title}

**Created:** {timestamp}
**Status:** pending
**Priority:** {priority}

## Objective
{description}

## Task Information
- **Original Task:** {title}
- **From:** {sender}
- **Priority:** {priority}

## Step-by-Step Checklist

{steps}

## Notes
- Review each step before proceeding
- Document any findings or issues
- Update status as steps are completed

## Status Tracking
- **Started:** Not yet
- **In Progress:** No
- **Completed:** No
- **Issues:** None

---
*Generated by Plan Generator*
"""
        return plan_content

    def _generate_steps(self, description):
        """Generate step-by-step checklist from task description"""
        # Generic steps that apply to most tasks
        steps = [
            "- [ ] Review task requirements and acceptance criteria",
            "- [ ] Break down task into smaller sub-tasks if needed",
            "- [ ] Identify any dependencies or blockers",
            "- [ ] Research and gather necessary information",
            "- [ ] Create implementation plan with timeline",
            "- [ ] Begin execution of task",
            "- [ ] Review and validate work completed",
            "- [ ] Document findings and results",
            "- [ ] Obtain approval from stakeholder",
            "- [ ] Mark task as complete"
        ]

        return "\n".join(steps)

    def _generate_plan(self, file_path):
        """Generate plan for a task"""
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

            # Extract task information
            task_info = self._extract_task_info(content)

            # Create plan
            self._create_plan(file_path, task_info)
            self.logger.info(f"✅ Plan generated for: {file_path.name}")

        except Exception as e:
            self.logger.error(f"❌ Error processing task: {str(e)}", exc_info=True)

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
    """Main function to run the plan generator"""
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
    logger.info(f"Output directory: {base_path / 'Plans'}")
    logger.info("ℹ️  Using PollingObserver (WSL-compatible, polls every 2 seconds)")

    # Create event handler and observer
    event_handler = PlanGenerator(logger, base_path)
    observer = PollingObserver(timeout=2)  # Poll every 2 seconds
    observer.schedule(event_handler, str(watch_path), recursive=False)

    # Start watching
    try:
        logger.info("Starting plan generator...")
        observer.start()
        logger.info("✅ Generator is running. Waiting for new tasks...")
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
        logger.info("Plan generator shutdown complete")
        logger.info("=" * 80)


if __name__ == "__main__":
    main()
