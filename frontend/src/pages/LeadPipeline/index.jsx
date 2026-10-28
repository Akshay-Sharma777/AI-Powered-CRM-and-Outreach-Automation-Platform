import React, { useState, useMemo } from 'react'
import { LeadTable } from './LeadTable'
import { LeadFilters } from './LeadFilters'
import {
  createDefaultFilters,
  readFiltersFromUrl,
} from '../../store/filters'
import { Button } from '../../components/ui/Button'
import { MOCK_LEADS } from '../../mocks/sampleLeads'

/**
 * Lead Pipeline page.
 * FE-09: table now fetches/pages/sorts itself via the server-side API.
 * FE-10: filters and search controls with URL parameter synchronization.
 * FE-11: preview panel is a placeholder and will be replaced by the drawer.
 */
export default function LeadPipelinePage({ currentUser }) {
  const [filters, setFilters] = useState(() => readFiltersFromUrl())
  const [appliedSearch, setAppliedSearch] = useState(() => filters.search)
  const [selectedLeadId, setSelectedLeadId] = useState(null)
  const [refreshKey, setRefreshKey] = useState(0)

  const tableFilters = useMemo(() => {
    return {
      search: filters.search || '',
      score_band: filters.scoreBand === 'all' ? '' : filters.scoreBand,
      status: filters.status === 'all' ? '' : filters.status,
      assigned_to: filters.assignedTo === 'all' ? '' : filters.assignedTo,
      source: filters.sources?.length === 1 ? filters.sources[0] : (filters.sources?.length > 1 ? filters.sources.join(',') : ''),
      experience_min: filters.experienceMin,
      experience_max: filters.experienceMax,
      ...filters,
    }
  }, [filters])

  return (
    <div
      style={{
        padding: '24px',
        display: 'flex',
        flexDirection: 'column',
        gap: '20px',
        minWidth: 0,
        maxWidth: '100%',
      }}
    >
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          flexWrap: 'wrap',
          gap: '12px',
        }}
      >
        <div>
          <h1 style={{ fontSize: '22px', fontWeight: 700 }}>Lead Pipeline & Discovery</h1>
          <p style={{ fontSize: '13px', color: 'var(--color-text-muted)' }}>
            Daily scraped 0-2 yr fresher opportunities across verified platforms.
          </p>
        </div>
        <Button variant="secondary" onClick={() => setRefreshKey((k) => k + 1)}>
          ↻ Refresh
        </Button>
      </div>

      {/* Filter Bar (FE-10) */}
      <LeadFilters
        leads={MOCK_LEADS}
        filters={filters}
        onFiltersChange={setFilters}
        onSearchChange={setAppliedSearch}
        onClear={() => {
          const defaults = createDefaultFilters()
          setFilters(defaults)
          setAppliedSearch('')
        }}
      />

      <LeadTable
        filters={tableFilters}
        currentUserId={currentUser?.id}
        selectedId={selectedLeadId}
        refreshKey={refreshKey}
        onSelect={(leadId) => setSelectedLeadId(leadId)}
      />

      {/* Placeholder until the FE-11 Lead Detail Drawer exists */}
      {selectedLeadId && (
        <div
          style={{
            backgroundColor: 'var(--color-bg-surface)',
            padding: '20px',
            borderRadius: 'var(--radius-md)',
            border: '1px solid var(--color-border)',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
          }}
        >
          <div style={{ fontSize: '14px' }}>
            Lead selected: <code>{selectedLeadId}</code> — detail drawer arrives in FE-11.
          </div>
          <button
            onClick={() => setSelectedLeadId(null)}
            aria-label="Close preview"
            style={{ background: 'none', border: 'none', cursor: 'pointer' }}
          >
            ✕
          </button>
        </div>
      )}
    </div>
  )
}

