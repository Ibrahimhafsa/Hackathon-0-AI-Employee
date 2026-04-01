#!/usr/bin/env python3
"""
Social Media Generator for AI_Employee_Vault - Platinum Tier
Monitors Needs_Action/ folder and creates social media post approval requests
DRY RUN MODE: No actual posts created, only logged and approved
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

    log_file = log_dir / f"social_media_generator_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

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
    logger.info("SOCIAL MEDIA GENERATOR STARTED (PLATINUM TIER - DRY RUN MODE)")
    logger.info(f"Log file: {log_file}")
    logger.info("=" * 80)

    return logger


class SocialMediaGenerator(FileSystemEventHandler):
    """Monitor Needs_Action/ folder and generate social media post approval requests"""

    def __init__(self, logger, base_path):
        self.logger = logger
        self.base_path = base_path
        self.watch_dir = base_path / "Needs_Action"
        self.approval_dir = base_path / "Pending_Approval"
        self.approval_dir.mkdir(exist_ok=True)
        self.processed_files = set()
        self._load_existing_approvals()

    def _load_existing_approvals(self):
        """Load list of existing social media approvals to avoid recreating them"""
        if self.approval_dir.exists():
            for approval_file in self.approval_dir.glob("SOCIAL_APPROVAL_*.json"):
                # Extract the original filename from approval filename
                match = re.search(r'SOCIAL_APPROVAL_(.+)\.json', approval_file.name)
                if match:
                    original_name = match.group(1) + ".md"
                    self.processed_files.add(original_name)
                    self.logger.debug(f"Loaded existing social media approval: {original_name}")

    def on_created(self, event):
        """Handle file creation events"""
        if event.is_directory:
            return

        file_path = Path(event.src_path)

        # Skip hidden files and metadata files
        if file_path.name.startswith('.') or '_metadata.md' in file_path.name:
            return

        # Only process .md files that start with SOCIAL_
        if not file_path.name.startswith('SOCIAL_') or file_path.suffix != '.md':
            return

        # Avoid processing the same file twice
        if file_path.name in self.processed_files:
            self.logger.debug(f"Social media approval already exists for: {file_path.name}")
            return

        self.logger.info(f"📱 Social media task detected: {file_path.name}")
        self.processed_files.add(file_path.name)
        self._generate_post_approval(file_path)

    def _read_task_file(self, file_path):
        """Read and parse task file"""
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            return content
        except Exception as e:
            self.logger.warning(f"⚠️  Could not read task file: {str(e)}")
            return None

    def _extract_post_info(self, content):
        """Extract social media post information from file content"""
        post_info = {
            'platform': '',      # Twitter or LinkedIn
            'content': '',        # Post text content
            'hashtags': '',       # Hashtags (optional)
            'mentions': '',       # @mentions (optional)
            'from': 'AI_Employee_Vault',
            'priority': 'Normal'
        }

        # Extract platform (To: for compatibility, Platform: is also supported)
        platform_match = re.search(r'\*\*Platform:\*\*\s*(.+?)(?:\n|$)', content)
        if not platform_match:
            platform_match = re.search(r'\*\*To:\*\*\s*(.+?)(?:\n|$)', content)
        if platform_match:
            post_info['platform'] = platform_match.group(1).strip()

        # Extract post content
        content_match = re.search(r'## Post Content\n(.+?)(?=\n##|\*\*|\Z)', content, re.DOTALL)
        if content_match:
            post_info['content'] = content_match.group(1).strip()
        else:
            # Fallback: look for any content after Platform
            content_match = re.search(r'\*\*Platform:\*\*.*?\n(.+?)(?:\n##|\Z)', content, re.DOTALL)
            if content_match:
                post_info['content'] = content_match.group(1).strip()

        # Extract hashtags
        hashtags_match = re.search(r'\*\*Hashtags:\*\*\s*(.+?)(?:\n|$)', content)
        if hashtags_match:
            tags_value = hashtags_match.group(1).strip()
            if tags_value.lower() != 'none' and tags_value:
                post_info['hashtags'] = tags_value

        # Extract mentions
        mentions_match = re.search(r'\*\*Mentions:\*\*\s*(.+?)(?:\n|$)', content)
        if mentions_match:
            mentions_value = mentions_match.group(1).strip()
            if mentions_value.lower() != 'none' and mentions_value:
                post_info['mentions'] = mentions_value

        # Extract priority
        priority_match = re.search(r'\*\*Priority:\*\*\s*(.+?)(?:\n|$)', content)
        if priority_match:
            post_info['priority'] = priority_match.group(1).strip()

        return post_info

    def _validate_post_info(self, post_info):
        """Validate that post has required fields"""
        if not post_info['platform']:
            return False, "Missing platform (Twitter/LinkedIn)"
        if not post_info['content']:
            return False, "Missing post content"

        # Validate platform name
        valid_platforms = ['twitter', 'x', 'linkedin']
        if post_info['platform'].lower() not in valid_platforms:
            return False, f"Invalid platform. Use: {', '.join(valid_platforms)}"

        # Validate content length
        if len(post_info['content']) < 10:
            return False, "Post content too short (minimum 10 characters)"

        return True, "Valid"

    def _create_post_approval(self, file_path, post_info):
        """Create a social media post approval request JSON file"""
        try:
            # Validate post info
            is_valid, message = self._validate_post_info(post_info)
            if not is_valid:
                self.logger.error(f"   ❌ Invalid post: {message}")
                return False

            # Create approval filename
            approval_filename = f"SOCIAL_APPROVAL_{file_path.stem}.json"
            approval_file = self.approval_dir / approval_filename

            # Ensure no conflicts
            if approval_file.exists():
                self.logger.warning(f"Social media approval already exists: {approval_filename}")
                return False

            # Create approval data
            approval_data = {
                'action': 'post_social_media',
                'type': 'social_media_post',
                'platform': post_info['platform'].lower(),
                'content': post_info['content'],
                'hashtags': post_info['hashtags'],
                'mentions': post_info['mentions'],
                'from': post_info['from'],
                'priority': post_info['priority'],
                'created_at': datetime.now().isoformat(),
                'dry_run': True,
                'mode': 'DRY_RUN'
            }

            # Write approval file
            with open(approval_file, 'w') as f:
                json.dump(approval_data, f, indent=2)

            # Log approval creation
            self.logger.info(f"   ✅ Post approval created: {approval_filename}")
            self.logger.info(f"   → Platform: {post_info['platform']}")
            self.logger.info(f"   → Content preview: {post_info['content'][:60]}...")
            if post_info['hashtags']:
                self.logger.info(f"   → Hashtags: {post_info['hashtags']}")
            self.logger.info(f"   → Mode: DRY RUN (will not actually post)")

            return True

        except Exception as e:
            self.logger.error(f"❌ Error creating post approval: {str(e)}", exc_info=True)
            return False

    def _generate_post_approval(self, file_path):
        """Generate post approval for a social media task"""
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

            # Extract post information
            post_info = self._extract_post_info(content)

            # Create post approval
            if self._create_post_approval(file_path, post_info):
                self.logger.info(f"✅ Post approval generated for: {file_path.name}")
            else:
                self.logger.error(f"❌ Failed to generate post approval for: {file_path.name}")

        except Exception as e:
            self.logger.error(f"❌ Error processing social media task: {str(e)}", exc_info=True)

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
    """Main function to run the social media generator"""
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
    logger.info("ℹ️  DRY RUN MODE: Posts will be logged but not actually posted")

    # Create event handler and observer
    event_handler = SocialMediaGenerator(logger, base_path)
    observer = PollingObserver(timeout=2)  # Poll every 2 seconds
    observer.schedule(event_handler, str(watch_path), recursive=False)

    # Start watching
    try:
        logger.info("Starting social media generator...")
        observer.start()
        logger.info("✅ Generator is running. Waiting for social media tasks...")
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
        logger.info("Social media generator shutdown complete")
        logger.info("=" * 80)


if __name__ == "__main__":
    main()
