/**
 * Role Constants and Permission Helper (FE-08).
 */

export const ROLES = {
  ADMIN: 'admin',
  RESEARCHER: 'researcher',
  CAMPAIGN_MANAGER: 'campaign_manager',
  DEVELOPER: 'developer',
}

const PERMISSIONS = {
  view_pipeline: [ROLES.ADMIN, ROLES.RESEARCHER, ROLES.CAMPAIGN_MANAGER, ROLES.DEVELOPER],
  claim_leads: [ROLES.ADMIN, ROLES.RESEARCHER],
  enrich_contact: [ROLES.ADMIN, ROLES.RESEARCHER],
  verify_email: [ROLES.ADMIN, ROLES.RESEARCHER],
  review_drafts: [ROLES.ADMIN, ROLES.CAMPAIGN_MANAGER],
  approve_and_send: [ROLES.ADMIN, ROLES.CAMPAIGN_MANAGER],
  manage_suppression: [ROLES.ADMIN, ROLES.CAMPAIGN_MANAGER],
  view_system_health: [ROLES.ADMIN, ROLES.DEVELOPER],
  view_error_center: [ROLES.ADMIN, ROLES.DEVELOPER],
  replay_errors: [ROLES.ADMIN, ROLES.DEVELOPER],
  manage_users: [ROLES.ADMIN],
  manage_sources_budgets: [ROLES.ADMIN],
}

export function can(role, action) {
  if (!role) return false
  const allowed = PERMISSIONS[action]
  if (!allowed) return false
  return allowed.includes(role)
}
