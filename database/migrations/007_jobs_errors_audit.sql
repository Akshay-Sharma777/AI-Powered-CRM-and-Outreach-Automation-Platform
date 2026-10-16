-- Migration: 007_jobs_errors_audit.sql
-- Description: Creates automation_jobs, automation_errors, and immutable audit_logs tables

BEGIN;

CREATE TABLE IF NOT EXISTS automation_jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workflow VARCHAR(100) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'running' CHECK (status IN ('running', 'completed', 'failed', 'retrying')),
    correlation_id VARCHAR(100) NOT NULL,
    started_at TIMESTAMPTZ NOT NULL DEFAULT (NOW() AT TIME ZONE 'UTC'),
    finished_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_jobs_correlation ON automation_jobs (correlation_id);
CREATE INDEX IF NOT EXISTS idx_jobs_status ON automation_jobs (status, started_at DESC);

CREATE TABLE IF NOT EXISTS automation_errors (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_id UUID REFERENCES automation_jobs(id) ON DELETE SET NULL,
    workflow VARCHAR(100) NOT NULL,
    failed_step VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL CHECK (category IN (
        'temporary_network', 'rate_limit', 'invalid_input', 'expired_credential',
        'credit_exhaustion', 'source_layout_changed', 'ai_output_invalid',
        'send_timeout', 'permanent_provider_rejection'
    )),
    redacted_message TEXT NOT NULL,
    retry_count INTEGER NOT NULL DEFAULT 0,
    next_retry_at TIMESTAMPTZ,
    owner VARCHAR(100) NOT NULL DEFAULT 'unassigned',
    replay_eligible BOOLEAN NOT NULL DEFAULT TRUE,
    ai_suggestion TEXT,
    resolution_notes TEXT,
    status VARCHAR(50) NOT NULL DEFAULT 'open' CHECK (status IN ('open', 'retrying', 'resolved', 'ignored')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT (NOW() AT TIME ZONE 'UTC'),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT (NOW() AT TIME ZONE 'UTC')
);

CREATE INDEX IF NOT EXISTS idx_errors_status_retry ON automation_errors (status, next_retry_at);
CREATE INDEX IF NOT EXISTS idx_errors_category ON automation_errors (category);

-- Immutable audit logs table: strictly append-only (no update/delete)
CREATE TABLE IF NOT EXISTS audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    actor VARCHAR(255) NOT NULL,
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(100) NOT NULL,
    entity_id VARCHAR(255) NOT NULL,
    details JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT (NOW() AT TIME ZONE 'UTC')
);

CREATE INDEX IF NOT EXISTS idx_audit_entity ON audit_logs (entity_type, entity_id);
CREATE INDEX IF NOT EXISTS idx_audit_actor ON audit_logs (actor, created_at DESC);

COMMIT;
