#!/usr/bin/env python3
"""
Generate diagrams from project analysis using Mermaid and PlantUML.
"""

import json
import sys
import subprocess
from pathlib import Path
from typing import Dict, List
import os


class DiagramGenerator:
    """Generate architecture and class diagrams."""

    def __init__(self, analysis_data: Dict, output_dir: str = None):
        self.analysis = analysis_data
        self.output_dir = Path(output_dir or "docs/diagrams/generated")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.src_dir = Path(output_dir or "docs/diagrams").parent / "diagrams" / "src"
        self.src_dir.mkdir(parents=True, exist_ok=True)

    def generate_all(self) -> List[str]:
        """Generate all recommended diagrams."""
        recommended = self.analysis.get("recommended_diagrams", [])
        generated = []

        if "architecture" in recommended:
            self._generate_architecture_diagram()
            generated.append("architecture.mmd")

        if "class_diagram" in recommended:
            self._generate_class_diagram()
            generated.append("classes.puml")

        if "dependency_graph" in recommended:
            self._generate_dependency_graph()
            generated.append("dependencies.mmd")

        return generated

    def _generate_architecture_diagram(self):
        """Generate Mermaid architecture diagram from modules."""
        modules = self.analysis.get("modules", [])

        mermaid = "graph TB\n"
        mermaid += "    subgraph Architecture[\"System Architecture\"]\n"

        # Group modules by depth
        for i, module in enumerate(sorted(modules)[:10]):  # Limit to 10 for clarity
            parts = module.split('.')
            if len(parts) == 1:
                mermaid += f"        {module.replace('.', '_')}[\"<b>{module}</b>\"]\n"

        # Add simple relationships
        if len(modules) > 1:
            for i, module in enumerate(sorted(modules)[:-1]):
                next_module = sorted(modules)[i + 1]
                mermaid += f"        {module.replace('.', '_')} --> {next_module.replace('.', '_')}\n"

        mermaid += "    end\n"
        mermaid += f"\n    style Architecture fill:#e1f5ff\n"

        # Write to file
        src_file = self.src_dir / "architecture.mmd"
        with open(src_file, 'w') as f:
            f.write(mermaid)

        # Try to render as SVG
        self._render_mermaid(src_file)

    def _generate_class_diagram(self):
        """Generate PlantUML class diagram."""
        classes = self.analysis.get("classes", [])[:20]  # Limit to 20 classes

        puml = "@startuml\n"
        puml += "!theme plain\n"
        puml += "skinparam backgroundColor #FEFEFE\n"
        puml += "skinparam classBackgroundColor #F0F0F0\n"
        puml += "skinparam classBorderColor #666666\n\n"

        # Add classes
        for cls in classes:
            puml += f"class {cls['name']} {{\n"
            for method in cls['methods'][:5]:  # Limit to 5 methods
                puml += f"  {method}()\n"
            puml += "}\n\n"

        # Add inheritance relationships
        for cls in classes:
            if cls['bases']:
                for base in cls['bases']:
                    if base != 'object':
                        puml += f"{cls['name']} --|> {base}\n"

        puml += "@enduml\n"

        # Write to file
        src_file = self.src_dir / "classes.puml"
        with open(src_file, 'w') as f:
            f.write(puml)

        # Try to render
        self._render_plantuml(src_file)

    def _generate_dependency_graph(self):
        """Generate module dependency graph."""
        modules = self.analysis.get("modules", [])

        mermaid = "graph LR\n"
        mermaid += "    subgraph Dependencies[\"Module Dependencies\"]\n"

        for i, module in enumerate(sorted(modules)[:8]):
            mermaid += f"        {module.replace('.', '_')}[\"{module}\"]\n"

        # Add some example relationships
        for i, module in enumerate(sorted(modules)[:-1]):
            if i < 5:  # Limit connections
                next_module = sorted(modules)[i + 1]
                mermaid += f"        {module.replace('.', '_')} --> {next_module.replace('.', '_')}\n"

        mermaid += "    end\n"

        src_file = self.src_dir / "dependencies.mmd"
        with open(src_file, 'w') as f:
            f.write(mermaid)

        self._render_mermaid(src_file)

    def _render_mermaid(self, src_file: Path):
        """Render Mermaid diagram to SVG."""
        output_file = self.output_dir / src_file.stem

        try:
            # Try using mmdc (mermaid-cli)
            svg_file = output_file.with_suffix('.svg')
            result = subprocess.run(
                ['mmdc', '-i', str(src_file), '-o', str(svg_file)],
                capture_output=True,
                timeout=10
            )
            if result.returncode != 0:
                print(f"Warning: Mermaid rendering failed for {src_file.name}", file=sys.stderr)
        except FileNotFoundError:
            print(f"Note: mermaid-cli not found. Install with: npm install -g @mermaid-js/mermaid-cli", file=sys.stderr)
        except Exception as e:
            print(f"Warning: Could not render {src_file.name}: {e}", file=sys.stderr)

    def _render_plantuml(self, src_file: Path):
        """Render PlantUML diagram to SVG."""
        output_file = self.output_dir / src_file.stem

        try:
            svg_file = output_file.with_suffix('.svg')
            result = subprocess.run(
                ['plantuml', '-svg', '-o', str(self.output_dir), str(src_file)],
                capture_output=True,
                timeout=10
            )
            if result.returncode != 0:
                print(f"Warning: PlantUML rendering failed for {src_file.name}", file=sys.stderr)
        except FileNotFoundError:
            print(f"Note: plantuml not found. Install with: apt-get install plantuml", file=sys.stderr)
        except Exception as e:
            print(f"Warning: Could not render {src_file.name}: {e}", file=sys.stderr)


def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_diagrams.py <analysis_json_file> [output_dir]")
        sys.exit(1)

    analysis_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "docs/diagrams/generated"

    # Load analysis data
    try:
        with open(analysis_file, 'r') as f:
            analysis = json.load(f)
    except FileNotFoundError:
        print(f"Error: Analysis file not found: {analysis_file}", file=sys.stderr)
        sys.exit(1)

    # Generate diagrams
    generator = DiagramGenerator(analysis, output_dir)
    generated = generator.generate_all()

    print(json.dumps({
        "status": "success",
        "generated_diagrams": generated,
        "output_directory": str(generator.output_dir),
        "source_directory": str(generator.src_dir)
    }, indent=2))


if __name__ == '__main__':
    main()
