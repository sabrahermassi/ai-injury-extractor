# CLAUDE.md

Guidance for working in this repository.

## Project Purpose

AI Injury Extractor is a demo serverless application that turns a free-text
injury description (e.g. "I hurt my left knee doing squats two weeks ago,
pain is 6/10") into structured JSON (injury name, body area, pain level,
symptoms, possible causes) using an LLM, and stores/retrieves those entries.
It's explicitly built as a portfolio/demo piece showing an end-to-end
serverless AWS stack, and is designed to later be embedded as a component
inside a larger injury-tracking application (which would own auth and a
relational DB).

## Architecture

```
Next.js frontend (frontend/)
        │  fetch(NEXT_PUBLIC_API_URL + "/extract" | "/injuries")
        ▼
API Gateway (REGIONAL REST API, "dev" stage)   [infrastructure/api_gateway.tf]
        │  AWS_PROXY integration
        ▼
Single AWS Lambda "injury-extractor"           [lambda/handler.py]
        │  routes on event.httpMethod (POST → extract, GET → history)
   ┌────┴────┐
   ▼         ▼
Groq API   DynamoDB table "InjuryEntries"
(LLM,      (PK: userId, SK: timestamp)
llama-3.1-8b-instant)
```

All infra is defined in Terraform (`infrastructure/`). There is one Lambda
function that handles both `/extract` (POST) and `/injuries` (GET) via a
manual `httpMethod` switch — there is no framework/router in use.

## Directory Structure

- `frontend/` — Next.js 16 (App Router) + React 19 + Tailwind v4 + shadcn/radix-ui
  components. `src/app/page.tsx` is the single page; `src/components/` holds
  the injury-extractor form, the extraction result card, and the injury
  history list/card. `src/lib/api.ts` is the only place that talks to the
  backend; `src/lib/injury-schema.ts` defines the TS shapes (note: these are
  NOT validated at runtime — the backend response is trusted as-is).
- `lambda/` — Python 3.12 Lambda handler (`handler.py`), `requirements.txt`
  (currently just `groq`), and `deploy.sh` (builds `function.zip` and runs
  `terraform apply`). `venv/` and `package/` are local build artifacts, not
  committed.
- `infrastructure/` — Terraform for API Gateway, the Lambda function, the
  DynamoDB table, and IAM. Single environment ("dev"), no remote state
  backend configured (local `.tfstate`, gitignored).
- `docs/` — design docs (`dynamodb-design.md`, `lambda-design.md`) and
  `ROADMAP.md`, which tracks known future work. These docs are more
  aspirational/explanatory than the README and are a good source of "why"
  for current design choices (e.g. why Scan instead of Query, why a single
  Lambda).

## Tech Stack

- **Frontend**: Next.js 16, React 19, TypeScript, Tailwind CSS v4, shadcn/ui
  components on top of `radix-ui`, `lucide-react` icons.
- **Backend**: Python 3.12 on AWS Lambda, `groq` SDK for LLM calls
  (`llama-3.1-8b-instant`), `boto3` (via the Lambda runtime) for DynamoDB.
- **Infra**: Terraform (`hashicorp/aws` ~> 5.0), API Gateway REST API
  (AWS_PROXY), DynamoDB (pay-per-request, point-in-time recovery on).
- **AI**: Groq is used instead of e.g. OpenAI/Anthropic for extraction
  latency/cost reasons typical of demo projects; prompt asks for raw JSON
  matching a fixed schema, temperature 0.

## Running Locally

### Frontend

```bash
cd frontend
npm install
npm run dev   # http://localhost:3000
```

Requires `NEXT_PUBLIC_API_URL` set (e.g. in `frontend/.env.local`) to the
deployed API Gateway invoke URL (no trailing slash, no path suffix — the
client appends `/extract` and `/injuries` itself). There is currently no
local/mocked backend option — the frontend always calls a real deployed API.

### Backend / Infrastructure

There is no local Lambda emulation in this repo (no SAM/LocalStack setup).
To exercise the backend you deploy it:

```bash
cd lambda
./deploy.sh        # installs deps into package/, zips function.zip, then `terraform apply` in ../infrastructure
```

Requires AWS CLI credentials, Terraform installed, and `TF_VAR_groq_api_key`
(or a `terraform.tfvars`, gitignored) set for the `groq_api_key` Terraform
variable. See root `README.md` for `curl` examples against the deployed
`/extract` and `/injuries` endpoints, plus common `aws`/Terraform operational
commands (tailing logs, updating env vars, etc.).

## Testing

**There is no test suite in this repository** — no Lambda unit tests, no API
integration tests, no frontend component tests. This is a known, tracked gap
(see `docs/ROADMAP.md` "Developer Experience Improvements"). Any change to
`lambda/handler.py` or the frontend should be manually exercised via the
`curl` examples in the README and by running the frontend against a real
deployed API until a test suite exists.

## Conventions

- Lambda handler functions return the full API Gateway proxy response dict
  (`statusCode`, `headers`, `body`) directly — every branch repeats
  `CORS_HEADERS` and a JSON-encoded body; there is no shared response helper.
- Error handling in `handler.py` is broad `except Exception` blocks per
  function that log via `print(...)` and return a generic 500 — no
  distinction between e.g. a Groq failure, a malformed LLM response, and a
  DynamoDB failure.
- Frontend API responses are trusted as-is; `src/lib/injury-schema.ts` types
  are not enforced/validated at runtime (no zod/schema validation).
- `userId` is currently hardcoded to `"test-user-001"` everywhere (no auth
  yet) — this is intentional per the docs (auth is meant to be owned by a
  future consuming application) but means `/injuries` currently returns
  every stored entry to every caller.
- Frontend components favor shadcn primitives in `src/components/ui/` with
  small local composition components (`Field`, `BadgeList`) duplicated
  between `extraction-result.tsx` and `injury-history-card.tsx` rather than
  shared.

## Known Constraints / Gotchas

- `/injuries` (GET) and `/extract` (POST) are both unauthenticated by
  design for this dev/demo repo — see the "Integration" section of the
  README. Do not treat this as accidental, but also do not assume it's safe
  to point this at a real deployment with real user data without adding auth
  first.
- CORS is hardcoded to `http://localhost:3000` in both `lambda/handler.py`
  and `infrastructure/api_gateway.tf` (the OPTIONS mock integration
  response) — a deployed frontend on any other origin will be blocked by
  CORS until this is parameterized.
- `get_injury_history()` uses an unpaginated `table.scan()` — for a table
  beyond ~1MB of items this silently returns only a partial result set (no
  `LastEvaluatedKey` handling), and results are not explicitly sorted by
  timestamp.
- The Groq model name (`llama-3.1-8b-instant`) is hardcoded in
  `handler.py` rather than read from an environment variable, even though
  `docs/ROADMAP.md` already flags this as needed (deprecated models get
  retired by providers periodically).
- There's no schema/type validation on the LLM's JSON output beyond
  checking the five keys are present — a malformed `pain_level` (e.g. a
  string, or out of 0–10 range) or non-array `symptoms`/`possible_causes`
  will be stored and served as-is.
- Terraform has no remote state backend configured — state is local-only
  (gitignored), so it isn't shared across machines/collaborators.
