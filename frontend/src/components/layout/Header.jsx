import React from 'react'
import { Badge } from '../ui/Badge'

export function Header({ user, onLogout }) {
  return (
    <header
      style={{
        height: '60px',
        backgroundColor: 'var(--color-bg-surface)',
        borderBottom: '1px solid var(--color-border)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '0 24px',
        width: '100%'
      }}
    >
      <div style={{ fontSize: '14px', fontWeight: 500, color: 'var(--color-text-muted)' }}>
        Internal Operations Portal
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
        {user ? (
          <>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <span style={{ fontSize: '14px', fontWeight: 600 }}>{user.full_name || user.email}</span>
              <Badge variant="info">{user.role || 'researcher'}</Badge>
            </div>
            <button
              onClick={onLogout}
              style={{
                background: 'none',
                border: '1px solid var(--color-border)',
                borderRadius: 'var(--radius-md)',
                padding: '4px 10px',
                fontSize: '12px',
                color: 'var(--color-text-muted)',
                cursor: 'pointer'
              }}
            >
              Sign Out
            </button>
          </>
        ) : (
          <span style={{ fontSize: '13px', color: 'var(--color-text-muted)' }}>Not Signed In</span>
        )}
      </div>
    </header>
  )
}
