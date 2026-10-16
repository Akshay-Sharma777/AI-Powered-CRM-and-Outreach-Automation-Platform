import React from 'react'

export function Spinner({ size = 24 }) {
  return (
    <div
      role="status"
      aria-label="Loading"
      style={{
        display: 'inline-block',
        width: `${size}px`,
        height: `${size}px`,
        border: '3px solid var(--color-border)',
        borderTopColor: 'var(--color-primary)',
        borderRadius: '50%',
        animation: 'spin 0.8s linear infinite'
      }}
    />
  )
}

export function EmptyState({ title = 'No records found', message, action }) {
  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '48px 16px',
        textAlign: 'center',
        backgroundColor: 'var(--color-bg-surface)',
        borderRadius: 'var(--radius-md)',
        border: '1px dashed var(--color-border)'
      }}
    >
      <div style={{ fontSize: '32px', marginBottom: '8px' }}>📂</div>
      <h3 style={{ fontSize: '16px', fontWeight: 600, color: 'var(--color-text-main)', marginBottom: '4px' }}>
        {title}
      </h3>
      {message && (
        <p style={{ fontSize: '14px', color: 'var(--color-text-muted)', marginBottom: '16px', maxWidth: '400px' }}>
          {message}
        </p>
      )}
      {action}
    </div>
  )
}

export function ErrorBanner({ message = 'An error occurred', onRetry }) {
  return (
    <div
      role="alert"
      style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '12px 16px',
        backgroundColor: 'var(--color-score-low-bg)',
        border: '1px solid var(--color-score-low)',
        borderRadius: 'var(--radius-md)',
        color: 'var(--color-score-low)',
        marginBottom: '16px'
      }}
    >
      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
        <span>⚠️</span>
        <span style={{ fontSize: '14px', fontWeight: 500 }}>{message}</span>
      </div>
      {onRetry && (
        <button
          onClick={onRetry}
          style={{
            background: 'none',
            border: 'none',
            color: 'var(--color-score-low)',
            textDecoration: 'underline',
            fontWeight: 600,
            cursor: 'pointer',
            fontSize: '13px'
          }}
        >
          Retry
        </button>
      )}
    </div>
  )
}
