# Contributing Guidelines & Working Rules for Interns

Welcome to the **AI-Powered Lead Intelligence, CRM & Outreach Automation** project!
This project uses a monorepo architecture where multiple teams (Frontend, Backend, AI, Automation) build concurrently in a contract-first setup.

To ensure smooth collaboration, zero merge conflicts, and high engineering standards, every team member must strictly follow these rules.

---

## 10 Core Working Rules for Interns

1. **One task = one branch = one pull request**
   - Branch naming format: `feature/<TASK-ID>-<short-name>`
   - Example: `feature/FE-09-lead-table` or `feature/BE-04-users-migration` or `feature/AI-03-draft-schema`
2. **Touch only the folder or file in your task row**
   - If your ticket says `frontend/src/pages/LeadPipeline/LeadTable.jsx`, edit only that file.
   - If you need a change in another team's folder or a shared file, **do not edit it yourself** — open an issue and tag your lead.
3. **Shared files are Lead-Only**
   - The following files can only be modified by team leads:
     - `package.json` / `package-lock.json`
     - `backend/requirements.txt` / `pyproject.toml`
     - `docker-compose.yml`
     - `.env.example`
     - Anything under `contracts/` and `.github/`
   - Need a new npm package or Python library? Open a GitHub Issue using the **Library Request** template!
4. **Contract-First Development**
   - All teams agree upon API interfaces before writing implementation code.
   - Frontend and AI build against `contracts/openapi.yaml`, `contracts/events.md`, and fake data (`frontend/src/mocks/`, `ai/fixtures/`).
   - Nobody has to wait for another team to finish backend endpoints or models.
5. **Strictly No ORM**
   - All database access uses parameterised raw SQL via `psycopg` and `psycopg_pool`.
   - Never use SQLAlchemy ORM, Tortoise, Peewee, or string concatenation/f-strings for SQL queries.
   - All migrations live in `database/migrations/` as numbered SQL files (`001_*.sql`).
6. **Never Commit Secrets**
   - API keys, passwords, connection strings, and tokens must only live in `.env` (which is git-ignored).
   - Never hardcode or commit keys to Git.
7. **Pull Request Requirements**
   - Every PR must use the [PR Template](.github/pull_request_template.md).
   - Include:
     - Task ID and title
     - Short description of changes
     - Screenshot/video recording (for Frontend) or test run output (for Backend / AI)
     - At least 1 peer review + 1 Team Lead review approval before merging.
8. **CODEOWNERS Enforced**
   - GitHub automatically requests reviews from your domain lead. Merging without lead approval is blocked.
9. **Task Sizing Roadmap**
   - Tasks are sized as:
     - **S (Small)**: ~1 day. Ideal warm-up tickets (`FE-02`, `FE-06`, `FE-13`, `BE-04`, `BE-11`, `AI-04`, `AI-09`).
     - **M (Medium)**: 2–3 days.
     - **L (Large)**: ~1 week. Pair with a mentor or peer.
10. **Documentation with Every PR**
    - Every completed task must add a brief summary or update to the respective guide in `docs/` (`docs/frontend-guide.md`, `docs/backend-guide.md`, `docs/ai-guide.md`).

---

## Getting Started: Daily Workflow

### Step 1: Pick an Assigned Task Ticket
Check the [Team Tasksheet](docs/tasksheet.md) or GitHub Projects board. Find your assigned Task ID (e.g. `FE-04`, `BE-15`, `AI-02`).

### Step 2: Create Your Feature Branch
```bash
git checkout main
git pull origin main
git checkout -b feature/FE-04-ui-component-kit
```

### Step 3: Implement & Test Locally
- Follow the exact **"What to build"** and **"Acceptance Criteria"** in your ticket.
- Verify that **"Out of Scope"** boundaries are respected.
- Run linters and tests:
  ```bash
  # For frontend:
  cd frontend
  npm run lint
  npm run test

  # For backend:
  pytest backend/tests

  # For AI:
  pytest ai/evals
  ```

### Step 4: Commit & Push
```bash
git add <files-in-your-task>
git commit -m "feat(fe-04): implement button, input, badge and kitchen sink demo"
git push origin feature/FE-04-ui-component-kit
```

### Step 5: Open a Pull Request
- Target branch: `main`
- Fill in the PR template with screenshots or test logs.
- Tag your reviewer and lead.
