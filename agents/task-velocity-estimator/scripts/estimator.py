#!/usr/bin/env python3
"""
Time estimation algorithm for task velocity tracking.
Uses weighted similarity approach based on historical data.
"""

from typing import Dict, Any, List, Optional
from database import VelocityDatabase


class TaskEstimator:
    """Calculates time estimates based on historical velocity data."""

    # Baseline minutes per subtask by domain (when no historical data exists)
    BASELINE_MINUTES = {
        'frontend': 25,
        'backend': 30,
        'testing': 20,
        'deployment': 15,
        'refactoring': 35,
        'debugging': 40,
        'documentation': 15,
        'analysis': 30
    }

    def __init__(self, db: Optional[VelocityDatabase] = None):
        """
        Initialize estimator.

        Args:
            db: Database instance. If None, creates new instance.
        """
        self.db = db or VelocityDatabase()

    def estimate_task(
        self,
        complexity: int,
        scope: int,
        domain: str,
        project_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Estimate task duration based on historical data.

        Args:
            complexity: Task complexity (1-10)
            scope: Number of subtasks
            domain: Task domain
            project_name: Optional project name for filtering

        Returns:
            Dictionary with estimation results
        """
        # Query similar historical tasks
        similar_tasks = self.db.query_similar_tasks(
            complexity=complexity,
            scope=scope,
            domain=domain,
            project_name=project_name,
            limit=20
        )

        if not similar_tasks:
            # No historical data - use baseline estimates
            return self._baseline_estimate(complexity, scope, domain)

        # Calculate weighted estimate from similar tasks
        return self._weighted_estimate(
            complexity=complexity,
            scope=scope,
            domain=domain,
            similar_tasks=similar_tasks
        )

    def _baseline_estimate(
        self,
        complexity: int,
        scope: int,
        domain: str
    ) -> Dict[str, Any]:
        """
        Calculate baseline estimate when no historical data exists.

        Args:
            complexity: Task complexity (1-10)
            scope: Number of subtasks
            domain: Task domain

        Returns:
            Estimation dictionary
        """
        base_time = self.BASELINE_MINUTES.get(domain, 30)
        complexity_multiplier = complexity / 5  # Normalize around 1.0 for mid-complexity

        estimated_minutes = int(base_time * scope * complexity_multiplier)

        return {
            'estimated_minutes': estimated_minutes,
            'confidence': 0.5,  # Low confidence without historical data
            'similar_count': 0,
            'avg_accuracy': None,
            'method': 'baseline',
            'range_min': None,
            'range_max': None
        }

    def _weighted_estimate(
        self,
        complexity: int,
        scope: int,
        domain: str,
        similar_tasks: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Calculate weighted estimate from similar historical tasks.

        Args:
            complexity: Task complexity (1-10)
            scope: Number of subtasks
            domain: Task domain
            similar_tasks: List of similar task records

        Returns:
            Estimation dictionary
        """
        # Get model weights
        model_stats = self.db.get_model_stats()
        complexity_weight = model_stats['complexity_weight']
        scope_weight = model_stats['scope_weight']
        domain_weight = model_stats['domain_weight']

        total_weight = 0
        weighted_sum = 0
        accuracies = []
        durations = []

        for task in similar_tasks:
            # Calculate similarity score (0-1)
            complexity_diff = abs(task['complexity'] - complexity)
            scope_diff = abs(task['scope'] - scope)
            domain_match = 1.0 if task['domain'] == domain else 0.3

            # Weighted similarity calculation
            similarity = (
                (10 - complexity_diff) / 10 * complexity_weight +
                (20 - min(scope_diff, 20)) / 20 * scope_weight +
                domain_match * domain_weight
            )

            # Weight by similarity and recency (more recent = higher weight)
            weighted_sum += task['actual_minutes'] * similarity
            total_weight += similarity

            if task['accuracy_percent'] is not None:
                accuracies.append(task['accuracy_percent'])

            durations.append(task['actual_minutes'])

        # Calculate weighted average
        estimated_minutes = int(weighted_sum / total_weight) if total_weight > 0 else 60

        # Calculate confidence based on sample size and consistency
        confidence = self._calculate_confidence(len(similar_tasks), accuracies)

        # Calculate average accuracy
        avg_accuracy = sum(accuracies) / len(accuracies) if accuracies else None

        # Calculate duration range
        range_min = min(durations) if durations else None
        range_max = max(durations) if durations else None

        return {
            'estimated_minutes': estimated_minutes,
            'confidence': confidence,
            'similar_count': len(similar_tasks),
            'avg_accuracy': avg_accuracy,
            'method': 'weighted',
            'range_min': range_min,
            'range_max': range_max
        }

    def _calculate_confidence(
        self,
        sample_size: int,
        accuracies: List[float]
    ) -> float:
        """
        Calculate confidence level based on sample size and historical accuracy.

        Args:
            sample_size: Number of similar tasks
            accuracies: List of accuracy percentages

        Returns:
            Confidence level (0.0 to 1.0)
        """
        # Base confidence on sample size (more samples = higher confidence)
        size_confidence = min(0.95, 0.5 + (sample_size / 20) * 0.45)

        # Adjust by historical accuracy consistency
        if accuracies:
            avg_accuracy = sum(accuracies) / len(accuracies)
            # High accuracy boosts confidence, low accuracy reduces it
            accuracy_factor = avg_accuracy / 100
            final_confidence = size_confidence * (0.7 + 0.3 * accuracy_factor)
        else:
            final_confidence = size_confidence

        return round(final_confidence, 2)

    def calculate_accuracy(
        self,
        estimated_minutes: int,
        actual_minutes: int
    ) -> float:
        """
        Calculate accuracy percentage for an estimate.

        Args:
            estimated_minutes: Estimated duration
            actual_minutes: Actual duration

        Returns:
            Accuracy percentage (0-100)
        """
        if estimated_minutes == 0:
            return 0.0

        # Calculate deviation
        deviation = abs(actual_minutes - estimated_minutes)
        accuracy = 100 - (deviation / estimated_minutes * 100)

        # Cap at 0-100 range
        return max(0.0, min(100.0, accuracy))

    def format_estimate_report(
        self,
        task_description: str,
        complexity: int,
        scope: int,
        domain: str,
        model: str,
        estimate: Dict[str, Any]
    ) -> str:
        """
        Format estimation results as human-readable report.

        Args:
            task_description: Task description
            complexity: Task complexity
            scope: Number of subtasks
            domain: Task domain
            model: Model being used
            estimate: Estimation results

        Returns:
            Formatted report string
        """
        minutes = estimate['estimated_minutes']
        hours = minutes // 60
        mins = minutes % 60

        confidence_pct = int(estimate['confidence'] * 100)

        report = f"""
📊 Task Velocity Estimate
─────────────────────────────────────────
Task: {task_description}
Estimated Duration: {hours}h {mins}m
Confidence: {confidence_pct}% (based on {estimate['similar_count']} similar tasks)

Task Profile:
• Complexity: {complexity}/10
• Scope: {scope} subtasks
• Domain: {domain}
• Model: {model}
"""

        if estimate['similar_count'] > 0:
            avg_h = estimate['range_min'] // 60 if estimate['range_min'] else 0
            avg_m = estimate['range_min'] % 60 if estimate['range_min'] else 0
            max_h = estimate['range_max'] // 60 if estimate['range_max'] else 0
            max_m = estimate['range_max'] % 60 if estimate['range_max'] else 0

            report += f"""
Historical Context:
• Similar tasks: {estimate['similar_count']} found
• Range: {avg_h}h {avg_m}m - {max_h}h {max_m}m"""

            if estimate['avg_accuracy']:
                report += f"\n• Model accuracy: {int(estimate['avg_accuracy'])}%"
        else:
            report += "\n\nNo historical data - using baseline estimates"

        report += "\n─────────────────────────────────────────"

        return report

    def format_completion_report(
        self,
        estimated_minutes: int,
        actual_minutes: int,
        accuracy: float,
        confidence: float,
        total_tasks: int,
        domain: str
    ) -> str:
        """
        Format task completion report.

        Args:
            estimated_minutes: Estimated duration
            actual_minutes: Actual duration
            accuracy: Accuracy percentage
            confidence: Confidence level
            total_tasks: Total tasks tracked
            domain: Task domain

        Returns:
            Formatted report string
        """
        est_h = estimated_minutes // 60
        est_m = estimated_minutes % 60
        act_h = actual_minutes // 60
        act_m = actual_minutes % 60

        deviation = actual_minutes - estimated_minutes
        deviation_sign = "+" if deviation > 0 else ""

        velocity = "faster" if deviation < 0 else "slower" if deviation > 0 else "exactly on track"

        confidence_pct = int(confidence * 100)

        report = f"""
✅ Task Velocity Report
─────────────────────────────────────────
Estimated: {est_h}h {est_m}m
Actual: {act_h}h {act_m}m
Accuracy: {int(accuracy)}%

Performance:
• Deviation: {deviation_sign}{deviation} minutes
• Your velocity: {velocity}
• Model confidence was: {confidence_pct}%

Database Updated:
• Total tasks tracked: {total_tasks}
"""

        # Get domain accuracy if available
        domain_accuracy = self.db.get_domain_accuracy(domain)
        if domain_accuracy:
            report += f"• Domain accuracy ({domain}): {int(domain_accuracy)}%\n"

        report += "─────────────────────────────────────────"

        return report
