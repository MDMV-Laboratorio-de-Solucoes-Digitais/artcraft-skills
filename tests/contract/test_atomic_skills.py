"""Contract tests for atomic skill SKILL.md files (001 SC-003)."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SKILLS = ["image-generate", "image-edit", "background-remove", "image-upscale", "mesh-generate"]


def test_atomic_skills_exist_and_validate():
    for name in SKILLS:
        skill_dir = ROOT / "skills" / "creative" / name
        assert skill_dir.exists(), f"missing skill dir: {name}"
        assert (skill_dir / "SKILL.md").exists(), f"missing SKILL.md: {name}"
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "validate_skill.py"), str(skill_dir)],
            capture_output=True, text=True, cwd=ROOT,
        )
        assert result.returncode == 0, f"validation failed for {name}: {result.stdout}\n{result.stderr}"


def test_build_before_generating_philosophy():
    # Verify composer exists and exposes compose/compose_parallel (build before generating)
    from skills.core.composer import SkillComposer
    assert hasattr(SkillComposer, "compose")
    assert hasattr(SkillComposer, "compose_parallel")
