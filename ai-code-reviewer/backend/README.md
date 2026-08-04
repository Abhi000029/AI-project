# AI Code Reviewer — Backend

FastAPI + MongoDB (Motor) backend implementing the P0 features from the PRD:
FR-1 (PR ingestion), FR-2 (AI analysis engine), FR-3 (structured feedback),
FR-4 (rule configuration), FR-5 (analytics dashboard).

## Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env`:
- `MONGODB_URI` — point at a local `mongod` or a MongoDB Atlas connection string.
- `ANTHROPIC_API_KEY` — your Anthropic API key (used by the review engine).

## Run MongoDB locally (if you don't already have it)

```bash
docker run -d --name ai-reviewer-mongo -p 27017:27017 mongo:7
```

## Run the API

```bash
uvicorn app.main:app --reload --port 8000
```

API docs: http://localhost:8000/docs

## Endpoints

| Method | Path | Purpose |
|---|---|---|
| POST | `/api/v1/reviews/analyze` | Submit a PR diff for AI review |
| GET | `/api/v1/reviews/{review_id}` | Get a review + its findings |
| GET | `/api/v1/reviews` | List recent reviews |
| GET | `/api/v1/analytics/dashboard` | Aggregate dashboard metrics |
| POST | `/api/v1/config/rules` | Create/update a review rule |
| GET | `/api/v1/config/rules` | List rules for an org |
| DELETE | `/api/v1/config/rules/{rule_id}` | Delete a rule |
| GET | `/api/v1/health` | Health check |

## Example request

```bash
curl -X POST http://localhost:8000/api/v1/reviews/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "repo_full_name": "acme/webapp",
    "pr_number": 42,
    "pr_title": "Add user auth endpoint",
    "author": "priya",
    "language": "python",
    "diff": "diff --git a/auth.py b/auth.py\n+password = request.args.get(\"password\")\n+if password == stored_password:\n+    return login_user()\n"
  }'
```
