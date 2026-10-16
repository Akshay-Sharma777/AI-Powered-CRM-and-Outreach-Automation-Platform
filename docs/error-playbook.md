# Automation & System Error Playbook

Automations, web scrapers, and external APIs will inevitably encounter failures. This playbook outlines the failure taxonomy, required automated handling, and operational procedures for the Error Center.

---

## 1. Error Classification & Handling Matrix

| Failure Category | Root Cause | Automated Handling | Replay Eligible? |
| :--- | :--- | :--- | :--- |
| **temporary_network** | DNS blip, connection reset, 502/503 | Retry with bounded exponential backoff & jitter (max 3) | **Yes** |
| **rate_limit** | HTTP 429 from source or provider | Pause and reschedule after cooldown window | **Yes** |
| **invalid_input** | Missing required fields, schema mismatch | Stop immediate execution; log validation error; do not auto-retry | **No** (Fix payload first) |
| **expired_credential**| API key rotated or expired token | Pause affected integration, log high-priority alert to Admin | **Yes** (After key updated) |
| **credit_exhaustion** | ContactOut / Snov credit limit reached | Stop all paid lookups immediately, notify owner | **Yes** (After budget reset) |
| **source_layout_changed**| Target HTML altered, selector broke | Quarantine source output, trigger AI selector suggestion | **No** (Developer updates selector) |
| **ai_output_invalid** | Model output failed schema or fact-check | Retry generation once with error prompt; if failing again, route to manual review | **Yes** |
| **send_timeout** | Socket timeout during provider dispatch | Reconcile message status with provider API before any retry. **NEVER BLINDLY RESEND!** | **No** (Manual check required) |
| **provider_rejection**| Hard bounce, invalid recipient address | Record event, add to `suppression_entries`, cancel pending follow-ups | **No** |

---

## 2. Redaction & Privacy Guardrails

Before any error payload or stack trace is written to `automation_errors` or sent to the Error Webhook:
1. **Passwords, Tokens, API Keys**: Regex-redacted to `[REDACTED_SECRET]`.
2. **Personal Emails & Phone Numbers**: Masked in error messages (e.g. `j***@example.com`).
3. **Database Credentials**: Stripped from any PostgreSQL exception strings.

---

## 3. The Error Center Operational Flow

1. Any failed n8n node or scraper error triggers the `global_error_workflow.json`.
2. The workflow POSTs the error context to `/api/v1/guardrails/error-webhook`.
3. Backend records an entry in `automation_errors`.
4. (Optional) Backend calls AI diagnostics to populate `ai_suggestion`.
5. An engineer or researcher inspects the Error Center dashboard:
   - Views the redacted stack trace and payload snapshot.
   - For replay-eligible transient errors, clicks **Replay**.
   - Note: Dispatch send errors are strictly non-replayable without reconciliation.
