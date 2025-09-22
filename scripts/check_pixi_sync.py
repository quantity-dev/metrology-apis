#!/usr/bin/env python3
"""
Validate that pixi sections in ``pyproject.toml`` mirror the dependency groups.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List
import tomllib


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PYPROJECT = PROJECT_ROOT / "pyproject.toml"


@dataclass
class RequirementSet:
    name: str
    expected: Iterable[str]
    actual: Iterable[str]

    def differences(self) -> List[str]:
        expected_norm = {canon(r) for r in self.expected}
        actual_norm = {canon(r) for r in self.actual}
        messages: List[str] = []
        missing = expected_norm - actual_norm
        extra = actual_norm - expected_norm
        if missing:
            messages.append(f"missing from {self.name}: {', '.join(sorted(missing))}")
        if extra:
            messages.append(f"extra entries in {self.name}: {', '.join(sorted(extra))}")
        if not messages and expected_norm != actual_norm:
            messages.append(
                f"ordering differs for {self.name}; consider aligning sorted output"
            )
        return messages


def canon(requirement: str) -> str:
    return requirement.replace(" ", "")


def parse_group_entries(entries: Iterable[str]) -> List[str]:
    return [canon(entry) for entry in entries]


def parse_pixi_block(block: Dict[str, str]) -> List[str]:
    return [canon(f"{name}{spec}") for name, spec in block.items()]


def main() -> int:
    data = tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))

    groups = data.get("dependency-groups", {})
    pixi = data.get("tool", {}).get("pixi", {})

    checks: List[RequirementSet] = []

    runtime_expected = parse_group_entries(groups.get("runtime", []))
    runtime_actual = parse_pixi_block(pixi.get("dependencies", {}))
    checks.append(
        RequirementSet("tool.pixi.dependencies", runtime_expected, runtime_actual)
    )

    lint_expected = parse_group_entries(groups.get("lint", []))
    lint_actual = parse_pixi_block(
        pixi.get("feature", {}).get("lint", {}).get("dependencies", {})
    )
    checks.append(
        RequirementSet(
            "tool.pixi.feature.lint.dependencies", lint_expected, lint_actual
        )
    )

    errors: List[str] = []
    for check in checks:
        errors.extend(check.differences())

    if errors:
        print("Pixi configuration is out of sync with dependency groups:")
        for line in errors:
            print(f"  - {line}")
        print(
            "Fix instructions:\n"
            "  1. Regenerate the pixi tables from the dependency groups, e.g.\n"
            "     pixi run --environment=lint generate-pixi > /tmp/pixi-sections.toml\n"
            "  2. Copy the updated [tool.pixi.*] blocks from that output back into pyproject.toml\n"
            "  3. Re-run pixi run lint to confirm the hook passes."
        )
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
