# Quickstart: Shared CLI/MCP Adapter

## Usage

```python
from skills.core import artcraft_app_client

# Discover CLI
cli = artcraft_app_client.discover_cli()

# Discover commands
commands = artcraft_app_client.discover_cli_commands(cli)

# Find generation command
gen_cmd = artcraft_app_client.discover_generation_command(commands)

# Run generation
result = artcraft_app_client.run_cli_generation(cli, gen_cmd, {"prompt": "test"})
```

## Validation

```bash
# Test image-generate still works
python -m pytest tests/unit/test_image_generate*.py tests/contract/test_image_generate.py tests/integration/test_image_generate_composition.py -v

# Validate skills
python scripts/validate_skill.py skills/creative/image-generate
python scripts/validate_all_skills.py
```

## Future Skill Example

```python
from skills.core import artcraft_app_client

# Custom keywords and override for a mesh-generate skill
cmds = artcraft_app_client.discover_cli_commands(cli)
gen_cmd = artcraft_app_client.discover_generation_command(
    cmds, keywords=["mesh", "generate-mesh", "mesh.generate"], override=None
)

# Normalize arbitrary output keys
data = artcraft_app_client.normalize_output(raw, keys=["mesh_url", "vertex_count"])

# Mode selection
mode = artcraft_app_client.select_mode("auto", cli_available=True, mcp_available=False)
```

Future creative skills (image-edit, background-remove, image-upscale, mesh-generate) MUST use the shared adapter and MUST NOT duplicate discovery/invocation logic.
