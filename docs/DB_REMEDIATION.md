# Database contamination remediation plan

This document describes a safe, step-by-step plan to diagnose and remediate cross-contamination between the `main` database and per-company/module databases (for example `artstudio3d`).

Important: Always make full backups before performing any destructive operation.

## Goals (high level)
- Confirm which tables are out of place in `main`.
- Produce a read-only diagnostic report with table lists, row counts and sample rows.
- Back up the affected databases.
- Decide whether to move tables to their correct DB, or restore `main` from a clean backup.
- Implement safeguards to prevent future accidental deployments into the wrong DB.

## Step 0 — Safety first
1. Take full backups of *both* `main` and `artstudio3d` (and any `company_*` DBs possibly involved). Use mysqldump / database snapshots or file-level backups depending on your infrastructure.
2. If possible, work on copies or test instances to validate the migration steps.

## Step 1 — Diagnose (read-only)
Use the `scripts/db_diff_report.py` script (added to this repo) to:
- Produce a list of tables per configured database.
- Compute row counts for each table.
- Show sample rows (first N rows) for suspicious (module) tables.

Run (example):
```bash
.venv/bin/python scripts/db_diff_report.py --databases main artstudio3d --sample 3
```

This script is read-only and intended to help you evaluate how to proceed.

## Step 2 — Plan the remediation
Options:

- Restore: If `main` contains tables that were present there due to an accidental migration and you have a clean backup, restoring `main` from a pre-contamination backup is the safest option.

- Move tables: If `main` contains unique data that needs to be preserved and moved into `artstudio3d` or company DBs, plan for:
  1. Exporting affected tables from `main` (dump or CSV).
  2. Importing into target DB(s), making sure schema matches (run migrations first).
 3. Re-create any foreign keys and relationships pointing to company DBs.
 4. Do validation pass (row counts, spot checks).

## Step 3 — Implement safety measures
- Add CI checks to prevent migrations from running against `main` for module-specific changes (example: enforce target DB name as `company_*` or `artstudio3d`).
- Add a test that ensures `main` contains only global tables (core models).

## Who should run remediation
- DBAs or developers with database admin access. This may require coordination with production deployment teams.

## Notes
- The diagnostics script is intentionally read-only.
- If you'd like, I can prepare non-destructive export scripts next or prepare step-by-step move commands after we inspect the diagnostics output.
