# Handbook Tools

Automation utilities used to maintain the SRE Engineering Handbook.

---

## Available Tools

### generate_index.py

Automatically updates Markdown indexes used across the handbook.

Features:

- Generates README indexes
- Preserves manual content
- Updates only AUTO-INDEX regions
- Supports validation mode
- Safe and idempotent

---

## Usage

Check indexes:

```bash
python3 tools/generate_index.py --check
```

Update indexes:

```bash
python3 tools/generate_index.py --write
```

Check only one module:

```bash
python3 tools/generate_index.py --check --module linux
```

---

More automation utilities will be added over time.