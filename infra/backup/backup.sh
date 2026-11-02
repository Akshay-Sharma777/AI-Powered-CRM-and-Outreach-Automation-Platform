#!/usr/bin/env bash
# ==============================================================================
# Database Backup and Rotation Script (BE-57)
# Dumps the PostgreSQL (Neon) database to a compressed file and keeps the
# newest 7 daily and 4 weekly copies. Intended to run once a day.
#
# Usage:    DATABASE_URL="<direct connection string>" ./infra/backup/backup.sh
# Optional: BACKUP_DIR   (default /var/backups/outreach-crm)
#           DAILY_KEEP   (default 7)
#           WEEKLY_KEEP  (default 4)
# Restore:  see infra/backup/restore_guide.md
# ==============================================================================

set -euo pipefail

BACKUP_DIR="${BACKUP_DIR:-/var/backups/outreach-crm}"
DAILY_KEEP="${DAILY_KEEP:-7}"
WEEKLY_KEEP="${WEEKLY_KEEP:-4}"
DATE_TAG="$(date +'%Y%m%d_%H%M%S')"
DAY_OF_WEEK="${DAY_OF_WEEK:-$(date +'%u')}" # 1 = Monday, 7 = Sunday (override only for testing)
DAILY_DIR="${BACKUP_DIR}/daily"
WEEKLY_DIR="${BACKUP_DIR}/weekly"
DUMP_FILE="${DAILY_DIR}/crm_db_${DATE_TAG}.sql.gz"
TMP_FILE="${DUMP_FILE}.partial"

if [ -z "${DATABASE_URL:-}" ]; then
  echo "Error: DATABASE_URL environment variable is not set." >&2
  exit 1
fi

# Remove a half-written dump if anything below fails.
trap 'rm -f "${TMP_FILE}"' EXIT

mkdir -p "${DAILY_DIR}" "${WEEKLY_DIR}"

echo "[$(date -u)] Starting database backup..."

# Plain SQL dump without owner/privilege statements, so it restores into any
# empty database. Compress, verify the archive, then move it into place.
pg_dump --no-owner --no-privileges "${DATABASE_URL}" | gzip > "${TMP_FILE}"
gzip -t "${TMP_FILE}"
mv "${TMP_FILE}" "${DUMP_FILE}"

# Weekly retention copy on Sundays
if [ "${DAY_OF_WEEK}" -eq 7 ]; then
  echo "[$(date -u)] Storing weekly retention copy..."
  cp "${DUMP_FILE}" "${WEEKLY_DIR}/"
fi

# Keep only the newest N files in a folder. File names start with a timestamp,
# so a reverse name sort puts the newest first.
prune() {
  local dir="$1" keep="$2"
  find "${dir}" -maxdepth 1 -type f -name 'crm_db_*.sql.gz' \
    | sort -r \
    | tail -n +"$((keep + 1))" \
    | while IFS= read -r old; do
        echo "Removing old backup: ${old}"
        rm -f -- "${old}"
      done
}

prune "${DAILY_DIR}" "${DAILY_KEEP}"
prune "${WEEKLY_DIR}" "${WEEKLY_KEEP}"

echo "[$(date -u)] Database backup completed successfully: ${DUMP_FILE}"