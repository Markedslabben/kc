#!/usr/bin/env python3
"""
Auto-detection of qualifying tasks for velocity tracking.
Analyzes task descriptions to determine if tracking should be enabled.
"""

import re
from typing import Dict, Any, Optional, Tuple


class TaskDetector:
    """Detects and characterizes tasks for velocity tracking."""

    # Keywords that indicate comprehensive work
    COMPREHENSIVE_KEYWORDS = [
        'implement', 'create', 'build', 'develop', 'refactor',
        'migrate', 'upgrade', 'redesign', 'optimize', 'integrate'
    ]

    # Keywords that indicate simple tasks (not comprehensive)
    SIMPLE_KEYWORDS = [
        'read', 'check', 'view', 'list', 'show', 'explain',
        'what', 'how', 'why', 'tell me', 'describe'
    ]

    # Domain indicators
    DOMAIN_KEYWORDS = {
        'frontend': ['ui', 'component', 'react', 'vue', 'angular', 'css', 'html', 'interface', 'design'],
        'backend': ['api', 'server', 'database', 'endpoint', 'service', 'backend', 'sql'],
        'testing': ['test', 'spec', 'unit test', 'integration test', 'e2e', 'validation'],
        'deployment': ['deploy', 'build', 'ci/cd', 'docker', 'kubernetes', 'production'],
        'refactoring': ['refactor', 'cleanup', 'restructure', 'reorganize', 'simplify'],
        'debugging': ['debug', 'fix', 'bug', 'error', 'issue', 'problem', 'broken'],
        'documentation': ['document', 'readme', 'docs', 'documentation', 'comment'],
        'analysis': ['analyze', 'review', 'investigate', 'examine', 'assess']
    }

    def is_qualifying_task(self, task_description: str) -> bool:
        """
        Determine if task qualifies for velocity tracking.

        Args:
            task_description: User's task request

        Returns:
            True if task should be tracked
        """
        description_lower = task_description.lower()

        # Check for simple task indicators
        if any(keyword in description_lower for keyword in self.SIMPLE_KEYWORDS):
            # If it's a question or simple request, don't track
            if description_lower.strip().endswith('?'):
                return False

        # Check for comprehensive work indicators
        has_comprehensive_keyword = any(
            keyword in description_lower
            for keyword in self.COMPREHENSIVE_KEYWORDS
        )

        # Check for multiple components/files mentioned
        has_multiple_parts = (
            description_lower.count(' and ') >= 2 or
            description_lower.count(',') >= 2 or
            bool(re.search(r'\d+\+?\s+(files?|components?|modules?|services?)', description_lower))
        )

        # Must have either comprehensive keyword or multiple parts
        return has_comprehensive_keyword or has_multiple_parts

    def estimate_complexity(self, task_description: str) -> int:
        """
        Estimate task complexity (1-10 scale).

        Args:
            task_description: Task description

        Returns:
            Complexity score 1-10
        """
        description_lower = task_description.lower()
        complexity = 5  # Start at medium

        # Indicators of high complexity
        if any(word in description_lower for word in ['architecture', 'design', 'system', 'complex']):
            complexity += 2

        if any(word in description_lower for word in ['multiple', 'across', 'integrate', 'migration']):
            complexity += 1

        if any(word in description_lower for word in ['new', 'from scratch', 'build']):
            complexity += 1

        # Indicators of lower complexity
        if any(word in description_lower for word in ['simple', 'basic', 'straightforward', 'quick']):
            complexity -= 2

        if any(word in description_lower for word in ['update', 'modify', 'change']):
            complexity -= 1

        # Check for uncertainty markers (increases complexity)
        if any(word in description_lower for word in ['unclear', 'not sure', 'might need', 'maybe']):
            complexity += 1

        # Cap at 1-10 range
        return max(1, min(10, complexity))

    def estimate_scope(self, task_description: str) -> int:
        """
        Estimate number of subtasks.

        Args:
            task_description: Task description

        Returns:
            Estimated subtask count
        """
        description_lower = task_description.lower()
        scope = 3  # Default minimum for qualifying tasks

        # Look for explicit numbers
        numbers = re.findall(r'\b(\d+)\+?\s+(files?|components?|modules?|services?|steps?)', description_lower)
        if numbers:
            scope = max(scope, int(numbers[0][0]))

        # Count comma-separated items
        comma_count = description_lower.count(',')
        if comma_count >= 2:
            scope = max(scope, comma_count + 1)

        # Count "and" conjunctions
        and_count = description_lower.count(' and ')
        if and_count >= 2:
            scope = max(scope, and_count + 1)

        # Adjust based on keywords
        if 'full' in description_lower or 'complete' in description_lower:
            scope += 2

        if 'simple' in description_lower or 'small' in description_lower:
            scope = max(3, scope - 1)

        return scope

    def detect_domain(self, task_description: str) -> str:
        """
        Detect task domain from description.

        Args:
            task_description: Task description

        Returns:
            Domain name (frontend, backend, etc.)
        """
        description_lower = task_description.lower()

        # Count matches for each domain
        domain_scores = {}
        for domain, keywords in self.DOMAIN_KEYWORDS.items():
            score = sum(1 for keyword in keywords if keyword in description_lower)
            if score > 0:
                domain_scores[domain] = score

        # Return domain with highest score, or 'backend' as default
        if domain_scores:
            return max(domain_scores, key=domain_scores.get)
        else:
            return 'backend'  # Default fallback

    def detect_parallelization(self, task_description: str) -> str:
        """
        Detect parallelization potential.

        Args:
            task_description: Task description

        Returns:
            Parallelization level (sequential, partial, full)
        """
        description_lower = task_description.lower()

        # Full parallelization indicators
        if any(word in description_lower for word in ['independent', 'separate', 'parallel']):
            return 'full'

        # Partial parallelization indicators
        if any(word in description_lower for word in ['multiple files', 'components', 'modules']):
            return 'partial'

        # Sequential by default
        return 'sequential'

    def characterize_task(
        self,
        task_description: str,
        model: str = 'sonnet'
    ) -> Dict[str, Any]:
        """
        Fully characterize a task for velocity tracking.

        Args:
            task_description: Task description
            model: Claude model being used

        Returns:
            Dictionary with task characteristics
        """
        return {
            'description': task_description,
            'complexity': self.estimate_complexity(task_description),
            'scope': self.estimate_scope(task_description),
            'domain': self.detect_domain(task_description),
            'model': model,
            'parallelization': self.detect_parallelization(task_description),
            'tool_count': self._estimate_tool_count(task_description)
        }

    def _estimate_tool_count(self, task_description: str) -> int:
        """
        Estimate number of distinct tools needed.

        Args:
            task_description: Task description

        Returns:
            Estimated tool count
        """
        description_lower = task_description.lower()
        tool_count = 5  # Base estimate

        # Adjust based on task type
        if 'read' in description_lower or 'analyze' in description_lower:
            tool_count += 2  # Read, Grep

        if 'write' in description_lower or 'create' in description_lower:
            tool_count += 2  # Write, Edit

        if 'test' in description_lower:
            tool_count += 2  # Bash, testing tools

        if 'deploy' in description_lower or 'build' in description_lower:
            tool_count += 3  # Bash, Docker, etc.

        return min(15, tool_count)  # Cap at reasonable max
