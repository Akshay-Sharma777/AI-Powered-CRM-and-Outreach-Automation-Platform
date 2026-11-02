# Database Restore Guide (BE-57)

How to restore a backup made by `infra/backup/backup.sh` and verify that it worked.
Practise restores on an empty **test** database. Never restore on top of the live database.

## 1. What a backup is

- File name: `crm_db_<YYYYMMDD_HHMMSS>.sql.gz`, a gzip-compressed plain SQL dump made with `pg_dump --no-owner --no-privileges`.
- Location: `$BACKUP_DIR/daily/` (newest 7 files) and `$BACKUP_DIR/weekly/` (newest 4 files, one per Sunday). The default `BACKUP_DIR` is `/var/backups/outreach-crm`.
- Backups are never committed to Git. `.gitignore` excludes `*.sql.gz`, `*.dump` and `infra/backup/dumps/`.

## 2. Before you start

- `pg_dump`, `psql`, `createdb` and `dropdb` are installed. The `pg_dump` major version must be the same as, or newer than, the database server's. Check with `pg_dump --version`.
- For Neon, back up with the **direct** connection string (the host without `-pooler`), not the pooled one.
- Connection details come from environment variables only. Never write passwords or connection strings into files, commits, tickets or chat.

## 3. Take a backup

```bash
export DATABASE_URL="<direct connection string>"   # set in your shell only
./infra/backup/backup.sh
```

Optionally set `BACKUP_DIR` to choose another folder. A successful run ends with
`Database backup completed successfully` and prints the new file name.

## 4. Restore into an empty test database and verify

1. **Pick a dump.** For the newest daily one:
   ```bash
   LATEST="$(ls -1 "$BACKUP_DIR"/daily/*.sql.gz | sort | tail -n 1)"
   echo "$LATEST"
   ```
2. **Check the archive.** No output from this means the file is intact:
   ```bash
   gzip -t "$LATEST"
   ```
3. **Create an empty test database.** It must be a new, separate database (locally, or a new Neon branch or database):
   ```bash
   createdb crm_restore_test
   ```
4. **Restore it.** `ON_ERROR_STOP` makes the restore stop at the first error:
   ```bash
   gunzip -c "$LATEST" | psql -v ON_ERROR_STOP=1 -q -d crm_restore_test
   ```
5. **Verify the result.**
   - List the tables and confirm they match the source database:
     ```bash
     psql -d crm_restore_test -c "\dt"
     ```
   - Compare row counts for a few important tables on both databases:
     ```bash
     psql -d crm_restore_test -c "SELECT count(*) FROM <table>;"
     ```
   - Spot-check a few rows with `SELECT * FROM <table> LIMIT 5;`.
6. **Clean up the test database:**
   ```bash
   dropdb crm_restore_test
   ```

The restore is verified when the restore command finishes without errors and the table list and row counts match the source.

## 5. Restoring after a real incident

Do not restore on top of the live database. Restore into a **new** empty database (or a new Neon branch), run the checks in section 4, then point the application's `DATABASE_URL` at it in the deployment environment (never in Git) and tell the team.

## 6. Troubleshooting

| Symptom | Likely cause | What to do |
|---|---|---|
| `pg_dump: error: aborting because of server version mismatch` | `pg_dump` is older than the server | Install a newer PostgreSQL client |
| Backup fails to connect or hangs | A pooled connection string was used | Use the direct connection string |
| `gzip: unexpected end of file` | The file is truncated or corrupt | Use the previous backup |
| `relation ... already exists` during restore | The target database was not empty | Create a fresh empty database |
| `extension ... is not available` | The target server lacks an extension used by the schema | Install the extension, or restore into the same kind of server (for example a Neon branch) |

## 7. Running it on a schedule (example)

Keep the connection string in a file **outside the repository**, readable only by its owner (for example `/etc/outreach-crm/backup.env` with `chmod 600`), containing `export DATABASE_URL=...`. Then add a cron entry like:

```
0 2 * * * . /etc/outreach-crm/backup.env && /path/to/repo/infra/backup/backup.sh >> /var/log/outreach-crm-backup.log 2>&1
```

Run it once a day. The weekly copy is taken on Sundays, so the job must run on Sundays.