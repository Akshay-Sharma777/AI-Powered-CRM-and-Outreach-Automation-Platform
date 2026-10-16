-- Migration: 003_opportunities_contacts.sql
-- Description: Creates opportunities, contacts, contact_methods, and opportunity_contacts link table

BEGIN;

CREATE TABLE IF NOT EXISTS opportunities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL CHECK (type IN ('job', 'startup', 'internship', 'hackathon', 'college')),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    experience_min INTEGER,
    experience_max INTEGER,
    salary_text TEXT,
    location VARCHAR(255),
    source_id VARCHAR(50) NOT NULL REFERENCES sources(id) ON DELETE RESTRICT,
    source_url TEXT NOT NULL,
    source_identifier VARCHAR(255) NOT NULL,
    published_at TIMESTAMPTZ,
    discovered_at TIMESTAMPTZ NOT NULL DEFAULT (NOW() AT TIME ZONE 'UTC'),
    extraction_details JSONB NOT NULL DEFAULT '{}'::jsonb,
    source_confidence INTEGER NOT NULL DEFAULT 100,
    status VARCHAR(50) NOT NULL DEFAULT 'new' CHECK (status IN ('new', 'needs_enrichment', 'verified', 'draft_ready', 'approved', 'sent', 'closed')),
    assigned_to UUID REFERENCES users(id) ON DELETE SET NULL,
    claimed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT (NOW() AT TIME ZONE 'UTC'),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT (NOW() AT TIME ZONE 'UTC')
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_opp_source_identifier ON opportunities (source_id, source_identifier);
CREATE UNIQUE INDEX IF NOT EXISTS idx_opp_source_url ON opportunities (source_url);
CREATE INDEX IF NOT EXISTS idx_opp_status ON opportunities (status);
CREATE INDEX IF NOT EXISTS idx_opp_discovered_at ON opportunities (discovered_at DESC);
CREATE INDEX IF NOT EXISTS idx_opp_assigned_to ON opportunities (assigned_to);
CREATE INDEX IF NOT EXISTS idx_opp_org ON opportunities (organization_id);

CREATE TABLE IF NOT EXISTS contacts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    role_title VARCHAR(255),
    created_at TIMESTAMPTZ NOT NULL DEFAULT (NOW() AT TIME ZONE 'UTC'),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT (NOW() AT TIME ZONE 'UTC')
);

CREATE INDEX IF NOT EXISTS idx_contacts_org ON contacts (organization_id);

CREATE TABLE IF NOT EXISTS contact_methods (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    contact_id UUID NOT NULL REFERENCES contacts(id) ON DELETE CASCADE,
    kind VARCHAR(50) NOT NULL CHECK (kind IN ('email', 'phone', 'linkedin_url')),
    value TEXT NOT NULL,
    provenance TEXT,
    verified_status VARCHAR(50) NOT NULL DEFAULT 'unknown' CHECK (verified_status IN ('deliverable', 'undeliverable', 'catch_all', 'risky', 'unknown', 'failed')),
    verified_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT (NOW() AT TIME ZONE 'UTC')
);

CREATE INDEX IF NOT EXISTS idx_contact_methods_kind_val ON contact_methods (kind, value);
CREATE INDEX IF NOT EXISTS idx_contact_methods_contact_id ON contact_methods (contact_id);

CREATE TABLE IF NOT EXISTS opportunity_contacts (
    opportunity_id UUID NOT NULL REFERENCES opportunities(id) ON DELETE CASCADE,
    contact_id UUID NOT NULL REFERENCES contacts(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT (NOW() AT TIME ZONE 'UTC'),
    PRIMARY KEY (opportunity_id, contact_id)
);

COMMIT;
