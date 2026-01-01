#!/usr/bin/env python3
"""
Main velocity tracker - coordinates task detection, estimation, and recording.
Entry point for velocity tracking operations.
"""

import sys
import os
import subprocess
from datetime import datetime
from typing import Optional
from pathlib import Path

# Add scripts directory to Python path
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from database import VelocityDatabase
from estimator import TaskEstimator
from task_detector import TaskDetector


class VelocityTracker:
    """Main coordinator for task velocity tracking."""

    def __init__(self):
        """Initialize tracker components."""
        self.db = VelocityDatabase()
        self.estimator = TaskEstimator(self.db)
        self.detector = TaskDetector()
        self.project_name = self._get_project_name()

    def _get_project_name(self) -> Optional[str]:
        """
        Get project name from git repo or current directory.

        Returns:
            Project name or None
        """
        try:
            # Try to get git repo name
            result = subprocess.run(
                ['git', 'rev-parse', '--show-toplevel'],
                capture_output=True,
                text=True,
                timeout=2
            )
            if result.returncode == 0:
                repo_path = result.stdout.strip()
                return Path(repo_path).name
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass

        # Fallback to current directory name
        return Path.cwd().name

    def start_task(self, task_description: str, model: str = 'sonnet') -> Optional[dict]:
        """
        Start tracking a task - provide estimate.

        Args:
            task_description: Description of the task
            model: Claude model being used

        Returns:
            Estimation data or None if task doesn't qualify
        """
        # Check if task qualifies for tracking
        if not self.detector.is_qualifying_task(task_description):
            return None

        # Characterize the task
        task_profile = self.detector.characterize_task(task_description, model)

        # Get time estimate
        estimate = self.estimator.estimate_task(
            complexity=task_profile['complexity'],
            scope=task_profile['scope'],
            domain=task_profile['domain'],
            project_name=self.project_name
        )

        # Format and display report
        report = self.estimator.format_estimate_report(
            task_description=task_description,
            complexity=task_profile['complexity'],
            scope=task_profile['scope'],
            domain=task_profile['domain'],
            model=model,
            estimate=estimate
        )

        print(report)

        # Return data for tracking
        return {
            **task_profile,
            **estimate,
            'start_time': datetime.now(),
            'project_name': self.project_name
        }

    def complete_task(
        self,
        task_data: dict,
        actual_minutes: Optional[int] = None
    ):
        """
        Complete task tracking - record results.

        Args:
            task_data: Task data from start_task
            actual_minutes: Actual duration (calculated if None)
        """
        # Calculate actual time if not provided
        if actual_minutes is None:
            start_time = task_data['start_time']
            elapsed = datetime.now() - start_time
            actual_minutes = int(elapsed.total_seconds() / 60)

        # Calculate accuracy
        estimated_minutes = task_data['estimated_minutes']
        accuracy = self.estimator.calculate_accuracy(estimated_minutes, actual_minutes)

        # Store in database
        record = {
            'timestamp': task_data['start_time'].isoformat(),
            'project_name': task_data.get('project_name'),
            'description': task_data['description'],
            'complexity': task_data['complexity'],
            'scope': task_data['scope'],
            'model': task_data['model'],
            'domain': task_data['domain'],
            'tool_count': task_data['tool_count'],
            'parallelization': task_data['parallelization'],
            'estimated_minutes': estimated_minutes,
            'actual_minutes': actual_minutes,
            'accuracy_percent': accuracy,
            'confidence_level': task_data['confidence'],
            'similar_task_count': task_data['similar_count']
        }

        self.db.insert_task(record)

        # Update model stats every 5 tasks
        total_tasks = self.db.get_task_count()
        if total_tasks % 5 == 0:
            self.db.update_model_stats()

        # Format and display completion report
        report = self.estimator.format_completion_report(
            estimated_minutes=estimated_minutes,
            actual_minutes=actual_minutes,
            accuracy=accuracy,
            confidence=task_data['confidence'],
            total_tasks=total_tasks,
            domain=task_data['domain']
        )

        print(report)


def main():
    """Main entry point for velocity tracker CLI."""
    if len(sys.argv) < 2:
        print("Usage: velocity_tracker.py <command> [args]")
        print("Commands:")
        print("  start <description> [model]  - Start tracking a task")
        print("  complete <task_id> [minutes] - Complete a task")
        print("  stats                        - Show database statistics")
        sys.exit(1)

    tracker = VelocityTracker()
    command = sys.argv[1]

    if command == "start":
        if len(sys.argv) < 3:
            print("Error: Task description required")
            sys.exit(1)

        description = sys.argv[2]
        model = sys.argv[3] if len(sys.argv) > 3 else 'sonnet'

        result = tracker.start_task(description, model)
        if result is None:
            print("Task does not qualify for velocity tracking (too simple)")
            sys.exit(0)

    elif command == "stats":
        total = tracker.db.get_task_count()
        recent = tracker.db.get_recent_tasks(5)

        print(f"\n📊 Velocity Database Statistics")
        print(f"─────────────────────────────────────────")
        print(f"Total tasks tracked: {total}")
        print(f"Project: {tracker.project_name}")
        print(f"\nRecent tasks:")
        for task in recent:
            print(f"  • {task['description'][:50]}... ({task['actual_minutes']}min)")
        print(f"─────────────────────────────────────────\n")

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
