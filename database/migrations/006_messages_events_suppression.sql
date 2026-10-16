-- Migration: 006_messages_events_suppression.sql
-- Description: Creates outreach_messages, message_events, and suppression_entries tables

BEGIN;

CREATE TABLE IF NOT EXISTS outreach_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    draft_id UUID NOT NULL REFERENCES campaign_drafts(id) ON DELETE RESTRICT,
    approval_id UUID NOT NULL REFERENCES approvals(id) ON DELETE RESTRICT,
    recipient TEXT NOT NULL,
    idempotency_key VARCHAR(128) UNIQUE NOT NULL,
    provider VARCHAR(50) NOT NULL,
    provider_message_id VARCHAR(255),
    status VARCHAR(50) NOT NULL DEFAULT 'sent' CHECK (status IN ('queued', 'sent', 'failed', 'cancelled')),
    sent_at TIMESTAMPTZ NOT NULL DEFAULT (NOW() AT TIME ZONE 'UTC')
);

CREATE INDEX IF NOT EXISTS idx_outreach_recipient ON outreach_messages (recipient);
CREATE INDEX IF NOT EXISTS idx_outreach_status ON outreach_messages (status, sent_at DESC);

CREATE TABLE IF NOT EXISTS message_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    message_id UUID NOT NULL REFERENCES outreach_messages(id) ON DELETE CASCADE,
    provider_event_id VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL CHECK (type IN ('delivered', 'opened', 'clicked', 'replied', 'bounce', 'unsubscribe')),
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    occurred_at TIMESTAMPTZ NOT NULL DEFAULT (NOW() AT TIME ZONE 'UTC')
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_events_provider_event ON message_events (provider_event_id);
CREATE INDEX IF NOT EXISTS idx_events_message ON message_events (message_id, type);

CREATE TABLE IF NOT EXISTS suppression_entries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    value VARCHAR(255) NOT NULL,
    kind VARCHAR(20) NOT NULL CHECK (kind IN ('email', 'domain')),
    reason TEXT NOT NULL,
    source VARCHAR(50) NOT NULL DEFAULT 'manual' CHECK (source IN ('manual', 'bounce', 'unsubscribe', 'admin')),
    created_by UUID REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT (NOW() AT TIME ZONE 'UTC')
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_suppression_val_kind ON suppression_entries (LOWER(value), kind);

COMMIT;
