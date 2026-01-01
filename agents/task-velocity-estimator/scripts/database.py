#!/usr/bin/env python3
"""
Database operations for task velocity tracking.
Handles SQLite interactions for storing and querying task history.
"""

import sqlite3
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any


class VelocityDatabase:
    """SQLite database manager for task velocity tracking."""

    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize database connection.

        Args:
            db_path: Path to SQLite database file. If None, uses default KC location.
        """
        if db_path is None:
            # Default to KC agent data directory
            agent_dir = Path(__file__).parent.parent
            db_path = agent_dir / "data" / "velocity.db"

        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize_database()

    def _initialize_database(self):
        """Create database schema if it doesn't exist."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Tasks table with project_name field added
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    project_name TEXT,
                    description TEXT NOT NULL,
                    complexity INTEGER CHECK(complexity BETWEEN 1 AND 10),
                    scope INTEGER CHECK(scope > 0),
                    model TEXT CHECK(model IN ('sonnet', 'opus', 'haiku')),
                    domain TEXT,
                    tool_count INTEGER,
                    parallelization TEXT CHECK(parallelization IN ('sequential', 'partial', 'full')),
                    estimated_minutes INTEGER,
                    actual_minutes INTEGER,
                    accuracy_percent REAL,
                    confidence_level REAL,
                    similar_task_count INTEGER
                )
            """)

            # Estimation model table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS estimation_model (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    updated_at TEXT NOT NULL,
                    total_tasks INTEGER,
                    avg_accuracy_percent REAL,
                    complexity_weight REAL DEFAULT 0.4,
                    scope_weight REAL DEFAULT 0.35,
                    domain_weight REAL DEFAULT 0.25
                )
            """)

            # Create indexes for performance
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_complexity ON tasks(complexity)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_domain ON tasks(domain)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON tasks(timestamp)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_project ON tasks(project_name)")

            conn.commit()

    def insert_task(self, task_data: Dict[str, Any]) -> int:
        """
        Insert a new task record.

        Args:
            task_data: Dictionary containing task fields

        Returns:
            ID of inserted task
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO tasks (
                    timestamp, project_name, description, complexity, scope, model,
                    domain, tool_count, parallelization, estimated_minutes,
                    actual_minutes, accuracy_percent, confidence_level, similar_task_count
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                task_data.get('timestamp', datetime.now().isoformat()),
                task_data.get('project_name'),
                task_data['description'],
                task_data['complexity'],
                task_data['scope'],
                task_data.get('model', 'sonnet'),
                task_data.get('domain'),
                task_data.get('tool_count', 0),
                task_data.get('parallelization', 'sequential'),
                task_data.get('estimated_minutes'),
                task_data.get('actual_minutes'),
                task_data.get('accuracy_percent'),
                task_data.get('confidence_level'),
                task_data.get('similar_task_count', 0)
            ))
            conn.commit()
            return cursor.lastrowid

    def query_similar_tasks(
        self,
        complexity: int,
        scope: int,
        domain: str,
        project_name: Optional[str] = None,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Query similar tasks from history.

        Args:
            complexity: Task complexity (1-10)
            scope: Number of subtasks
            domain: Task domain (frontend, backend, etc.)
            project_name: Optional project filter
            limit: Maximum results to return

        Returns:
            List of similar task records
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # Find tasks within complexity ±2 and scope ±5
            query = """
                SELECT * FROM tasks
                WHERE complexity BETWEEN ? AND ?
                  AND scope BETWEEN ? AND ?
                  AND domain = ?
                  AND actual_minutes IS NOT NULL
            """
            params = [
                max(1, complexity - 2),
                min(10, complexity + 2),
                max(1, scope - 5),
                scope + 5,
                domain
            ]

            if project_name:
                query += " AND project_name = ?"
                params.append(project_name)

            query += " ORDER BY timestamp DESC LIMIT ?"
            params.append(limit)

            cursor.execute(query, params)

            return [dict(row) for row in cursor.fetchall()]

    def get_model_stats(self) -> Dict[str, Any]:
        """
        Get current model statistics.

        Returns:
            Dictionary with model accuracy and weights
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # Get latest model stats
            cursor.execute("""
                SELECT * FROM estimation_model
                ORDER BY updated_at DESC
                LIMIT 1
            """)

            row = cursor.fetchone()
            return dict(row) if row else {
                'total_tasks': 0,
                'avg_accuracy_percent': None,
                'complexity_weight': 0.4,
                'scope_weight': 0.35,
                'domain_weight': 0.25
            }

    def update_model_stats(self):
        """Update estimation model statistics based on recent tasks."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Calculate stats from last 10 tasks
            cursor.execute("""
                SELECT
                    COUNT(*) as total,
                    AVG(accuracy_percent) as avg_accuracy
                FROM (
                    SELECT accuracy_percent
                    FROM tasks
                    WHERE accuracy_percent IS NOT NULL
                    ORDER BY timestamp DESC
                    LIMIT 10
                )
            """)

            row = cursor.fetchone()
            total_tasks, avg_accuracy = row if row else (0, None)

            # Get total all-time tasks
            cursor.execute("SELECT COUNT(*) FROM tasks")
            all_time_total = cursor.fetchone()[0]

            # Insert updated model stats
            cursor.execute("""
                INSERT INTO estimation_model (
                    updated_at, total_tasks, avg_accuracy_percent,
                    complexity_weight, scope_weight, domain_weight
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (
                datetime.now().isoformat(),
                all_time_total,
                avg_accuracy,
                0.4,  # These could be dynamically adjusted
                0.35,
                0.25
            ))

            conn.commit()

    def get_task_count(self) -> int:
        """Get total number of tasks in database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM tasks")
            return cursor.fetchone()[0]

    def get_recent_tasks(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get most recent tasks.

        Args:
            limit: Maximum number of tasks to return

        Returns:
            List of recent task records
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("""
                SELECT * FROM tasks
                ORDER BY timestamp DESC
                LIMIT ?
            """, (limit,))

            return [dict(row) for row in cursor.fetchall()]

    def get_domain_accuracy(self, domain: str) -> Optional[float]:
        """
        Get average accuracy for a specific domain.

        Args:
            domain: Task domain

        Returns:
            Average accuracy percentage or None if no data
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT AVG(accuracy_percent)
                FROM tasks
                WHERE domain = ? AND accuracy_percent IS NOT NULL
            """, (domain,))

            result = cursor.fetchone()[0]
            return result if result is not None else None
