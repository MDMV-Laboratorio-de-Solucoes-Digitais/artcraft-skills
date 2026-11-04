"""Contract tests for generalizable workflow skills (001 US5, T050)."""

import os
import sys
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

WORKFLOW_SKILLS = [
    "orchestrator",
    "policy-redaction",
    "structured-packager",
    "dag-orchestrator",
    "evidence-audit",
]


def test_workflow_skills_exist():
    for name in WORKFLOW_SKILLS:
        skill_dir = ROOT / "skills" / "workflow" / name
        assert skill_dir.exists(), f"missing skill dir: {name}"
        assert (skill_dir / "SKILL.md").exists(), f"missing SKILL.md: {name}"


def test_workflow_skills_validate():
    for name in WORKFLOW_SKILLS:
        skill_dir = ROOT / "skills" / "workflow" / name
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "validate_skill.py"), str(skill_dir)],
            capture_output=True, text=True, cwd=ROOT,
        )
        assert result.returncode == 0, f"validation failed for {name}: {result.stdout}\n{result.stderr}"


def test_workflow_skills_frontmatter():
    import yaml
    for name in WORKFLOW_SKILLS:
        skill_dir = ROOT / "skills" / "workflow" / name
        text = (skill_dir / "SKILL.md").read_text()
        assert text.startswith("---")
        parts = text.split("---", 2)
        assert len(parts) >= 3, f"invalid frontmatter: {name}"
        fm = yaml.safe_load(parts[1])
        assert fm is not None
        assert "name" in fm and fm["name"] == name
        assert "description" in fm and isinstance(fm["description"], str) and fm["description"].strip()
        # kebab-case name
        import re
        assert re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", fm["name"]), f"bad name: {name}"


def test_workflow_skills_generalizable_no_branding():
    for name in WORKFLOW_SKILLS:
        skill_dir = ROOT / "skills" / "workflow" / name
        text = (skill_dir / "SKILL.md").read_text().lower()
        # no MDMV-specific branding in skill content
        assert "mdmv" not in text, f"MDMV branding found in {name}"


def test_dag_orchestrator_skill_present():
    assert (ROOT / "skills" / "workflow" / "dag-orchestrator" / "SKILL.md").exists()


def test_composer_available():
    from skills.core.composer import SkillComposer
    assert hasattr(SkillComposer, "compose")
    assert hasattr(SkillComposer, "compose_parallel")


def test_dag_orchestrator_core_available():
    from skills.core.orchestrator import DAGOrchestrator
    orch = DAGOrchestrator()
    assert orch is not None
    assert hasattr(orch, "validate_dag")
    assert hasattr(orch, "get_ready_nodes")
