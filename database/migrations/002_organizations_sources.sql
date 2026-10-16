-- Migration: 002_organizations_sources.sql
-- Description: Creates organizations and approved sources tables

BEGIN;

CREATE TABLE IF NOT EXISTS organizations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    normalized_name VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL CHECK (type IN ('company', 'startup', 'college', 'organiser')),
    domain VARCHAR(255),
    website TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT (NOW() AT TIME ZONE 'UTC'),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT (NOW() AT TIME ZONE 'UTC')
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_org_normalized_domain 
ON organizations (normalized_name, COALESCE(domain, ''));

CREATE INDEX IF NOT EXISTS idx_organizations_type ON organizations (type);

CREATE TABLE IF NOT EXISTS sources (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    base_url TEXT NOT NULL,
    is_enabled BOOLEAN NOT NULL DEFAULT FALSE,
    permitted_use_note TEXT,
    status VARCHAR(50) NOT NULL DEFAULT 'healthy' CHECK (status IN ('healthy', 'quarantined', 'disabled', 'rate_limited')),
    last_run_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT (NOW() AT TIME ZONE 'UTC')
);

CREATE INDEX IF NOT EXISTS idx_sources_status ON sources (status, is_enabled);

COMMIT;
