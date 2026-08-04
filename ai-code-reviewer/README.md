# AI Code Reviewer

A working MVP of the AI Code Reviewer PRD: a full-stack app that runs an AI-powered
multi-dimensional review (bugs, security, performance, style, best practices) against a
pull-request diff and stores results in MongoDB.

```
├── backend/     FastAPI + MongoDB (Motor) + Anthropic API review engine
├── frontend/    React + TypeScript + Tailwind
└── docker-compose.yml
```

## What's implemented (P0/P1 from the PRD)

| PRD Requirement | Status |
|---|---|
| FR-1 PR ingestion (diff submission) | ✅ manual submission form; webhook receiver is the next step |
| FR-2 AI multi-dimensional analysis engine | ✅ `backend/app/services/ai_reviewer.py` |
| FR-3 Structured, actionable feedback (severity, suggestions) | ✅ |
| FR-4 Rule configuration | ✅ `/api/v1/config/rules` |
| FR-5 Analytics dashboard | ✅ `/api/v1/analytics/dashboard` + charts |
| FR-6 Slack/email notifications | ⬜ not built (P2, out of MVP scope) |
| GitHub/GitLab/Bitbucket live webhooks | ⬜ the `/analyze` endpoint is what a webhook handler would call — wiring the actual webhook receiver + signature verification is the next step |

## Quick start (Docker — recommended)

```bash
export ANTHROPIC_API_KEY=sk-ant-...
docker compose up --build
```

- Frontend: http://localhost:5173
- Backend API docs: http://localhost:8000/docs
- MongoDB: localhost:27017

## Quick start (manual)

**1. MongoDB**
```bash
docker run -d -p 27017:27017 mongo:7
```

**2. Backend**
```bash
cd backend
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # set ANTHROPIC_API_KEY
uvicorn app.main:app --reload --port 8000
```

**3. Frontend**
```bash
cd frontend
npm install
npm run dev
```
Visit http://localhost:5173.

## How it works

1. The **Review** tab lets you paste a unified diff (this is what a GitHub/GitLab/Bitbucket
   webhook would deliver automatically in production — the payload shape is the same).
2. The backend sends the diff to Claude with a system prompt (FR-2/FR-3) that returns strict
   JSON: a quality score, a summary, and a list of findings (file, line, severity, category,
   message, fix suggestion).
3. Findings and the review record are persisted to MongoDB (`reviews`, `findings` collections).
4. The **Dashboard** tab aggregates that data: total reviews, average score, severity/category
   breakdowns, and recent activity — via MongoDB aggregation pipelines.

## MongoDB collections

Matches the PRD data model (§6.4): `reviews`, `findings`, `rules` are implemented now.
`users`, `organizations`, `repositories`, `pull_requests` are modeled in
`backend/app/models.py` conceptually but not yet given their own collections/endpoints —
add these when you wire up real auth and webhook ingestion.

## Notes / what to build next

- **Webhook receivers**: add `POST /webhooks/github`, `/webhooks/gitlab`, `/webhooks/bitbucket`
  that verify signatures, extract the diff via each provider's API, and call the same
  `analyze_diff` service.
- **Auth**: no auth layer yet (SSO/SAML/OAuth from NFR-2 is not implemented).
- **Rule enforcement**: rules are stored (FR-4) but not yet fed into the AI prompt or used to
  filter findings/block merges — join `rules` into `ai_reviewer.py` before generating findings.
- This sandbox has no outbound network access, so `npm install` and live MongoDB/Anthropic
  calls were not run here — the code is written and reviewed for correctness, but you should
  do a first local run to catch any environment-specific issues.
