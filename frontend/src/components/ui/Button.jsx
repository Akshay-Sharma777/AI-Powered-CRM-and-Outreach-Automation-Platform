import React from 'react'

/**
 * Button Component (FE-04).
 * Props:
 *  - variant: 'primary' | 'secondary' | 'danger'
 *  - isLoading: boolean
 *  - disabled: boolean
 *  - children: ReactNode
 */
export function Button({
  variant = 'primary',
  isLoading = false,
  disabled = false,
  children,
  onClick,
  type = 'button',
  style = {},
  ...props
}) {
  let bg = 'var(--color-primary)'
  let color = '#ffffff'
  let border = 'none'

  if (variant === 'secondary') {
    bg = 'var(--color-bg-surface)'
    color = 'var(--color-text-main)'
    border = '1px solid var(--color-border)'
  } else if (variant === 'danger') {
    bg = 'var(--color-danger)'
    color = '#ffffff'
  }

  const baseStyle = {
    display: 'inline-flex',
    alignItems: 'center',
    justifyContent: 'center',
    padding: '8px 16px',
    borderRadius: 'var(--radius-md)',
    fontWeight: 500,
    fontSize: '14px',
    backgroundColor: bg,
    color,
    border,
    cursor: disabled || isLoading ? 'not-allowed' : 'pointer',
    opacity: disabled || isLoading ? 0.6 : 1,
    transition: 'background-color 0.15s ease',
    ...style
  }

  return (
    <button
      type={type}
      disabled={disabled || isLoading}
      onClick={onClick}
      style={baseStyle}
      {...props}
    >
      {isLoading ? (
        <span style={{ display: 'inline-flex', alignItems: 'center', gap: '8px' }}>
          <span style={{ animation: 'spin 1s linear infinite' }}>⏳</span>
          Loading...
        </span>
      ) : (
        children
      )}
    </button>
  )
}
