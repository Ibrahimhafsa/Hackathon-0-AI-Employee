# AI Employee System 🤖

An autonomous AI-powered task management and execution system that intelligently processes, plans, and executes tasks with human oversight and approval.

## Project Overview

The AI Employee System is an intelligent automation platform built to manage complex workflows through a Human-in-the-Loop (HITL) framework. It monitors a vault of tasks, generates executable plans, submits them for human approval, and executes approved actions—all while maintaining transparency and control at every stage.

## Features

- **File Watcher System**: Monitors task directories for new items and changes
- **Intelligent Plan Generation**: Automatically creates structured execution plans for tasks
- **Human-in-the-Loop Approval**: Routes plans to human reviewers before execution
- **Task Execution Engine**: Executes approved actions with full auditability
- **Obsidian Vault Integration**: Uses Obsidian for task and plan organization
- **Metadata Tracking**: Maintains detailed task and execution metadata
- **Status Management**: Tracks tasks through the complete workflow lifecycle

## Architecture

### Core Components

**Watchers**
- File system watchers monitor the `Needs_Action` directory for new tasks
- Automatically detect task files and metadata changes
- Trigger the planning phase when new tasks arrive

**Plans**
- AI-generated execution plans analyze tasks and determine optimal actions
- Plans are structured documents with step-by-step instructions
- Stored with full context for human reviewers to understand reasoning

**Approvals**
- Human reviewers examine generated plans in the `Pending_Approval` directory
- Plans can be approved, rejected, or sent back for revision
- Approval workflow ensures quality control and safety

**Execution**
- Approved plans move to execution
- Actions are performed according to plan specifications
- Completed tasks move to `Done` directory with execution records

## Workflow

```
Needs_Action → Plans → Pending_Approval → Approved → Done
```

1. **Needs_Action**: Tasks that require processing
2. **Plans**: AI-generated execution plans awaiting review
3. **Pending_Approval**: Plans submitted for human decision
4. **Approved**: Plans cleared for execution
5. **Done**: Completed tasks with execution records

## Technologies Used

- **Python**: Core system implementation
- **File System Watchers**: Real-time task detection and monitoring
- **Obsidian Vault**: Task and plan organization framework
- **JSON/Markdown**: Task and metadata storage formats
- **Python Standard Library**: File I/O, OS operations, threading

## How to Run the System

### Prerequisites
- Python 3.8+
- Obsidian (optional, for vault visualization)

### Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Hackathon-0-AI-Employee
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the main system:
   ```bash
   python main.py
   ```

### Directory Structure

```
AI_Employee_Vault/
├── Needs_Action/      # New tasks waiting to be processed
├── Plans/             # Generated execution plans
├── Pending_Approval/  # Plans awaiting human review
├── Approved/          # Approved plans ready for execution
└── Done/              # Completed tasks with records
```

### Usage

1. Add task files to the `Needs_Action` directory
2. The system will monitor and generate plans
3. Review and approve plans in the workflow
4. Approved plans execute automatically
5. Completed tasks appear in `Done`

## Tiers Completed

- Bronze ✅
- Silver ✅

## Author

Hafsa Ibrahim
