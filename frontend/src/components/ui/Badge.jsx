import React from 'react'

export function Badge({ variant = 'neutral', children }) {
  let bg = 'var(--color-bg-subtle)'
  let color = 'var(--color-text-main)'

  if (variant === 'success') {
    bg = 'var(--color-score-high-bg)'
    color = 'var(--color-score-high)'
  } else if (variant === 'warning') {
    bg = 'var(--color-score-medium-bg)'
    color = 'var(--color-score-medium)'
  } else if (variant === 'danger') {
    bg = 'var(--color-score-low-bg)'
    color = 'var(--color-score-low)'
  } else if (variant === 'info') {
    bg = 'var(--color-primary-light)'
    color = 'var(--color-primary)'
  }

  return (
    <span
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        padding: '2px 8px',
        borderRadius: 'var(--radius-full)',
        fontSize: '12px',
        fontWeight: 500,
        backgroundColor: bg,
        color
      }}
    >
      {children}
    </span>
  )
}

export function Table({ headers = [], children }) {
  return (
    <div style={{ width: '100%', overflowX: 'auto', border: '1px solid var(--color-border)', borderRadius: 'var(--radius-md)' }}>
      <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '14px' }}>
        <thead style={{ backgroundColor: 'var(--color-bg-subtle)', borderBottom: '1px solid var(--color-border)' }}>
          <tr>
            {headers.map((h, idx) => (
              <th key={idx} style={{ padding: '12px 16px', fontWeight: 600, color: 'var(--color-text-muted)' }}>
                {h}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>{children}</tbody>
      </table>
    </div>
  )
}
