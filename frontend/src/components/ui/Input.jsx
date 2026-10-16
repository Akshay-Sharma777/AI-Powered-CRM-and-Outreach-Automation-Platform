import React from 'react'

export function Input({ label, error, style = {}, ...props }) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '4px', width: '100%' }}>
      {label && (
        <label style={{ fontSize: '13px', fontWeight: 500, color: 'var(--color-text-main)' }}>
          {label}
        </label>
      )}
      <input
        style={{
          padding: '8px 12px',
          borderRadius: 'var(--radius-md)',
          border: `1px solid ${error ? 'var(--color-danger)' : 'var(--color-border)'}`,
          fontSize: '14px',
          outline: 'none',
          backgroundColor: 'var(--color-bg-surface)',
          ...style
        }}
        {...props}
      />
      {error && (
        <span style={{ fontSize: '12px', color: 'var(--color-danger)' }}>{error}</span>
      )}
    </div>
  )
}

export function Select({ label, error, options = [], style = {}, ...props }) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '4px', width: '100%' }}>
      {label && (
        <label style={{ fontSize: '13px', fontWeight: 500, color: 'var(--color-text-main)' }}>
          {label}
        </label>
      )}
      <select
        style={{
          padding: '8px 12px',
          borderRadius: 'var(--radius-md)',
          border: `1px solid ${error ? 'var(--color-danger)' : 'var(--color-border)'}`,
          fontSize: '14px',
          outline: 'none',
          backgroundColor: 'var(--color-bg-surface)',
          ...style
        }}
        {...props}
      >
        {options.map((opt) => (
          <option key={opt.value} value={opt.value}>
            {opt.label}
          </option>
        ))}
      </select>
    </div>
  )
}
