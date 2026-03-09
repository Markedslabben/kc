#!/usr/bin/env python3
"""
Analyze Python project structure with cohesion metrics and bloat detection.

Features:
- Class/module counting
- Cohesion analysis (using cohesion library if available)
- LCOM4 metric calculation (built-in)
- Architecture bloat detection (Pydantic, thin wrappers, layer tax)
- Class consolidation suggestions
"""

import ast
import json
import sys
import subprocess
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Set, Tuple, Optional


# ═══════════════════════════════════════════════════════════════════════════════
# COHESION ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════

class CohesionAnalyzer:
    """Analyze class cohesion using LCOM4 metric and cohesion library."""

    def __init__(self):
        self.cohesion_available = self._check_cohesion_library()

    def _check_cohesion_library(self) -> bool:
        """Check if cohesion library is installed."""
        try:
            import cohesion
            return True
        except ImportError:
            return False

    def analyze_file_cohesion(self, filepath: Path) -> List[Dict]:
        """Analyze cohesion for all classes in a file using cohesion library."""
        if not self.cohesion_available:
            return []

        try:
            result = subprocess.run(
                ['python3', '-m', 'cohesion', '-f', str(filepath)],
                capture_output=True, text=True, timeout=30
            )
            return self._parse_cohesion_output(result.stdout, filepath)
        except Exception:
            return []

    def _parse_cohesion_output(self, output: str, filepath: Path) -> List[Dict]:
        """Parse cohesion tool output into structured data."""
        results = []
        current_class = None

        for line in output.split('\n'):
            line = line.strip()
            if line.startswith('Class:'):
                # Extract class name: "Class: ClassName (line:col)"
                parts = line.split('Class:')[1].strip()
                class_name = parts.split('(')[0].strip()
                current_class = {'name': class_name, 'file': str(filepath), 'methods': []}
            elif line.startswith('Total:') and current_class:
                # Extract total cohesion: "Total: 33.33%"
                try:
                    pct = float(line.split(':')[1].strip().replace('%', ''))
                    current_class['cohesion_percent'] = pct
                    current_class['cohesion_status'] = (
                        'good' if pct >= 80 else
                        'medium' if pct >= 50 else
                        'low'
                    )
                    results.append(current_class)
                    current_class = None
                except ValueError:
                    pass
            elif line.startswith('Function:') and current_class:
                # Extract method cohesion: "Function: method_name 2/4 50.00%"
                try:
                    parts = line.split()
                    method_name = parts[1]
                    pct = float(parts[-1].replace('%', ''))
                    current_class['methods'].append({
                        'name': method_name,
                        'cohesion_percent': pct
                    })
                except (IndexError, ValueError):
                    pass

        return results

    def calculate_lcom4(self, filepath: Path) -> List[Dict]:
        """
        Calculate LCOM4 (Lack of Cohesion of Methods) metric.

        LCOM4 counts connected components in a graph where:
        - Nodes = methods
        - Edges = shared instance variables

        LCOM4 > 1 suggests the class should be split.
        """
        results = []

        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                tree = ast.parse(f.read())
        except (SyntaxError, FileNotFoundError):
            return results

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                lcom4_result = self._calculate_class_lcom4(node)
                if lcom4_result:
                    lcom4_result['file'] = str(filepath)
                    results.append(lcom4_result)

        return results

    def _calculate_class_lcom4(self, class_node: ast.ClassDef) -> Optional[Dict]:
        """Calculate LCOM4 for a single class."""
        methods = {}

        # Extract methods and their accessed attributes
        for item in class_node.body:
            if isinstance(item, ast.FunctionDef):
                attrs = set()
                for n in ast.walk(item):
                    if (isinstance(n, ast.Attribute) and
                        isinstance(n.value, ast.Name) and
                        n.value.id == 'self'):
                        attrs.add(n.attr)
                methods[item.name] = attrs

        if len(methods) <= 1:
            return None

        # Build graph of methods connected by shared attributes
        graph = defaultdict(set)
        method_list = list(methods.keys())

        for i, m1 in enumerate(method_list):
            for m2 in method_list[i+1:]:
                if methods[m1] & methods[m2]:  # Shared attributes
                    graph[m1].add(m2)
                    graph[m2].add(m1)

        # Count connected components (LCOM4)
        visited = set()
        components = 0
        component_methods = []

        for m in method_list:
            if m not in visited:
                components += 1
                component = []
                stack = [m]
                while stack:
                    curr = stack.pop()
                    if curr not in visited:
                        visited.add(curr)
                        component.append(curr)
                        stack.extend(graph[curr] - visited)
                component_methods.append(component)

        return {
            'name': class_node.name,
            'lcom4': components,
            'should_split': components > 1,
            'method_count': len(methods),
            'components': component_methods,
            'suggestion': (
                f"Consider splitting into {components} classes"
                if components > 1 else "Cohesive class"
            )
        }


# ═══════════════════════════════════════════════════════════════════════════════
# BLOAT DETECTION
# ═══════════════════════════════════════════════════════════════════════════════

class BloatDetector:
    """Detect architecture anti-patterns that inflate class counts."""

    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.pydantic_classes = []
        self.dataclasses = []
        self.thin_wrappers = []
        self.service_classes = []

    def analyze(self) -> Dict:
        """Run all bloat detection analyses."""
        py_files = list(self.project_path.rglob("*.py"))
        total_classes = 0
        total_loc = 0

        for py_file in py_files:
            try:
                with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    total_loc += len(content.split('\n'))
                    tree = ast.parse(content)
                    self._analyze_file(py_file, tree, content)
                    total_classes += sum(1 for n in ast.walk(tree) if isinstance(n, ast.ClassDef))
            except Exception:
                continue

        return self._generate_bloat_report(total_classes, total_loc)

    def _analyze_file(self, filepath: Path, tree: ast.AST, content: str):
        """Analyze a single file for bloat patterns."""
        lines = content.split('\n')

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # Check for Pydantic - safely extract base names
                bases = []
                for b in node.bases:
                    if isinstance(b, ast.Name):
                        bases.append(b.id)
                    elif isinstance(b, ast.Attribute):
                        bases.append(b.attr)

                if 'BaseModel' in bases:
                    field_count = sum(1 for item in node.body
                                     if isinstance(item, ast.AnnAssign))
                    self.pydantic_classes.append({
                        'name': node.name,
                        'file': str(filepath),
                        'field_count': field_count,
                        'is_thin': field_count < 5
                    })

                # Check for dataclass
                for decorator in node.decorator_list:
                    if (isinstance(decorator, ast.Name) and decorator.id == 'dataclass') or \
                       (isinstance(decorator, ast.Attribute) and decorator.attr == 'dataclass'):
                        self.dataclasses.append({
                            'name': node.name,
                            'file': str(filepath)
                        })

                # Check for thin wrappers (< 50 LOC, < 3 methods)
                class_lines = node.end_lineno - node.lineno if hasattr(node, 'end_lineno') else 50
                method_count = sum(1 for item in node.body if isinstance(item, ast.FunctionDef))

                if class_lines < 50 and method_count < 3:
                    self.thin_wrappers.append({
                        'name': node.name,
                        'file': str(filepath),
                        'lines': class_lines,
                        'methods': method_count
                    })

                # Check for "Service/Manager/Handler" naming anti-pattern
                if any(suffix in node.name for suffix in ['Service', 'Manager', 'Handler', 'Helper', 'Wrapper']):
                    self.service_classes.append({
                        'name': node.name,
                        'file': str(filepath)
                    })

    def _generate_bloat_report(self, total_classes: int, total_loc: int) -> Dict:
        """Generate bloat analysis report."""
        kloc = total_loc / 1000
        classes_per_kloc = total_classes / kloc if kloc > 0 else 0
        avg_loc_per_class = total_loc / total_classes if total_classes > 0 else 0

        pydantic_ratio = len(self.pydantic_classes) / total_classes if total_classes > 0 else 0
        thin_pydantic = [p for p in self.pydantic_classes if p['is_thin']]

        # Health assessment
        health_issues = []
        if pydantic_ratio > 0.30:
            health_issues.append(f"Pydantic ratio {pydantic_ratio:.0%} exceeds 30% threshold")
        if classes_per_kloc > 6:
            health_issues.append(f"Classes/KLOC {classes_per_kloc:.1f} exceeds 6 (target: <5)")
        if avg_loc_per_class < 50:
            health_issues.append(f"Average class size {avg_loc_per_class:.0f} LOC is very small (target: 100-300)")
        if len(self.thin_wrappers) > total_classes * 0.20:
            health_issues.append(f"Too many thin wrapper classes ({len(self.thin_wrappers)})")

        return {
            'metrics': {
                'total_classes': total_classes,
                'total_kloc': round(kloc, 1),
                'classes_per_kloc': round(classes_per_kloc, 1),
                'avg_loc_per_class': round(avg_loc_per_class, 0),
                'pydantic_count': len(self.pydantic_classes),
                'pydantic_ratio': round(pydantic_ratio * 100, 1),
                'dataclass_count': len(self.dataclasses),
                'thin_wrapper_count': len(self.thin_wrappers),
                'service_naming_count': len(self.service_classes)
            },
            'health_status': 'healthy' if not health_issues else 'warning' if len(health_issues) < 3 else 'bloated',
            'health_issues': health_issues,
            'thin_pydantic_models': [p['name'] for p in thin_pydantic[:10]],
            'service_named_classes': [s['name'] for s in self.service_classes[:10]],
            'recommendations': self._generate_recommendations(
                pydantic_ratio, classes_per_kloc, thin_pydantic
            )
        }

    def _generate_recommendations(self, pydantic_ratio: float, classes_per_kloc: float,
                                  thin_pydantic: List) -> List[str]:
        """Generate actionable recommendations."""
        recs = []

        if pydantic_ratio > 0.30:
            recs.append("Convert internal Pydantic models to @dataclass (keep Pydantic only at API boundaries)")

        if thin_pydantic:
            recs.append(f"Consider inlining {len(thin_pydantic)} thin Pydantic models (<5 fields)")

        if classes_per_kloc > 6:
            recs.append("Consolidate related classes - too many small classes")

        if self.service_classes:
            recs.append("Rename 'Service/Manager/Handler' classes to domain nouns (e.g., RoofAnalyzer not RoofAnalysisService)")

        if not recs:
            recs.append("Architecture looks healthy - no major bloat detected")

        return recs


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN ANALYZER
# ═══════════════════════════════════════════════════════════════════════════════

class PythonAnalyzer:
    """Analyze Python project structure with cohesion and bloat detection."""

    def __init__(self, project_path: str):
        self.project_path = Path(project_path).resolve()
        self.modules = {}
        self.classes = []
        self.functions = []
        self.imports = defaultdict(set)
        self.relationships = []
        self.cohesion_analyzer = CohesionAnalyzer()
        self.bloat_detector = BloatDetector(self.project_path)

    def analyze(self, include_cohesion: bool = True) -> Dict:
        """Analyze the project and return findings."""
        if not self.project_path.exists():
            raise FileNotFoundError(f"Project path not found: {self.project_path}")

        py_files = list(self.project_path.rglob("*.py"))

        if not py_files:
            return {
                "status": "error",
                "message": f"No Python files found in {self.project_path}"
            }

        # Analyze each file
        cohesion_results = []
        lcom4_results = []

        for py_file in py_files:
            try:
                self._analyze_file(py_file)

                if include_cohesion:
                    # Run cohesion library analysis
                    cohesion_results.extend(
                        self.cohesion_analyzer.analyze_file_cohesion(py_file)
                    )
                    # Run LCOM4 analysis
                    lcom4_results.extend(
                        self.cohesion_analyzer.calculate_lcom4(py_file)
                    )
            except Exception as e:
                print(f"Warning: Could not analyze {py_file}: {e}", file=sys.stderr)

        # Run bloat detection
        bloat_report = self.bloat_detector.analyze()

        # Generate full report
        report = self._generate_report()
        report['cohesion_analysis'] = {
            'library_available': self.cohesion_analyzer.cohesion_available,
            'classes_analyzed': len(cohesion_results),
            'low_cohesion_classes': [
                c for c in cohesion_results
                if c.get('cohesion_status') == 'low'
            ],
            'cohesion_summary': self._summarize_cohesion(cohesion_results)
        }
        report['lcom4_analysis'] = {
            'classes_analyzed': len(lcom4_results),
            'classes_to_split': [
                r for r in lcom4_results if r.get('should_split')
            ],
            'total_splits_suggested': sum(
                r['lcom4'] - 1 for r in lcom4_results if r.get('should_split')
            )
        }
        report['bloat_analysis'] = bloat_report
        report['architecture_health'] = self._calculate_health_score(
            cohesion_results, lcom4_results, bloat_report
        )

        return report

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
                # Safely extract base class names
                bases = []
                for b in node.bases:
                    if isinstance(b, ast.Name):
                        bases.append(b.id)
                    elif isinstance(b, ast.Attribute):
                        bases.append(b.attr)
                    else:
                        bases.append(str(type(b).__name__))

                class_info = {
                    'name': node.name,
                    'module': module_name,
                    'methods': [],
                    'bases': bases,
                    'lineno': node.lineno
                }

                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        class_info['methods'].append(item.name)

                self.classes.append(class_info)

            elif isinstance(node, ast.FunctionDef) and not any(
                isinstance(parent, ast.ClassDef)
                for parent in ast.walk(tree)
                if hasattr(parent, 'body') and isinstance(parent.body, list) and node in parent.body
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
            "functions": self.functions[:10],
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

    def _summarize_cohesion(self, cohesion_results: List[Dict]) -> Dict:
        """Summarize cohesion analysis results."""
        if not cohesion_results:
            return {'status': 'not_analyzed'}

        percentages = [c.get('cohesion_percent', 0) for c in cohesion_results]
        avg_cohesion = sum(percentages) / len(percentages) if percentages else 0

        return {
            'average_cohesion': round(avg_cohesion, 1),
            'high_cohesion_count': sum(1 for p in percentages if p >= 80),
            'medium_cohesion_count': sum(1 for p in percentages if 50 <= p < 80),
            'low_cohesion_count': sum(1 for p in percentages if p < 50),
            'status': 'good' if avg_cohesion >= 70 else 'needs_attention' if avg_cohesion >= 50 else 'poor'
        }

    def _calculate_health_score(self, cohesion_results: List, lcom4_results: List,
                                bloat_report: Dict) -> Dict:
        """Calculate overall architecture health score."""
        score = 10.0
        issues = []

        # Cohesion penalties
        if cohesion_results:
            avg_cohesion = sum(c.get('cohesion_percent', 0) for c in cohesion_results) / len(cohesion_results)
            if avg_cohesion < 50:
                score -= 2.0
                issues.append(f"Low average cohesion ({avg_cohesion:.0f}%)")
            elif avg_cohesion < 70:
                score -= 1.0

        # LCOM4 penalties
        split_count = sum(1 for r in lcom4_results if r.get('should_split'))
        if split_count > 5:
            score -= 1.5
            issues.append(f"{split_count} classes should be split (LCOM4 > 1)")
        elif split_count > 0:
            score -= 0.5 * min(split_count, 3)

        # Bloat penalties
        metrics = bloat_report.get('metrics', {})
        if metrics.get('pydantic_ratio', 0) > 30:
            score -= 1.0
            issues.append("Pydantic overuse (>30% of classes)")
        if metrics.get('classes_per_kloc', 0) > 6:
            score -= 1.0
            issues.append("Too many classes per KLOC")
        if metrics.get('thin_wrapper_count', 0) > 10:
            score -= 0.5

        score = max(0, min(10, score))

        return {
            'score': round(score, 1),
            'grade': 'A' if score >= 8 else 'B' if score >= 6 else 'C' if score >= 4 else 'D',
            'issues': issues,
            'summary': (
                'Healthy architecture' if score >= 8 else
                'Minor improvements needed' if score >= 6 else
                'Significant refactoring recommended' if score >= 4 else
                'Architecture needs major restructuring'
            )
        }


def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_project.py <project_path> [--no-cohesion]")
        sys.exit(1)

    project_path = sys.argv[1]
    include_cohesion = '--no-cohesion' not in sys.argv

    analyzer = PythonAnalyzer(project_path)
    report = analyzer.analyze(include_cohesion=include_cohesion)

    # Pretty print JSON
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
