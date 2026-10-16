-- Migration: 004_enrichment_verification_scores.sql
-- Description: Creates enrichment_requests, verification_results, and data_quality_scores tables

BEGIN;

CREATE TABLE IF NOT EXISTS enrichment_requests (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    opportunity_id UUID REFERENCES opportunities(id) ON DELETE SET NULL,
    provider VARCHAR(50) NOT NULL CHECK (provider IN ('contactout', 'snov', 'manual')),
    requested_by UUID NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    credits_estimated INTEGER NOT NULL DEFAULT 1,
    credits_used INTEGER NOT NULL DEFAULT 0,
    status VARCHAR(50) NOT NULL DEFAULT 'completed' CHECK (status IN ('pending', 'completed', 'failed', 'budget_exceeded')),
    result_summary TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT (NOW() AT TIME ZONE 'UTC')
);

CREATE INDEX IF NOT EXISTS idx_enrichment_created ON enrichment_requests (created_at DESC);
CREATE INDEX IF NOT EXISTS idx_enrichment_user ON enrichment_requests (requested_by);

CREATE TABLE IF NOT EXISTS verification_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    contact_method_id UUID NOT NULL REFERENCES contact_methods(id) ON DELETE CASCADE,
    result VARCHAR(50) NOT NULL CHECK (result IN ('deliverable', 'undeliverable', 'catch_all', 'risky', 'unknown', 'failed')),
    raw_response JSONB DEFAULT '{}'::jsonb,
    checked_at TIMESTAMPTZ NOT NULL DEFAULT (NOW() AT TIME ZONE 'UTC')
);

CREATE INDEX IF NOT EXISTS idx_verification_contact_method ON verification_results (contact_method_id, checked_at DESC);

CREATE TABLE IF NOT EXISTS data_quality_scores (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    opportunity_id UUID NOT NULL REFERENCES opportunities(id) ON DELETE CASCADE,
    score INTEGER NOT NULL CHECK (score >= 0 AND score <= 100),
    band VARCHAR(20) NOT NULL CHECK (band IN ('high', 'medium', 'low', 'suppressed')),
    reasons JSONB NOT NULL DEFAULT '[]'::jsonb,
    factor_breakdown JSONB NOT NULL DEFAULT '{}'::jsonb,
    scoring_version VARCHAR(20) NOT NULL DEFAULT '1.0.0',
    scored_at TIMESTAMPTZ NOT NULL DEFAULT (NOW() AT TIME ZONE 'UTC')
);

CREATE INDEX IF NOT EXISTS idx_quality_scores_opp ON data_quality_scores (opportunity_id, scored_at DESC);
CREATE INDEX IF NOT EXISTS idx_quality_scores_band ON data_quality_scores (band, score);

COMMIT;
