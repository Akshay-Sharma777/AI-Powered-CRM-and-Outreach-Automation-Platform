# System Architecture & Technical Specifications

This document defines the high-level architecture and free-tier deployment design for the **AI-Powered Lead Intelligence, CRM & Outreach Automation Platform** (based on PRD Version 1.0).

---

## 1. Executive Summary & Core Principles

The platform identifies freshers (0-1 and 0-2 year) and student-focused opportunities (internships, hackathons, college recruitment), stores them in a centralized PostgreSQL CRM, supports human-gated contact enrichment, performs email deliverability verification, calculates explainable data quality scores, and drafts verified outreach via Gemini Flash.

### Foundational Principles:
1. **Free-Tier First**: The MVP operates entirely on free services (Cloudflare Pages, Oracle Cloud Always Free VM, Neon Free PostgreSQL, Gemini Flash free tier).
2. **Collect Approved Data Only**: Respect `robots.txt` and terms of service. Disallow unauthorized scraping (e.g. LinkedIn, WhatsApp bots).
3. **Strict Human-in-the-Loop**: No email is ever sent automatically without explicit Campaign Manager approval.
4. **Explainable Scoring**: Every lead gets a 0–100 score based on 5 rule-driven factors and explicit reason codes.
5. **Traceability & Auditability**: Full provenance of sources, immutable audit trails, and correlation IDs across all requests.
6. **Zero ORM Overhead**: Direct, parameterised SQL with connection pooling via `psycopg` and `psycopg_pool`.

---

## 2. Five-Stage Operational Workflow

```
[1. Lead Discovery] ---> [2. Contact Enrichment] ---> [3. Verification & Scoring] ---> [4. AI Draft (Gemini)] ---> [5. Human Approval & Dispatch]
  - n8n + Playwright       - Manual trigger only      - Deliverability test (API)     - Verified facts only       - Manager approves exact body
  - Approved sources       - Paid credit budgeting    - 0-100 score with codes        - Strict anti-hallucination - Idempotency & suppression check
```

### Stage 1: Lead Discovery (Automated Daily)
- Scrapes/crawls approved entry-level opportunities (Internshala, Naukri, Apna, WorkIndia, Shine, College TPO directories, hackathon portals).
- Ingests data through `POST /api/v1/webhooks/scraper-ingest` with duplicate detection.

### Stage 2: Cost-Controlled Contact Enrichment (Manual)
- Because enrichment APIs (ContactOut, Snov.io) consume paid credits, lookups are triggered on-demand via the React UI.
- Quotas and daily/monthly credit limits are strictly enforced.

### Stage 3: Verification & Data Quality Gate
- Verifies email address validity (deliverable, undeliverable, catch-all, risky).
- Generates a **0–100 Confidence Score** across 5 factors:
  - Source reliability (max 25)
  - Organization & contact association (max 25)
  - Verification evidence (max 20)
  - Data freshness (max 15)
  - Completeness & consistency (max 15)
- **Score Bands**:
  - `80–100`: High confidence (Eligible for outreach campaign)
  - `60–79`: Medium confidence (Requires researcher review)
  - `< 60`: Low confidence (Held or rejected)
  - `Suppressed`: Never eligible for outreach.

### Stage 4: AI-Assisted Message Drafting (Gemini Flash)
- Gemini Flash takes verified facts and produces a personalized email draft adhering to the `draft_output` schema.
- Anti-hallucination rule: The model must cite fact IDs for all claims and cannot invent compensation, job titles, or connections.

### Stage 5: Human Approval & Controlled Dispatch
- Campaign Manager reviews exact subject, body, and recipient.
- On approval, a cryptographic hash (`content_hash`) is generated.
- Backend runs pre-send checks: suppression verification, daily limits, budget, and idempotency key before dispatch.

---

## 3. Free-Tier Hosting Topology

| Component | Provider / Tier | Deployment Description |
| :--- | :--- | :--- |
| **Frontend CRM** | Cloudflare Pages (Free) | Static Vite + React SPA deployed directly from Git |
| **Backend API** | Oracle Cloud Always Free VM | Docker container running FastAPI with Uvicorn |
| **Database** | Neon PostgreSQL (Free) | Managed remote serverless PostgreSQL with direct SQL pooling |
| **Automation** | Oracle Cloud Always Free VM | Self-hosted n8n Community Edition in Docker with persistent volume |
| **Scraper Worker**| Oracle Cloud Always Free VM | Playwright worker executing within bounded concurrency (max 2) |
| **Reverse Proxy** | Caddy (Docker) | Automatic TLS provisioning & reverse proxy for ports 80/443 |
| **AI Engine** | Google Gemini API (Flash) | Fast, structured JSON generation under free tier quotas |

---

## 4. Security & Compliance Guardrails

- **No LinkedIn Automation**: No automated LinkedIn profile extraction, connection requests, or InMail bots.
- **No WhatsApp Bots**: Unofficial WhatsApp tools are strictly excluded to avoid phone number bans.
- **Suppression Management**: Immediate unsubscriptions and bounce handling to preserve email sender reputation.
- **Rate & Concurrency Limiting**: Playwright concurrency capped at 2 to preserve Oracle VM RAM and CPU.
