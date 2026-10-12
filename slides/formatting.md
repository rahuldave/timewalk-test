# Formatting, as a document

This step shows one whole Markdown file instead of slides. It scrolls, and it has no slide arrows. A line
that is exactly three dashes is a rule here, not a new slide.

---

## What changed

`uv add --dev ruff` puts ruff in the group `dev` of `pyproject.toml`. Then ruff gets a line length:

```toml
[tool.ruff]
line-length = 100
```

## Why a document

Some steps need more than a slide, for example a setup to follow, a table or a long example. A document holds all of it,
and the presenter scrolls it while the class reads.

| Tool | Reads |
|---|---|
| ruff | `[tool.ruff]` |
| pytest | `[tool.pytest.ini_options]` |
