-- Migration: 005_campaigns_drafts_approvals.sql
-- Description: Creates campaigns, campaign_drafts, and approvals tables

BEGIN;

CREATE TABLE IF NOT EXISTS campaigns (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    purpose TEXT NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'draft' CHECK (status IN ('draft', 'active', 'paused', 'completed')),
    daily_limit INTEGER NOT NULL DEFAULT 50,
    created_by UUID NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT (NOW() AT TIME ZONE 'UTC'),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT (NOW() AT TIME ZONE 'UTC')
);

CREATE INDEX IF NOT EXISTS idx_campaigns_status ON campaigns (status);

CREATE TABLE IF NOT EXISTS campaign_drafts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    campaign_id UUID NOT NULL REFERENCES campaigns(id) ON DELETE CASCADE,
    opportunity_id UUID NOT NULL REFERENCES opportunities(id) ON DELETE CASCADE,
    recipient_contact_method_id UUID NOT NULL REFERENCES contact_methods(id) ON DELETE RESTRICT,
    model VARCHAR(100) NOT NULL,
    prompt_version VARCHAR(50) NOT NULL,
    input_refs JSONB NOT NULL DEFAULT '{}'::jsonb,
    ai_output JSONB NOT NULL,
    edited_subject TEXT,
    edited_body TEXT,
    status VARCHAR(50) NOT NULL DEFAULT 'generated' CHECK (status IN ('generated', 'needs_review', 'approved', 'rejected', 'sent')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT (NOW() AT TIME ZONE 'UTC'),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT (NOW() AT TIME ZONE 'UTC')
);

CREATE INDEX IF NOT EXISTS idx_drafts_campaign ON campaign_drafts (campaign_id, status);
CREATE INDEX IF NOT EXISTS idx_drafts_opp ON campaign_drafts (opportunity_id);

CREATE TABLE IF NOT EXISTS approvals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    draft_id UUID NOT NULL REFERENCES campaign_drafts(id) ON DELETE CASCADE,
    approved_by UUID NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    recipient TEXT NOT NULL,
    content_hash VARCHAR(64) NOT NULL,
    approved_at TIMESTAMPTZ NOT NULL DEFAULT (NOW() AT TIME ZONE 'UTC'),
    revoked_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_approvals_draft ON approvals (draft_id);
CREATE INDEX IF NOT EXISTS idx_approvals_hash ON approvals (content_hash);

COMMIT;
