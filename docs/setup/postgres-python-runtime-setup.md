# Finish the Day 6 migration attempt: runtime prerequisite

## Current evidence

Latest October10 read-only inspection after learner extension setup: database merlin_d6/cluster7694311451826794534; plpython3u1.0 installed. Users, notes, note_weighted_length(text) and all three migration role names are absent. No naming collisions observed. The learner can now attempt the up migration; its early Unicode-function call tests embedded imports/pins and a failure must abort the entire application transaction.

From the Ubuntu checkout /home/vipra/Merlin, learner attempt command:

```bash
docker compose -p merlin-d6-20261008105707 exec -T postgres psql -X -U merlin_d6 -d merlin_d6 -v ON_ERROR_STOP=1 --single-transaction -f - < migrations/001_users_notes.up.sql
```

The shell reads the existing learner-reviewed file and passes it into psql inside the explicit disposable container. No new migration is authored by this command. ON_ERROR_STOP stops at the first SQL error; --single-transaction rolls back migration changes if any statement fails. Previously enabled PL/Python was installed separately and remains installed after such a rollback. Do not assume success: send the actual output/first error and do not rerun individual CREATE statements. This command has not been executed by the assistant.

October 10, 2026: read-only inspection of project merlin-d6-20261008105707 confirmed Debian 12 bookworm inside the PostgreSQL container. No python3 executable was found on PATH. The current apt cache produced no candidate information for postgresql-plpython3-17; this does not prove the package is unavailable from its repositories. PostgreSQL shared files are under /usr/share/postgresql/17. Earlier fresh database inspection confirmed merlin_d6, cluster7694311451826794534, absent PL/Python availability and absent users/notes tables.

The existing migration requires PL/Python plus emoji2.16.0 and regex2026.9.29 inside the database server's Python runtime. The application virtual environment already has its required packages. Do not repeat application setup or reinstall them there.

## Exact first action for the learner

Run from your Ubuntu terminal at /home/vipra/Merlin:

```bash
docker compose -p merlin-d6-20261008105707 exec -u root -T postgres apt-get update
docker compose -p merlin-d6-20261008105707 exec -T postgres apt-cache policy postgresql-17 postgresql-plpython3-17 python3 python3-pip
```

The first command refreshes package lists inside the explicitly named disposable container. It changes package metadata there, but does not install packages, alter database tables, or touch Sprint 0 storage. The second lists installed/candidate versions. Stop if the first command fails. Share the candidate output; do not run an install yet. Package lists are needed to plan a compatible installation rather than guessing a package version or inadvertently changing PostgreSQL.

These commands have not been executed by the assistant. The assistant's inspection was read-only. Do not omit the project name, use a default compose project, or run host apt commands for this prerequisite.

## Remaining sequence within the same coding hour

### Server Python verified; Unicode packages next

Latest learner metadata output confirms both pinned packages in the shared directory. Assistant import-only check as postgres succeeded: emoji2.16.0, regex2026.9.29, family emoji recognized and exactly one grapheme. This is external server-Python proof, not yet an embedded PL/Python call.

Next learner action: enable plpython3u only in the explicit merlin_d6 database, then list installed extensions. This is infrastructure setup, not a users/notes migration. Do not enable it in template databases or preserved Sprint 0. Confirm the target fingerprint remains7694311451826794534 before any database change. Embedded runtime verification and the migration attempt remain pending.

Learner reported Python3.11.2. Fresh assistant read-only checks confirm the correct merlin_d6/cluster7694311451826794534 and plpython3u is now AVAILABLE but not enabled (installed_version NULL). Python's shared search path includes /usr/local/lib/python3.11/dist-packages.

Next learner commands:

```bash
docker compose -p merlin-d6-20261008105707 exec -u root -T postgres python3 -m pip install --no-cache-dir --only-binary=:all: --no-deps --target /usr/local/lib/python3.11/dist-packages 'emoji==2.16.0' 'regex==2026.9.29'
docker compose -p merlin-d6-20261008105707 exec -u postgres -T postgres python3 -m pip show emoji regex
```

Stop if the install fails. The shared target avoids root-only user packages and avoids replacing Debian-managed packages. Binary-only installation refuses an unexpected source build. The second command checks package metadata visibility as the database operating-system user. Expected versions2.16.0 and2026.9.29. These learner commands have not been run by the assistant. Metadata visibility is still not an import/function proof inside PL/Python; enablement and embedded-runtime checks remain next, before migration.

### Package plan now checked

The learner refreshed package lists and reported installed PostgreSQL17.11-1.pgdg12+2 with the same candidate for postgresql-plpython3-17. The trailing python3/python3-pip names were accidentally executed as a separate Windows command; that failed outside the container and did not install anything.

The assistant then ran apt-get -s install --no-install-recommends postgresql-plpython3-17=17.11-1.pgdg12+2 python3-pip inside the explicit disposable container. Simulation passed:21new packages,0upgraded,0removed. Dependencies include the server's Python3.11 runtime. Nothing was installed by the simulation.

Next learner commands, from Ubuntu at /home/vipra/Merlin:

```bash
docker compose -p merlin-d6-20261008105707 exec -u root -T postgres apt-get install -y --no-install-recommends postgresql-plpython3-17=17.11-1.pgdg12+2 python3-pip
docker compose -p merlin-d6-20261008105707 exec -T postgres python3 --version
```

The first command installs the reviewed extension package and Python/pip runtime only inside the disposable container. It does not enable the extension in a database or apply the migration. Stop on error; send the result. Pinned emoji/regex installation and database extension enablement still need their own verification. This temporary container-layer installation is lost on recreation, while the database volume remains separate; record that limitation instead of claiming reproducible deployment.

1. Compare package candidates with the running PostgreSQL17.11 version and inspect installation dependencies before choosing the runtime installation. Prefer a reviewed reproducible disposable image; an in-container installation is temporary and disappears when that container is recreated. The learner writes any configuration; no Docker/configuration files are supplied here.
2. Provide the compatible PL/Python package and pinned Unicode packages to the Python interpreter actually embedded in the server. Check imports as the PostgreSQL operating-system user, not merely root or the application .venv. Avoid user-scoped pip installations unavailable to the server process. Package/runtime installation remains unperformed.
3. Enable the extension only in the fingerprint-verified merlin_d6 database. The learner authors any SQL; the required extension name is plpython3u. Do not enable it in the preserved database or template databases. Creating untrusted-language functions requires a superuser; application-role denial needs separate limited-role tests.
4. Confirm extension/runtime availability, review the migration and potential cluster-wide role-name collisions, then personally apply the existing up file as one transaction with ON_ERROR_STOP to the explicit isolated endpoint. Record the actual first result/error. Do not manually rerun partial statements after failure.
5. Re-run the learner probe if needed and inspect whether public.users/public.notes now exist. This supplies migration attempt evidence for Step3.3; it is separate from Step4 acceptance tests and down/reapplication.

A recorded failed attempt is honest attempt evidence; it is not a working migration. Do not run a known-blocked migration merely to satisfy a checkbox. Prerequisite work consumes the existing60-minute implementation block; actual minutes remain unknown. Keep the360-minute day cap. No maintenance run, migration, installation, reset, commit, push or upload occurred during this planning review. Preserve merlin_postgres_data/cluster7691749973399031842. AWS/DSA deferred.

📚 Learn first: [PostgreSQL17 PL/Python](https://www.postgresql.org/docs/17/plpython.html), separate package and untrusted-language permissions; [PostgreSQL Debian packages](https://www.postgresql.org/download/linux/debian/), supported bookworm/PGDG repository. Verified October10,2026. Package candidates remain unverified until the learner's commands return.

↩ Return: send package candidate output before choosing the installation command; do not apply the migration while the runtime gate remains blocked.
