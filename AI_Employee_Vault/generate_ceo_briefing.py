#!/usr/bin/env python3
"""CEO Briefing System - Reads completed tasks and generates weekly report"""

import json
import os
from pathlib import Path
from datetime import datetime
from collections import defaultdict

def get_task_type(filename):
    """Determine task type from filename"""
    if 'EMAIL' in filename.upper():
        return 'email'
    elif 'SOCIAL' in filename.upper():
        return 'social'
    else:
        return 'general'

def parse_markdown_task(filepath):
    """Parse markdown task file"""
    try:
        with open(filepath, 'r') as f:
            content = f.read()

        # Extract title from first heading or filename
        title = Path(filepath).stem.replace('APPROVAL_PLAN_', '').replace('_', ' ')

        return {
            'title': title,
            'type': get_task_type(str(filepath)),
            'file': Path(filepath).name,
            'content': content[:200]  # Brief preview
        }
    except Exception as e:
        print(f"Error parsing markdown {filepath}: {e}")
        return None

def parse_json_task(filepath):
    """Parse JSON task file"""
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)

        # Extract relevant fields
        title = data.get('type', 'Unknown').replace('_', ' ').title()
        platform = data.get('platform', '')
        if platform:
            title = f"{title} ({platform})"

        return {
            'title': title,
            'type': get_task_type(str(filepath)),
            'file': Path(filepath).name,
            'priority': data.get('priority', 'Normal'),
            'mode': data.get('mode', 'N/A')
        }
    except Exception as e:
        print(f"Error parsing JSON {filepath}: {e}")
        return None

def generate_ceo_report():
    """Generate CEO briefing report"""
    done_dir = Path('Done')

    # Collect all tasks
    tasks = []
    tasks_by_type = defaultdict(list)

    if done_dir.exists():
        for file in sorted(done_dir.iterdir()):
            if file.is_file():
                task = None
                if file.suffix == '.md':
                    task = parse_markdown_task(file)
                elif file.suffix == '.json':
                    task = parse_json_task(file)

                if task:
                    tasks.append(task)
                    tasks_by_type[task['type']].append(task)

    # Generate report
    report = []
    report.append("# CEO Weekly Briefing Report")
    report.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")

    # Executive Summary
    report.append("## Executive Summary")
    report.append(f"- **Total Tasks Completed:** {len(tasks)}")
    report.append(f"- **Email Tasks:** {len(tasks_by_type['email'])}")
    report.append(f"- **Social Media Tasks:** {len(tasks_by_type['social'])}")
    report.append(f"- **General Tasks:** {len(tasks_by_type['general'])}")
    report.append("")

    # Key Metrics
    report.append("## Key Metrics")
    report.append(f"| Category | Count | Percentage |")
    report.append(f"|----------|-------|-----------|")
    for task_type in ['email', 'social', 'general']:
        count = len(tasks_by_type[task_type])
        percentage = (count / len(tasks) * 100) if len(tasks) > 0 else 0
        report.append(f"| {task_type.title()} | {count} | {percentage:.1f}% |")
    report.append("")

    # Email Tasks Summary
    if tasks_by_type['email']:
        report.append("## Email Communications")
        report.append(f"**Total:** {len(tasks_by_type['email'])} emails processed")
        report.append("")
        for task in tasks_by_type['email']:
            report.append(f"- **{task['title']}**")
        report.append("")

    # Social Media Tasks Summary
    if tasks_by_type['social']:
        report.append("## Social Media Activity")
        report.append(f"**Total:** {len(tasks_by_type['social'])} posts published")
        report.append("")
        for task in tasks_by_type['social']:
            mode = task.get('mode', 'N/A')
            report.append(f"- **{task['title']}** [{mode}]")
        report.append("")

    # General Tasks Summary
    if tasks_by_type['general']:
        report.append("## General Task Completions")
        report.append(f"**Total:** {len(tasks_by_type['general'])} tasks completed")
        report.append("")
        for task in tasks_by_type['general']:
            report.append(f"- {task['title']}")
        report.append("")

    # Key Highlights
    report.append("## Key Highlights")
    if tasks_by_type['social']:
        report.append("✓ Social media engagement initiatives launched")
    if tasks_by_type['email']:
        report.append("✓ Communication campaigns processed")
    if tasks_by_type['general']:
        report.append("✓ Standard operational tasks completed")
    report.append("")

    # Status Overview
    report.append("## Status Overview")
    report.append(f"All {len(tasks)} tasks have been successfully completed and documented.")
    report.append("")

    # Footer
    report.append("---")
    report.append("*This briefing was auto-generated by the CEO Briefing System*")

    return '\n'.join(report)

if __name__ == '__main__':
    report = generate_ceo_report()

    # Create Briefings directory if it doesn't exist
    briefings_dir = Path('Briefings')
    briefings_dir.mkdir(exist_ok=True)

    # Save report
    output_file = briefings_dir / 'CEO_REPORT.md'
    with open(output_file, 'w') as f:
        f.write(report)

    print(f"CEO Briefing generated successfully!")
    print(f"Report saved to: {output_file}")
    print("")
    print(report)
