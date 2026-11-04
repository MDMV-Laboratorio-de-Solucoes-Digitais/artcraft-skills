"""Check that skills/docs contain no MDMV-specific branding or lock-in."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FORBIDDEN = ["mdmv", "tirateima", "crsdd-fabro", "tirateima_fc"]
TARGETS = [ROOT / "skills", ROOT / "docs"]
bad = []
for target in TARGETS:
    if not target.exists():
        continue
    for path in target.rglob("*"):
        if path.is_file() and path.suffix in {".md", ".py", ".json", ".yaml", ".yml"}:
            text = path.read_text(encoding="utf-8", errors="ignore").lower()
            for token in FORBIDDEN:
                if token in text:
                    bad.append((str(path.relative_to(ROOT)), token))
if bad:
    for p, t in bad:
        print(f"VENDOR-NEUTRALITY VIOLATION: {p} contains '{t}'")
    sys.exit(1)
print("Vendor-neutrality check passed: no forbidden tokens found.")
