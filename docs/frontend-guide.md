# Frontend Developer Guide

Welcome to the frontend team! This guide covers everything you need to know to build, test, and ship components and pages for the CRM dashboard.

---

## 1. Tech Stack & Key Choices

- **Build Tool**: Vite (fast HMR, lightweight output)
- **Framework**: React 18+
- **Styling**: Standard CSS with Design Tokens (`tokens.css`, `global.css`). No bloated CSS frameworks.
- **Mocking**: MSW (Mock Service Worker) & fixtures so you can build complete features without waiting for backend APIs.
- **Testing**: Vitest + React Testing Library.

---

## 2. Directory Structure

```
frontend/
├── package.json          # (LEAD-ONLY) Root dependencies
├── vite.config.js        # Vite config with proxy settings
├── public/
│   └── _redirects        # Cloudflare Pages SPA routing rewrite rules
└── src/
    ├── main.jsx          # Entry point
    ├── App.jsx           # Router & layout provider
    ├── styles/
    │   ├── tokens.css    # Design tokens (colors, spacing, score bands)
    │   └── global.css    # Reset and typography
    ├── api/
    │   ├── client.js     # Shared fetch wrapper (JWT, X-Correlation-ID, error handling)
    │   └── leads.js      # Leads API client
    ├── mocks/
    │   ├── handlers.js   # MSW mock handlers
    │   └── sampleLeads.js# Fake leads fixture
    ├── components/
    │   ├── ui/           # Button, Input, Modal, Table, Badge
    │   ├── layout/       # Sidebar, Header
    │   ├── score/        # ScoreBadge
    │   ├── verification/ # VerificationStatusChip
    │   └── feedback/     # Spinner, EmptyState, ErrorBanner
    └── pages/
        ├── _Kitchen/     # Component kit showcase / test harness
        ├── Login/
        ├── LeadPipeline/ # Main CRM table & Kanban
        ├── MyLeads/      # Assigned / claimed leads
        ├── EnrichmentQueue/
        ├── CampaignManager/
        ├── Suppression/
        ├── SystemHealth/
        └── ErrorCenter/
```

---

## 3. Getting Started Locally

```bash
cd frontend
npm install
npm run dev
```

The application will be running at `http://localhost:5173`.
By default, `VITE_USE_MOCKS=true` in `.env`, allowing you to develop fully offline against mock data.

---

## 4. UI Kit & The Kitchen Sink Demo (`/_Kitchen`)

Whenever you build or test a UI component (`Button`, `Input`, `Modal`, `Badge`, `Table`), always add its variants to `src/pages/_Kitchen/index.jsx`.
This serves as our live design system gallery.

### Design Tokens
Colors, score bands, and radii are defined in `src/styles/tokens.css`:
- High Confidence: `var(--color-score-high)` (Green)
- Medium Confidence: `var(--color-score-medium)` (Amber)
- Low Confidence: `var(--color-score-low)` (Red)
- Primary Accent: `var(--color-primary)`

---

## 5. Working Rules Reminder for Frontend Interns

1. Check your assigned Task ID in the [Tasksheet](tasksheet.md) (e.g. `FE-04`, `FE-09`).
2. Only edit files assigned to your ticket.
3. Do not modify `package.json` — if you need a library, open a **Library Request** issue.
4. Always test keyboard accessibility (tab focus, Escape key to close modals).
5. Attach a screenshot or video recording to your Pull Request!
