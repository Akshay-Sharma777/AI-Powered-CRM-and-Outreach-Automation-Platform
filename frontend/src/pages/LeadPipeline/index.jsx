import React, { useState, useEffect } from 'react'
import { LeadTable } from './LeadTable'
import { LeadFilters } from './LeadFilters'
import {
  createDefaultFilters,
  readFiltersFromUrl
} from '../../store/filters'
import { Button } from '../../components/ui/Button'
import { Spinner, EmptyState, ErrorBanner } from '../../components/feedback/Spinner'
import { apiClient } from '../../api/client'
import { MOCK_LEADS } from '../../mocks/sampleLeads'

export default function LeadPipelinePage({ currentUser }) {
  const [leads, setLeads] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [filters, setFilters] = useState(() => readFiltersFromUrl())
  const [appliedSearch, setAppliedSearch] = useState(() => filters.search)
  const [selectedLead, setSelectedLead] = useState(null)

  async function fetchLeads() {
    setLoading(true)
    setError(null)
    try {
      const data = await apiClient('/leads')
      setLeads(data.items || data)
    } catch (err) {
      // Offline / mock mode fallback
      console.warn('Backend unavailable, falling back to offline fixtures:', err)
      setLeads(MOCK_LEADS)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchLeads()
  }, [])

  async function handleClaimLead(leadId) {
    try {
      await apiClient(`/leads/${leadId}/claim`, { method: 'POST' })
      setLeads((prev) =>
        prev.map((l) => (l.id === leadId ? { ...l, assigned_to: currentUser?.id || 'me' } : l))
      )
    } catch (err) {
      // Local optimistic update if mock mode
      setLeads((prev) =>
        prev.map((l) => (l.id === leadId ? { ...l, assigned_to: currentUser?.id || 'me' } : l))
      )
    }
  }

  const filteredLeads = leads.filter((lead) => {
    const query = appliedSearch.trim().toLowerCase()

    const matchesSearch =
      !query ||
      (lead.title || '').toLowerCase().includes(query) ||
      (lead.organization_name || '').toLowerCase().includes(query)

    const matchesSource =
      filters.sources.length === 0 ||
      filters.sources.includes(lead.source_name)

    const experienceMin = lead.experience_min ?? 0
    const experienceMax = lead.experience_max ?? 0

    const matchesExperience =
      experienceMax >= filters.experienceMin &&
      experienceMin <= filters.experienceMax

    const matchesScore =
      filters.scoreBand === 'all' ||
      lead.score_band === filters.scoreBand

    const matchesStatus =
      filters.status === 'all' ||
      lead.status === filters.status

    const matchesAssigned =
      filters.assignedTo === 'all' ||
      (filters.assignedTo === 'unassigned'
        ? !lead.assigned_to
        : lead.assigned_to === filters.assignedTo)

    return (
      matchesSearch &&
      matchesSource &&
      matchesExperience &&
      matchesScore &&
      matchesStatus &&
      matchesAssigned
    )
  })
  return (
    <div style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '20px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h1 style={{ fontSize: '22px', fontWeight: 700 }}>Lead Pipeline & Discovery</h1>
          <p style={{ fontSize: '13px', color: 'var(--color-text-muted)' }}>
            Daily scraped 0-2 yr fresher opportunities across verified platforms.
          </p>
        </div>
        <Button variant="secondary" onClick={fetchLeads}>
          ↻ Refresh
        </Button>
      </div>

      {error && <ErrorBanner message={error} onRetry={fetchLeads} />}

      {/* Filter Bar */}
      <LeadFilters
        leads={leads}
        filters={filters}
        onFiltersChange={setFilters}
        onSearchChange={setAppliedSearch}
        onClear={() => {
          const defaults = createDefaultFilters()
          setFilters(defaults)
          setAppliedSearch('')
        }}
      />

      {/* Table Content */}
      {loading ? (
        <div style={{ display: 'flex', justifyContent: 'center', padding: '48px' }}>
          <Spinner size={32} />
        </div>
      ) : filteredLeads.length === 0 ? (
        <EmptyState
          title="No leads match your criteria"
          message="Try adjusting your search terms or score band filter."
        />
      ) : (
        <LeadTable
          leads={filteredLeads}
          currentUserId={currentUser?.id}
          onClaimLead={handleClaimLead}
          onSelectLead={(lead) => setSelectedLead(lead)}
        />
      )}

      {/* Quick Detail Drawer / Modal Preview */}
      {selectedLead && (
        <div
          style={{
            backgroundColor: 'var(--color-bg-surface)',
            padding: '20px',
            borderRadius: 'var(--radius-md)',
            border: '1px solid var(--color-border)'
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <h3 style={{ fontSize: '16px', fontWeight: 600 }}>{selectedLead.title}</h3>
            <button
              onClick={() => setSelectedLead(null)}
              style={{ background: 'none', border: 'none', cursor: 'pointer' }}
            >
              ✕
            </button>
          </div>
          <p style={{ fontSize: '14px', color: 'var(--color-text-muted)', margin: '8px 0' }}>
            {selectedLead.organization_name} •{' '}
            <a href={selectedLead.source_url} target="_blank" rel="noreferrer">
              Original Listing ↗
            </a>
          </p>
          <div style={{ fontSize: '13px', marginTop: '8px' }}>
            <strong>Source Provenance:</strong> {selectedLead.source_name} • Discovered at{' '}
            {new Date(selectedLead.discovered_at).toLocaleDateString()}
          </div>
        </div>
      )}
    </div>
  )
}
