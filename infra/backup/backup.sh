#!/usr/bin/env bash
# ==============================================================================
# Database Backup and Rotation Script (BE-57)
# Dumps PostgreSQL database and maintains 7 daily and 4 weekly copies.
# ==============================================================================

set -euo pipefail

BACKUP_DIR="${BACKUP_DIR:-/var/backups/outreach-crm}"
DATE_TAG="$(date +'%Y%m%d_%H%M%S')"
DAY_OF_WEEK="$(date +'%u')" # 1 = Monday, 7 = Sunday
DUMP_FILE="${BACKUP_DIR}/crm_db_${DATE_TAG}.sql.gz"

mkdir -p "${BACKUP_DIR}/daily"
mkdir -p "${BACKUP_DIR}/weekly"

echo "[$(date -u)] Starting database backup..."

if [ -z "${DATABASE_URL:-}" ]; then
  echo "Error: DATABASE_URL environment variable is not set." >&2
  exit 1
fi

# Run pg_dump and compress
pg_dump "${DATABASE_URL}" | gzip > "${DUMP_FILE}"
cp "${DUMP_FILE}" "${BACKUP_DIR}/daily/"

# Weekly backup on Sundays
if [ "${DAY_OF_WEEK}" -eq 7 ]; then
  echo "[$(date -u)] Storing weekly retention copy..."
  cp "${DUMP_FILE}" "${BACKUP_DIR}/weekly/"
fi

# Remove daily backups older than 7 days
find "${BACKUP_DIR}/daily" -type f -name "*.sql.gz" -mtime +7 -delete

# Remove weekly backups older than 28 days (4 weeks)
find "${BACKUP_DIR}/weekly" -type f -name "*.sql.gz" -mtime +28 -delete

echo "[$(date -u)] Database backup completed successfully: ${DUMP_FILE}"
