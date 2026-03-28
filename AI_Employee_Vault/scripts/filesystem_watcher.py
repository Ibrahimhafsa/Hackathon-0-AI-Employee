#!/usr/bin/env python3
"""
Filesystem Watcher for AI_Employee_Vault
Monitors AI_Drop_Folder for new files and processes them
"""

import os
import sys
import shutil
import logging
import time
from pathlib import Path
from datetime import datetime
from watchdog.observers.polling import PollingObserver
from watchdog.events import FileSystemEventHandler


# Setup logging
def setup_logging():
    """Configure logging to file and console"""
    log_dir = Path(__file__).parent.parent / "Logs"
    log_dir.mkdir(exist_ok=True)

    log_file = log_dir / f"watcher_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

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
    logger.info("FILESYSTEM WATCHER STARTED")
    logger.info(f"Log file: {log_file}")
    logger.info("=" * 80)

    return logger


class FileDropHandler(FileSystemEventHandler):
    """Handle file system events in AI_Drop_Folder"""

    def __init__(self, logger, base_path):
        self.logger = logger
        self.base_path = base_path
        self.watch_dir = base_path / "AI_Drop_Folder"
        self.action_dir = base_path / "Needs_Action"
        self.action_dir.mkdir(exist_ok=True)
        self.processed_files = set()  # Track already-processed files to avoid duplicates

    def on_created(self, event):
        """Handle file creation events"""
        if event.is_directory:
            return

        # Skip hidden files and metadata files
        file_path = Path(event.src_path)
        if file_path.name.startswith('.'):
            return

        # Avoid processing the same file twice
        file_key = str(file_path.absolute())
        if file_key in self.processed_files:
            self.logger.debug(f"Already processed: {file_path.name}")
            return

        self.logger.info(f"📁 File detected: {file_path.name}")
        self.processed_files.add(file_key)
        self._process_file(file_path)

    def on_modified(self, event):
        """Handle file modification events (for completeness)"""
        if event.is_directory:
            return

        file_path = Path(event.src_path)
        if file_path.name.startswith('.'):
            return

        # Only process if file size is stable (not being written)
        if self._is_file_stable(file_path):
            self.logger.info(f"File modified (stable): {file_path.name}")
            # Optionally process on modification

    def _wait_for_file_stable(self, file_path, timeout=5, check_interval=0.5):
        """Wait for file size to stabilize (indicates write is complete)"""
        try:
            elapsed = 0
            last_size = None

            while elapsed < timeout:
                try:
                    current_size = file_path.stat().st_size

                    if last_size is not None and last_size == current_size:
                        # Size hasn't changed, file is stable
                        return True

                    last_size = current_size
                    time.sleep(check_interval)
                    elapsed += check_interval

                except (OSError, FileNotFoundError):
                    # File disappeared
                    return False

            # Timeout reached, assume file is stable
            return True

        except Exception as e:
            self.logger.warning(f"Error checking file stability: {e}")
            return True  # Proceed anyway

    def _process_file(self, file_path):
        """Process the dropped file"""
        try:
            # Wait for file to finish writing (check for stable size)
            if not self._wait_for_file_stable(file_path, timeout=5):
                self.logger.warning(f"⏱️  File not stable after timeout: {file_path.name}")
                return

            # Check if file still exists
            if not file_path.exists():
                self.logger.warning(f"⚠️  File no longer exists: {file_path.name}")
                return

            # Create destination filename with FILE_ prefix
            dest_filename = f"FILE_{file_path.name}"
            dest_file = self.action_dir / dest_filename

            # Handle filename conflicts
            if dest_file.exists():
                base_name = file_path.stem
                ext = file_path.suffix
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                dest_filename = f"FILE_{base_name}_{timestamp}{ext}"
                dest_file = self.action_dir / dest_filename
                self.logger.info(f"   → Name collision, using: {dest_filename}")

            # Copy file
            self.logger.info(f"   → Copying {file_path.name}...")
            shutil.copy2(file_path, dest_file)
            self.logger.info(f"✅ File copied to Needs_Action: {dest_file.name}")

            # Create metadata file
            self._create_metadata(dest_file, file_path)

        except Exception as e:
            self.logger.error(f"❌ Error processing {file_path.name}: {str(e)}", exc_info=True)

    def _create_metadata(self, dest_file, src_file):
        """Create .md metadata file for the processed file"""
        try:
            metadata_filename = f"{dest_file.stem}_metadata.md"
            metadata_file = dest_file.parent / metadata_filename

            # Get file info
            src_stat = src_file.stat()
            dest_stat = dest_file.stat()

            # Create metadata content
            metadata_content = f"""# File Processing Metadata

**Original File:** `{src_file.name}`
**Processed File:** `{dest_file.name}`
**Metadata File:** `{metadata_filename}`

## Timestamps
- **Detected:** {datetime.now().isoformat()}
- **Source Modified:** {datetime.fromtimestamp(src_stat.st_mtime).isoformat()}

## File Information
- **Source Size:** {src_stat.st_size:,} bytes
- **Destination Size:** {dest_stat.st_size:,} bytes
- **Original Path:** `{src_file.absolute()}`

## Status
- **Status:** Ready for Action
- **Action Required:** Review and process from `Needs_Action/` folder

---
*Generated by Filesystem Watcher (PollingObserver - WSL Compatible)*
"""

            with open(metadata_file, 'w') as f:
                f.write(metadata_content)

            self.logger.info(f"✅ Metadata created: {metadata_filename}")

        except Exception as e:
            self.logger.error(f"❌ Error creating metadata: {str(e)}", exc_info=True)


def main():
    """Main function to run the filesystem watcher"""
    # Get project base path
    base_path = Path(__file__).parent.parent
    watch_path = base_path / "AI_Drop_Folder"

    # Setup logging
    logger = setup_logging()

    # Verify paths
    if not watch_path.exists():
        logger.error(f"Watch directory does not exist: {watch_path}")
        sys.exit(1)

    logger.info(f"Watching directory: {watch_path}")
    logger.info(f"Output directory: {base_path / 'Needs_Action'}")
    logger.info("ℹ️  Using PollingObserver (WSL-compatible, polls every 2 seconds)")

    # Create event handler and observer
    event_handler = FileDropHandler(logger, base_path)
    observer = PollingObserver(timeout=2)  # Poll every 2 seconds
    observer.schedule(event_handler, str(watch_path), recursive=False)

    # Start watching
    try:
        logger.info("Starting filesystem observer...")
        observer.start()
        logger.info("✅ Observer is running. Waiting for files...")
        logger.info(f"Polling frequency: every 2 seconds")
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
        logger.info("Filesystem watcher shutdown complete")
        logger.info("=" * 80)


if __name__ == "__main__":
    main()
