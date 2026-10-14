# Injected fault catalogue

Faults exist only in audit copies, memory or isolated transactions. A surviving experiment is not a passing product test. Invalid harness runs never count as fault detections.

## Python

| ID | Fault | Status | Source change |
|---|---|---|---|
| PY-M001 | emoji-weight-one | DETECTED | app/note_rules.py: 4 if emoji.is_emoji(part) else 1 → 1 if emoji.is_emoji(part) else 1 |
| PY-M002 | codepoint-instead-of-grapheme | DETECTED | app/note_rules.py: _GRAPHEMES.findall(value) → value |
| PY-M003 | title-bound-relaxed | DETECTED | app/note_rules.py: title_length &gt; 175 → title_length &gt; 176 |
| PY-M004 | title-bound-too-strict | DETECTED | app/note_rules.py: title_length &gt; 175 → title_length &gt;= 175 |
| PY-M005 | body-bound-relaxed | DETECTED | app/note_rules.py: weighted_length(body) &gt; 7000 → weighted_length(body) &gt; 7001 |
| PY-M006 | body-bound-too-strict | DETECTED | app/note_rules.py: weighted_length(body) &gt; 7000 → weighted_length(body) &gt;= 7000 |
| PY-M007 | body-stripped | DETECTED | app/note_rules.py: body = "" if body is None else body → body = "" if body is None else body.strip() |
| PY-M008 | real-title-stripped | DETECTED | app/note_rules.py: return ValidatedNote(title, body, → return ValidatedNote(None if title is None else title.strip(), body, |
| PY-M009 | email-lowercased | DETECTED | app/note_rules.py: return value.strip() or None → return value.strip().lower() or None |
| PY-M010 | blank-title-stored-empty | DETECTED | app/note_rules.py: if not title.strip():             title = None → if not title.strip():             title = "" |
| PY-M011 | draft-delete-protection-removed | DETECTED | app/note_rules.py: not is_draft and title is None and not body.strip() → title is None and not body.strip() |
| PY-M012 | nul-check-removed | DETECTED | app/note_rules.py: if "\x00" in value: → if False: |
| PY-M013 | target-check-skipped | DETECTED | app/notes_maintenance.py:         verify_target(conn)  →         pass  |
| PY-M014 | identity-or-changed-to-and | DETECTED | app/notes_maintenance.py: database != "merlin_d6" or int(identifier) != EXPECTED_CLUSTER → database != "merlin_d6" and int(identifier) != EXPECTED_CLUSTER |
| PY-M015 | target-port-original-db | DETECTED | app/notes_maintenance.py: port=55432 → port=5432 |
| PY-M016 | batch1001-allowed | DETECTED | app/notes_maintenance.py: 1 &lt;= batch_size &lt;= 1000 → 1 &lt;= batch_size &lt;= 1001 |
| PY-M017 | lock-timeout-removed | DETECTED | app/notes_maintenance.py:             cur.execute("SET LOCAL lock_timeout = '2s'")  →  |
| PY-M018 | wrong-expiry-function | DETECTED | app/notes_maintenance.py: SELECT public.cleanup_expired_blank_notes(%s) → SELECT public.wrong_cleanup(%s) |
| PY-M019 | once-flag-ignored | DETECTED | app/notes_maintenance.py: if args.once: → if False: |
| PY-M020 | custom-interval-ignored | DETECTED | app/notes_maintenance.py: time.sleep(args.interval) → time.sleep(60) |
| PY-M021 | cli-error-secret-leaked | DETECTED | app/notes_maintenance.py: raise SystemExit("Maintenance failed; check target, migration and permissions. No credentials printed.") → raise SystemExit("Maintenance failed: " + password) |
| PY-M022 | strict-batch-guard-removed | DETECTED | app/notes_maintenance.py: if type(batch_size) is not int: → if False: |
| PY-M023 | strict-draft-guard-removed | DETECTED | app/note_rules.py: if not isinstance(is_draft, bool): → if False: |
| PY-M024 | utf8-guard-removed | DETECTED | app/note_rules.py: value.encode("utf-8") → pass |
| PY-M025 | unexpected-extra-sql | DETECTED | app/notes_maintenance.py:             cur.execute("SELECT public.cleanup_expired_blank_notes(%s)", (batch_size,)) →             cur.execute("SELECT 42")             cur.execute("SELECT public.cleanup_expired_blank_notes(%s)", (batch_size,)) |
| PY-M026 | email-padding-retained | DETECTED | app/note_rules.py: return value.strip() or None → return value or None |
| PY-M027 | optional-email-empty-string | DETECTED | app/note_rules.py: if value is None:         return None → if value is None:         return "" |
| PY-M028 | empty-email-empty-string | DETECTED | app/note_rules.py: return value.strip() or None → return value.strip() |
| PY-M029 | none-body-not-normalized | DETECTED | app/note_rules.py: body = "" if body is None else body → body = body |
| PY-M030 | draft-title-bypasses-limit | DETECTED | app/note_rules.py: elif title_length &gt; 175: → elif not is_draft and title_length &gt; 175: |
| PY-M031 | draft-body-bypasses-limit | DETECTED | app/note_rules.py: if weighted_length(body) &gt; 7000: → if not is_draft and weighted_length(body) &gt; 7000: |
| PY-M032 | save-default-is-draft | DETECTED | app/note_rules.py: is_draft: bool = False → is_draft: bool = True |
| PY-M033 | text-type-guard-disabled | DETECTED | app/note_rules.py: if not isinstance(value, str): → if False: |
| PY-M034 | valid-unicode-rejected-ascii | DETECTED | app/note_rules.py: value.encode("utf-8") → value.encode("ascii") |
| PY-M035 | nul-only-at-start | DETECTED | app/note_rules.py: if "\x00" in value: → if value.startswith("\x00"): |
| PY-M036 | valid-body-erased | DETECTED | app/note_rules.py: return ValidatedNote(title, body, → return ValidatedNote(title, "", |
| PY-M037 | valid-title-erased | DETECTED | app/note_rules.py: return ValidatedNote(title, body, → return ValidatedNote(None, body, |
| PY-M038 | blank-save-never-deletes | DETECTED | app/note_rules.py: not is_draft and title is None and not body.strip() → False |
| PY-M039 | target-host-public | DETECTED | app/notes_maintenance.py: host="127.0.0.1" → host="0.0.0.0" |
| PY-M040 | target-database-original | DETECTED | app/notes_maintenance.py: dbname="merlin_d6" → dbname="merlin_db" |
| PY-M041 | target-user-original | DETECTED | app/notes_maintenance.py: user="merlin_d6" → user="merlin" |
| PY-M042 | connection-timeout-unbounded | DETECTED | app/notes_maintenance.py: connect_timeout=3 → connect_timeout=0 |
| PY-M043 | batch-zero-allowed | DETECTED | app/notes_maintenance.py: 1 &lt;= batch_size &lt;= 1000 → 0 &lt;= batch_size &lt;= 1000 |
| PY-M044 | batch1000-rejected | DETECTED | app/notes_maintenance.py: 1 &lt;= batch_size &lt;= 1000 → 1 &lt;= batch_size &lt;= 999 |
| PY-M045 | statement-timeout-removed | DETECTED | app/notes_maintenance.py:             cur.execute("SET LOCAL statement_timeout = '10s'")  →  |
| PY-M046 | purge-parameter-altered | DETECTED | app/notes_maintenance.py: cur.execute("SELECT public.purge_deleted_notes(%s)", (batch_size,)) → cur.execute("SELECT public.purge_deleted_notes(%s)", (batch_size - 1,)) |
| PY-M047 | cleanup-counts-swapped | DETECTED | app/notes_maintenance.py: return expired, purged → return purged, expired |
| PY-M048 | early-explicit-commit | DETECTED | app/notes_maintenance.py:             expired = cur.fetchone()&lbrack;0&rbrack; →             expired = cur.fetchone()&lbrack;0&rbrack;             conn.commit() |
| PY-M049 | default-interval-altered | DETECTED | app/notes_maintenance.py: default=60 → default=59 |
| PY-M050 | nine-second-interval-allowed | DETECTED | app/notes_maintenance.py: args.interval &lt; 10 → args.interval &lt; 9 |
| PY-M051 | ten-second-interval-rejected | DETECTED | app/notes_maintenance.py: args.interval &lt; 10 → args.interval &lt; 11 |
| PY-M052 | runtime-error-not-sanitized | DETECTED | app/notes_maintenance.py: except (psycopg.Error, RuntimeError): → except psycopg.Error: |
| PY-M053 | output-counts-swapped | DETECTED | app/notes_maintenance.py: Expired title-only notes: {expired}; purged deleted notes: {purged} → Expired title-only notes: {purged}; purged deleted notes: {expired} |
| PY-M054 | interrupt-message-omitted | DETECTED | app/notes_maintenance.py: print("Maintenance stopped") → pass |
| PY-M055 | nul-error-echoes-input | DETECTED | app/note_rules.py: raise ValueError("PostgreSQL text cannot contain NUL") → raise ValueError("PostgreSQL text cannot contain NUL: " + value) |
| PY-M056 | probe-only-operational-errors | DETECTED | app/database_connectivity_probe.py: except psycopg.Error: → except psycopg.OperationalError: |
| PY-M057 | probe-leaks-error | DETECTED | app/database_connectivity_probe.py: print("DB Probe Failed: Connection or query failed.", file=sys.stderr) → print("DB Probe Failed: " + password, file=sys.stderr) |
| PY-M058 | probe-wrong-failure-status | DETECTED | app/database_connectivity_probe.py: sys.exit(1) → sys.exit(0) |
| PY-M059 | probe-wrong-success-status | DETECTED | app/database_connectivity_probe.py: sys.exit(0) → sys.exit(1) |
| PY-M060 | probe-not-read-only | DETECTED | app/database_connectivity_probe.py: conn.read_only = True → conn.read_only = False |
| PY-M061 | probe-wrong-port | DETECTED | app/database_connectivity_probe.py: port=55432 → port=5432 |
| PY-M062 | probe-fetch-twice | DETECTED | app/database_connectivity_probe.py: db_name, db_user = cur.fetchone() → db_name, db_user = cur.fetchone(); cur.fetchone() |
| PY-M063 | probe-mask-programming-bug | DETECTED | app/database_connectivity_probe.py: except psycopg.Error: → except Exception: |
| PY-M064 | probe-extra-query | DETECTED | app/database_connectivity_probe.py: cur.execute("SELECT current_database(), current_user;") → cur.execute("SELECT 42"); cur.execute("SELECT current_database(), current_user;") |
| PY-M065 | probe-error-on-stdout | DETECTED | app/database_connectivity_probe.py: file=sys.stderr → file=sys.stdout |
| PY-M066 | worker-malformed-identity-not-sanitized | DETECTED | app/notes_maintenance.py: raise RuntimeError("Refusing malformed Day 6 database identity") from None → raise |
| PY-M067 | text-plain-weight-zero | DETECTED | app/note_rules.py: else 1 for part → else 0 for part |
| PY-M068 | text-all-empty-rejected | DETECTED | app/note_rules.py: return sum( → if value == "": raise ValueError("Empty text rejected")     return sum( |
| PY-M069 | text-drafts-all-delete | DETECTED | app/note_rules.py: not is_draft and title is None and not body.strip() → is_draft or (title is None and not body.strip()) |
| PY-M070 | text-all-emails-null | DETECTED | app/note_rules.py: return value.strip() or None → return None |
| PY-M071 | text-whitespace-body-trimmed | DETECTED | app/note_rules.py: body = "" if body is None else body → body = "" if body is None else body.strip() |
| PY-M072 | doctor-command-timeout-unbounded | DETECTED | tools/doctor.py: timeout=30, → timeout=None, |
| PY-M073 | doctor-command-raises-on-errors | DETECTED | tools/doctor.py: check=False, → check=True, |
| PY-M074 | doctor-command-does-not-capture | DETECTED | tools/doctor.py: capture_output=True → capture_output=False |
| PY-M075 | doctor-command-ignores-cwd | DETECTED | tools/doctor.py: cwd=root → cwd=None |
| PY-M076 | doctor-timeout-reports-success | DETECTED | tools/doctor.py: return subprocess.CompletedProcess(args, 127, '', '') → return subprocess.CompletedProcess(args, 0, '', '') |
| PY-M077 | doctor-negative-auth-accepts-any-error | DETECTED | tools/doctor.py: negative.returncode != 0 and 'password authentication failed' in negative.stderr.lower() → negative.returncode != 0 |
| PY-M078 | doctor-negative-auth-accepts-success | DETECTED | tools/doctor.py: negative.returncode != 0 and 'password authentication failed' in negative.stderr.lower() → negative.returncode == 0 or 'password authentication failed' in negative.stderr.lower() |
| PY-M079 | doctor-nested-inspection-guard-disabled | DETECTED | tools/doctor.py: ports = host.get('PortBindings', {}) → return health, host, mounts, labels             ports = host.get('PortBindings', {}) |
| PY-M080 | doctor-malformed-manifest-crashes | DETECTED | tools/doctor.py: except (OSError, ValueError, KeyError, TypeError): → except (OSError, ValueError, KeyError): |
| PY-M081 | doctor-missing-manifest-pin-crashes | DETECTED | tools/doctor.py: except (OSError, ValueError, KeyError, TypeError): → except (OSError, ValueError, TypeError): |
| PY-M082 | doctor-all-python-pins-accepted | DETECTED | tools/doctor.py: python_ok = declared in → python_ok = True or declared in |
| PY-M083 | doctor-unicode-port-crash | DETECTED | tools/doctor.py: bool(re.fullmatch(r'&lbrack;0-9&rbrack;{1,5}', str(bindings&lbrack;0&rbrack;.get('HostPort', '')))) → str(bindings&lbrack;0&rbrack;.get('HostPort', '')).isdigit() |
| PY-M084 | worker-invalid-interval-falls-back | DETECTED | app/notes_maintenance.py: type=int, default=60 → type=lambda value: int(value) if value.isdecimal() else 60, default=60 |
| PY-M085 | worker-help-disabled | DETECTED | app/notes_maintenance.py: argparse.ArgumentParser(description=__doc__) → argparse.ArgumentParser(description=__doc__, add_help=False) |
| PY-M086 | worker-unknown-flags-ignored | DETECTED | app/notes_maintenance.py: args = parser.parse_args() → args, unknown = parser.parse_known_args() |
| PY-M087 | doctor-timeout-leaks-secret | DETECTED | tools/doctor.py: return subprocess.CompletedProcess(args, 127, '', '') → print(str(args)); return subprocess.CompletedProcess(args, 127, '', '') |
| PY-M088 | doctor-static-runs-runtime | DETECTED | tools/doctor.py: if not self.static and available: → if available: |
| PY-M089 | doctor-all-reports-pass | DETECTED | tools/doctor.py: status = 'PASS' if ok else 'WARN' if warn else 'FAIL' → status = 'PASS' |
| PY-M090 | doctor-all-reports-fail | DETECTED | tools/doctor.py: status = 'PASS' if ok else 'WARN' if warn else 'FAIL' → status = 'FAIL' |
| PY-M091 | doctor-no-failure-accounting | DETECTED | tools/doctor.py: self.failures += int(status == 'FAIL') → self.failures += 0 |
| PY-M092 | doctor-inspect-always-refuses | DETECTED | tools/doctor.py: return health, host, mounts, labels → return None |
| PY-M093 | doctor-inspect-shape-guard-disabled | DETECTED | tools/doctor.py: if not (isinstance(health, str) → if False and not (isinstance(health, str) |
| PY-M094 | doctor-requests-secret-environment | DETECTED | tools/doctor.py: {{json .State.Health.Status}} → {{json .Config.Env}} |
| PY-M095 | doctor-service-auth-wrong-query | DETECTED | tools/doctor.py: base + "'SELECT 1'" → base + "'SELECT 2'" |
| PY-M096 | doctor-service-password-not-negative | DETECTED | tools/doctor.py: ${POSTGRES_PASSWORD}__doctor_wrong → ${POSTGRES_PASSWORD} |
| PY-M097 | doctor-host-password-not-negative | DETECTED | tools/doctor.py: password + '__doctor_wrong' → password |
| PY-M098 | doctor-host-public-interface | DETECTED | tools/doctor.py: '-h', '127.0.0.1', '-p', pg_port → '-h', '0.0.0.0', '-p', pg_port |
| PY-M099 | doctor-host-password-in-command | DETECTED | tools/doctor.py: '-Atqc', 'SELECT 1'&rbrack; → '-Atqc', 'SELECT 1', password&rbrack; |
| PY-M100 | doctor-cluster-expected-ignored | DETECTED | tools/doctor.py: self.expect_cluster is None or observed == self.expect_cluster → True |
| PY-M101 | doctor-cluster-always-refuses | DETECTED | tools/doctor.py: valid and (self.expect_cluster is None or observed == self.expect_cluster) → False |
| PY-M102 | doctor-cluster-assumes-original | DETECTED | tools/doctor.py: self.expect_cluster is None or observed == self.expect_cluster → observed == '7691749973399031842' |
| PY-M103 | linter-empty-tree-passes | DETECTED | tools/prd_lint.py: return 1  → return 0  |
| PY-M104 | linter-legacy-folder-not-expanded | DETECTED | tools/prd_lint.py: return folder.parent → return folder |
| PY-M105 | linter-link-check-disabled | DETECTED | tools/prd_lint.py: if not destination.exists(): → if False: |
| PY-M106 | linter-existing-targets-rejected | DETECTED | tools/prd_lint.py: if not destination.exists(): → if True: |
| PY-M107 | linter-percent-encoding-not-decoded | DETECTED | tools/prd_lint.py: unquote(parsed.path) → parsed.path |
| PY-M108 | linter-checks-code-examples | DETECTED | tools/prd_lint.py: if fence is not None:             continue → if False:             continue |
| PY-M109 | linter-inline-examples-checked | DETECTED | tools/prd_lint.py: line = re.sub(r"(`+).*?\1", "", line) → line = line |
| PY-M110 | linter-code-limit-relaxed | DETECTED | tools/prd_lint.py: MAX_CODE_LINES = 15 → MAX_CODE_LINES = 16 |
| PY-M111 | linter-code-limit-too-strict | DETECTED | tools/prd_lint.py: MAX_CODE_LINES = 15 → MAX_CODE_LINES = 14 |
| PY-M112 | ast-database_connectivity_probe-21-11 | INVALID | app/database_connectivity_probe.py: import sys import psycopg import getpass  def probe_database():     try:         password = getpass.getpass(prompt='Password: ', stream=None)         with psycopg.connect(host="127.0.0.1", port=55432, dbname="merlin_d6", user="merlin_d6", password=password, connect_timeout=3) as conn:             conn.read_only = True             with conn.cursor() as cur:                 cur.execute("SELECT current_database(), current_user;")                 db_name, db_user = cur.fetchone()          print(f"PROBE SUCCESS: Connected to database '{db_name}' as user '{db_user}'.")         sys.exit(0)      except psycopg.Error:         print("DB Probe Failed: Connection or query failed.", file=sys.stderr)         sys.exit(1)  if __name__ == "__main__":     probe_database()  → import sys import psycopg import getpass  def probe_database():     try:         password = getpass.getpass(prompt='Password: ', stream=None)         with psycopg.connect(host="127.0.0.1", port=55432, dbname="merlin_d6", user="merlin_d6", password=password, connect_timeout=3) as conn:             conn.read_only = True             with conn.cursor() as cur:                 cur.execute("SELECT current_database(), current_user;")                 db_name, db_user = cur.fetchone()          print(f"PROBE SUCCESS: Connected to database '{db_name}' as user '{db_user}'.")         sys.exit(0)      except psycopg.Error:         print("DB Probe Failed: Connection or query failed.", file=sys.stderr)         sys.exit(1)  if (__name__ != '__main__'):     probe_database()  |
| PY-M113 | ast-notes_maintenance-76-42 | INVALID | app/notes_maintenance.py: - if __name__ == "__main__": ; + if (__name__ != '__main__'): |
| PY-M114 | ast-notes_maintenance-25-60 | DETECTED | app/notes_maintenance.py: -     if database != "merlin_d6" or int(identifier) != EXPECTED_CLUSTER: ; +     if (database != 'merlin_d6' and int(identifier) != EXPECTED_CLUSTER): |
| PY-M115 | ast-notes_maintenance-31-65 | DETECTED | app/notes_maintenance.py: -     if type(batch_size) is not int: ; +     if (type(batch_size) is int): |
| PY-M116 | ast-notes_maintenance-56-82 | DETECTED | app/notes_maintenance.py: -     if args.interval &lt; 10: ; +     if (args.interval &gt;= 10): |
| PY-M117 | ast-notes_maintenance-25-111 | DETECTED | app/notes_maintenance.py: -     if database != "merlin_d6" or int(identifier) != EXPECTED_CLUSTER: ; +     if (database == 'merlin_d6') or int(identifier) != EXPECTED_CLUSTER: |
| PY-M118 | ast-notes_maintenance-25-112 | DETECTED | app/notes_maintenance.py: -     if database != "merlin_d6" or int(identifier) != EXPECTED_CLUSTER: ; +     if database != "merlin_d6" or (int(identifier) == EXPECTED_CLUSTER): |
| PY-M119 | ast-note_rules-28-56 | DETECTED | app/note_rules.py: -     if value is None: ; +     if (value is not None): |
| PY-M120 | ast-note_rules-32-59 | DETECTED | app/note_rules.py: -     return value.strip() or None ; +     return (value.strip() and None) |
| PY-M121 | ast-note_rules-49-78 | DETECTED | app/note_rules.py: -     if title is not None: ; +     if (title is None): |
| PY-M122 | ast-note_rules-57-83 | DETECTED | app/note_rules.py: -     if weighted_length(body) &gt; 7000: ; +     if (weighted_length(body) &lt;= 7000): |
| PY-M123 | ast-note_rules-56-138 | DETECTED | app/note_rules.py: -     body = "" if body is None else body ; +     body = "" if (body is not None) else body |
| PY-M124 | ast-note_rules-60-148 | DETECTED | app/note_rules.py: -     return ValidatedNote(title, body, not is_draft and title is None and not body.strip()) ; +     return ValidatedNote(title, body, (not is_draft or title is None or (not body.strip()))) |
| PY-M125 | ast-note_rules-53-195 | DETECTED | app/note_rules.py: -         elif title_length &gt; 175: ; +         elif (title_length &lt;= 175): |
| PY-M126 | ast-note_rules-60-210 | DETECTED | app/note_rules.py: -     return ValidatedNote(title, body, not is_draft and title is None and not body.strip()) ; +     return ValidatedNote(title, body, not is_draft and (title is not None) and not body.strip()) |
| PY-M127 | ast-doctor-229-52 | INVALID | tools/doctor.py: - if __name__ == '__main__': ; + if (__name__ != '__main__'): |
| PY-M128 | ast-doctor-87-236 | DETECTED | tools/doctor.py: -         if available.returncode == 0: ; +         if (available.returncode != 0): |
| PY-M129 | ast-doctor-91-239 | DETECTED | tools/doctor.py: -         return available.returncode == 0 ; +         return (available.returncode != 0) |
| PY-M130 | ast-doctor-165-292 | DETECTED | tools/doctor.py: -         if pg_port and shutil.which('psql'): ; +         if (pg_port or shutil.which('psql')): |
| PY-M131 | ast-doctor-201-311 | DETECTED | tools/doctor.py: -         rejected = negative.returncode != 0 and 'password authentication failed' in negative.stderr.lower() ; +         rejected = (negative.returncode != 0 or 'password authentication failed' in negative.stderr.lower()) |
| PY-M132 | ast-doctor-207-318 | DETECTED | tools/doctor.py: -         valid = cluster.returncode == 0 and bool(re.fullmatch(r'\d{1,20}', observed)) ; +         valid = (cluster.returncode == 0 or bool(re.fullmatch('\\d{1,20}', observed))) |
| PY-M133 | ast-doctor-214-323 | DETECTED | tools/doctor.py: -         if not self.static and available: ; +         if (not self.static or available): |
| PY-M134 | ast-doctor-35-399 | DETECTED | tools/doctor.py: -         self.failures += int(status == 'FAIL') ; +         self.failures += int((status != 'FAIL')) |
| PY-M135 | ast-doctor-77-479 | DETECTED | tools/doctor.py: -         self.report('ENV-IGNORE', ignored.returncode == 0, 'environment file ignored', 'add .env to .gitignore') ; +         self.report('ENV-IGNORE', (ignored.returncode != 0), 'environment file ignored', 'add .env to .gitignore') |
| PY-M136 | ast-doctor-81-490 | DETECTED | tools/doctor.py: -         self.report('TRACKED-SECRETS', tracked.returncode == 0 and not secrets, ; +         self.report('TRACKED-SECRETS', (tracked.returncode == 0 or not secrets), |
| PY-M137 | ast-doctor-84-498 | DETECTED | tools/doctor.py: -         self.report('VENV-IGNORE', ignored_venv.returncode == 0, 'virtual environment ignored', 'add .venv/ to .gitignore') ; +         self.report('VENV-IGNORE', (ignored_venv.returncode != 0), 'virtual environment ignored', 'add .venv/ to .gitignore') |
| PY-M138 | ast-doctor-86-506 | DETECTED | tools/doctor.py: -         self.report('COMPOSE', available.returncode == 0, 'Docker Compose available', 'install Docker Compose plugin', warn=self.static) ; +         self.report('COMPOSE', (available.returncode != 0), 'Docker Compose available', 'install Docker Compose plugin', warn=self.static) |
| PY-M139 | ast-doctor-108-535 | DETECTED | tools/doctor.py: -             if not isinstance(ports, dict) or not isinstance(log, dict): ; +             if (not isinstance(ports, dict) and (not isinstance(log, dict))): |
| PY-M140 | ast-doctor-131-562 | DETECTED | tools/doctor.py: -             if info is None: ; +             if (info is not None): |
| PY-M141 | ast-doctor-135-568 | DETECTED | tools/doctor.py: -             bindings = host.get('PortBindings', {}).get(port) or &lbrack;&rbrack; ; +             bindings = (host.get('PortBindings', {}).get(port) and &lbrack;&rbrack;) |
| PY-M142 | ast-doctor-136-570 | DETECTED | tools/doctor.py: -             valid_port = len(bindings) == 1 and bindings&lbrack;0&rbrack;.get('HostIp') == '127.0.0.1' and bool(re.fullmatch(r'&lbrack;0-9&rbrack;{1,5}', str(bindings&lbrack;0&rbrack;.get('HostPort', '')))) and 0 &lt; int(bindings&lbrack;0&rbrack;&lbrack;'HostPort'&rbrack;) &lt;= 65535 ; +             valid_port = (len(bindings) == 1 or bindings&lbrack;0&rbrack;.get('HostIp') == '127.0.0.1' or bool(re.fullmatch('&lbrack;0-9&rbrack;{1,5}', str(bindings&lbrack;0&rbrack;.get('HostPort', '')))) or (0 &lt; int(bindings&lbrack;0&rbrack;&lbrack;'HostPort'&rbrack;) &lt;= 65535)) |
| PY-M143 | ast-doctor-157-597 | DETECTED | tools/doctor.py: -         self.report('REDIS-PONG', pong.returncode == 0 and pong.stdout.strip() == 'PONG', 'Redis responds PONG', 'check Redis service') ; +         self.report('REDIS-PONG', (pong.returncode == 0 or pong.stdout.strip() == 'PONG'), 'Redis responds PONG', 'check Redis service') |
| PY-M144 | ast-doctor-169-621 | DETECTED | tools/doctor.py: -             if credentials.returncode == 0 and len(parts) == 3 and all(parts): ; +             if (credentials.returncode == 0 or len(parts) == 3 or all(parts)): |
| PY-M145 | ast-doctor-188-638 | DETECTED | tools/doctor.py: -                   if redis_port and shutil.which('redis-cli') else None) ; +                   if (redis_port or shutil.which('redis-cli')) else None) |
| PY-M146 | ast-doctor-189-643 | DETECTED | tools/doctor.py: -         self.report('HOST-REDIS-PONG', result is not None and result.returncode == 0 and result.stdout.strip() == 'PONG', ; +         self.report('HOST-REDIS-PONG', (result is not None or result.returncode == 0 or result.stdout.strip() == 'PONG'), |
| PY-M147 | ast-doctor-196-657 | DETECTED | tools/doctor.py: -         self.report('PG-AUTH-POSITIVE', positive.returncode == 0 and positive.stdout.strip() == '1', ; +         self.report('PG-AUTH-POSITIVE', (positive.returncode == 0 or positive.stdout.strip() == '1'), |
| PY-M148 | ast-doctor-201-670 | DETECTED | tools/doctor.py: -         rejected = negative.returncode != 0 and 'password authentication failed' in negative.stderr.lower() ; +         rejected = (negative.returncode == 0) and 'password authentication failed' in negative.stderr.lower() |
| PY-M149 | ast-doctor-202-674 | DETECTED | tools/doctor.py: -         self.report('PG-AUTH-NEGATIVE', positive.returncode == 0 and positive.stdout.strip() == '1' and rejected, ; +         self.report('PG-AUTH-NEGATIVE', (positive.returncode == 0 or positive.stdout.strip() == '1' or rejected), |
| PY-M150 | ast-doctor-207-689 | DETECTED | tools/doctor.py: -         valid = cluster.returncode == 0 and bool(re.fullmatch(r'\d{1,20}', observed)) ; +         valid = (cluster.returncode != 0) and bool(re.fullmatch(r'\d{1,20}', observed)) |
| PY-M151 | ast-doctor-208-693 | DETECTED | tools/doctor.py: -         self.report('PG-CLUSTER', valid and (self.expect_cluster is None or observed == self.expect_cluster), ; +         self.report('PG-CLUSTER', (valid or (self.expect_cluster is None or observed == self.expect_cluster)), |
| PY-M152 | ast-doctor-59-844 | DETECTED | tools/doctor.py: -             self.report('UV-LOCK', result.returncode == 0, 'offline lock consistency checked', 'run uv lock and review changes') ; +             self.report('UV-LOCK', (result.returncode != 0), 'offline lock consistency checked', 'run uv lock and review changes') |
| PY-M153 | ast-doctor-67-873 | DETECTED | tools/doctor.py: -             self.report(tool.upper(), result.returncode == 0 and bool(match) and int(match&lbrack;1&rbrack;) == major, ; +             self.report(tool.upper(), (result.returncode == 0 or bool(match) or int(match&lbrack;1&rbrack;) == major), |
| PY-M154 | ast-doctor-75-893 | DETECTED | tools/doctor.py: -             self.report('ENV-MODE', env.stat().st_mode & 0o077 == 0, 'environment file private', 'chmod 600 .env') ; +             self.report('ENV-MODE', (env.stat().st_mode & 63 != 0), 'environment file private', 'chmod 600 .env') |
| PY-M155 | ast-doctor-79-917 | DETECTED | tools/doctor.py: +         secrets = &lbrack;p for p in tracked.stdout.split('\0') if (Path(p).name == '.env' and (Path(p).name.startswith('.env.') and Path(p).name != '.env.example'))&rbrack; ; -         secrets = &lbrack;p for p in tracked.stdout.split('\0') if Path(p).name == '.env' or ; -                    (Path(p).name.startswith('.env.') and Path(p).name != '.env.example')&rbrack; |
| PY-M156 | ast-doctor-81-921 | DETECTED | tools/doctor.py: -         self.report('TRACKED-SECRETS', tracked.returncode == 0 and not secrets, ; +         self.report('TRACKED-SECRETS', (tracked.returncode != 0) and not secrets, |
| PY-M157 | ast-doctor-89-951 | DETECTED | tools/doctor.py: -             self.report('COMPOSE-CONFIG', config.returncode == 0, 'quiet Compose validation completed', ; +             self.report('COMPOSE-CONFIG', (config.returncode != 0), 'quiet Compose validation completed', |
| PY-M158 | ast-doctor-102-975 | DETECTED | tools/doctor.py: +             if not ((isinstance(health, str) or isinstance(host, dict) or isinstance(mounts, list) or all((isinstance(mount, dict) for mount in mounts)) or isinstance(labels, dict))): ; -             if not (isinstance(health, str) and isinstance(host, dict) ; -                     and isinstance(mounts, list) and all(isinstance(mount, dict) for mount in mounts) ; -                     and isinstance(labels, dict)): |
| PY-M159 | ast-doctor-128-1029 | DETECTED | tools/doctor.py: -             info = self.inspect(container) if ids.returncode == 0 and re.fullmatch(r'&lbrack;a-f0-9&rbrack;{12,64}', container) else None ; +             info = self.inspect(container) if (ids.returncode == 0 or re.fullmatch('&lbrack;a-f0-9&rbrack;{12,64}', container)) else None |
| PY-M160 | ast-doctor-130-1036 | DETECTED | tools/doctor.py: -             self.report(prefix + '-RUNNING', info is not None, 'service inspect available', 'start this project with docker compose up -d') ; +             self.report(prefix + '-RUNNING', (info is None), 'service inspect available', 'start this project with docker compose up -d') |
| PY-M161 | ast-doctor-134-1050 | DETECTED | tools/doctor.py: -             self.report(prefix + '-HEALTH', health == 'healthy', 'service healthy', 'inspect service health privately') ; +             self.report(prefix + '-HEALTH', (health != 'healthy'), 'service healthy', 'inspect service health privately') |
| PY-M162 | ast-doctor-136-1059 | DETECTED | tools/doctor.py: -             valid_port = len(bindings) == 1 and bindings&lbrack;0&rbrack;.get('HostIp') == '127.0.0.1' and bool(re.fullmatch(r'&lbrack;0-9&rbrack;{1,5}', str(bindings&lbrack;0&rbrack;.get('HostPort', '')))) and 0 &lt; int(bindings&lbrack;0&rbrack;&lbrack;'HostPort'&rbrack;) &lt;= 65535 ; +             valid_port = (len(bindings) != 1) and bindings&lbrack;0&rbrack;.get('HostIp') == '127.0.0.1' and bool(re.fullmatch(r'&lbrack;0-9&rbrack;{1,5}', str(bindings&lbrack;0&rbrack;.get('HostPort', '')))) and 0 &lt; int(bindings&lbrack;0&rbrack;&lbrack;'HostPort'&rbrack;) &lt;= 65535 |
| PY-M163 | ast-doctor-136-1060 | DETECTED | tools/doctor.py: -             valid_port = len(bindings) == 1 and bindings&lbrack;0&rbrack;.get('HostIp') == '127.0.0.1' and bool(re.fullmatch(r'&lbrack;0-9&rbrack;{1,5}', str(bindings&lbrack;0&rbrack;.get('HostPort', '')))) and 0 &lt; int(bindings&lbrack;0&rbrack;&lbrack;'HostPort'&rbrack;) &lt;= 65535 ; +             valid_port = len(bindings) == 1 and (bindings&lbrack;0&rbrack;.get('HostIp') != '127.0.0.1') and bool(re.fullmatch(r'&lbrack;0-9&rbrack;{1,5}', str(bindings&lbrack;0&rbrack;.get('HostPort', '')))) and 0 &lt; int(bindings&lbrack;0&rbrack;&lbrack;'HostPort'&rbrack;) &lt;= 65535 |
| PY-M164 | ast-doctor-141-1073 | DETECTED | tools/doctor.py: -             self.report(prefix + '-LIMITS', host.get('Memory') == memory and host.get('NanoCpus') == cpus, ; +             self.report(prefix + '-LIMITS', (host.get('Memory') == memory or host.get('NanoCpus') == cpus), |
| PY-M165 | ast-doctor-144-1082 | DETECTED | tools/doctor.py: +             self.report(prefix + '-LOGS', (log.get('Type') == 'json-file' or log.get('Config', {}).get('max-size') == '10m' or log.get('Config', {}).get('max-file') == '3'), 'logs bounded', 'restore 10m / 3 log rotation') ; -             self.report(prefix + '-LOGS', log.get('Type') == 'json-file' and log.get('Config', {}).get('max-size') == '10m' ; -                         and log.get('Config', {}).get('max-file') == '3', 'logs bounded', 'restore 10m / 3 log rotation') |
| PY-M166 | ast-doctor-148-1094 | DETECTED | tools/doctor.py: -             self.report(prefix + '-VOLUME', bool(project) and len(matching) == 1 and matching&lbrack;0&rbrack;.get('Type') == 'volume' ; +             self.report(prefix + '-VOLUME', (bool(project) or len(matching) == 1 or matching&lbrack;0&rbrack;.get('Type') == 'volume' or (matching&lbrack;0&rbrack;.get('Name') == f'{project}_{service}_data')), ; -                         and matching&lbrack;0&rbrack;.get('Name') == f'{project}_{service}_data', |
| PY-M167 | ast-doctor-152-1107 | DETECTED | tools/doctor.py: -             self.report(prefix + '-UID', uid.returncode == 0 and uid.stdout.strip() == '999', ; +             self.report(prefix + '-UID', (uid.returncode == 0 or uid.stdout.strip() == '999'), |
| PY-M168 | ast-doctor-157-1119 | DETECTED | tools/doctor.py: -         self.report('REDIS-PONG', pong.returncode == 0 and pong.stdout.strip() == 'PONG', 'Redis responds PONG', 'check Redis service') ; +         self.report('REDIS-PONG', (pong.returncode != 0) and pong.stdout.strip() == 'PONG', 'Redis responds PONG', 'check Redis service') |
| PY-M169 | ast-doctor-157-1120 | DETECTED | tools/doctor.py: -         self.report('REDIS-PONG', pong.returncode == 0 and pong.stdout.strip() == 'PONG', 'Redis responds PONG', 'check Redis service') ; +         self.report('REDIS-PONG', pong.returncode == 0 and (pong.stdout.strip() != 'PONG'), 'Redis responds PONG', 'check Redis service') |
| PY-M170 | ast-doctor-160-1147 | DETECTED | tools/doctor.py: -             self.report('REDIS-' + key.upper(), result.returncode == 0 and result.stdout.splitlines() == &lbrack;key, value&rbrack;, ; +             self.report('REDIS-' + key.upper(), (result.returncode == 0 or result.stdout.splitlines() == &lbrack;key, value&rbrack;), |
| PY-M171 | ast-doctor-169-1167 | DETECTED | tools/doctor.py: -             if credentials.returncode == 0 and len(parts) == 3 and all(parts): ; +             if (credentials.returncode != 0) and len(parts) == 3 and all(parts): |
| PY-M172 | ast-doctor-169-1168 | DETECTED | tools/doctor.py: -             if credentials.returncode == 0 and len(parts) == 3 and all(parts): ; +             if credentials.returncode == 0 and (len(parts) != 3) and all(parts): |
| PY-M173 | ast-doctor-177-1183 | DETECTED | tools/doctor.py: -                 accepted = positive.returncode == 0 and positive.stdout.strip() == '1' ; +                 accepted = (positive.returncode == 0 or positive.stdout.strip() == '1') |
| PY-M174 | ast-doctor-178-1185 | DETECTED | tools/doctor.py: -                 rejected = negative.returncode != 0 and 'password authentication failed' in negative.stderr.lower() ; +                 rejected = (negative.returncode != 0 or 'password authentication failed' in negative.stderr.lower()) |
| PY-M175 | ast-doctor-189-1205 | DETECTED | tools/doctor.py: -         self.report('HOST-REDIS-PONG', result is not None and result.returncode == 0 and result.stdout.strip() == 'PONG', ; +         self.report('HOST-REDIS-PONG', (result is None) and result.returncode == 0 and result.stdout.strip() == 'PONG', |
| PY-M176 | ast-doctor-189-1206 | DETECTED | tools/doctor.py: -         self.report('HOST-REDIS-PONG', result is not None and result.returncode == 0 and result.stdout.strip() == 'PONG', ; +         self.report('HOST-REDIS-PONG', result is not None and (result.returncode != 0) and result.stdout.strip() == 'PONG', |
| PY-M177 | ast-doctor-189-1207 | DETECTED | tools/doctor.py: -         self.report('HOST-REDIS-PONG', result is not None and result.returncode == 0 and result.stdout.strip() == 'PONG', ; +         self.report('HOST-REDIS-PONG', result is not None and result.returncode == 0 and (result.stdout.strip() != 'PONG'), |
| PY-M178 | ast-doctor-196-1216 | DETECTED | tools/doctor.py: -         self.report('PG-AUTH-POSITIVE', positive.returncode == 0 and positive.stdout.strip() == '1', ; +         self.report('PG-AUTH-POSITIVE', (positive.returncode != 0) and positive.stdout.strip() == '1', |
| PY-M179 | ast-doctor-196-1217 | DETECTED | tools/doctor.py: -         self.report('PG-AUTH-POSITIVE', positive.returncode == 0 and positive.stdout.strip() == '1', ; +         self.report('PG-AUTH-POSITIVE', positive.returncode == 0 and (positive.stdout.strip() != '1'), |
| PY-M180 | ast-doctor-202-1232 | DETECTED | tools/doctor.py: -         self.report('PG-AUTH-NEGATIVE', positive.returncode == 0 and positive.stdout.strip() == '1' and rejected, ; +         self.report('PG-AUTH-NEGATIVE', (positive.returncode != 0) and positive.stdout.strip() == '1' and rejected, |
| PY-M181 | ast-doctor-202-1233 | DETECTED | tools/doctor.py: -         self.report('PG-AUTH-NEGATIVE', positive.returncode == 0 and positive.stdout.strip() == '1' and rejected, ; +         self.report('PG-AUTH-NEGATIVE', positive.returncode == 0 and (positive.stdout.strip() != '1') and rejected, |
| PY-M182 | ast-doctor-208-1251 | DETECTED | tools/doctor.py: -         self.report('PG-CLUSTER', valid and (self.expect_cluster is None or observed == self.expect_cluster), ; +         self.report('PG-CLUSTER', valid and ((self.expect_cluster is None and observed == self.expect_cluster)), |
| PY-M183 | ast-doctor-67-1382 | DETECTED | tools/doctor.py: -             self.report(tool.upper(), result.returncode == 0 and bool(match) and int(match&lbrack;1&rbrack;) == major, ; +             self.report(tool.upper(), (result.returncode != 0) and bool(match) and int(match&lbrack;1&rbrack;) == major, |
| PY-M184 | ast-doctor-67-1384 | DETECTED | tools/doctor.py: -             self.report(tool.upper(), result.returncode == 0 and bool(match) and int(match&lbrack;1&rbrack;) == major, ; +             self.report(tool.upper(), result.returncode == 0 and bool(match) and (int(match&lbrack;1&rbrack;) != major), |
| PY-M185 | ast-doctor-79-1422 | DETECTED | tools/doctor.py: -         secrets = &lbrack;p for p in tracked.stdout.split('\0') if Path(p).name == '.env' or ; +         secrets = &lbrack;p for p in tracked.stdout.split('\0') if (Path(p).name != '.env') or |
| PY-M186 | ast-doctor-80-1423 | DETECTED | tools/doctor.py: -                    (Path(p).name.startswith('.env.') and Path(p).name != '.env.example')&rbrack; ; +                    ((Path(p).name.startswith('.env.') or Path(p).name != '.env.example'))&rbrack; |
| PY-M187 | ast-doctor-90-1448 | DETECTED | tools/doctor.py: -                         'check local environment and Compose syntax privately', warn=self.static and not env.is_file()) ; +                         'check local environment and Compose syntax privately', warn=(self.static or not env.is_file())) |
| PY-M188 | ast-doctor-112-1479 | DETECTED | tools/doctor.py: +             if any((bindings is not None or (not isinstance(bindings, list) or any((not isinstance(binding, dict) for binding in bindings)))) ; -             if any(bindings is not None and ( ; -                     not isinstance(bindings, list) ; -                     or any(not isinstance(binding, dict) for binding in bindings)) |
| PY-M189 | ast-doctor-128-1493 | DETECTED | tools/doctor.py: -             info = self.inspect(container) if ids.returncode == 0 and re.fullmatch(r'&lbrack;a-f0-9&rbrack;{12,64}', container) else None ; +             info = self.inspect(container) if (ids.returncode != 0) and re.fullmatch(r'&lbrack;a-f0-9&rbrack;{12,64}', container) else None |
| PY-M190 | ast-doctor-141-1553 | DETECTED | tools/doctor.py: -             self.report(prefix + '-LIMITS', host.get('Memory') == memory and host.get('NanoCpus') == cpus, ; +             self.report(prefix + '-LIMITS', (host.get('Memory') != memory) and host.get('NanoCpus') == cpus, |
| PY-M191 | ast-doctor-141-1554 | DETECTED | tools/doctor.py: -             self.report(prefix + '-LIMITS', host.get('Memory') == memory and host.get('NanoCpus') == cpus, ; +             self.report(prefix + '-LIMITS', host.get('Memory') == memory and (host.get('NanoCpus') != cpus), |
| PY-M192 | ast-doctor-144-1563 | DETECTED | tools/doctor.py: -             self.report(prefix + '-LOGS', log.get('Type') == 'json-file' and log.get('Config', {}).get('max-size') == '10m' ; +             self.report(prefix + '-LOGS', (log.get('Type') != 'json-file') and log.get('Config', {}).get('max-size') == '10m' |
| PY-M193 | ast-doctor-144-1564 | DETECTED | tools/doctor.py: -             self.report(prefix + '-LOGS', log.get('Type') == 'json-file' and log.get('Config', {}).get('max-size') == '10m' ; +             self.report(prefix + '-LOGS', log.get('Type') == 'json-file' and (log.get('Config', {}).get('max-size') != '10m') |
| PY-M194 | ast-doctor-145-1565 | DETECTED | tools/doctor.py: -                         and log.get('Config', {}).get('max-file') == '3', 'logs bounded', 'restore 10m / 3 log rotation') ; +                         and (log.get('Config', {}).get('max-file') != '3'), 'logs bounded', 'restore 10m / 3 log rotation') |
| PY-M195 | ast-doctor-147-1571 | DETECTED | tools/doctor.py: -             matching = &lbrack;m for m in mounts if m.get('Destination') == destination&rbrack; ; +             matching = &lbrack;m for m in mounts if (m.get('Destination') != destination)&rbrack; |
| PY-M196 | ast-doctor-148-1579 | DETECTED | tools/doctor.py: -             self.report(prefix + '-VOLUME', bool(project) and len(matching) == 1 and matching&lbrack;0&rbrack;.get('Type') == 'volume' ; +             self.report(prefix + '-VOLUME', bool(project) and (len(matching) != 1) and matching&lbrack;0&rbrack;.get('Type') == 'volume' |
| PY-M197 | ast-doctor-148-1580 | DETECTED | tools/doctor.py: -             self.report(prefix + '-VOLUME', bool(project) and len(matching) == 1 and matching&lbrack;0&rbrack;.get('Type') == 'volume' ; +             self.report(prefix + '-VOLUME', bool(project) and len(matching) == 1 and (matching&lbrack;0&rbrack;.get('Type') != 'volume') |
| PY-M198 | ast-doctor-149-1581 | DETECTED | tools/doctor.py: -                         and matching&lbrack;0&rbrack;.get('Name') == f'{project}_{service}_data', ; +                         and (matching&lbrack;0&rbrack;.get('Name') != f'{project}_{service}_data'), |
| PY-M199 | ast-doctor-152-1591 | DETECTED | tools/doctor.py: -             self.report(prefix + '-UID', uid.returncode == 0 and uid.stdout.strip() == '999', ; +             self.report(prefix + '-UID', (uid.returncode != 0) and uid.stdout.strip() == '999', |
| PY-M200 | ast-doctor-152-1592 | DETECTED | tools/doctor.py: -             self.report(prefix + '-UID', uid.returncode == 0 and uid.stdout.strip() == '999', ; +             self.report(prefix + '-UID', uid.returncode == 0 and (uid.stdout.strip() != '999'), |
| PY-M201 | ast-doctor-160-1612 | DETECTED | tools/doctor.py: -             self.report('REDIS-' + key.upper(), result.returncode == 0 and result.stdout.splitlines() == &lbrack;key, value&rbrack;, ; +             self.report('REDIS-' + key.upper(), (result.returncode != 0) and result.stdout.splitlines() == &lbrack;key, value&rbrack;, |
| PY-M202 | ast-doctor-160-1613 | DETECTED | tools/doctor.py: -             self.report('REDIS-' + key.upper(), result.returncode == 0 and result.stdout.splitlines() == &lbrack;key, value&rbrack;, ; +             self.report('REDIS-' + key.upper(), result.returncode == 0 and (result.stdout.splitlines() != &lbrack;key, value&rbrack;), |
| PY-M203 | ast-doctor-177-1671 | DETECTED | tools/doctor.py: -                 accepted = positive.returncode == 0 and positive.stdout.strip() == '1' ; +                 accepted = (positive.returncode != 0) and positive.stdout.strip() == '1' |
| PY-M204 | ast-doctor-177-1672 | DETECTED | tools/doctor.py: -                 accepted = positive.returncode == 0 and positive.stdout.strip() == '1' ; +                 accepted = positive.returncode == 0 and (positive.stdout.strip() != '1') |
| PY-M205 | ast-doctor-178-1675 | DETECTED | tools/doctor.py: -                 rejected = negative.returncode != 0 and 'password authentication failed' in negative.stderr.lower() ; +                 rejected = (negative.returncode == 0) and 'password authentication failed' in negative.stderr.lower() |
| PY-M206 | ast-doctor-180-1684 | DETECTED | tools/doctor.py: -                 self.report('HOST-PG-NEGATIVE', accepted and rejected, 'host TCP wrong password explicitly rejected', ; +                 self.report('HOST-PG-NEGATIVE', (accepted or rejected), 'host TCP wrong password explicitly rejected', |
| PY-M207 | ast-doctor-208-1760 | DETECTED | tools/doctor.py: -         self.report('PG-CLUSTER', valid and (self.expect_cluster is None or observed == self.expect_cluster), ; +         self.report('PG-CLUSTER', valid and ((self.expect_cluster is not None) or observed == self.expect_cluster), |
| PY-M208 | ast-doctor-208-1761 | DETECTED | tools/doctor.py: -         self.report('PG-CLUSTER', valid and (self.expect_cluster is None or observed == self.expect_cluster), ; +         self.report('PG-CLUSTER', valid and (self.expect_cluster is None or (observed != self.expect_cluster)), |
| PY-M209 | ast-doctor-80-1859 | DETECTED | tools/doctor.py: -                    (Path(p).name.startswith('.env.') and Path(p).name != '.env.example')&rbrack; ; +                    (Path(p).name.startswith('.env.') and (Path(p).name == '.env.example'))&rbrack; |
| PY-M210 | ast-doctor-112-1907 | DETECTED | tools/doctor.py: -             if any(bindings is not None and ( ; +             if any((bindings is None) and ( |
| PY-M211 | ast-doctor-113-1908 | DETECTED | tools/doctor.py: -                     not isinstance(bindings, list) ; -                     or any(not isinstance(binding, dict) for binding in bindings)) ; +                     (not isinstance(bindings, list) and any((not isinstance(binding, dict) for binding in bindings)))) |
| PY-M212 | ast-prd_lint-181-88 | INVALID | tools/prd_lint.py: - if __name__ == "__main__": ; + if (__name__ != '__main__'): |
| PY-M213 | ast-prd_lint-36-136 | DETECTED | tools/prd_lint.py: -     if folder.name == "planning" and folder.parent.name == "docs": ; +     if (folder.name == 'planning' or folder.parent.name == 'docs'): |
| PY-M214 | ast-prd_lint-148-212 | DETECTED | tools/prd_lint.py: -     if folder.name == "docs": ; +     if (folder.name != 'docs'): |
| PY-M215 | ast-prd_lint-36-268 | DETECTED | tools/prd_lint.py: -     if folder.name == "planning" and folder.parent.name == "docs": ; +     if (folder.name != 'planning') and folder.parent.name == "docs": |
| PY-M216 | ast-prd_lint-36-269 | DETECTED | tools/prd_lint.py: -     if folder.name == "planning" and folder.parent.name == "docs": ; +     if folder.name == "planning" and (folder.parent.name != 'docs'): |
| PY-M217 | ast-prd_lint-53-286 | DETECTED | tools/prd_lint.py: -         if fence is not None: ; +         if (fence is None): |
| PY-M218 | ast-prd_lint-55-288 | DETECTED | tools/prd_lint.py: -         if path.suffix == ".md": ; +         if (path.suffix != '.md'): |
| PY-M219 | ast-prd_lint-154-425 | DETECTED | tools/prd_lint.py: -         if len(v) &gt; 1: ; +         if (len(v) &lt;= 1): |
| PY-M220 | ast-prd_lint-157-431 | DETECTED | tools/prd_lint.py: -         if len(v) &gt; 1: ; +         if (len(v) &lt;= 1): |
| PY-M221 | ast-prd_lint-162-438 | DETECTED | tools/prd_lint.py: -         if missing and len(days) &gt; 5: ; +         if (missing or len(days) &gt; 5): |
| PY-M222 | ast-prd_lint-46-491 | DETECTED | tools/prd_lint.py: -         marker = re.match(r"^\s*(`{3,}\|~{3,})(.*)$", line) if path.suffix == ".md" else None ; +         marker = re.match(r"^\s*(`{3,}\|~{3,})(.*)$", line) if (path.suffix != '.md') else None |
| PY-M223 | ast-prd_lint-48-495 | DETECTED | tools/prd_lint.py: -             if fence is None: ; +             if (fence is not None): |
| PY-M224 | ast-prd_lint-65-524 | DETECTED | tools/prd_lint.py: -             if parsed.scheme or parsed.netloc or not parsed.path: ; +             if (parsed.scheme and parsed.netloc and (not parsed.path)): |
| PY-M225 | ast-prd_lint-94-550 | DETECTED | tools/prd_lint.py: -             if SPRINT_PART.match(path.name) and re.match(r"^DAY\s+\d+", line, re.I): ; +             if (SPRINT_PART.match(path.name) or re.match('^DAY\\s+\\d+', line, re.I)): |
| PY-M226 | ast-prd_lint-108-568 | DETECTED | tools/prd_lint.py: -             if kid and h.group(2).lower().startswith(("sk-", "skill")): ; +             if (kid or h.group(2).lower().startswith(('sk-', 'skill'))): |
| PY-M227 | ast-prd_lint-120-593 | DETECTED | tools/prd_lint.py: -             if lvl &lt;= level: ; +             if (lvl &gt; level): |
| PY-M228 | ast-prd_lint-162-690 | DETECTED | tools/prd_lint.py: -         if missing and len(days) &gt; 5: ; +         if missing and (len(days) &lt;= 5): |
| PY-M229 | ast-prd_lint-50-752 | DETECTED | tools/prd_lint.py: -             elif marker.group(1)&lbrack;0&rbrack; == fence&lbrack;0&rbrack; and len(marker.group(1)) &gt;= len(fence) and not marker.group(2).strip(): ; +             elif (marker.group(1)&lbrack;0&rbrack; == fence&lbrack;0&rbrack; or len(marker.group(1)) &gt;= len(fence) or (not marker.group(2).strip())): |
| PY-M230 | ast-prd_lint-85-801 | DETECTED | tools/prd_lint.py: -             elif m.group(1)&lbrack;0&rbrack; == fence&lbrack;0&rbrack; and len(m.group(1)) &gt;= len(fence) and not m.group(2).strip(): ; +             elif (m.group(1)&lbrack;0&rbrack; == fence&lbrack;0&rbrack; or len(m.group(1)) &gt;= len(fence) or (not m.group(2).strip())): |
| PY-M231 | ast-prd_lint-111-834 | DETECTED | tools/prd_lint.py: -             d = DAY_ENTRY.match(h.group(2)) if SPRINT_PART.match(path.name) and len(h.group(1)) == 2 else None ; +             d = DAY_ENTRY.match(h.group(2)) if (SPRINT_PART.match(path.name) or len(h.group(1)) == 2) else None |
| PY-M232 | ast-prd_lint-161-927 | DETECTED | tools/prd_lint.py: -         dupes = {d: v for d, v in days.items() if len(v) &gt; 1} ; +         dupes = {d: v for d, v in days.items() if (len(v) &lt;= 1)} |
| PY-M233 | ast-prd_lint-50-979 | DETECTED | tools/prd_lint.py: -             elif marker.group(1)&lbrack;0&rbrack; == fence&lbrack;0&rbrack; and len(marker.group(1)) &gt;= len(fence) and not marker.group(2).strip(): ; +             elif (marker.group(1)&lbrack;0&rbrack; != fence&lbrack;0&rbrack;) and len(marker.group(1)) &gt;= len(fence) and not marker.group(2).strip(): |
| PY-M234 | ast-prd_lint-50-980 | DETECTED | tools/prd_lint.py: -             elif marker.group(1)&lbrack;0&rbrack; == fence&lbrack;0&rbrack; and len(marker.group(1)) &gt;= len(fence) and not marker.group(2).strip(): ; +             elif marker.group(1)&lbrack;0&rbrack; == fence&lbrack;0&rbrack; and (len(marker.group(1)) &lt; len(fence)) and not marker.group(2).strip(): |
| PY-M235 | ast-prd_lint-85-1027 | DETECTED | tools/prd_lint.py: -             elif m.group(1)&lbrack;0&rbrack; == fence&lbrack;0&rbrack; and len(m.group(1)) &gt;= len(fence) and not m.group(2).strip(): ; +             elif (m.group(1)&lbrack;0&rbrack; != fence&lbrack;0&rbrack;) and len(m.group(1)) &gt;= len(fence) and not m.group(2).strip(): |
| PY-M236 | ast-prd_lint-85-1028 | DETECTED | tools/prd_lint.py: -             elif m.group(1)&lbrack;0&rbrack; == fence&lbrack;0&rbrack; and len(m.group(1)) &gt;= len(fence) and not m.group(2).strip(): ; +             elif m.group(1)&lbrack;0&rbrack; == fence&lbrack;0&rbrack; and (len(m.group(1)) &lt; len(fence)) and not m.group(2).strip(): |
| PY-M237 | ast-prd_lint-87-1032 | DETECTED | tools/prd_lint.py: -                 if lang in CODE_LANGS and n &gt; MAX_CODE_LINES: ; +                 if (lang in CODE_LANGS or n &gt; MAX_CODE_LINES): |
| PY-M238 | ast-prd_lint-111-1079 | DETECTED | tools/prd_lint.py: -             d = DAY_ENTRY.match(h.group(2)) if SPRINT_PART.match(path.name) and len(h.group(1)) == 2 else None ; +             d = DAY_ENTRY.match(h.group(2)) if SPRINT_PART.match(path.name) and (len(h.group(1)) != 2) else None |
| PY-M239 | ast-prd_lint-87-1260 | DETECTED | tools/prd_lint.py: -                 if lang in CODE_LANGS and n &gt; MAX_CODE_LINES: ; +                 if lang in CODE_LANGS and (n &lt;= MAX_CODE_LINES): |

## PostgreSQL

The same transaction-local schema fault was paired with several cases. Its status records all pair outcomes; it need not break unrelated behavior.

| ID | Fault | Pair outcomes | Transaction-local SQL |
|---|---|---|---|
| SQL-M001 | incorrect-weighted-count | {'DETECTED_ASSERTION': 8} | CREATE OR REPLACE FUNCTION public.note_weighted_length(value TEXT) RETURNS INTEGER LANGUAGE plpython3u AS $fault$ return 0 $fault$; |
| SQL-M002 | incorrect-weighted-count | {'DETECTED_ASSERTION': 1} | CREATE OR REPLACE FUNCTION public.note_weighted_length(value TEXT) RETURNS INTEGER LANGUAGE plpython3u AS $fault$ return 1 $fault$; |
| SQL-M003 | valid-text-overcounted | {'DETECTED_BEHAVIOR_ERROR': 6} | CREATE OR REPLACE FUNCTION public.note_weighted_length(value TEXT) RETURNS INTEGER LANGUAGE plpython3u AS $fault$ return len(value) + 10000 $fault$; |
| SQL-M004 | constraint-removed-notes_title_limit | {'DETECTED_ASSERTION': 3} | ALTER TABLE public.notes DROP CONSTRAINT notes_title_limit; |
| SQL-M005 | constraint-removed-notes_body_limit | {'DETECTED_ASSERTION': 3} | ALTER TABLE public.notes DROP CONSTRAINT notes_body_limit; |
| SQL-M006 | whitespace-misclassified-content | {'DETECTED_ASSERTION': 122, 'DETECTED_BEHAVIOR_ERROR': 29} | CREATE OR REPLACE FUNCTION public.note_text_is_blank(value TEXT) RETURNS BOOLEAN LANGUAGE plpython3u AS $fault$ return value is None $fault$; |
| SQL-M007 | real-content-trimmed | {'DETECTED_ASSERTION': 1} | CREATE OR REPLACE FUNCTION public.manage_note_content() RETURNS TRIGGER LANGUAGE plpgsql AS $fault$ BEGIN NEW.title:=btrim(NEW.title); RETURN NEW; END $fault$; |
| SQL-M008 | real-content-trimmed | {'DETECTED_ASSERTION': 1} | CREATE OR REPLACE FUNCTION public.manage_note_content() RETURNS TRIGGER LANGUAGE plpgsql AS $fault$ BEGIN NEW.body:=btrim(NEW.body); RETURN NEW; END $fault$; |
| SQL-M009 | constraint-removed-notes_has_content | {'DETECTED_ASSERTION': 31} | ALTER TABLE public.notes DROP CONSTRAINT notes_has_content; |
| SQL-M010 | drafts-now-forbidden | {'DETECTED_BEHAVIOR_ERROR': 2} | ALTER TABLE public.notes ADD CONSTRAINT audit_reject_drafts CHECK (NOT is_draft); |
| SQL-M011 | countdown-too-short | {'DETECTED_ASSERTION': 36, 'SURVIVED': 5} | DO $mutate$ DECLARE original text; BEGIN SELECT pg_get_functiondef('public.manage_note_content()'::regprocedure) INTO original; IF position($old$INTERVAL '24 hours'$old$ IN original)=0 THEN RAISE EXCEPTION 'UNAPPLIED source fault'; END IF; EXECUTE replace(original,$old$INTERVAL '24 hours'$old$,$new$INTERVAL '1 hour'$new$); END $mutate$; |
| SQL-M012 | countdown-not-preserved | {'SURVIVED': 37, 'DETECTED_ASSERTION': 4} | DO $mutate$ DECLARE original text; BEGIN SELECT pg_get_functiondef('public.manage_note_content()'::regprocedure) INTO original; IF position($old$NEW.blank_body_expires_at := OLD.blank_body_expires_at;$old$ IN original)=0 THEN RAISE EXCEPTION 'UNAPPLIED source fault'; END IF; EXECUTE replace(original,$old$NEW.blank_body_expires_at := OLD.blank_body_expires_at;$old$,$new$NEW.blank_body_expires_at := statement_timestamp() + INTERVAL '48 hours';$new$); END $mutate$; |
| SQL-M013 | optional-title-now-required | {'DETECTED_BEHAVIOR_ERROR': 1} | ALTER TABLE public.notes ALTER COLUMN title SET NOT NULL; |
| SQL-M014 | null-emails-now-unique | {'DETECTED_BEHAVIOR_ERROR': 1} | CREATE UNIQUE INDEX audit_null_email ON public.users(email) NULLS NOT DISTINCT; |
| SQL-M015 | email-uniqueness-removed | {'DETECTED_ASSERTION': 2} | DROP INDEX public.users_email_unique; |
| SQL-M016 | email-cleanliness-always-accepts, stored-email-validation-removed | {'SURVIVED': 1, 'DETECTED_ASSERTION': 94} | CREATE OR REPLACE FUNCTION public.note_email_is_clean(value TEXT) RETURNS BOOLEAN LANGUAGE plpython3u AS $fault$ return True $fault$; |
| SQL-M017 | constraint-removed-users_email_clean | {'DETECTED_ASSERTION': 94} | ALTER TABLE public.users DROP CONSTRAINT users_email_clean; |
| SQL-M018 | required-column-now-nullable | {'DETECTED_ASSERTION': 1} | ALTER TABLE public.users ALTER COLUMN username DROP NOT NULL; |
| SQL-M019 | constraint-removed-users_username_format | {'DETECTED_ASSERTION': 4} | ALTER TABLE public.users DROP CONSTRAINT users_username_format; |
| SQL-M020 | valid-username-limit-too-strict | {'DETECTED_BEHAVIOR_ERROR': 1} | ALTER TABLE public.users ADD CONSTRAINT audit_username_limit CHECK(length(username)&lt;20); |
| SQL-M021 | constraint-removed-users_username_unique | {'DETECTED_ASSERTION': 1} | ALTER TABLE public.users DROP CONSTRAINT users_username_unique; |
| SQL-M022 | canonical-column-not-generated | {'DETECTED_ASSERTION': 1} | ALTER TABLE public.users ALTER COLUMN username_canonical DROP EXPRESSION; |
| SQL-M023 | uuid-default-missing | {'DETECTED_BEHAVIOR_ERROR': 1} | ALTER TABLE public.users ALTER COLUMN id DROP DEFAULT; |
| SQL-M024 | uuid-default-missing | {'DETECTED_BEHAVIOR_ERROR': 1} | ALTER TABLE public.notes ALTER COLUMN id DROP DEFAULT; |
| SQL-M025 | constraint-removed-users_id_uuidv4 | {'DETECTED_ASSERTION': 2} | ALTER TABLE public.users DROP CONSTRAINT users_id_uuidv4; |
| SQL-M026 | constraint-removed-notes_id_uuidv4 | {'DETECTED_ASSERTION': 2} | ALTER TABLE public.notes DROP CONSTRAINT notes_id_uuidv4; |
| SQL-M027 | constraint-removed-notes_pkey | {'DETECTED_ASSERTION': 1} | ALTER TABLE public.notes DROP CONSTRAINT notes_pkey; |
| SQL-M028 | required-column-now-nullable | {'DETECTED_ASSERTION': 1} | ALTER TABLE public.notes ALTER COLUMN user_id DROP NOT NULL; |
| SQL-M029 | constraint-removed-notes_user_id_fkey | {'DETECTED_ASSERTION': 1} | ALTER TABLE public.notes DROP CONSTRAINT notes_user_id_fkey; |
| SQL-M030 | cascade-now-restricts | {'DETECTED_BEHAVIOR_ERROR': 2} | ALTER TABLE public.notes DROP CONSTRAINT notes_user_id_fkey; ALTER TABLE public.notes ADD CONSTRAINT notes_user_id_fkey FOREIGN KEY(user_id) REFERENCES public.users(id) ON DELETE NO ACTION; |
| SQL-M031 | immutable-fields-no-longer-protected | {'DETECTED_ASSERTION': 5, 'DETECTED_BEHAVIOR_ERROR': 1} | CREATE OR REPLACE FUNCTION public.manage_users_notes_timestamps() RETURNS TRIGGER LANGUAGE plpgsql AS $fault$ BEGIN RETURN NEW; END $fault$; |
| SQL-M032 | actor-policies-allow-everyone | {'DETECTED_ASSERTION': 7} | ALTER POLICY users_own_account ON public.users USING(true) WITH CHECK(true); ALTER POLICY notes_own_account ON public.notes USING(true) WITH CHECK(true); |
| SQL-M033 | app-can-assume-owner | {'DETECTED_ASSERTION': 1} | GRANT merlin_d6_owner TO merlin_d6_app; |
| SQL-M034 | protected-column-write-granted | {'DETECTED_BEHAVIOR_ERROR': 1} | GRANT UPDATE(id) ON public.notes TO merlin_d6_app; |
| SQL-M035 | protected-column-write-granted | {'DETECTED_BEHAVIOR_ERROR': 1} | GRANT UPDATE(user_id) ON public.notes TO merlin_d6_app; |
| SQL-M036 | protected-column-write-granted | {'DETECTED_BEHAVIOR_ERROR': 1} | GRANT UPDATE(created_at) ON public.notes TO merlin_d6_app; |
| SQL-M037 | protected-column-write-granted | {'DETECTED_ASSERTION': 1} | GRANT UPDATE(updated_at) ON public.notes TO merlin_d6_app; |
| SQL-M038 | protected-column-write-granted | {'DETECTED_ASSERTION': 1} | GRANT UPDATE(blank_body_expires_at) ON public.notes TO merlin_d6_app; |
| SQL-M039 | actor-policy-rejects-owner | {'DETECTED_ASSERTION': 1, 'DETECTED_BEHAVIOR_ERROR': 1} | ALTER POLICY notes_own_account ON public.notes USING(false) WITH CHECK(false); |
| SQL-M040 | saved-notes-permanently-deletable | {'DETECTED_ASSERTION': 1} | ALTER POLICY notes_app_delete_limit ON public.notes USING(true); |
| SQL-M041 | blank-draft-deletion-forbidden | {'DETECTED_ASSERTION': 31} | ALTER POLICY notes_app_delete_limit ON public.notes USING(false); |
| SQL-M042 | server-insert-clocks-forged | {'DETECTED_ASSERTION': 3} | DO $mutate$ DECLARE original text; BEGIN SELECT pg_get_functiondef('public.manage_users_notes_timestamps()'::regprocedure) INTO original; IF position($old$NEW.updated_at := NEW.created_at;$old$ IN original)=0 THEN RAISE EXCEPTION 'UNAPPLIED source fault'; END IF; EXECUTE replace(original,$old$NEW.updated_at := NEW.created_at;$old$,$new$NEW.updated_at := NEW.created_at - INTERVAL '1 day';$new$); END $mutate$; |
| SQL-M043 | server-edit-clock-wrong | {'SURVIVED': 1, 'DETECTED_ASSERTION': 5} | DO $mutate$ DECLARE original text; BEGIN SELECT pg_get_functiondef('public.manage_users_notes_timestamps()'::regprocedure) INTO original; IF position($old$NEW.updated_at := OLD.updated_at;$old$ IN original)=0 THEN RAISE EXCEPTION 'UNAPPLIED source fault'; END IF; EXECUTE replace(original,$old$NEW.updated_at := OLD.updated_at;$old$,$new$NEW.updated_at := statement_timestamp() + INTERVAL '1 day';$new$); END $mutate$; |
| SQL-M044 | content-edits-keep-old-clock | {'DETECTED_ASSERTION': 1, 'SURVIVED': 5} | DO $mutate$ DECLARE original text; BEGIN SELECT pg_get_functiondef('public.manage_users_notes_timestamps()'::regprocedure) INTO original; IF position($old$NEW.updated_at := statement_timestamp();$old$ IN original)=0 THEN RAISE EXCEPTION 'UNAPPLIED source fault'; END IF; EXECUTE replace(original,$old$NEW.updated_at := statement_timestamp();$old$,$new$NEW.updated_at := OLD.updated_at;$new$); END $mutate$; |
| SQL-M045 | device-clock-not-normalized | {'DETECTED_ASSERTION': 1} | DO $mutate$ DECLARE original text; BEGIN SELECT pg_get_functiondef('public.manage_note_content()'::regprocedure) INTO original; IF position($old$NEW.device_edited_at := NEW.device_created_at;$old$ IN original)=0 THEN RAISE EXCEPTION 'UNAPPLIED source fault'; END IF; EXECUTE replace(original,$old$NEW.device_edited_at := NEW.device_created_at;$old$,$new$NULL;$new$); END $mutate$; |
| SQL-M046 | trash-guards-and-clock-removed | {'DETECTED_ASSERTION': 7} | CREATE OR REPLACE FUNCTION public.manage_note_deletion() RETURNS TRIGGER LANGUAGE plpgsql AS $fault$ BEGIN RETURN NEW; END $fault$; |
| SQL-M047 | device-instant-shifted | {'DETECTED_ASSERTION': 1} | DO $mutate$ DECLARE original text; BEGIN SELECT pg_get_functiondef('public.manage_note_content()'::regprocedure) INTO original; IF position($old$NEW.device_edited_at := NEW.device_created_at;$old$ IN original)=0 THEN RAISE EXCEPTION 'UNAPPLIED source fault'; END IF; EXECUTE replace(original,$old$NEW.device_edited_at := NEW.device_created_at;$old$,$new$NEW.device_created_at := NEW.device_created_at + INTERVAL '1 hour'; NEW.device_edited_at := NEW.device_created_at;$new$); END $mutate$; |
| SQL-M048 | body-refill-does-not-clear-countdown | {'DETECTED_BEHAVIOR_ERROR': 1} | DO $mutate$ DECLARE original text; BEGIN SELECT pg_get_functiondef('public.manage_note_content()'::regprocedure) INTO original; IF position($old$NEW.blank_body_expires_at := NULL;$old$ IN original)=0 THEN RAISE EXCEPTION 'UNAPPLIED source fault'; END IF; EXECUTE replace(original,$old$NEW.blank_body_expires_at := NULL;$old$,$new$NEW.blank_body_expires_at := statement_timestamp() + INTERVAL '24 hours';$new$); END $mutate$; |
| SQL-M049 | saved-notes-can-become-drafts | {'DETECTED_ASSERTION': 1} | CREATE OR REPLACE FUNCTION public.manage_note_content() RETURNS TRIGGER LANGUAGE plpgsql AS $fault$ BEGIN RETURN NEW; END $fault$; |
| SQL-M050 | expiry-output-wrong | {'DETECTED_ASSERTION': 5} | CREATE OR REPLACE FUNCTION public.cleanup_expired_blank_notes(batch_size INTEGER DEFAULT 100) RETURNS BIGINT LANGUAGE plpgsql AS $fault$ BEGIN RETURN 1; END $fault$; |
| SQL-M051 | expiry-output-wrong, invalid-batch-accepted | {'DETECTED_ASSERTION': 36, 'SURVIVED': 1} | CREATE OR REPLACE FUNCTION public.cleanup_expired_blank_notes(batch_size INTEGER DEFAULT 100) RETURNS BIGINT LANGUAGE plpgsql AS $fault$ BEGIN RETURN 0; END $fault$; |
| SQL-M052 | active-view-filter-wrong | {'DETECTED_ASSERTION': 1} | CREATE OR REPLACE VIEW public.active_notes WITH (security_invoker=true) AS SELECT * FROM public.notes WHERE true; |
| SQL-M053 | active-view-filter-wrong | {'DETECTED_ASSERTION': 1} | CREATE OR REPLACE VIEW public.active_notes WITH (security_invoker=true) AS SELECT * FROM public.notes WHERE false; |
| SQL-M054 | purge-output-wrong | {'DETECTED_ASSERTION': 4} | CREATE OR REPLACE FUNCTION public.purge_deleted_notes(batch_size INTEGER DEFAULT 100) RETURNS BIGINT LANGUAGE plpgsql AS $fault$ BEGIN RETURN 1; END $fault$; |
| SQL-M055 | invalid-batch-accepted, purge-output-wrong | {'DETECTED_ASSERTION': 7} | CREATE OR REPLACE FUNCTION public.purge_deleted_notes(batch_size INTEGER DEFAULT 100) RETURNS BIGINT LANGUAGE plpgsql AS $fault$ BEGIN RETURN 0; END $fault$; |
| SQL-M056 | recent-trash-purge-allowed | {'DETECTED_ASSERTION': 1} | ALTER POLICY notes_maintenance_delete_limit ON public.notes USING(true); |
| SQL-M057 | worker-sees-active-private-content | {'DETECTED_ASSERTION': 1} | ALTER POLICY notes_maintenance ON public.notes USING(true); |
| SQL-M058 | required-column-now-nullable | {'DETECTED_ASSERTION': 1} | ALTER TABLE public.notes ALTER COLUMN body DROP NOT NULL; |
| SQL-M059 | required-column-now-nullable | {'DETECTED_ASSERTION': 1} | ALTER TABLE public.notes ALTER COLUMN device_created_at DROP NOT NULL; |
| SQL-M060 | required-column-now-nullable | {'DETECTED_ASSERTION': 1} | ALTER TABLE public.notes ALTER COLUMN is_draft DROP NOT NULL; |
| SQL-M061 | permission-role-can-login | {'DETECTED_ASSERTION': 1} | ALTER ROLE merlin_d6_app LOGIN; |
| SQL-M062 | owner-not-subject-to-rls | {'DETECTED_ASSERTION': 1} | ALTER TABLE public.notes NO FORCE ROW LEVEL SECURITY; |
| SQL-M063 | app-incorrectly-granted-execute | {'DETECTED_ASSERTION': 1} | GRANT EXECUTE ON FUNCTION public.cleanup_expired_blank_notes(INTEGER) TO merlin_d6_app; |
| SQL-M064 | app-can-create-schema-objects | {'DETECTED_ASSERTION': 1} | GRANT CREATE ON SCHEMA public TO merlin_d6_app; |
| SQL-M065 | timeline-index-missing | {'DETECTED_ASSERTION': 1} | DROP INDEX public.notes_user_created_idx; |
| SQL-M066 | timeline-index-missing | {'DETECTED_ASSERTION': 1} | DROP INDEX public.notes_user_updated_idx; |
| SQL-M067 | timeline-index-missing | {'DETECTED_ASSERTION': 1} | DROP INDEX public.notes_user_device_updated_idx; |
| SQL-M068 | timeline-index-missing | {'DETECTED_ASSERTION': 1} | DROP INDEX public.notes_user_draft_updated_idx; |
| SQL-M069 | constraint-removed-users_pkey | {'DETECTED_ASSERTION': 1} | ALTER TABLE public.users DROP CONSTRAINT users_pkey CASCADE; |
| SQL-M070 | invisible-content-misclassified-blank | {'DETECTED_BEHAVIOR_ERROR': 3} | CREATE OR REPLACE FUNCTION public.note_text_is_blank(value TEXT) RETURNS BOOLEAN LANGUAGE plpython3u AS $fault$ return True $fault$; |
| SQL-M071 | missing-note-owner-foreign-key | {'DETECTED_ASSERTION': 1} | missing-note-owner-foreign-key |

## Quiz pure logic

| ID | Fault | Status |
|---|---|---|
| JS-M001 | script-syntax-error | DETECTED |
| JS-M002 | bank-duplicate-id | DETECTED |
| JS-M003 | bank-critical-removed | DETECTED |
| JS-M004 | answers-always-wrong | DETECTED |
| JS-M005 | answers-always-correct | DETECTED |
| JS-M006 | threshold-too-strict | DETECTED |
| JS-M007 | threshold-too-permissive | DETECTED |
| JS-M008 | critical-errors-ignored | DETECTED |
| JS-M009 | invalid-answers-accepted | DETECTED |
| JS-M010 | negative-answer-accepted | DETECTED |
| JS-M011 | too-large-answer-accepted | DETECTED |
| JS-M012 | integer-check-removed | DETECTED |
| JS-M013 | empty-attempt-passes | DETECTED |
| JS-M014 | unknown-question-ignored | DETECTED |
| JS-M015 | full-bank-denominator | DETECTED |
| JS-M016 | caller-answers-overwritten | DETECTED |
| JS-M017 | topic-totals-not-counted | DETECTED |
| JS-M018 | topic-correct-not-counted | DETECTED |
| JS-M019 | saved-states-all-rejected | DETECTED |
| JS-M020 | saved-states-all-accepted | DETECTED |
| JS-M021 | empty-ids-accepted | DETECTED |
| JS-M022 | duplicate-ids-accepted | DETECTED |
| JS-M023 | unknown-ids-accepted | DETECTED |
| JS-M024 | answers-not-required | DETECTED |
| JS-M025 | answer-arrays-accepted | DETECTED |
| JS-M026 | order-not-required | DETECTED |
| JS-M027 | permutation-length-ignored | DETECTED |
| JS-M028 | permutation-duplicates-ignored | DETECTED |
| JS-M029 | permutation-bounds-ignored | DETECTED |
| JS-M030 | permutation-integers-ignored | DETECTED |
| JS-M031 | saved-answer-types-ignored | DETECTED |
| JS-M032 | partial-submitted-cache-accepted | DETECTED |
| JS-M033 | shuffle-disabled | DETECTED |
| JS-M034 | shuffle-loses-choice | DETECTED |
| JS-M035 | partial-saved-state-modified | DETECTED |

## Real Chromium workflows

| ID | Fault | Status |
|---|---|---|
| UI-M001 | for(const &lbrack;number,id&rbrack; of ids.entries()) → for(const &lbrack;number,id&rbrack; of ids.slice(1).entries()) | DETECTED |
| UI-M002 | if(lastGrade.missing.length){ → if(false){ | DETECTED |
| UI-M003 | answers&lbrack;id&rbrack;=index; → answers&lbrack;id&rbrack;=0; | DETECTED |
| UI-M004 | input.checked=answers&lbrack;id&rbrack;===index; → input.checked=false; | DETECTED |
| UI-M005 | box.querySelectorAll('input').forEach(n=&gt;n.disabled=true); →  | DETECTED |
| UI-M006 | if(!submitted)showResults(); → showResults(); | DETECTED |
| UI-M007 | ids=&lbrack;...lastGrade.missed&rbrack;; → ids=QUESTIONS.map(q=&gt;q.id); | DETECTED |
| UI-M008 | ids.length&lt;QUESTIONS.length?'Practice threshold met':'Quiz threshold met' → 'Quiz threshold met' | DETECTED |
| UI-M009 | ids=QUESTIONS.map(q=&gt;q.id);answers={};order={};submitted=false;lastGrade=null; → ids=&lbrack;1&rbrack;;answers={};order={};submitted=false;lastGrade=null; | DETECTED |
| UI-M010 | if(submitted)showResults(false); →  | DETECTED |
| UI-M011 | if(saved.submitted===true&&saved.ids.some(id=&gt;!Object.hasOwn(saved.answers,id)))return false; →  | DETECTED |
| UI-M012 | }catch{} function save() → }catch{throw new Error("cache failure");} function save() | DETECTED |
| UI-M013 | Array.isArray(saved.answers) → false | DETECTED |
| UI-M014 | }catch{}} function el → }catch{throw new Error("storage failure");}} function el | DETECTED |
| UI-M015 | lastGrade.criticalMissed.length?' Review the missed critical secret/authentication/storage questions even if the percentage is high.':'' → '' | DETECTED |
| UI-M016 | ()=&gt;window.print() → ()=&gt;{} | DETECTED |

## PostgreSQL lifecycle

| ID | Fault | Status |
|---|---|---|
| LIFE-M001 | Remove the note-owner foreign key during account deletion | DETECTED |
| LIFE-M002 | Remove SKIP LOCKED from expiry cleanup | DETECTED |
| LIFE-M003 | Remove SKIP LOCKED from retention purge | DETECTED |
| LIFE-M004 | Remove the expiry batch limit | DETECTED |
| LIFE-M005 | Commit the first cleanup before the second operation fails | DETECTED |
