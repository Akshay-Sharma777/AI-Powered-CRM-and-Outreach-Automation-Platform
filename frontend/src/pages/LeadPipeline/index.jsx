import React, { useState, useEffect } from 'react'
import { LeadTable } from './LeadTable'
import { Input, Select } from '../../components/ui/Input'
import { Button } from '../../components/ui/Button'

/**
 * Lead Pipeline page.
 * FE-09: table now fetches/pages/sorts itself via the server-side API.
 * The search + score-band controls below are TEMPORARY and are replaced by FE-10;
 * the preview panel is a placeholder and is replaced by the FE-11 drawer.
 */
export default function LeadPipelinePage({ currentUser }) {
  const [search, setSearch] = useState('')
  const [debouncedSearch, setDebouncedSearch] = useState('')
  const [scoreBand, setScoreBand] = useState('all')
  const [selectedLeadId, setSelectedLeadId] = useState(null)
  const [refreshKey, setRefreshKey] = useState(0)

  // Avoid firing a request on every keystroke.
  useEffect(() => {
    const timer = setTimeout(() => setDebouncedSearch(search.trim()), 300)
    return () => clearTimeout(timer)
  }, [search])

  const filters = {
    search: debouncedSearch,
    score_band: scoreBand === 'all' ? '' : scoreBand,
  }

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

      {/* Temporary filter bar (replaced by FE-10) */}
      <div
        style={{
          display: 'flex',
          gap: '12px',
          backgroundColor: 'var(--color-bg-surface)',
          padding: '16px',
          borderRadius: 'var(--radius-md)',
          border: '1px solid var(--color-border)',
          flexWrap: 'wrap',
        }}
      >
        <div style={{ flex: 1, minWidth: '240px' }}>
          <Input
            placeholder="Search company or job title..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
        <div style={{ width: '180px' }}>
          <Select
            value={scoreBand}
            onChange={(e) => setScoreBand(e.target.value)}
            options={[
              { value: 'all', label: 'All Score Bands' },
              { value: 'high', label: 'High (80+ Eligible)' },
              { value: 'medium', label: 'Medium (60-79)' },
              { value: 'low', label: 'Low (< 60)' },
              { value: 'suppressed', label: 'Suppressed' },
            ]}
          />
        </div>
      </div>

      <LeadTable
        filters={filters}
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
