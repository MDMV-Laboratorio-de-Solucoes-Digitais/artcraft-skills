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
