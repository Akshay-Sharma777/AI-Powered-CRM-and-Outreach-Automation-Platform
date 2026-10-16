import React, { useState } from 'react'
import { translateReasonCode } from './scoreReasons'

/**
 * ScoreBadge Component (FE-13).
 * Props:
 *  - score: number (0-100)
 *  - band: 'high' | 'medium' | 'low' | 'suppressed'
 *  - reasons: Array<{ code: string, points?: number }>
 */
export function ScoreBadge({ score = 0, band = 'low', reasons = [] }) {
  const [showTooltip, setShowTooltip] = useState(false)

  let badgeColor = 'var(--color-score-low)'
  let badgeBg = 'var(--color-score-low-bg)'

  if (band === 'high' || score >= 80) {
    badgeColor = 'var(--color-score-high)'
    badgeBg = 'var(--color-score-high-bg)'
  } else if (band === 'medium' || (score >= 60 && score < 80)) {
    badgeColor = 'var(--color-score-medium)'
    badgeBg = 'var(--color-score-medium-bg)'
  } else if (band === 'suppressed') {
    badgeColor = 'var(--color-score-suppressed)'
    badgeBg = 'var(--color-score-suppressed-bg)'
  }

  return (
    <div
      style={{ position: 'relative', display: 'inline-block' }}
      onMouseEnter={() => setShowTooltip(true)}
      onMouseLeave={() => setShowTooltip(false)}
    >
      <span
        tabIndex={0}
        role="button"
        aria-label={`Data Quality Score: ${score} out of 100`}
        onFocus={() => setShowTooltip(true)}
        onBlur={() => setShowTooltip(false)}
        style={{
          display: 'inline-flex',
          alignItems: 'center',
          justifyContent: 'center',
          padding: '2px 8px',
          borderRadius: 'var(--radius-full)',
          fontWeight: 600,
          fontSize: '12px',
          color: badgeColor,
          backgroundColor: badgeBg,
          cursor: 'help',
          border: `1px solid ${badgeColor}`
        }}
      >
        {score}/100
      </span>

      {showTooltip && (
        <div
          role="tooltip"
          style={{
            position: 'absolute',
            bottom: '100%',
            left: '50%',
            transform: 'translateX(-50%)',
            marginBottom: '8px',
            width: '260px',
            backgroundColor: '#0f172a',
            color: '#ffffff',
            padding: '10px 12px',
            borderRadius: 'var(--radius-md)',
            fontSize: '12px',
            lineHeight: '1.4',
            boxShadow: 'var(--shadow-lg)',
            zIndex: 50,
            pointerEvents: 'none'
          }}
        >
          <div style={{ fontWeight: 700, marginBottom: '4px', borderBottom: '1px solid #334155', paddingBottom: '4px' }}>
            Score Factors ({score}/100)
          </div>
          {reasons && reasons.length > 0 ? (
            <ul style={{ paddingLeft: '16px', margin: 0 }}>
              {reasons.map((r, idx) => (
                <li key={idx} style={{ marginBottom: '2px' }}>
                  {translateReasonCode(r.code || r)}
                </li>
              ))}
            </ul>
          ) : (
            <p style={{ margin: 0, color: '#94a3b8' }}>Standard scoring algorithm applied.</p>
          )}
        </div>
      )}
    </div>
  )
}
