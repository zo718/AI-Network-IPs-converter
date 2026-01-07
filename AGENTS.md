# Repository Guidelines

## Project Structure & Module Organization
This repository currently contains a single documentation file: `README.md`. There is no `src/`, `tests/`, or asset directory yet. When adding tools, keep a simple top-level layout, for example: `src/` for code, `tests/` for automated checks, and `assets/` for data files or diagrams. If you introduce language-specific modules (e.g., Python), place them under `src/` with clear subfolders such as `src/cli/` or `src/lib/`.

## Build, Test, and Development Commands
No build, test, or run commands are defined today. If you add a tool that needs setup, document the exact commands in `README.md` and keep them consistent across scripts. Example patterns to adopt when applicable:
- `python -m venv .venv` and `source .venv/bin/activate` for local setup.
- `make test` or `npm test` for a single, canonical test entry point.

## Coding Style & Naming Conventions
There are no enforced style rules yet. Prefer clear, descriptive names and avoid abbreviations in new tool modules. Use lowercase with dashes for new top-level directories (e.g., `network-scripts/`) and snake_case for Python files. Keep Markdown files concise with one blank line between sections.

## Testing Guidelines
No tests exist yet. If you add automation, place tests under `tests/` and name them consistently (e.g., `test_cli_basic.py`). State any coverage targets or required fixtures directly in the test README if introduced.

## Commit & Pull Request Guidelines
Git history currently contains a single commit (`Initial commit`), so no convention is established. Use short, imperative commit messages such as `Add device inventory parser`. For pull requests, include a brief description, list any new dependencies, and note example usage or sample commands.

## Security & Configuration Tips
Do not commit credentials, tokens, or device configs with secrets. If tools require configuration, use a `.env` file and document required keys in `README.md`. Add `.env` to `.gitignore` when you introduce it.
