/**
 * Score Reason Code Translations (FE-13).
 */

export const REASON_CODE_MAP = {
  OFFICIAL_COMPANY_SOURCE: 'Opportunity originated directly from verified official employer careers portal.',
  VERIFIED_PORTAL_SOURCE: 'Discovered via an approved curated job portal.',
  AGGREGATOR_SOURCE: 'Discovered from a general job aggregator.',
  CONTACT_ROLE_CONFIRMED: 'Associated contact role verified as recruiter or talent lead.',
  CONTACT_ROLE_UNCONFIRMED: 'Direct recruiter role is unconfirmed.',
  EMAIL_VERIFIED_DELIVERABLE: 'Email deliverability confirmed via active verification.',
  EMAIL_CATCH_ALL: 'Domain accepts catch-all mail; individual recipient certainty is lower.',
  EMAIL_RISKY: 'Mailbox flagged as potential bounce risk.',
  EMAIL_UNVERIFIED: 'Email has not yet been verified.',
  DATA_VERY_FRESH: 'Discovered within 3 days of publication.',
  DATA_MODERATELY_FRESH: 'Published within the last 14 days.',
  DATA_AGED: 'Posting is more than 14 days old.',
  COMPLETE_FIELDS: 'Full description, location, and requirements extracted.',
  SALARY_MISSING: 'Compensation details were not listed in the opportunity.',
  PUBLICATION_DATE_MISSING: 'Original publication date missing from source.'
}

export function translateReasonCode(code) {
  return REASON_CODE_MAP[code] || code
}
