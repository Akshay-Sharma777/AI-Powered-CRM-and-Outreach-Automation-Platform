# Event & Webhook Contracts

This document specifies the exact JSON schemas and header conventions for asynchronous events, webhooks, and automation triggers across n8n, scrapers, and FastAPI backend services.

---

## 1. Scraper Ingestion Webhook

- **Endpoint**: `POST /api/v1/webhooks/scraper-ingest`
- **Authentication**: `X-Scraper-Secret: <SCRAPER_INGEST_SECRET>` header
- **Trigger**: Sent by n8n scheduled workflow or scraper runner at batch completion.
- **Constraints**: Maximum 200 items per batch payload.

### Request Body Schema
```json
{
  "source_id": "internshala",
  "batch_id": "batch_20261016_090000",
  "items": [
    {
      "source_identifier": "int-98124",
      "source_url": "https://internshala.com/internship/detail/python-intern-98124",
      "company_name": "Acme Robotics",
      "title": "Junior Python Developer Intern",
      "description": "Looking for freshers with basic Python knowledge...",
      "opportunity_type": "internship",
      "experience_text": "0-1 yrs",
      "salary_text": "₹25,000 /month",
      "location": "Bengaluru (Hybrid)",
      "published_at": "2026-10-15T08:30:00Z"
    }
  ]
}
```

### Success Response (`200 OK`)
```json
{
  "inserted": 42,
  "updated": 3,
  "skipped": 5,
  "rejected": 0
}
```

---

## 2. Provider Callback Webhook (Email Delivery & Engagement)

- **Endpoint**: `POST /api/v1/callbacks`
- **Authentication**: `X-Provider-Signature: <HMAC_SHA256>`
- **Timestamp check**: Must be within 5 minutes of current server UTC.
- **Allowed event types**: `delivered`, `opened`, `clicked`, `replied`, `bounce`, `unsubscribe`

### Request Body Schema
```json
{
  "provider": "resend",
  "provider_event_id": "evt_abc123456789",
  "event_type": "replied",
  "occurred_at": "2026-10-16T12:00:00Z",
  "provider_message_id": "msg_987654321",
  "recipient": "hr@acmerobotics.example.com",
  "payload": {
    "reply_subject": "Re: Collaboration opportunity",
    "bounce_code": null,
    "bounce_reason": null
  }
}
```

### Core Logic Triggered:
- If `event_type == 'bounce'` (hard bounce) or `'unsubscribe'`:
  - Automatically insert into `suppression_entries`.
  - Automatically cancel all pending follow-up messages for this recipient.

---

## 3. Automation Error Webhook (Error Center)

- **Endpoint**: `POST /api/v1/guardrails/error-webhook`
- **Authentication**: `X-Error-Secret: <GUARDRAIL_SECRET>`
- **Source**: Triggered by n8n `global_error_workflow.json` or scraper failure wrapper.

### Request Body Schema
```json
{
  "workflow": "daily_discovery",
  "job_id": "job_20261016_01",
  "correlation_id": "corr_c8f2b730-811c",
  "failed_step": "fetch_naukri_listings",
  "category": "rate_limit", 
  "redacted_message": "HTTP 429 Too Many Requests received from target source",
  "retry_count": 2,
  "next_retry_at": "2026-10-16T14:30:00Z",
  "owner": "automation",
  "replay_eligible": true,
  "payload_snapshot": {
    "source": "naukri",
    "page": 3
  }
}
```

### Categories Supported:
- `temporary_network`
- `rate_limit`
- `invalid_input`
- `expired_credential`
- `credit_exhaustion`
- `source_layout_changed`
- `ai_output_invalid`
- `send_timeout` (marked `replay_eligible = false`)
- `provider_rejection` (marked `replay_eligible = false`)
