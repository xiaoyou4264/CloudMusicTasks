# Repository Guidelines

## Project Structure

- `index.py` loads JSON5 configuration, merges per-account overrides, and runs the configured tasks. `scheduler.py` provides Docker scheduling, and `user.py` handles account state and task dispatch.
- `api.py` wraps NetEase endpoints and `encrypt.py` builds encrypted requests. Task handlers live in `task/`, and notification adapters live in `push/` with aggregation in `pusher.py`.
- `config.example.json` documents configuration. `serverless/` and `.github/workflows/` contain deployment automation. README screenshots live in `public/img/`.

## Build and Development

- `python3 -m pip install -r requirements.txt` installs the Python dependencies. In a fresh checkout, copy `config.example.json` to `config.json` and configure a test account before running.
- `python3 index.py` runs one batch with the current account, task, and push settings.
- `docker compose build` builds the local image. `docker compose up -d` starts the scheduler, and `docker compose logs --tail=50` displays recent output.

## Coding and Configuration

Use four-space indentation and snake_case for new Python functions. Preserve existing task and push module names, including their case, because configuration references them by name. Task handlers expose `start(user, task)`. Update `config.example.json` when adding user-facing settings and keep existing configurations usable. Keep account cookies, passwords, and push keys in the ignored local `config.json`.

## Validation

The repository has no configured test suite, formatter, linter, or coverage threshold. Use `python3 -m compileall -q index.py scheduler.py api.py user.py task push` for syntax checks and `docker compose config --quiet` to validate Compose. Mock NetEase and push responses when checking dispatch, reward claims, or failure paths. A live run can modify account state and send notifications.

## Commits and Pull Requests

Use short, specific commit subjects. Recent history uses prefixes such as `feat:`, `fix:`, and `docs:`. In pull requests, summarize the behavior change, link related issues, and report the validation performed. Redact credentials and account data from logs or screenshots.
