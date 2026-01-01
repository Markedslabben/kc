#!/usr/bin/env python3
"""
Analyze Python project structure to understand codebase and recommend diagrams.
"""

import ast
import json
import sys
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Set, Tuple

class PythonAnalyzer:
    """Analyze Python project structure."""

    def __init__(self, project_path: str):
        self.project_path = Path(project_path).resolve()
        self.modules = {}
        self.classes = []
        self.functions = []
        self.imports = defaultdict(set)
        self.relationships = []

    def analyze(self) -> Dict:
        """Analyze the project and return findings."""
        if not self.project_path.exists():
            raise FileNotFoundError(f"Project path not found: {self.project_path}")

        # Find all Python files
        py_files = list(self.project_path.rglob("*.py"))

        if not py_files:
            return {
                "status": "error",
                "message": f"No Python files found in {self.project_path}"
            }

        # Analyze each file
        for py_file in py_files:
            try:
                self._analyze_file(py_file)
            except Exception as e:
                print(f"Warning: Could not analyze {py_file}: {e}", file=sys.stderr)

        # Generate recommendations
        return self._generate_report()

    def _analyze_file(self, filepath: Path):
        """Extract structure from a single Python file."""
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            try:
                tree = ast.parse(f.read())
            except SyntaxError:
                return

        rel_path = filepath.relative_to(self.project_path)
        module_name = str(rel_path.with_suffix(''))

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_info = {
                    'name': node.name,
                    'module': module_name,
                    'methods': [],
                    'bases': [b.id if isinstance(b, ast.Name) else str(b) for b in node.bases],
                    'lineno': node.lineno
                }

                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        class_info['methods'].append(item.name)

                self.classes.append(class_info)

            elif isinstance(node, ast.FunctionDef) and not any(
                isinstance(parent, ast.ClassDef)
                for parent in ast.walk(tree)
                if hasattr(parent, 'body') and node in parent.body
            ):
                self.functions.append({
                    'name': node.name,
                    'module': module_name,
                    'lineno': node.lineno
                })

            elif isinstance(node, ast.Import):
                for alias in node.names:
                    self.imports[module_name].add(alias.name.split('.')[0])

            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    self.imports[module_name].add(node.module.split('.')[0])

    def _generate_report(self) -> Dict:
        """Generate analysis report with recommendations."""
        num_classes = len(self.classes)
        num_functions = len(self.functions)
        num_modules = len(set(c['module'] for c in self.classes))

        # Determine complexity
        if num_classes < 3:
            complexity = "SIMPLE"
        elif num_classes < 15:
            complexity = "MEDIUM"
        else:
            complexity = "COMPLEX"

        # Recommend diagrams
        recommended = []
        if num_modules > 1:
            recommended.append("architecture")
        if num_classes >= 3:
            recommended.append("class_diagram")
        if num_modules > 2 and len(self.imports) > 0:
            recommended.append("dependency_graph")

        # Check for inheritance relationships
        has_inheritance = any(c['bases'] for c in self.classes)
        if has_inheritance:
            recommended.append("class_hierarchy")

        return {
            "status": "success",
            "project_path": str(self.project_path),
            "summary": {
                "total_modules": num_modules,
                "total_classes": num_classes,
                "total_functions": num_functions,
                "complexity": complexity,
                "has_inheritance": has_inheritance
            },
            "classes": self.classes,
            "functions": self.functions[:10],  # Top 10 for brevity
            "modules": list(set(c['module'] for c in self.classes)),
            "recommended_diagrams": list(set(recommended)) if recommended else ["architecture"],
            "key_insights": self._generate_insights()
        }

    def _generate_insights(self) -> List[str]:
        """Generate insights about the codebase."""
        insights = []

        if len(self.classes) == 0:
            insights.append("Project has no classes - may be purely functional")
        elif len(self.classes) < 5:
            insights.append("Small project - manual documentation may be sufficient")
        elif len(self.classes) > 30:
            insights.append("Large project - class diagram will be complex, consider subsystem view")

        modules_with_many_classes = defaultdict(int)
        for c in self.classes:
            modules_with_many_classes[c['module']] += 1

        heavy_modules = [m for m, count in modules_with_many_classes.items() if count > 5]
        if heavy_modules:
            insights.append(f"Modules with many classes: {', '.join(heavy_modules[:3])}")

        if len(set(c['module'] for c in self.classes)) == 1:
            insights.append("All classes in single module - consider refactoring into packages")

        inheritance_depth = max(
            (len(c['bases']) for c in self.classes),
            default=0
        )
        if inheritance_depth > 2:
            insights.append("Deep inheritance hierarchy detected - class diagram recommended")

        return insights


def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_project.py <project_path>")
        sys.exit(1)

    project_path = sys.argv[1]

    analyzer = PythonAnalyzer(project_path)
    report = analyzer.analyze()

    # Pretty print JSON
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
