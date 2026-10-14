# Setup and documentation case/fault necessity review

Reviewed October 12, 2026. Every item below was compared with its concrete fixture, assertions and responsible source. No code or test was removed.

Counts: {"case_rows": 118, "case_decisions": {"KEEP": 114, "MERGE": 3, "IMPROVE": 1}, "fault_rows": 150, "fault_decisions": {"KEEP": 148, "IMPROVE": 2}}.

These protect developer setup, privacy and planning checks. They are not 118 application business requirements. Keep this distinction when describing coverage.

## Every baseline and subtest

### `tests/test_doctor_failure_cases.py::test_typed_malformed_inspect_data_is_rejected[host-is-array]`

**KEEP** — Reject independently malformed host/mount/label types before dereferencing; avoids crashes and unsafe acceptance.

Input: `host-is-array`. Source: `tests/test_doctor_failure_cases.py:19`.

Assertions: `assert instance.inspect('a' * 64) is None`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_typed_malformed_inspect_data_is_rejected[mounts-are-null]`

**KEEP** — Reject independently malformed host/mount/label types before dereferencing; avoids crashes and unsafe acceptance.

Input: `mounts-are-null`. Source: `tests/test_doctor_failure_cases.py:19`.

Assertions: `assert instance.inspect('a' * 64) is None`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_typed_malformed_inspect_data_is_rejected[labels-are-array]`

**KEEP** — Reject independently malformed host/mount/label types before dereferencing; avoids crashes and unsafe acceptance.

Input: `labels-are-array`. Source: `tests/test_doctor_failure_cases.py:19`.

Assertions: `assert instance.inspect('a' * 64) is None`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_valid_inspection_is_preserved`

**KEEP** — Valid JSON inspection must survive decoding; complements refuse-invalid tests so reject-everything cannot pass.

Input: `see exact fixture/source below`. Source: `tests/test_doctor_failure_cases.py:26`.

Assertions: `assert instance.inspect('a' * 64) == tuple(values)`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_nested_malformed_inspection_is_rejected[ports-null]`

**KEEP** — Validate nested port-binding/log structure at the specific null, list or element path supplied.

Input: `ports-null`. Source: `tests/test_doctor_failure_cases.py:42`.

Assertions: `assert instance.inspect('a' * 64) is None`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_nested_malformed_inspection_is_rejected[ports-array]`

**KEEP** — Validate nested port-binding/log structure at the specific null, list or element path supplied.

Input: `ports-array`. Source: `tests/test_doctor_failure_cases.py:42`.

Assertions: `assert instance.inspect('a' * 64) is None`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_nested_malformed_inspection_is_rejected[binding-null]`

**KEEP** — Validate nested port-binding/log structure at the specific null, list or element path supplied.

Input: `binding-null`. Source: `tests/test_doctor_failure_cases.py:42`.

Assertions: `assert instance.inspect('a' * 64) is None`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_nested_malformed_inspection_is_rejected[binding-string]`

**KEEP** — Validate nested port-binding/log structure at the specific null, list or element path supplied.

Input: `binding-string`. Source: `tests/test_doctor_failure_cases.py:42`.

Assertions: `assert instance.inspect('a' * 64) is None`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_nested_malformed_inspection_is_rejected[log-null]`

**KEEP** — Validate nested port-binding/log structure at the specific null, list or element path supplied.

Input: `log-null`. Source: `tests/test_doctor_failure_cases.py:42`.

Assertions: `assert instance.inspect('a' * 64) is None`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_nested_malformed_inspection_is_rejected[log-array]`

**KEEP** — Validate nested port-binding/log structure at the specific null, list or element path supplied.

Input: `log-array`. Source: `tests/test_doctor_failure_cases.py:42`.

Assertions: `assert instance.inspect('a' * 64) is None`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_nested_malformed_inspection_is_rejected[log-options-null]`

**KEEP** — Validate nested port-binding/log structure at the specific null, list or element path supplied.

Input: `log-options-null`. Source: `tests/test_doctor_failure_cases.py:42`.

Assertions: `assert instance.inspect('a' * 64) is None`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_nested_malformed_inspection_is_rejected[log-options-array]`

**KEEP** — Validate nested port-binding/log structure at the specific null, list or element path supplied.

Input: `log-options-array`. Source: `tests/test_doctor_failure_cases.py:42`.

Assertions: `assert instance.inspect('a' * 64) is None`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_negative_auth_cannot_pass_without_a_valid_positive[positive-connection-fails]`

**KEEP** — A negative authentication observation needs a working positive control, not merely an unreachable server.

Input: `positive-connection-fails`. Source: `tests/test_doctor_failure_cases.py:51`.

Assertions: `assert 'PG-AUTH-POSITIVE FAIL' in output`; `assert 'PG-AUTH-NEGATIVE FAIL' in output`; `assert instance.failures == 2`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_negative_auth_cannot_pass_without_a_valid_positive[positive-output-is-wrong]`

**KEEP** — A negative authentication observation needs a working positive control, not merely an unreachable server.

Input: `positive-output-is-wrong`. Source: `tests/test_doctor_failure_cases.py:51`.

Assertions: `assert 'PG-AUTH-POSITIVE FAIL' in output`; `assert 'PG-AUTH-NEGATIVE FAIL' in output`; `assert instance.failures == 2`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_cluster_comparison_uses_the_expected_fingerprint[456-456-True]`

**KEEP** — Compare actual cluster identity with the supplied expectation; reject nonnumeric identity independently.

Input: `456-456-True`. Source: `tests/test_doctor_failure_cases.py:64`.

Assertions: `assert 'PG-CLUSTER ' + ('PASS' if passes else 'FAIL') in output`; `assert instance.failures == (0 if passes else 1)`; `assert observed not in output`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_cluster_comparison_uses_the_expected_fingerprint[456-123-False]`

**KEEP** — Compare actual cluster identity with the supplied expectation; reject nonnumeric identity independently.

Input: `456-123-False`. Source: `tests/test_doctor_failure_cases.py:64`.

Assertions: `assert 'PG-CLUSTER ' + ('PASS' if passes else 'FAIL') in output`; `assert instance.failures == (0 if passes else 1)`; `assert observed not in output`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_cluster_comparison_uses_the_expected_fingerprint[not-a-cluster-None-False]`

**KEEP** — Compare actual cluster identity with the supplied expectation; reject nonnumeric identity independently.

Input: `not-a-cluster-None-False`. Source: `tests/test_doctor_failure_cases.py:64`.

Assertions: `assert 'PG-CLUSTER ' + ('PASS' if passes else 'FAIL') in output`; `assert instance.failures == (0 if passes else 1)`; `assert observed not in output`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_auth_commands_use_tcp_and_different_passwords`

**KEEP** — Exercise compose-side TCP authentication with genuinely different passwords, fixed safe command environment and identity query.

Input: `see exact fixture/source below`. Source: `tests/test_doctor_failure_cases.py:76`.

Assertions: `assert 'PGPASSWORD="$POSTGRES_PASSWORD"' in positive`; `assert 'PGPASSWORD="${POSTGRES_PASSWORD}__doctor_wrong"' in negative`; `assert positive.endswith("'SELECT 1'") and negative.endswith("'SELECT 1'")`; `assert identity.endswith("'SELECT system_identifier FROM pg_control_system()'")`; `assert instance.failures == 0`; `assert '-h postgres' in command and '-X -w' in command`; `assert '-U "$POSTGRES_USER"' in command and '-d "$POSTGRES_DB"' in command`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_static_checker_rejects_each_bad_prerequisite[python-version-PYTHON]`

**KEEP** — Report the named prerequisite failure precisely: version, lock, environment permission/ignore/tracking or invalid compose input.

Input: `python-version-PYTHON`. Source: `tests/test_doctor_failure_cases.py:102`.

Assertions: `assert [line.split()[0] for line in lines if ' FAIL:' in line] == [expected]`; `assert instance.failures == 1`; `assert args == ['docker', 'compose', 'version']`; `assert instance.static_checks() is True`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_static_checker_rejects_each_bad_prerequisite[python-pin-PYTHON-PIN]`

**KEEP** — Report the named prerequisite failure precisely: version, lock, environment permission/ignore/tracking or invalid compose input.

Input: `python-pin-PYTHON-PIN`. Source: `tests/test_doctor_failure_cases.py:102`.

Assertions: `assert [line.split()[0] for line in lines if ' FAIL:' in line] == [expected]`; `assert instance.failures == 1`; `assert args == ['docker', 'compose', 'version']`; `assert instance.static_checks() is True`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_static_checker_rejects_each_bad_prerequisite[lock-missing-LOCKFILES]`

**KEEP** — Report the named prerequisite failure precisely: version, lock, environment permission/ignore/tracking or invalid compose input.

Input: `lock-missing-LOCKFILES`. Source: `tests/test_doctor_failure_cases.py:102`.

Assertions: `assert [line.split()[0] for line in lines if ' FAIL:' in line] == [expected]`; `assert instance.failures == 1`; `assert args == ['docker', 'compose', 'version']`; `assert instance.static_checks() is True`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_static_checker_rejects_each_bad_prerequisite[lock-stale-UV-LOCK]`

**KEEP** — Report the named prerequisite failure precisely: version, lock, environment permission/ignore/tracking or invalid compose input.

Input: `lock-stale-UV-LOCK`. Source: `tests/test_doctor_failure_cases.py:102`.

Assertions: `assert [line.split()[0] for line in lines if ' FAIL:' in line] == [expected]`; `assert instance.failures == 1`; `assert args == ['docker', 'compose', 'version']`; `assert instance.static_checks() is True`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_static_checker_rejects_each_bad_prerequisite[node-version-NODE]`

**KEEP** — Report the named prerequisite failure precisely: version, lock, environment permission/ignore/tracking or invalid compose input.

Input: `node-version-NODE`. Source: `tests/test_doctor_failure_cases.py:102`.

Assertions: `assert [line.split()[0] for line in lines if ' FAIL:' in line] == [expected]`; `assert instance.failures == 1`; `assert args == ['docker', 'compose', 'version']`; `assert instance.static_checks() is True`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_static_checker_rejects_each_bad_prerequisite[pnpm-version-PNPM]`

**KEEP** — Report the named prerequisite failure precisely: version, lock, environment permission/ignore/tracking or invalid compose input.

Input: `pnpm-version-PNPM`. Source: `tests/test_doctor_failure_cases.py:102`.

Assertions: `assert [line.split()[0] for line in lines if ' FAIL:' in line] == [expected]`; `assert instance.failures == 1`; `assert args == ['docker', 'compose', 'version']`; `assert instance.static_checks() is True`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_static_checker_rejects_each_bad_prerequisite[env-public-ENV-MODE]`

**KEEP** — Report the named prerequisite failure precisely: version, lock, environment permission/ignore/tracking or invalid compose input.

Input: `env-public-ENV-MODE`. Source: `tests/test_doctor_failure_cases.py:102`.

Assertions: `assert [line.split()[0] for line in lines if ' FAIL:' in line] == [expected]`; `assert instance.failures == 1`; `assert args == ['docker', 'compose', 'version']`; `assert instance.static_checks() is True`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_static_checker_rejects_each_bad_prerequisite[env-not-ignored-ENV-IGNORE]`

**KEEP** — Report the named prerequisite failure precisely: version, lock, environment permission/ignore/tracking or invalid compose input.

Input: `env-not-ignored-ENV-IGNORE`. Source: `tests/test_doctor_failure_cases.py:102`.

Assertions: `assert [line.split()[0] for line in lines if ' FAIL:' in line] == [expected]`; `assert instance.failures == 1`; `assert args == ['docker', 'compose', 'version']`; `assert instance.static_checks() is True`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_static_checker_rejects_each_bad_prerequisite[env-tracked-TRACKED-SECRETS]`

**KEEP** — Report the named prerequisite failure precisely: version, lock, environment permission/ignore/tracking or invalid compose input.

Input: `env-tracked-TRACKED-SECRETS`. Source: `tests/test_doctor_failure_cases.py:102`.

Assertions: `assert [line.split()[0] for line in lines if ' FAIL:' in line] == [expected]`; `assert instance.failures == 1`; `assert args == ['docker', 'compose', 'version']`; `assert instance.static_checks() is True`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_static_checker_rejects_each_bad_prerequisite[env-variant-tracked-TRACKED-SECRETS]`

**KEEP** — Report the named prerequisite failure precisely: version, lock, environment permission/ignore/tracking or invalid compose input.

Input: `env-variant-tracked-TRACKED-SECRETS`. Source: `tests/test_doctor_failure_cases.py:102`.

Assertions: `assert [line.split()[0] for line in lines if ' FAIL:' in line] == [expected]`; `assert instance.failures == 1`; `assert args == ['docker', 'compose', 'version']`; `assert instance.static_checks() is True`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_static_checker_rejects_each_bad_prerequisite[git-list-failed-TRACKED-SECRETS]`

**KEEP** — Report the named prerequisite failure precisely: version, lock, environment permission/ignore/tracking or invalid compose input.

Input: `git-list-failed-TRACKED-SECRETS`. Source: `tests/test_doctor_failure_cases.py:102`.

Assertions: `assert [line.split()[0] for line in lines if ' FAIL:' in line] == [expected]`; `assert instance.failures == 1`; `assert args == ['docker', 'compose', 'version']`; `assert instance.static_checks() is True`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_static_checker_rejects_each_bad_prerequisite[venv-tracked-VENV-IGNORE]`

**KEEP** — Report the named prerequisite failure precisely: version, lock, environment permission/ignore/tracking or invalid compose input.

Input: `venv-tracked-VENV-IGNORE`. Source: `tests/test_doctor_failure_cases.py:102`.

Assertions: `assert [line.split()[0] for line in lines if ' FAIL:' in line] == [expected]`; `assert instance.failures == 1`; `assert args == ['docker', 'compose', 'version']`; `assert instance.static_checks() is True`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_static_checker_rejects_each_bad_prerequisite[compose-invalid-COMPOSE-CONFIG]`

**KEEP** — Report the named prerequisite failure precisely: version, lock, environment permission/ignore/tracking or invalid compose input.

Input: `compose-invalid-COMPOSE-CONFIG`. Source: `tests/test_doctor_failure_cases.py:102`.

Assertions: `assert [line.split()[0] for line in lines if ' FAIL:' in line] == [expected]`; `assert instance.failures == 1`; `assert args == ['docker', 'compose', 'version']`; `assert instance.static_checks() is True`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_static_checker_rejects_each_bad_prerequisite[compose-invalid-static-COMPOSE-CONFIG]`

**KEEP** — Report the named prerequisite failure precisely: version, lock, environment permission/ignore/tracking or invalid compose input.

Input: `compose-invalid-static-COMPOSE-CONFIG`. Source: `tests/test_doctor_failure_cases.py:102`.

Assertions: `assert [line.split()[0] for line in lines if ' FAIL:' in line] == [expected]`; `assert instance.failures == 1`; `assert args == ['docker', 'compose', 'version']`; `assert instance.static_checks() is True`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_malformed_manifest_is_reported_without_crashing[project=[]]`

**KEEP** — Malformed project shape, malformed requires-python or missing declaration must produce a controlled pin failure rather than traceback.

Input: `project=[`. Source: `tests/test_doctor_failure_cases.py:138`.

Assertions: `assert 'PYTHON-PIN FAIL' in capsys.readouterr().out`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_malformed_manifest_is_reported_without_crashing[[project]\nrequires-python=[]]`

**KEEP** — Malformed project shape, malformed requires-python or missing declaration must produce a controlled pin failure rather than traceback.

Input: `[project]\nrequires-python=[`. Source: `tests/test_doctor_failure_cases.py:138`.

Assertions: `assert 'PYTHON-PIN FAIL' in capsys.readouterr().out`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_malformed_manifest_is_reported_without_crashing[[project]\n]`

**KEEP** — Malformed project shape, malformed requires-python or missing declaration must produce a controlled pin failure rather than traceback.

Input: `[project]\n`. Source: `tests/test_doctor_failure_cases.py:138`.

Assertions: `assert 'PYTHON-PIN FAIL' in capsys.readouterr().out`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_runtime_checker_rejects_each_bad_postgres_boundary[public-port-PORT]`

**KEEP** — Reject the specific live service boundary: public/invalid ports, uncapped resources, logging, storage ownership, health or root UID.

Input: `public-port-PORT`. Source: `tests/test_doctor_failure_cases.py:155`.

Assertions: `assert [line.split()[0] for line in capsys.readouterr().out.splitlines() if ' FAIL:' in line] == ['POSTGRES-' + expected, 'REDIS-RUNNING']`; `assert 'postgres' not in instance.host_ports`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_runtime_checker_rejects_each_bad_postgres_boundary[two-ports-PORT]`

**KEEP** — Reject the specific live service boundary: public/invalid ports, uncapped resources, logging, storage ownership, health or root UID.

Input: `two-ports-PORT`. Source: `tests/test_doctor_failure_cases.py:155`.

Assertions: `assert [line.split()[0] for line in capsys.readouterr().out.splitlines() if ' FAIL:' in line] == ['POSTGRES-' + expected, 'REDIS-RUNNING']`; `assert 'postgres' not in instance.host_ports`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_runtime_checker_rejects_each_bad_postgres_boundary[zero-port-PORT]`

**KEEP** — Reject the specific live service boundary: public/invalid ports, uncapped resources, logging, storage ownership, health or root UID.

Input: `zero-port-PORT`. Source: `tests/test_doctor_failure_cases.py:155`.

Assertions: `assert [line.split()[0] for line in capsys.readouterr().out.splitlines() if ' FAIL:' in line] == ['POSTGRES-' + expected, 'REDIS-RUNNING']`; `assert 'postgres' not in instance.host_ports`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_runtime_checker_rejects_each_bad_postgres_boundary[huge-port-PORT]`

**KEEP** — Reject the specific live service boundary: public/invalid ports, uncapped resources, logging, storage ownership, health or root UID.

Input: `huge-port-PORT`. Source: `tests/test_doctor_failure_cases.py:155`.

Assertions: `assert [line.split()[0] for line in capsys.readouterr().out.splitlines() if ' FAIL:' in line] == ['POSTGRES-' + expected, 'REDIS-RUNNING']`; `assert 'postgres' not in instance.host_ports`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_runtime_checker_rejects_each_bad_postgres_boundary[unicode-digit-port-PORT]`

**KEEP** — Reject the specific live service boundary: public/invalid ports, uncapped resources, logging, storage ownership, health or root UID.

Input: `unicode-digit-port-PORT`. Source: `tests/test_doctor_failure_cases.py:155`.

Assertions: `assert [line.split()[0] for line in capsys.readouterr().out.splitlines() if ' FAIL:' in line] == ['POSTGRES-' + expected, 'REDIS-RUNNING']`; `assert 'postgres' not in instance.host_ports`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_runtime_checker_rejects_each_bad_postgres_boundary[memory-LIMITS]`

**KEEP** — Reject the specific live service boundary: public/invalid ports, uncapped resources, logging, storage ownership, health or root UID.

Input: `memory-LIMITS`. Source: `tests/test_doctor_failure_cases.py:155`.

Assertions: `assert [line.split()[0] for line in capsys.readouterr().out.splitlines() if ' FAIL:' in line] == ['POSTGRES-' + expected, 'REDIS-RUNNING']`; `assert 'postgres' not in instance.host_ports`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_runtime_checker_rejects_each_bad_postgres_boundary[cpu-LIMITS]`

**KEEP** — Reject the specific live service boundary: public/invalid ports, uncapped resources, logging, storage ownership, health or root UID.

Input: `cpu-LIMITS`. Source: `tests/test_doctor_failure_cases.py:155`.

Assertions: `assert [line.split()[0] for line in capsys.readouterr().out.splitlines() if ' FAIL:' in line] == ['POSTGRES-' + expected, 'REDIS-RUNNING']`; `assert 'postgres' not in instance.host_ports`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_runtime_checker_rejects_each_bad_postgres_boundary[log-type-LOGS]`

**KEEP** — Reject the specific live service boundary: public/invalid ports, uncapped resources, logging, storage ownership, health or root UID.

Input: `log-type-LOGS`. Source: `tests/test_doctor_failure_cases.py:155`.

Assertions: `assert [line.split()[0] for line in capsys.readouterr().out.splitlines() if ' FAIL:' in line] == ['POSTGRES-' + expected, 'REDIS-RUNNING']`; `assert 'postgres' not in instance.host_ports`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_runtime_checker_rejects_each_bad_postgres_boundary[log-size-LOGS]`

**KEEP** — Reject the specific live service boundary: public/invalid ports, uncapped resources, logging, storage ownership, health or root UID.

Input: `log-size-LOGS`. Source: `tests/test_doctor_failure_cases.py:155`.

Assertions: `assert [line.split()[0] for line in capsys.readouterr().out.splitlines() if ' FAIL:' in line] == ['POSTGRES-' + expected, 'REDIS-RUNNING']`; `assert 'postgres' not in instance.host_ports`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_runtime_checker_rejects_each_bad_postgres_boundary[log-count-LOGS]`

**KEEP** — Reject the specific live service boundary: public/invalid ports, uncapped resources, logging, storage ownership, health or root UID.

Input: `log-count-LOGS`. Source: `tests/test_doctor_failure_cases.py:155`.

Assertions: `assert [line.split()[0] for line in capsys.readouterr().out.splitlines() if ' FAIL:' in line] == ['POSTGRES-' + expected, 'REDIS-RUNNING']`; `assert 'postgres' not in instance.host_ports`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_runtime_checker_rejects_each_bad_postgres_boundary[volume-name-VOLUME]`

**KEEP** — Reject the specific live service boundary: public/invalid ports, uncapped resources, logging, storage ownership, health or root UID.

Input: `volume-name-VOLUME`. Source: `tests/test_doctor_failure_cases.py:155`.

Assertions: `assert [line.split()[0] for line in capsys.readouterr().out.splitlines() if ' FAIL:' in line] == ['POSTGRES-' + expected, 'REDIS-RUNNING']`; `assert 'postgres' not in instance.host_ports`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_runtime_checker_rejects_each_bad_postgres_boundary[volume-type-VOLUME]`

**KEEP** — Reject the specific live service boundary: public/invalid ports, uncapped resources, logging, storage ownership, health or root UID.

Input: `volume-type-VOLUME`. Source: `tests/test_doctor_failure_cases.py:155`.

Assertions: `assert [line.split()[0] for line in capsys.readouterr().out.splitlines() if ' FAIL:' in line] == ['POSTGRES-' + expected, 'REDIS-RUNNING']`; `assert 'postgres' not in instance.host_ports`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_runtime_checker_rejects_each_bad_postgres_boundary[volume-missing-VOLUME]`

**KEEP** — Reject the specific live service boundary: public/invalid ports, uncapped resources, logging, storage ownership, health or root UID.

Input: `volume-missing-VOLUME`. Source: `tests/test_doctor_failure_cases.py:155`.

Assertions: `assert [line.split()[0] for line in capsys.readouterr().out.splitlines() if ' FAIL:' in line] == ['POSTGRES-' + expected, 'REDIS-RUNNING']`; `assert 'postgres' not in instance.host_ports`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_runtime_checker_rejects_each_bad_postgres_boundary[volume-duplicate-VOLUME]`

**KEEP** — Reject the specific live service boundary: public/invalid ports, uncapped resources, logging, storage ownership, health or root UID.

Input: `volume-duplicate-VOLUME`. Source: `tests/test_doctor_failure_cases.py:155`.

Assertions: `assert [line.split()[0] for line in capsys.readouterr().out.splitlines() if ' FAIL:' in line] == ['POSTGRES-' + expected, 'REDIS-RUNNING']`; `assert 'postgres' not in instance.host_ports`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_runtime_checker_rejects_each_bad_postgres_boundary[project-missing-VOLUME]`

**KEEP** — Reject the specific live service boundary: public/invalid ports, uncapped resources, logging, storage ownership, health or root UID.

Input: `project-missing-VOLUME`. Source: `tests/test_doctor_failure_cases.py:155`.

Assertions: `assert [line.split()[0] for line in capsys.readouterr().out.splitlines() if ' FAIL:' in line] == ['POSTGRES-' + expected, 'REDIS-RUNNING']`; `assert 'postgres' not in instance.host_ports`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_runtime_checker_rejects_each_bad_postgres_boundary[unhealthy-HEALTH]`

**KEEP** — Reject the specific live service boundary: public/invalid ports, uncapped resources, logging, storage ownership, health or root UID.

Input: `unhealthy-HEALTH`. Source: `tests/test_doctor_failure_cases.py:155`.

Assertions: `assert [line.split()[0] for line in capsys.readouterr().out.splitlines() if ' FAIL:' in line] == ['POSTGRES-' + expected, 'REDIS-RUNNING']`; `assert 'postgres' not in instance.host_ports`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_runtime_checker_rejects_each_bad_postgres_boundary[uid-root-UID]`

**KEEP** — Reject the specific live service boundary: public/invalid ports, uncapped resources, logging, storage ownership, health or root UID.

Input: `uid-root-UID`. Source: `tests/test_doctor_failure_cases.py:155`.

Assertions: `assert [line.split()[0] for line in capsys.readouterr().out.splitlines() if ' FAIL:' in line] == ['POSTGRES-' + expected, 'REDIS-RUNNING']`; `assert 'postgres' not in instance.host_ports`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_host_proof_requires_valid_credentials_clients_and_responses[positive-status]`

**KEEP** — Require complete credentials, clients, loopback port, successful command and exact response before declaring host health/auth proof; suppress private output.

Input: `positive-status`. Source: `tests/test_doctor_failure_cases.py:197`.

Assertions: `assert 'HOST-PG-POSITIVE ' + ('PASS' if pg_ok else 'FAIL') in lines`; `assert 'HOST-REDIS-PONG ' + ('PASS' if redis_ok else 'FAIL') in lines`; `assert 'secret' not in lines`; `assert len(pg_calls) == (2 if pg_ok or fault in {'positive-status', 'positive-output'} else 0)`; `assert args[args.index('-h') + 1] == '127.0.0.1'`; `assert args[args.index('-p') + 1] in {'55432', '56379'}`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_host_proof_requires_valid_credentials_clients_and_responses[positive-output]`

**KEEP** — Require complete credentials, clients, loopback port, successful command and exact response before declaring host health/auth proof; suppress private output.

Input: `positive-output`. Source: `tests/test_doctor_failure_cases.py:197`.

Assertions: `assert 'HOST-PG-POSITIVE ' + ('PASS' if pg_ok else 'FAIL') in lines`; `assert 'HOST-REDIS-PONG ' + ('PASS' if redis_ok else 'FAIL') in lines`; `assert 'secret' not in lines`; `assert len(pg_calls) == (2 if pg_ok or fault in {'positive-status', 'positive-output'} else 0)`; `assert args[args.index('-h') + 1] == '127.0.0.1'`; `assert args[args.index('-p') + 1] in {'55432', '56379'}`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_host_proof_requires_valid_credentials_clients_and_responses[credential-status]`

**KEEP** — Require complete credentials, clients, loopback port, successful command and exact response before declaring host health/auth proof; suppress private output.

Input: `credential-status`. Source: `tests/test_doctor_failure_cases.py:197`.

Assertions: `assert 'HOST-PG-POSITIVE ' + ('PASS' if pg_ok else 'FAIL') in lines`; `assert 'HOST-REDIS-PONG ' + ('PASS' if redis_ok else 'FAIL') in lines`; `assert 'secret' not in lines`; `assert len(pg_calls) == (2 if pg_ok or fault in {'positive-status', 'positive-output'} else 0)`; `assert args[args.index('-h') + 1] == '127.0.0.1'`; `assert args[args.index('-p') + 1] in {'55432', '56379'}`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_host_proof_requires_valid_credentials_clients_and_responses[credential-count]`

**KEEP** — Require complete credentials, clients, loopback port, successful command and exact response before declaring host health/auth proof; suppress private output.

Input: `credential-count`. Source: `tests/test_doctor_failure_cases.py:197`.

Assertions: `assert 'HOST-PG-POSITIVE ' + ('PASS' if pg_ok else 'FAIL') in lines`; `assert 'HOST-REDIS-PONG ' + ('PASS' if redis_ok else 'FAIL') in lines`; `assert 'secret' not in lines`; `assert len(pg_calls) == (2 if pg_ok or fault in {'positive-status', 'positive-output'} else 0)`; `assert args[args.index('-h') + 1] == '127.0.0.1'`; `assert args[args.index('-p') + 1] in {'55432', '56379'}`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_host_proof_requires_valid_credentials_clients_and_responses[credential-empty]`

**KEEP** — Require complete credentials, clients, loopback port, successful command and exact response before declaring host health/auth proof; suppress private output.

Input: `credential-empty`. Source: `tests/test_doctor_failure_cases.py:197`.

Assertions: `assert 'HOST-PG-POSITIVE ' + ('PASS' if pg_ok else 'FAIL') in lines`; `assert 'HOST-REDIS-PONG ' + ('PASS' if redis_ok else 'FAIL') in lines`; `assert 'secret' not in lines`; `assert len(pg_calls) == (2 if pg_ok or fault in {'positive-status', 'positive-output'} else 0)`; `assert args[args.index('-h') + 1] == '127.0.0.1'`; `assert args[args.index('-p') + 1] in {'55432', '56379'}`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_host_proof_requires_valid_credentials_clients_and_responses[pg-client-missing]`

**KEEP** — Require complete credentials, clients, loopback port, successful command and exact response before declaring host health/auth proof; suppress private output.

Input: `pg-client-missing`. Source: `tests/test_doctor_failure_cases.py:197`.

Assertions: `assert 'HOST-PG-POSITIVE ' + ('PASS' if pg_ok else 'FAIL') in lines`; `assert 'HOST-REDIS-PONG ' + ('PASS' if redis_ok else 'FAIL') in lines`; `assert 'secret' not in lines`; `assert len(pg_calls) == (2 if pg_ok or fault in {'positive-status', 'positive-output'} else 0)`; `assert args[args.index('-h') + 1] == '127.0.0.1'`; `assert args[args.index('-p') + 1] in {'55432', '56379'}`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_host_proof_requires_valid_credentials_clients_and_responses[pg-port-missing]`

**KEEP** — Require complete credentials, clients, loopback port, successful command and exact response before declaring host health/auth proof; suppress private output.

Input: `pg-port-missing`. Source: `tests/test_doctor_failure_cases.py:197`.

Assertions: `assert 'HOST-PG-POSITIVE ' + ('PASS' if pg_ok else 'FAIL') in lines`; `assert 'HOST-REDIS-PONG ' + ('PASS' if redis_ok else 'FAIL') in lines`; `assert 'secret' not in lines`; `assert len(pg_calls) == (2 if pg_ok or fault in {'positive-status', 'positive-output'} else 0)`; `assert args[args.index('-h') + 1] == '127.0.0.1'`; `assert args[args.index('-p') + 1] in {'55432', '56379'}`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_host_proof_requires_valid_credentials_clients_and_responses[redis-client-missing]`

**KEEP** — Require complete credentials, clients, loopback port, successful command and exact response before declaring host health/auth proof; suppress private output.

Input: `redis-client-missing`. Source: `tests/test_doctor_failure_cases.py:197`.

Assertions: `assert 'HOST-PG-POSITIVE ' + ('PASS' if pg_ok else 'FAIL') in lines`; `assert 'HOST-REDIS-PONG ' + ('PASS' if redis_ok else 'FAIL') in lines`; `assert 'secret' not in lines`; `assert len(pg_calls) == (2 if pg_ok or fault in {'positive-status', 'positive-output'} else 0)`; `assert args[args.index('-h') + 1] == '127.0.0.1'`; `assert args[args.index('-p') + 1] in {'55432', '56379'}`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_host_proof_requires_valid_credentials_clients_and_responses[redis-port-missing]`

**KEEP** — Require complete credentials, clients, loopback port, successful command and exact response before declaring host health/auth proof; suppress private output.

Input: `redis-port-missing`. Source: `tests/test_doctor_failure_cases.py:197`.

Assertions: `assert 'HOST-PG-POSITIVE ' + ('PASS' if pg_ok else 'FAIL') in lines`; `assert 'HOST-REDIS-PONG ' + ('PASS' if redis_ok else 'FAIL') in lines`; `assert 'secret' not in lines`; `assert len(pg_calls) == (2 if pg_ok or fault in {'positive-status', 'positive-output'} else 0)`; `assert args[args.index('-h') + 1] == '127.0.0.1'`; `assert args[args.index('-p') + 1] in {'55432', '56379'}`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_host_proof_requires_valid_credentials_clients_and_responses[redis-status]`

**KEEP** — Require complete credentials, clients, loopback port, successful command and exact response before declaring host health/auth proof; suppress private output.

Input: `redis-status`. Source: `tests/test_doctor_failure_cases.py:197`.

Assertions: `assert 'HOST-PG-POSITIVE ' + ('PASS' if pg_ok else 'FAIL') in lines`; `assert 'HOST-REDIS-PONG ' + ('PASS' if redis_ok else 'FAIL') in lines`; `assert 'secret' not in lines`; `assert len(pg_calls) == (2 if pg_ok or fault in {'positive-status', 'positive-output'} else 0)`; `assert args[args.index('-h') + 1] == '127.0.0.1'`; `assert args[args.index('-p') + 1] in {'55432', '56379'}`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_host_proof_requires_valid_credentials_clients_and_responses[redis-output]`

**KEEP** — Require complete credentials, clients, loopback port, successful command and exact response before declaring host health/auth proof; suppress private output.

Input: `redis-output`. Source: `tests/test_doctor_failure_cases.py:197`.

Assertions: `assert 'HOST-PG-POSITIVE ' + ('PASS' if pg_ok else 'FAIL') in lines`; `assert 'HOST-REDIS-PONG ' + ('PASS' if redis_ok else 'FAIL') in lines`; `assert 'secret' not in lines`; `assert len(pg_calls) == (2 if pg_ok or fault in {'positive-status', 'positive-output'} else 0)`; `assert args[args.index('-h') + 1] == '127.0.0.1'`; `assert args[args.index('-p') + 1] in {'55432', '56379'}`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_host_proof_requires_valid_credentials_clients_and_responses[healthy]`

**KEEP** — Require complete credentials, clients, loopback port, successful command and exact response before declaring host health/auth proof; suppress private output.

Input: `healthy`. Source: `tests/test_doctor_failure_cases.py:197`.

Assertions: `assert 'HOST-PG-POSITIVE ' + ('PASS' if pg_ok else 'FAIL') in lines`; `assert 'HOST-REDIS-PONG ' + ('PASS' if redis_ok else 'FAIL') in lines`; `assert 'secret' not in lines`; `assert len(pg_calls) == (2 if pg_ok or fault in {'positive-status', 'positive-output'} else 0)`; `assert args[args.index('-h') + 1] == '127.0.0.1'`; `assert args[args.index('-p') + 1] in {'55432', '56379'}`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_redis_runtime_proof_rejects_bad_responses_and_configuration[ping-output]`

**KEEP** — Reject the specific Redis proof/configuration field: PONG/status, disk persistence, memory bound or eviction policy.

Input: `ping-output`. Source: `tests/test_doctor_failure_cases.py:228`.

Assertions: `assert [line.split()[0] for line in capsys.readouterr().out.splitlines() if ' FAIL:' in line] == ['POSTGRES-RUNNING', 'REDIS-RUNNING', expected]`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_redis_runtime_proof_rejects_bad_responses_and_configuration[ping-status]`

**KEEP** — Reject the specific Redis proof/configuration field: PONG/status, disk persistence, memory bound or eviction policy.

Input: `ping-status`. Source: `tests/test_doctor_failure_cases.py:228`.

Assertions: `assert [line.split()[0] for line in capsys.readouterr().out.splitlines() if ' FAIL:' in line] == ['POSTGRES-RUNNING', 'REDIS-RUNNING', expected]`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_redis_runtime_proof_rejects_bad_responses_and_configuration[save]`

**KEEP** — Reject the specific Redis proof/configuration field: PONG/status, disk persistence, memory bound or eviction policy.

Input: `save`. Source: `tests/test_doctor_failure_cases.py:228`.

Assertions: `assert [line.split()[0] for line in capsys.readouterr().out.splitlines() if ' FAIL:' in line] == ['POSTGRES-RUNNING', 'REDIS-RUNNING', expected]`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_redis_runtime_proof_rejects_bad_responses_and_configuration[appendonly]`

**KEEP** — Reject the specific Redis proof/configuration field: PONG/status, disk persistence, memory bound or eviction policy.

Input: `appendonly`. Source: `tests/test_doctor_failure_cases.py:228`.

Assertions: `assert [line.split()[0] for line in capsys.readouterr().out.splitlines() if ' FAIL:' in line] == ['POSTGRES-RUNNING', 'REDIS-RUNNING', expected]`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_redis_runtime_proof_rejects_bad_responses_and_configuration[maxmemory]`

**KEEP** — Reject the specific Redis proof/configuration field: PONG/status, disk persistence, memory bound or eviction policy.

Input: `maxmemory`. Source: `tests/test_doctor_failure_cases.py:228`.

Assertions: `assert [line.split()[0] for line in capsys.readouterr().out.splitlines() if ' FAIL:' in line] == ['POSTGRES-RUNNING', 'REDIS-RUNNING', expected]`

Overlap: No independent redundancy established.

### `tests/test_doctor_failure_cases.py::test_redis_runtime_proof_rejects_bad_responses_and_configuration[maxmemory-policy]`

**KEEP** — Reject the specific Redis proof/configuration field: PONG/status, disk persistence, memory bound or eviction policy.

Input: `maxmemory-policy`. Source: `tests/test_doctor_failure_cases.py:228`.

Assertions: `assert [line.split()[0] for line in capsys.readouterr().out.splitlines() if ' FAIL:' in line] == ['POSTGRES-RUNNING', 'REDIS-RUNNING', expected]`

Overlap: No independent redundancy established.

### `tests/test_prd_lint.py::test_docs_subfolder_is_not_mistaken_for_legacy_planning_root`

**KEEP** — A named topic subfolder audits that subtree rather than accidentally auditing sibling docs.

Input: `see exact fixture/source below`. Source: `tests/test_prd_lint.py:15`.

Assertions: `assert result.returncode == 0 and 'Checked 1 file(s).' in result.stdout`

Overlap: No independent redundancy established.

### `tests/test_prd_lint.py::test_document_root_audits_external_entrypoints[README.md]`

**KEEP** — Root docs lint includes the particular README, AGENTS or quiz entrypoint; different entrypoint discovery paths.

Input: `README.md`. Source: `tests/test_prd_lint.py:25`.

Assertions: `assert result.returncode == 1 and str(entry) in result.stdout`

Overlap: No independent redundancy established.

### `tests/test_prd_lint.py::test_document_root_audits_external_entrypoints[AGENTS.md]`

**KEEP** — Root docs lint includes the particular README, AGENTS or quiz entrypoint; different entrypoint discovery paths.

Input: `AGENTS.md`. Source: `tests/test_prd_lint.py:25`.

Assertions: `assert result.returncode == 1 and str(entry) in result.stdout`

Overlap: No independent redundancy established.

### `tests/test_prd_lint.py::test_document_root_audits_external_entrypoints[quizzes/quiz.html]`

**KEEP** — Root docs lint includes the particular README, AGENTS or quiz entrypoint; different entrypoint discovery paths.

Input: `quizzes/quiz.html`. Source: `tests/test_prd_lint.py:25`.

Assertions: `assert result.returncode == 1 and str(entry) in result.stdout`

Overlap: No independent redundancy established.

### `tests/test_prd_lint.py::test_skill_heading_warnings_are_precise[# SK-01\n\U0001f4da Learn first\n\u21a9 Return\n-False]`

**KEEP** — Warn only for a duplicated defined skill, preserving valid single definitions and ordinary overview headings.

Input: `# SK-01\n\U0001f4da Learn first\n\u21a9 Return\n-False`. Source: `tests/test_prd_lint.py:41`.

Assertions: `assert result.returncode == 0`; `assert ('skill SK-01 appears' in result.stdout) is warning`

Overlap: No independent redundancy established.

### `tests/test_prd_lint.py::test_skill_heading_warnings_are_precise[# SK-01\n\U0001f4da Learn first\n\u21a9 Return\n# SK-01\n\U0001f4da Learn first\n\u21a9 Return\n-True]`

**KEEP** — Warn only for a duplicated defined skill, preserving valid single definitions and ordinary overview headings.

Input: `# SK-01\n\U0001f4da Learn first\n\u21a9 Return\n# SK-01\n\U0001f4da Learn first\n\u21a9 Return\n-True`. Source: `tests/test_prd_lint.py:41`.

Assertions: `assert result.returncode == 0`; `assert ('skill SK-01 appears' in result.stdout) is warning`

Overlap: No independent redundancy established.

### `tests/test_prd_lint.py::test_skill_heading_warnings_are_precise[# Skills overview\n-False]`

**KEEP** — Warn only for a duplicated defined skill, preserving valid single definitions and ordinary overview headings.

Input: `# Skills overview\n-False`. Source: `tests/test_prd_lint.py:41`.

Assertions: `assert result.returncode == 0`; `assert ('skill SK-01 appears' in result.stdout) is warning`

Overlap: No independent redundancy established.

### `tests/test_prd_lint.py::test_missing_schedule_warning_requires_a_substantial_incomplete_schedule[1-False]`

**KEEP** — Warning threshold distinguishes a tiny draft, substantial incomplete plan and complete 37-day schedule.

Input: `1-False`. Source: `tests/test_prd_lint.py:49`.

Assertions: `assert result.returncode == 0`; `assert ('missing DAY' in result.stdout) is warning`

Overlap: No independent redundancy established.

### `tests/test_prd_lint.py::test_missing_schedule_warning_requires_a_substantial_incomplete_schedule[6-True]`

**KEEP** — Warning threshold distinguishes a tiny draft, substantial incomplete plan and complete 37-day schedule.

Input: `6-True`. Source: `tests/test_prd_lint.py:49`.

Assertions: `assert result.returncode == 0`; `assert ('missing DAY' in result.stdout) is warning`

Overlap: No independent redundancy established.

### `tests/test_prd_lint.py::test_missing_schedule_warning_requires_a_substantial_incomplete_schedule[37-False]`

**KEEP** — Warning threshold distinguishes a tiny draft, substantial incomplete plan and complete 37-day schedule.

Input: `37-False`. Source: `tests/test_prd_lint.py:49`.

Assertions: `assert result.returncode == 0`; `assert ('missing DAY' in result.stdout) is warning`

Overlap: No independent redundancy established.

### `tests/test_prd_lint.py::test_fenced_day_examples_in_other_parts_do_not_become_schedule_entries`

**KEEP** — Fenced example days outside Sprint Parts must not inflate schedule duplicate detection.

Input: `see exact fixture/source below`. Source: `tests/test_prd_lint.py:56`.

Assertions: `assert result.returncode == 0 and 'DAY 1 appears' not in result.stdout`

Overlap: No independent redundancy established.

### `tests/test_prd_lint.py::test_peer_section_links_cannot_satisfy_a_missing_learn_return_block`

**KEEP** — Learn/Return evidence must be local to the required peer section, not borrowed from the next one.

Input: `see exact fixture/source below`. Source: `tests/test_prd_lint.py:62`.

Assertions: `assert result.returncode == 0`; `assert "no 📚 Learn-first block under 'C-01'" in result.stdout`; `assert "no ↩ Return line under 'C-01'" in result.stdout`; `assert "under 'C-02'" not in result.stdout`

Overlap: No independent redundancy established.

### `tests/test_prd_lint.py::test_links_after_a_closed_fence_are_audited[```]`

**KEEP** — Ignore the example inside the specified fence while detecting the actual broken link after the correctly closed fence.

Input: `\`\`\``. Source: `tests/test_prd_lint.py:72`.

Assertions: `assert len(errors) == 1 and ':4 LINK: missing local target missing.md' in errors[0]`

Overlap: No independent redundancy established.

### `tests/test_prd_lint.py::test_links_after_a_closed_fence_are_audited[~~~~]`

**KEEP** — Ignore the example inside the specified fence while detecting the actual broken link after the correctly closed fence.

Input: `~~~~`. Source: `tests/test_prd_lint.py:72`.

Assertions: `assert len(errors) == 1 and ':4 LINK: missing local target missing.md' in errors[0]`

Overlap: No independent redundancy established.

### `tests/test_prd_lint.py::test_incorrect_fence_closers_leave_examples_as_examples[~~~]`

**KEEP** — Wrong delimiter, too-short delimiter or info-bearing closer must not close a fence; applies both link examples and code-limit accounting.

Input: `~~~`. Source: `tests/test_prd_lint.py:80`.

Assertions: `assert local_link_errors(path) == []`; `assert result.returncode == 1 and 'R3: 16-line' in result.stdout`

Overlap: No independent redundancy established.

### `tests/test_prd_lint.py::test_incorrect_fence_closers_leave_examples_as_examples[``]`

**KEEP** — Wrong delimiter, too-short delimiter or info-bearing closer must not close a fence; applies both link examples and code-limit accounting.

Input: `\`\``. Source: `tests/test_prd_lint.py:80`.

Assertions: `assert local_link_errors(path) == []`; `assert result.returncode == 1 and 'R3: 16-line' in result.stdout`

Overlap: No independent redundancy established.

### `tests/test_prd_lint.py::test_incorrect_fence_closers_leave_examples_as_examples[```text]`

**KEEP** — Wrong delimiter, too-short delimiter or info-bearing closer must not close a fence; applies both link examples and code-limit accounting.

Input: `\`\`\`text`. Source: `tests/test_prd_lint.py:80`.

Assertions: `assert local_link_errors(path) == []`; `assert result.returncode == 1 and 'R3: 16-line' in result.stdout`

Overlap: No independent redundancy established.

### `tests/test_prd_lint.py::test_legacy_folder_finds_topic_parts`

**KEEP** — Legacy docs/planning invocation intentionally expands to moved topic Parts, distinct from explicit topic-folder isolation.

Input: `see exact fixture/source below`. Source: `tests/test_prd_lint.py:94`.

Assertions: `assert result.returncode == 0, result.stdout`; `assert 'Checked 1 file(s).' in result.stdout`

Overlap: No independent redundancy established.

### `tests/test_prd_lint.py::test_empty_tree_is_not_a_successful_lint`

**KEEP** — No numbered Parts cannot be mislabeled a successful planning audit.

Input: `see exact fixture/source below`. Source: `tests/test_prd_lint.py:104`.

Assertions: `assert result.returncode == 1`; `assert 'No part-*.md files' in result.stdout`

Overlap: No independent redundancy established.

### `tests/test_prd_lint.py::test_missing_targets_report_file_and_line[[Guide](missing.md)]`

**KEEP** — The particular Markdown inline/reference or HTML href spelling must point to the correct source file and line.

Input: `[Guide](missing.md)`. Source: `tests/test_prd_lint.py:113`.

Assertions: `assert len(errors) == 1`; `assert f'{path}:1 LINK: missing local target missing.md' == errors[0]`

Overlap: No independent redundancy established.

### `tests/test_prd_lint.py::test_missing_targets_report_file_and_line[[guide]: missing.md]`

**KEEP** — The particular Markdown inline/reference or HTML href spelling must point to the correct source file and line.

Input: `[guide]: missing.md`. Source: `tests/test_prd_lint.py:113`.

Assertions: `assert len(errors) == 1`; `assert f'{path}:1 LINK: missing local target missing.md' == errors[0]`

Overlap: No independent redundancy established.

### `tests/test_prd_lint.py::test_missing_targets_report_file_and_line[<a href="missing.md">Guide</a>]`

**KEEP** — The particular Markdown inline/reference or HTML href spelling must point to the correct source file and line.

Input: `<a href="missing.md">Guide</a>`. Source: `tests/test_prd_lint.py:113`.

Assertions: `assert len(errors) == 1`; `assert f'{path}:1 LINK: missing local target missing.md' == errors[0]`

Overlap: No independent redundancy established.

### `tests/test_prd_lint.py::test_valid_relative_encoded_external_and_anchor_links`

**KEEP** — Valid encoded-space file, fragment-only and external targets must avoid false failures; anchors/external URLs are not actually verified here.

Input: `see exact fixture/source below`. Source: `tests/test_prd_lint.py:121`.

Assertions: `assert local_link_errors(path) == []`

Overlap: No independent redundancy established.

### `tests/test_prd_lint.py::test_code_example_is_not_an_active_document_link`

**MERGE** — Fenced inline-link example is ignored; same behavior is asserted within richer closed-fence test. Consolidate into the richer case; preserve both ignore-example and detect-real-link assertions.

Input: `see exact fixture/source below`. Source: `tests/test_prd_lint.py:129`.

Assertions: `assert local_link_errors(path) == []`

Overlap: `tests/test_prd_lint.py::test_links_after_a_closed_fence_are_audited[```]`

### `tests/test_prd_lint.py::test_broken_guide_link_fails_whole_lint`

**KEEP** — Lint CLI failure includes a non-Part guide; direct helper tests alone do not prove CLI collection/exit behavior.

Input: `see exact fixture/source below`. Source: `tests/test_prd_lint.py:135`.

Assertions: `assert result.returncode == 1`; `assert 'LINK: missing local target missing.md' in result.stdout`

Overlap: No independent redundancy established.

### `tests/test_prd_lint.py::test_long_code_block_still_fails`

**KEEP** — Python code fence above the policy line cap fails; same language/input exists in false-closer policy exercise, but simple normal closer is an independent representative.

Input: `see exact fixture/source below`. Source: `tests/test_prd_lint.py:143`.

Assertions: `assert result.returncode == 1`; `assert 'R3: 16-line' in result.stdout`

Overlap: No independent redundancy established.

### `tests/test_prd_lint.py::test_duplicate_story_definitions_still_fail`

**KEEP** — Duplicate Story definitions in different Parts fail, unlike non-failing skill warnings.

Input: `see exact fixture/source below`. Source: `tests/test_prd_lint.py:150`.

Assertions: `assert result.returncode == 1`; `assert 'story E2-US04 defined 2 times' in result.stdout`

Overlap: No independent redundancy established.

### `tests/test_prd_lint.py::test_day_references_and_checklists_are_not_duplicate_schedule_entries`

**KEEP** — Only primary Sprint day headings count; checklist subheads and schema references do not add schedule entries.

Input: `see exact fixture/source below`. Source: `tests/test_prd_lint.py:158`.

Assertions: `assert result.returncode == 0, result.stdout`; `assert 'appears' not in result.stdout`

Overlap: No independent redundancy established.

### `tests/test_prd_lint.py::test_duplicate_primary_schedule_days_still_fail`

**KEEP** — Two genuine primary Sprint day declarations fail; complements reference-positive examples.

Input: `see exact fixture/source below`. Source: `tests/test_prd_lint.py:168`.

Assertions: `assert result.returncode == 1`; `assert 'DAY 6 appears 2 times' in result.stdout`

Overlap: No independent redundancy established.

### `tests/test_prd_lint.py::test_common_markdown_link_forms_are_valid[[Target](target.md 'A title')]`

**KEEP** — Optional quoted title and angle-bracket reference target forms resolve correctly rather than false missing-file errors.

Input: `[Target](target.md 'A title')`. Source: `tests/test_prd_lint.py:181`.

Assertions: `assert local_link_errors(path) == []`

Overlap: No independent redundancy established.

### `tests/test_prd_lint.py::test_common_markdown_link_forms_are_valid[[target]: <target file.md>]`

**KEEP** — Optional quoted title and angle-bracket reference target forms resolve correctly rather than false missing-file errors.

Input: `[target]: <target file.md>`. Source: `tests/test_prd_lint.py:181`.

Assertions: `assert local_link_errors(path) == []`

Overlap: No independent redundancy established.

### `tests/test_prd_lint.py::test_tilde_fenced_link_example_is_not_an_active_link`

**MERGE** — Tilde fence ignores an example; richer tilde closed-fence case contains the same expectation. Three versus four tildes are separate supported delimiter inputs; preserve the triple-tilde row in a unified fence fixture before deleting this function.

Input: `see exact fixture/source below`. Source: `tests/test_prd_lint.py:189`.

Assertions: `assert local_link_errors(path) == []`

Overlap: `tests/test_prd_lint.py::test_links_after_a_closed_fence_are_audited[~~~~]`

### `tests/test_prd_lint.py::test_all_supported_markdown_fences_enforce_the_code_limit[```]`

**KEEP** — Each supported delimiter shape enforces the SQL code-length rule; changing marker support can regress independently.

Input: `\`\`\``. Source: `tests/test_prd_lint.py:196`.

Assertions: `assert result.returncode == 1`; `assert 'R3: 16-line' in result.stdout`

Overlap: No independent redundancy established.

### `tests/test_prd_lint.py::test_all_supported_markdown_fences_enforce_the_code_limit[~~~]`

**KEEP** — Each supported delimiter shape enforces the SQL code-length rule; changing marker support can regress independently.

Input: `~~~`. Source: `tests/test_prd_lint.py:196`.

Assertions: `assert result.returncode == 1`; `assert 'R3: 16-line' in result.stdout`

Overlap: No independent redundancy established.

### `tests/test_prd_lint.py::test_all_supported_markdown_fences_enforce_the_code_limit[````]`

**KEEP** — Each supported delimiter shape enforces the SQL code-length rule; changing marker support can regress independently.

Input: `\`\`\`\``. Source: `tests/test_prd_lint.py:196`.

Assertions: `assert result.returncode == 1`; `assert 'R3: 16-line' in result.stdout`

Overlap: No independent redundancy established.

### `tests/test_prd_lint.py::test_exactly_fifteen_code_lines_are_allowed`

**KEEP** — Policy boundary permits exactly 15 rather than rejecting valid hint-sized code blocks.

Input: `see exact fixture/source below`. Source: `tests/test_prd_lint.py:203`.

Assertions: `assert result.returncode == 0, result.stdout`

Overlap: No independent redundancy established.

### `tests/test_prd_lint.py::test_inline_code_example_is_ignored_but_real_link_still_checked`

**KEEP** — Ignore inline-code link spelling while checking real link beside it; distinct parser state from fenced code.

Input: `see exact fixture/source below`. Source: `tests/test_prd_lint.py:209`.

Assertions: `assert local_link_errors(path) == [f'{path}:1 LINK: missing local target real-missing.md']`

Overlap: No independent redundancy established.

### `tools/test_doctor.py::DoctorTests::test_cluster_is_observed_without_assuming_original`

**KEEP** — Optional expected-cluster mode accepts a genuinely observed alternate cluster; do not hardcode Sprint 0 identity.

Input: `see exact fixture/source below`. Source: `tools/test_doctor.py:53`.

Assertions: `self.assertIn('PG-CLUSTER PASS: cluster identifier observed (456)', output.getvalue())`; `self.assertEqual(instance.failures, 0)`

Overlap: No independent redundancy established.

### `tools/test_doctor.py::DoctorTests::test_command_errors_are_captured_and_not_relayed`

**IMPROVE** — Captured subprocess failures must retain status without printing credentials; bounded subprocess invocation is part of diagnostic safety. Keep empty-output/status evidence; consider asserting bounded positive timeout rather than exact optional keyword values unless 30 seconds/check=False are fixed public contracts.

Input: `see exact fixture/source below`. Source: `tools/test_doctor.py:18`.

Assertions: `self.assertEqual(result.returncode, 1)`; `self.assertEqual(output.getvalue(), '')`; `self.assertTrue(called.call_args.kwargs['capture_output'])`; `self.assertTrue(called.call_args.kwargs['text'])`; `self.assertEqual(called.call_args.kwargs['cwd'], Path(directory))`; `self.assertEqual(called.call_args.kwargs['timeout'], 30)`; `self.assertFalse(called.call_args.kwargs['check'])`

Overlap: No independent redundancy established.

### `tools/test_doctor.py::DoctorTests::test_host_auth_uses_env_and_rejects_generic_errors`

**KEEP** — Native host command keeps secrets out of argv, gives positive/negative commands separate environment snapshots, and classifies authentication errors.

Input: `see exact fixture/source below`. Source: `tools/test_doctor.py:69`.

Assertions: `self.assertIn('HOST-PG-NEGATIVE ' + status, output.getvalue())`; `self.assertNotIn('secret', output.getvalue())`; `self.assertNotIn('secret', str(positive.args[0]))`; `self.assertEqual(positive.args[0][positive.args[0].index('-h') + 1], '127.0.0.1')`; `self.assertEqual(positive.args[2]['PGPASSWORD'], 'secret')`; `self.assertEqual(negative.args[2]['PGPASSWORD'], 'secret__doctor_wrong')`

Overlap: No independent redundancy established.

### `tools/test_doctor.py::DoctorTests::test_inspect_never_requests_environment_and_rejects_malformed_data`

**KEEP** — Do not request Docker secret environment and refuse non-JSON inspection; distinct from typed valid-JSON malformed structures.

Input: `see exact fixture/source below`. Source: `tools/test_doctor.py:62`.

Assertions: `self.assertNotIn('Config.Env', call.call_args.args[0][-2])`; `self.assertNotIn('config', call.call_args.args[0])`; `self.assertIsNone(instance.inspect('a' * 64))`

Overlap: No independent redundancy established.

### `tools/test_doctor.py::DoctorTests::test_runtime_accepts_clone_project_and_alternate_loopback_port`

**KEEP** — A valid clone project and alternate loopback port must pass actual runtime orchestration; negative-only configuration tests are insufficient.

Input: `see exact fixture/source below`. Source: `tools/test_doctor.py:93`.

Assertions: `self.assertEqual(instance.failures, 0)`; `self.assertEqual(instance.host_ports, {'postgres': '15432', 'redis': '16379'})`

Overlap: No independent redundancy established.

### `tools/test_doctor.py::DoctorTests::test_static_never_invokes_runtime`

**KEEP** — Static-only mode must not inspect/run live services; protects operational boundary, not merely formatting.

Input: `see exact fixture/source below`. Source: `tools/test_doctor.py:87`.

Assertions: `runtime.assert_not_called()`; `self.assertEqual(instance.execute(), 0)`

Overlap: No independent redundancy established.

### `tools/test_doctor.py::DoctorTests::test_timeout_does_not_print_partial_secret`

**KEEP** — Captured partial timeout output must never be echoed; timeout cannot become command success.

Input: `see exact fixture/source below`. Source: `tools/test_doctor.py:32`.

Assertions: `self.assertNotEqual(result.returncode, 0)`; `self.assertEqual(output.getvalue(), '')`

Overlap: No independent redundancy established.

### `tools/test_doctor.py::DoctorTests::test_wrong_password_requires_authentication_rejection`

**MERGE** — Distinguish credential rejection from network failure and accidentally accepted wrong password; parent row plus individual subtest rows. Parent row aggregates the three subtest branches; it is not an additional fourth independent input. Keep the unittest parent for execution but do not inflate input counts.

Input: `see exact fixture/source below`. Source: `tools/test_doctor.py:40`.

Assertions: `self.assertIn('PG-AUTH-NEGATIVE ' + ('PASS' if succeeds else 'FAIL'), output.getvalue())`; `self.assertNotIn('secret', output.getvalue())`

Overlap: No independent redundancy established.

### `tools/test_doctor.py::DoctorTests::test_wrong_password_requires_authentication_rejection::subtest{"negative": "2", "succeeds": "False"}`

**KEEP** — Distinguish credential rejection from network failure and accidentally accepted wrong password; parent row plus individual subtest rows.

Input: `see exact fixture/source below`. Source: `tools/test_doctor.py:40`.

Assertions: `self.assertIn('PG-AUTH-NEGATIVE ' + ('PASS' if succeeds else 'FAIL'), output.getvalue())`; `self.assertNotIn('secret', output.getvalue())`

Overlap: No independent redundancy established.

### `tools/test_doctor.py::DoctorTests::test_wrong_password_requires_authentication_rejection::subtest{"negative": "0", "succeeds": "False"}`

**KEEP** — Distinguish credential rejection from network failure and accidentally accepted wrong password; parent row plus individual subtest rows.

Input: `see exact fixture/source below`. Source: `tools/test_doctor.py:40`.

Assertions: `self.assertIn('PG-AUTH-NEGATIVE ' + ('PASS' if succeeds else 'FAIL'), output.getvalue())`; `self.assertNotIn('secret', output.getvalue())`

Overlap: No independent redundancy established.

### `tools/test_doctor.py::DoctorTests::test_wrong_password_requires_authentication_rejection::subtest{"negative": "2", "succeeds": "True"}`

**KEEP** — Distinguish credential rejection from network failure and accidentally accepted wrong password; parent row plus individual subtest rows.

Input: `see exact fixture/source below`. Source: `tools/test_doctor.py:40`.

Assertions: `self.assertIn('PG-AUTH-NEGATIVE ' + ('PASS' if succeeds else 'FAIL'), output.getvalue())`; `self.assertNotIn('secret', output.getvalue())`

Overlap: No independent redundancy established.

## Every source fault

### `doctor-command-timeout-unbounded`

**KEEP** — Targets run through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `run`; observed DETECTED; detects 1 cases.

- Line 21: `return subprocess.run(args, cwd=root, capture_output=True, text=True, timeout=30,` becomes `return subprocess.run(args, cwd=root, capture_output=True, text=True, timeout=None,`.

### `doctor-command-raises-on-errors`

**KEEP** — Targets run through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `run`; observed DETECTED; detects 1 cases.

- Line 22: `check=False, env=env)` becomes `check=True, env=env)`.

### `doctor-command-does-not-capture`

**KEEP** — Targets run through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `run`; observed DETECTED; detects 1 cases.

- Line 21: `return subprocess.run(args, cwd=root, capture_output=True, text=True, timeout=30,` becomes `return subprocess.run(args, cwd=root, capture_output=False, text=True, timeout=30,`.

### `doctor-command-ignores-cwd`

**KEEP** — Targets run through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `run`; observed DETECTED; detects 1 cases.

- Line 21: `return subprocess.run(args, cwd=root, capture_output=True, text=True, timeout=30,` becomes `return subprocess.run(args, cwd=None, capture_output=True, text=True, timeout=30,`.

### `doctor-timeout-reports-success`

**KEEP** — Targets run through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `run`; observed DETECTED; detects 1 cases.

- Line 24: `return subprocess.CompletedProcess(args, 127, '', '')` becomes `return subprocess.CompletedProcess(args, 0, '', '')`.

### `doctor-negative-auth-accepts-any-error`

**KEEP** — Targets host_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `host_checks`; observed DETECTED; detects 3 cases.

- Line 178: `rejected = negative.returncode != 0 and 'password authentication failed' in negative.stderr.lower()` becomes `rejected = negative.returncode != 0`.
- Line 201: `rejected = negative.returncode != 0 and 'password authentication failed' in negative.stderr.lower()` becomes `rejected = negative.returncode != 0`.

### `doctor-negative-auth-accepts-success`

**KEEP** — Targets host_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `host_checks`; observed DETECTED; detects 2 cases.

- Line 178: `rejected = negative.returncode != 0 and 'password authentication failed' in negative.stderr.lower()` becomes `rejected = negative.returncode == 0 or 'password authentication failed' in negative.stderr.lower()`.
- Line 201: `rejected = negative.returncode != 0 and 'password authentication failed' in negative.stderr.lower()` becomes `rejected = negative.returncode == 0 or 'password authentication failed' in negative.stderr.lower()`.

### `doctor-nested-inspection-guard-disabled`

**KEEP** — Targets inspect through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `inspect`; observed DETECTED; detects 8 cases.

- Line 106: `ports = host.get('PortBindings', {})` becomes `return health, host, mounts, labels`.
- Line 107: `log = host.get('LogConfig', {})` becomes `ports = host.get('PortBindings', {})`.
- Line 108: `if not isinstance(ports, dict) or not isinstance(log, dict):` becomes `log = host.get('LogConfig', {})`.

### `doctor-malformed-manifest-crashes`

**KEEP** — Targets static_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `static_checks`; observed DETECTED; detects 1 cases.

- Line 52: `except (OSError, ValueError, KeyError, TypeError):` becomes `except (OSError, ValueError, KeyError):`.

### `doctor-missing-manifest-pin-crashes`

**KEEP** — Targets static_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `static_checks`; observed DETECTED; detects 1 cases.

- Line 52: `except (OSError, ValueError, KeyError, TypeError):` becomes `except (OSError, ValueError, TypeError):`.

### `doctor-all-python-pins-accepted`

**KEEP** — Targets static_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `static_checks`; observed DETECTED; detects 2 cases.

- Line 50: `python_ok = declared in ('>=3.12,<3.13', '>=3.12, <3.13', '==3.12.*')` becomes `python_ok = True or declared in ('>=3.12,<3.13', '>=3.12, <3.13', '==3.12.*')`.

### `doctor-unicode-port-crash`

**KEEP** — Targets runtime_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `runtime_checks`; observed DETECTED; detects 1 cases.

- Line 136: `valid_port = len(bindings) == 1 and bindings[0].get('HostIp') == '127.0.0.1' and bool(re.fullmatch(r'[0-9]{1,5}', str(bindings[0].get('HostPort', '')))) and 0 < int(bindings[0]['HostPort']) <= 65535` becomes `valid_port = len(bindings) == 1 and bindings[0].get('HostIp') == '127.0.0.1' and str(bindings[0].get('HostPort', '')).isdigit() and 0 < int(bindings[0]['HostPort']) <= 65535`.

### `doctor-timeout-leaks-secret`

**KEEP** — Targets run through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `run`; observed DETECTED; detects 1 cases.

- Line 24: `return subprocess.CompletedProcess(args, 127, '', '')` becomes `print(str(args)); return subprocess.CompletedProcess(args, 127, '', '')`.

### `doctor-static-runs-runtime`

**KEEP** — Targets execute through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `execute`; observed DETECTED; detects 1 cases.

- Line 214: `if not self.static and available:` becomes `if available:`.

### `doctor-all-reports-pass`

**KEEP** — Targets report through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `report`; observed DETECTED; detects 59 cases.

- Line 34: `status = 'PASS' if ok else 'WARN' if warn else 'FAIL'` becomes `status = 'PASS'`.

### `doctor-all-reports-fail`

**KEEP** — Targets report through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `report`; observed DETECTED; detects 60 cases.

- Line 34: `status = 'PASS' if ok else 'WARN' if warn else 'FAIL'` becomes `status = 'FAIL'`.

### `doctor-no-failure-accounting`

**KEEP** — Targets report through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `report`; observed DETECTED; detects 18 cases.

- Line 35: `self.failures += int(status == 'FAIL')` becomes `self.failures += 0`.

### `doctor-inspect-always-refuses`

**KEEP** — Targets inspect through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `inspect`; observed DETECTED; detects 18 cases.

- Line 117: `return health, host, mounts, labels` becomes `return None`.

### `doctor-inspect-shape-guard-disabled`

**KEEP** — Targets inspect through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `inspect`; observed DETECTED; detects 3 cases.

- Line 102: `if not (isinstance(health, str) and isinstance(host, dict)` becomes `if False and not (isinstance(health, str) and isinstance(host, dict)`.

### `doctor-requests-secret-environment`

**KEEP** — Targets inspect through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `inspect`; observed DETECTED; detects 1 cases.

- Line 95: `template = '{{json .State.Health.Status}}|{{json .HostConfig}}|{{json .Mounts}}|{{json .Config.Labels}}'` becomes `template = '{{json .Config.Env}}|{{json .HostConfig}}|{{json .Mounts}}|{{json .Config.Labels}}'`.

### `doctor-service-auth-wrong-query`

**KEEP** — Targets postgres_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `postgres_checks`; observed DETECTED; detects 1 cases.

- Line 195: `'PGPASSWORD="$POSTGRES_PASSWORD" ' + base + "'SELECT 1'")` becomes `'PGPASSWORD="$POSTGRES_PASSWORD" ' + base + "'SELECT 2'")`.
- Line 199: `'PGPASSWORD="${POSTGRES_PASSWORD}__doctor_wrong" ' + base + "'SELECT 1'")` becomes `'PGPASSWORD="${POSTGRES_PASSWORD}__doctor_wrong" ' + base + "'SELECT 2'")`.

### `doctor-service-password-not-negative`

**KEEP** — Targets postgres_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `postgres_checks`; observed DETECTED; detects 1 cases.

- Line 199: `'PGPASSWORD="${POSTGRES_PASSWORD}__doctor_wrong" ' + base + "'SELECT 1'")` becomes `'PGPASSWORD="${POSTGRES_PASSWORD}" ' + base + "'SELECT 1'")`.

### `doctor-host-password-not-negative`

**KEEP** — Targets host_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `host_checks`; observed DETECTED; detects 1 cases.

- Line 175: `environment = dict(environment, PGPASSWORD=password + '__doctor_wrong')` becomes `environment = dict(environment, PGPASSWORD=password)`.

### `doctor-host-public-interface`

**KEEP** — Targets host_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `host_checks`; observed DETECTED; detects 8 cases.

- Line 171: `args = ['psql', '-X', '-w', '-h', '127.0.0.1', '-p', pg_port,` becomes `args = ['psql', '-X', '-w', '-h', '0.0.0.0', '-p', pg_port,`.

### `doctor-host-password-in-command`

**KEEP** — Targets host_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `host_checks`; observed DETECTED; detects 1 cases.

- Line 172: `'-U', user, '-d', database, '-Atqc', 'SELECT 1']` becomes `'-U', user, '-d', database, '-Atqc', 'SELECT 1', password]`.

### `doctor-cluster-expected-ignored`

**KEEP** — Targets postgres_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `postgres_checks`; observed DETECTED; detects 1 cases.

- Line 208: `self.report('PG-CLUSTER', valid and (self.expect_cluster is None or observed == self.expect_cluster),` becomes `self.report('PG-CLUSTER', valid and (True),`.

### `doctor-cluster-always-refuses`

**KEEP** — Targets postgres_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `postgres_checks`; observed DETECTED; detects 5 cases.

- Line 208: `self.report('PG-CLUSTER', valid and (self.expect_cluster is None or observed == self.expect_cluster),` becomes `self.report('PG-CLUSTER', False,`.

### `doctor-cluster-assumes-original`

**KEEP** — Targets postgres_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `postgres_checks`; observed DETECTED; detects 5 cases.

- Line 208: `self.report('PG-CLUSTER', valid and (self.expect_cluster is None or observed == self.expect_cluster),` becomes `self.report('PG-CLUSTER', valid and (observed == '7691749973399031842'),`.

### `linter-empty-tree-passes`

**KEEP** — Targets main through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/prd_lint.py`; responsible function: `main`; observed DETECTED; detects 1 cases.

- Line 139: `return 1` becomes `return 0`.

### `linter-legacy-folder-not-expanded`

**KEEP** — Targets document_root through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/prd_lint.py`; responsible function: `document_root`; observed DETECTED; detects 1 cases.

- Line 37: `return folder.parent` becomes `return folder`.

### `linter-link-check-disabled`

**KEEP** — Targets local_link_errors through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/prd_lint.py`; responsible function: `local_link_errors`; observed DETECTED; detects 10 cases.

- Line 68: `if not destination.exists():` becomes `if False:`.

### `linter-existing-targets-rejected`

**KEEP** — Targets local_link_errors through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/prd_lint.py`; responsible function: `local_link_errors`; observed DETECTED; detects 3 cases.

- Line 68: `if not destination.exists():` becomes `if True:`.

### `linter-percent-encoding-not-decoded`

**KEEP** — Targets local_link_errors through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/prd_lint.py`; responsible function: `local_link_errors`; observed DETECTED; detects 1 cases.

- Line 67: `destination = path.parent / unquote(parsed.path)` becomes `destination = path.parent / parsed.path`.

### `linter-checks-code-examples`

**KEEP** — Targets local_link_errors through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/prd_lint.py`; responsible function: `local_link_errors`; observed DETECTED; detects 7 cases.

- Line 53: `if fence is not None:` becomes `if False:`.

### `linter-inline-examples-checked`

**KEEP** — Targets local_link_errors through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/prd_lint.py`; responsible function: `local_link_errors`; observed DETECTED; detects 1 cases.

- Line 57: `line = re.sub(r"(\`+).*?\1", "", line)` becomes `line = line`.

### `linter-code-limit-relaxed`

**KEEP** — Targets module entry point through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/prd_lint.py`; responsible function: `module entry point`; observed DETECTED; detects 7 cases.

- Line 24: `MAX_CODE_LINES = 15` becomes `MAX_CODE_LINES = 16`.

### `linter-code-limit-too-strict`

**KEEP** — Targets module entry point through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/prd_lint.py`; responsible function: `module entry point`; observed DETECTED; detects 1 cases.

- Line 24: `MAX_CODE_LINES = 15` becomes `MAX_CODE_LINES = 14`.

### `ast-doctor-229-52`

**IMPROVE** — Reversed import/main guard causes CLI parsing before tests. Not a detected implementation fault. Move to explicit CLI-isolation regression; never credit INVALID as effectiveness.

Source: `tools/doctor.py`; responsible function: `module entry point`; observed INVALID; detects 0 cases.

- Line 229: `if __name__ == '__main__':` becomes `if (__name__ != '__main__'):`.

### `ast-doctor-87-236`

**KEEP** — Targets static_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `static_checks`; observed DETECTED; detects 2 cases.

- Line 87: `if available.returncode == 0:` becomes `if (available.returncode != 0):`.

### `ast-doctor-91-239`

**KEEP** — Targets static_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `static_checks`; observed DETECTED; detects 14 cases.

- Line 91: `return available.returncode == 0` becomes `return (available.returncode != 0)`.

### `ast-doctor-165-292`

**KEEP** — Targets host_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `host_checks`; observed DETECTED; detects 2 cases.

- Line 165: `if pg_port and shutil.which('psql'):` becomes `if (pg_port or shutil.which('psql')):`.

### `ast-doctor-201-311`

**KEEP** — Targets postgres_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `postgres_checks`; observed DETECTED; detects 2 cases.

- Line 201: `rejected = negative.returncode != 0 and 'password authentication failed' in negative.stderr.lower()` becomes `rejected = (negative.returncode != 0 or 'password authentication failed' in negative.stderr.lower())`.

### `ast-doctor-207-318`

**KEEP** — Targets postgres_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `postgres_checks`; observed DETECTED; detects 1 cases.

- Line 207: `valid = cluster.returncode == 0 and bool(re.fullmatch(r'\d{1,20}', observed))` becomes `valid = (cluster.returncode == 0 or bool(re.fullmatch('\\d{1,20}', observed)))`.

### `ast-doctor-214-323`

**KEEP** — Targets execute through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `execute`; observed DETECTED; detects 1 cases.

- Line 214: `if not self.static and available:` becomes `if (not self.static or available):`.

### `ast-doctor-35-399`

**KEEP** — Targets report through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `report`; observed DETECTED; detects 22 cases.

- Line 35: `self.failures += int(status == 'FAIL')` becomes `self.failures += int((status != 'FAIL'))`.

### `ast-doctor-77-479`

**KEEP** — Targets static_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `static_checks`; observed DETECTED; detects 14 cases.

- Line 77: `self.report('ENV-IGNORE', ignored.returncode == 0, 'environment file ignored', 'add .env to .gitignore')` becomes `self.report('ENV-IGNORE', (ignored.returncode != 0), 'environment file ignored', 'add .env to .gitignore')`.

### `ast-doctor-81-490`

**KEEP** — Targets static_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `static_checks`; observed DETECTED; detects 3 cases.

- Line 81: `self.report('TRACKED-SECRETS', tracked.returncode == 0 and not secrets,` becomes `self.report('TRACKED-SECRETS', (tracked.returncode == 0 or not secrets),`.

### `ast-doctor-84-498`

**KEEP** — Targets static_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `static_checks`; observed DETECTED; detects 14 cases.

- Line 84: `self.report('VENV-IGNORE', ignored_venv.returncode == 0, 'virtual environment ignored', 'add .venv/ to .gitignore')` becomes `self.report('VENV-IGNORE', (ignored_venv.returncode != 0), 'virtual environment ignored', 'add .venv/ to .gitignore')`.

### `ast-doctor-86-506`

**KEEP** — Targets static_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `static_checks`; observed DETECTED; detects 13 cases.

- Line 86: `self.report('COMPOSE', available.returncode == 0, 'Docker Compose available', 'install Docker Compose plugin', warn=self.static)` becomes `self.report('COMPOSE', (available.returncode != 0), 'Docker Compose available', 'install Docker Compose plugin', warn=self.static)`.

### `ast-doctor-108-535`

**KEEP** — Targets inspect through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `inspect`; observed DETECTED; detects 4 cases.

- Line 108: `if not isinstance(ports, dict) or not isinstance(log, dict):` becomes `if (not isinstance(ports, dict) and (not isinstance(log, dict))):`.

### `ast-doctor-131-562`

**KEEP** — Targets runtime_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `runtime_checks`; observed DETECTED; detects 24 cases.

- Line 131: `if info is None:` becomes `if (info is not None):`.

### `ast-doctor-135-568`

**KEEP** — Targets runtime_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `runtime_checks`; observed DETECTED; detects 13 cases.

- Line 135: `bindings = host.get('PortBindings', {}).get(port) or []` becomes `bindings = (host.get('PortBindings', {}).get(port) and [])`.

### `ast-doctor-136-570`

**KEEP** — Targets runtime_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `runtime_checks`; observed DETECTED; detects 5 cases.

- Line 136: `valid_port = len(bindings) == 1 and bindings[0].get('HostIp') == '127.0.0.1' and bool(re.fullmatch(r'[0-9]{1,5}', str(bindings[0].get('HostPort', '')))) and 0 < int(bindings[0]['HostPort']) <= 65535` becomes `valid_port = (len(bindings) == 1 or bindings[0].get('HostIp') == '127.0.0.1' or bool(re.fullmatch('[0-9]{1,5}', str(bindings[0].get('HostPort', '')))) or (0 < int(bindings[0]['HostPort']) <= 65535))`.

### `ast-doctor-157-597`

**KEEP** — Targets runtime_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `runtime_checks`; observed DETECTED; detects 2 cases.

- Line 157: `self.report('REDIS-PONG', pong.returncode == 0 and pong.stdout.strip() == 'PONG', 'Redis responds PONG', 'check Redis service')` becomes `self.report('REDIS-PONG', (pong.returncode == 0 or pong.stdout.strip() == 'PONG'), 'Redis responds PONG', 'check Redis service')`.

### `ast-doctor-169-621`

**KEEP** — Targets host_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `host_checks`; observed DETECTED; detects 3 cases.

- Line 169: `if credentials.returncode == 0 and len(parts) == 3 and all(parts):` becomes `if (credentials.returncode == 0 or len(parts) == 3 or all(parts)):`.

### `ast-doctor-188-638`

**KEEP** — Targets host_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `host_checks`; observed DETECTED; detects 2 cases.

- Line 188: `if redis_port and shutil.which('redis-cli') else None)` becomes `if (redis_port or shutil.which('redis-cli')) else None)`.

### `ast-doctor-189-643`

**KEEP** — Targets host_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `host_checks`; observed DETECTED; detects 4 cases.

- Line 189: `self.report('HOST-REDIS-PONG', result is not None and result.returncode == 0 and result.stdout.strip() == 'PONG',` becomes `self.report('HOST-REDIS-PONG', (result is not None or result.returncode == 0 or result.stdout.strip() == 'PONG'),`.

### `ast-doctor-196-657`

**KEEP** — Targets postgres_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `postgres_checks`; observed DETECTED; detects 1 cases.

- Line 196: `self.report('PG-AUTH-POSITIVE', positive.returncode == 0 and positive.stdout.strip() == '1',` becomes `self.report('PG-AUTH-POSITIVE', (positive.returncode == 0 or positive.stdout.strip() == '1'),`.

### `ast-doctor-201-670`

**KEEP** — Targets postgres_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `postgres_checks`; observed DETECTED; detects 7 cases.

- Line 201: `rejected = negative.returncode != 0 and 'password authentication failed' in negative.stderr.lower()` becomes `rejected = (negative.returncode == 0) and 'password authentication failed' in negative.stderr.lower()`.

### `ast-doctor-202-674`

**KEEP** — Targets postgres_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `postgres_checks`; observed DETECTED; detects 5 cases.

- Line 202: `self.report('PG-AUTH-NEGATIVE', positive.returncode == 0 and positive.stdout.strip() == '1' and rejected,` becomes `self.report('PG-AUTH-NEGATIVE', (positive.returncode == 0 or positive.stdout.strip() == '1' or rejected),`.

### `ast-doctor-207-689`

**KEEP** — Targets postgres_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `postgres_checks`; observed DETECTED; detects 5 cases.

- Line 207: `valid = cluster.returncode == 0 and bool(re.fullmatch(r'\d{1,20}', observed))` becomes `valid = (cluster.returncode != 0) and bool(re.fullmatch(r'\d{1,20}', observed))`.

### `ast-doctor-208-693`

**KEEP** — Targets postgres_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `postgres_checks`; observed DETECTED; detects 2 cases.

- Line 208: `self.report('PG-CLUSTER', valid and (self.expect_cluster is None or observed == self.expect_cluster),` becomes `self.report('PG-CLUSTER', (valid or (self.expect_cluster is None or observed == self.expect_cluster)),`.

### `ast-doctor-59-844`

**KEEP** — Targets static_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `static_checks`; observed DETECTED; detects 14 cases.

- Line 59: `self.report('UV-LOCK', result.returncode == 0, 'offline lock consistency checked', 'run uv lock and review changes')` becomes `self.report('UV-LOCK', (result.returncode != 0), 'offline lock consistency checked', 'run uv lock and review changes')`.

### `ast-doctor-67-873`

**KEEP** — Targets static_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `static_checks`; observed DETECTED; detects 5 cases.

- Line 67: `self.report(tool.upper(), result.returncode == 0 and bool(match) and int(match[1]) == major,` becomes `self.report(tool.upper(), (result.returncode == 0 or bool(match) or int(match[1]) == major),`.

### `ast-doctor-75-893`

**KEEP** — Targets static_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `static_checks`; observed DETECTED; detects 14 cases.

- Line 75: `self.report('ENV-MODE', env.stat().st_mode & 0o077 == 0, 'environment file private', 'chmod 600 .env')` becomes `self.report('ENV-MODE', (env.stat().st_mode & 63 != 0), 'environment file private', 'chmod 600 .env')`.

### `ast-doctor-79-917`

**KEEP** — Targets static_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `static_checks`; observed DETECTED; detects 2 cases.

- Line 79: `secrets = [p for p in tracked.stdout.split('\0') if Path(p).name == '.env' or` becomes `secrets = [p for p in tracked.stdout.split('\0') if (Path(p).name == '.env' and (Path(p).name.startswith('.env.') and Path(p).name != '.env.example'))]`.
- Line 80: `(Path(p).name.startswith('.env.') and Path(p).name != '.env.example')]` becomes `self.report('TRACKED-SECRETS', tracked.returncode == 0 and not secrets,`.
- Line 81: `self.report('TRACKED-SECRETS', tracked.returncode == 0 and not secrets,` becomes `'no environment secret files tracked', 'untrack secret files and rotate exposed credentials')`.

### `ast-doctor-81-921`

**KEEP** — Targets static_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `static_checks`; observed DETECTED; detects 12 cases.

- Line 81: `self.report('TRACKED-SECRETS', tracked.returncode == 0 and not secrets,` becomes `self.report('TRACKED-SECRETS', (tracked.returncode != 0) and not secrets,`.

### `ast-doctor-89-951`

**KEEP** — Targets static_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `static_checks`; observed DETECTED; detects 14 cases.

- Line 89: `self.report('COMPOSE-CONFIG', config.returncode == 0, 'quiet Compose validation completed',` becomes `self.report('COMPOSE-CONFIG', (config.returncode != 0), 'quiet Compose validation completed',`.

### `ast-doctor-102-975`

**KEEP** — Targets inspect through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `inspect`; observed DETECTED; detects 3 cases.

- Line 102: `if not (isinstance(health, str) and isinstance(host, dict)` becomes `if not ((isinstance(health, str) or isinstance(host, dict) or isinstance(mounts, list) or all((isinstance(mount, dict) for mount in mounts)) or isinstance(labels, dict))):`.
- Line 103: `and isinstance(mounts, list) and all(isinstance(mount, dict) for mount in mounts)` becomes `return None`.
- Line 104: `and isinstance(labels, dict)):` becomes `ports = host.get('PortBindings', {})`.

### `ast-doctor-128-1029`

**KEEP** — Targets runtime_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `runtime_checks`; observed DETECTED; detects 17 cases.

- Line 128: `info = self.inspect(container) if ids.returncode == 0 and re.fullmatch(r'[a-f0-9]{12,64}', container) else None` becomes `info = self.inspect(container) if (ids.returncode == 0 or re.fullmatch('[a-f0-9]{12,64}', container)) else None`.

### `ast-doctor-130-1036`

**KEEP** — Targets runtime_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `runtime_checks`; observed DETECTED; detects 24 cases.

- Line 130: `self.report(prefix + '-RUNNING', info is not None, 'service inspect available', 'start this project with docker compose up -d')` becomes `self.report(prefix + '-RUNNING', (info is None), 'service inspect available', 'start this project with docker compose up -d')`.

### `ast-doctor-134-1050`

**KEEP** — Targets runtime_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `runtime_checks`; observed DETECTED; detects 18 cases.

- Line 134: `self.report(prefix + '-HEALTH', health == 'healthy', 'service healthy', 'inspect service health privately')` becomes `self.report(prefix + '-HEALTH', (health != 'healthy'), 'service healthy', 'inspect service health privately')`.

### `ast-doctor-136-1059`

**KEEP** — Targets runtime_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `runtime_checks`; observed DETECTED; detects 14 cases.

- Line 136: `valid_port = len(bindings) == 1 and bindings[0].get('HostIp') == '127.0.0.1' and bool(re.fullmatch(r'[0-9]{1,5}', str(bindings[0].get('HostPort', '')))) and 0 < int(bindings[0]['HostPort']) <= 65535` becomes `valid_port = (len(bindings) != 1) and bindings[0].get('HostIp') == '127.0.0.1' and bool(re.fullmatch(r'[0-9]{1,5}', str(bindings[0].get('HostPort', '')))) and 0 < int(bindings[0]['HostPort']) <= 65535`.

### `ast-doctor-136-1060`

**KEEP** — Targets runtime_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `runtime_checks`; observed DETECTED; detects 14 cases.

- Line 136: `valid_port = len(bindings) == 1 and bindings[0].get('HostIp') == '127.0.0.1' and bool(re.fullmatch(r'[0-9]{1,5}', str(bindings[0].get('HostPort', '')))) and 0 < int(bindings[0]['HostPort']) <= 65535` becomes `valid_port = len(bindings) == 1 and (bindings[0].get('HostIp') != '127.0.0.1') and bool(re.fullmatch(r'[0-9]{1,5}', str(bindings[0].get('HostPort', '')))) and 0 < int(bindings[0]['HostPort']) <= 65535`.

### `ast-doctor-141-1073`

**KEEP** — Targets runtime_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `runtime_checks`; observed DETECTED; detects 2 cases.

- Line 141: `self.report(prefix + '-LIMITS', host.get('Memory') == memory and host.get('NanoCpus') == cpus,` becomes `self.report(prefix + '-LIMITS', (host.get('Memory') == memory or host.get('NanoCpus') == cpus),`.

### `ast-doctor-144-1082`

**KEEP** — Targets runtime_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `runtime_checks`; observed DETECTED; detects 3 cases.

- Line 144: `self.report(prefix + '-LOGS', log.get('Type') == 'json-file' and log.get('Config', {}).get('max-size') == '10m'` becomes `self.report(prefix + '-LOGS', (log.get('Type') == 'json-file' or log.get('Config', {}).get('max-size') == '10m' or log.get('Config', {}).get('max-file') == '3'), 'logs bounded', 'restore 10m / 3 log rotation')`.
- Line 145: `and log.get('Config', {}).get('max-file') == '3', 'logs bounded', 'restore 10m / 3 log rotation')` becomes `project = labels.get('com.docker.compose.project', '')`.
- Line 146: `project = labels.get('com.docker.compose.project', '')` becomes `matching = [m for m in mounts if m.get('Destination') == destination]`.

### `ast-doctor-148-1094`

**KEEP** — Targets runtime_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `runtime_checks`; observed DETECTED; detects 5 cases.

- Line 148: `self.report(prefix + '-VOLUME', bool(project) and len(matching) == 1 and matching[0].get('Type') == 'volume'` becomes `self.report(prefix + '-VOLUME', (bool(project) or len(matching) == 1 or matching[0].get('Type') == 'volume' or (matching[0].get('Name') == f'{project}_{service}_data')),`.
- Line 149: `and matching[0].get('Name') == f'{project}_{service}_data',` becomes `'project scoped named volume mounted', 'restore service named volume mount')`.
- Line 150: `'project scoped named volume mounted', 'restore service named volume mount')` becomes `uid = self.compose('exec', '-T', service, 'sh', '-c', "awk '/^Uid:/{print $2}' /proc/1/status")`.

### `ast-doctor-152-1107`

**KEEP** — Targets runtime_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `runtime_checks`; observed DETECTED; detects 1 cases.

- Line 152: `self.report(prefix + '-UID', uid.returncode == 0 and uid.stdout.strip() == '999',` becomes `self.report(prefix + '-UID', (uid.returncode == 0 or uid.stdout.strip() == '999'),`.

### `ast-doctor-157-1119`

**KEEP** — Targets runtime_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `runtime_checks`; observed DETECTED; detects 23 cases.

- Line 157: `self.report('REDIS-PONG', pong.returncode == 0 and pong.stdout.strip() == 'PONG', 'Redis responds PONG', 'check Redis service')` becomes `self.report('REDIS-PONG', (pong.returncode != 0) and pong.stdout.strip() == 'PONG', 'Redis responds PONG', 'check Redis service')`.

### `ast-doctor-157-1120`

**KEEP** — Targets runtime_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `runtime_checks`; observed DETECTED; detects 23 cases.

- Line 157: `self.report('REDIS-PONG', pong.returncode == 0 and pong.stdout.strip() == 'PONG', 'Redis responds PONG', 'check Redis service')` becomes `self.report('REDIS-PONG', pong.returncode == 0 and (pong.stdout.strip() != 'PONG'), 'Redis responds PONG', 'check Redis service')`.

### `ast-doctor-160-1147`

**KEEP** — Targets runtime_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `runtime_checks`; observed DETECTED; detects 4 cases.

- Line 160: `self.report('REDIS-' + key.upper(), result.returncode == 0 and result.stdout.splitlines() == [key, value],` becomes `self.report('REDIS-' + key.upper(), (result.returncode == 0 or result.stdout.splitlines() == [key, value]),`.

### `ast-doctor-169-1167`

**KEEP** — Targets host_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `host_checks`; observed DETECTED; detects 9 cases.

- Line 169: `if credentials.returncode == 0 and len(parts) == 3 and all(parts):` becomes `if (credentials.returncode != 0) and len(parts) == 3 and all(parts):`.

### `ast-doctor-169-1168`

**KEEP** — Targets host_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `host_checks`; observed DETECTED; detects 9 cases.

- Line 169: `if credentials.returncode == 0 and len(parts) == 3 and all(parts):` becomes `if credentials.returncode == 0 and (len(parts) != 3) and all(parts):`.

### `ast-doctor-177-1183`

**KEEP** — Targets host_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `host_checks`; observed DETECTED; detects 2 cases.

- Line 177: `accepted = positive.returncode == 0 and positive.stdout.strip() == '1'` becomes `accepted = (positive.returncode == 0 or positive.stdout.strip() == '1')`.

### `ast-doctor-178-1185`

**KEEP** — Targets host_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `host_checks`; observed DETECTED; detects 1 cases.

- Line 178: `rejected = negative.returncode != 0 and 'password authentication failed' in negative.stderr.lower()` becomes `rejected = (negative.returncode != 0 or 'password authentication failed' in negative.stderr.lower())`.

### `ast-doctor-189-1205`

**KEEP** — Targets host_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `host_checks`; observed DETECTED; detects 10 cases.

- Line 189: `self.report('HOST-REDIS-PONG', result is not None and result.returncode == 0 and result.stdout.strip() == 'PONG',` becomes `self.report('HOST-REDIS-PONG', (result is None) and result.returncode == 0 and result.stdout.strip() == 'PONG',`.

### `ast-doctor-189-1206`

**KEEP** — Targets host_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `host_checks`; observed DETECTED; detects 9 cases.

- Line 189: `self.report('HOST-REDIS-PONG', result is not None and result.returncode == 0 and result.stdout.strip() == 'PONG',` becomes `self.report('HOST-REDIS-PONG', result is not None and (result.returncode != 0) and result.stdout.strip() == 'PONG',`.

### `ast-doctor-189-1207`

**KEEP** — Targets host_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `host_checks`; observed DETECTED; detects 9 cases.

- Line 189: `self.report('HOST-REDIS-PONG', result is not None and result.returncode == 0 and result.stdout.strip() == 'PONG',` becomes `self.report('HOST-REDIS-PONG', result is not None and result.returncode == 0 and (result.stdout.strip() != 'PONG'),`.

### `ast-doctor-196-1216`

**KEEP** — Targets postgres_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `postgres_checks`; observed DETECTED; detects 5 cases.

- Line 196: `self.report('PG-AUTH-POSITIVE', positive.returncode == 0 and positive.stdout.strip() == '1',` becomes `self.report('PG-AUTH-POSITIVE', (positive.returncode != 0) and positive.stdout.strip() == '1',`.

### `ast-doctor-196-1217`

**KEEP** — Targets postgres_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `postgres_checks`; observed DETECTED; detects 6 cases.

- Line 196: `self.report('PG-AUTH-POSITIVE', positive.returncode == 0 and positive.stdout.strip() == '1',` becomes `self.report('PG-AUTH-POSITIVE', positive.returncode == 0 and (positive.stdout.strip() != '1'),`.

### `ast-doctor-202-1232`

**KEEP** — Targets postgres_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `postgres_checks`; observed DETECTED; detects 7 cases.

- Line 202: `self.report('PG-AUTH-NEGATIVE', positive.returncode == 0 and positive.stdout.strip() == '1' and rejected,` becomes `self.report('PG-AUTH-NEGATIVE', (positive.returncode != 0) and positive.stdout.strip() == '1' and rejected,`.

### `ast-doctor-202-1233`

**KEEP** — Targets postgres_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `postgres_checks`; observed DETECTED; detects 8 cases.

- Line 202: `self.report('PG-AUTH-NEGATIVE', positive.returncode == 0 and positive.stdout.strip() == '1' and rejected,` becomes `self.report('PG-AUTH-NEGATIVE', positive.returncode == 0 and (positive.stdout.strip() != '1') and rejected,`.

### `ast-doctor-208-1251`

**KEEP** — Targets postgres_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `postgres_checks`; observed DETECTED; detects 5 cases.

- Line 208: `self.report('PG-CLUSTER', valid and (self.expect_cluster is None or observed == self.expect_cluster),` becomes `self.report('PG-CLUSTER', valid and ((self.expect_cluster is None and observed == self.expect_cluster)),`.

### `ast-doctor-67-1382`

**KEEP** — Targets static_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `static_checks`; observed DETECTED; detects 13 cases.

- Line 67: `self.report(tool.upper(), result.returncode == 0 and bool(match) and int(match[1]) == major,` becomes `self.report(tool.upper(), (result.returncode != 0) and bool(match) and int(match[1]) == major,`.

### `ast-doctor-67-1384`

**KEEP** — Targets static_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `static_checks`; observed DETECTED; detects 13 cases.

- Line 67: `self.report(tool.upper(), result.returncode == 0 and bool(match) and int(match[1]) == major,` becomes `self.report(tool.upper(), result.returncode == 0 and bool(match) and (int(match[1]) != major),`.

### `ast-doctor-79-1422`

**KEEP** — Targets static_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `static_checks`; observed DETECTED; detects 11 cases.

- Line 79: `secrets = [p for p in tracked.stdout.split('\0') if Path(p).name == '.env' or` becomes `secrets = [p for p in tracked.stdout.split('\0') if (Path(p).name != '.env') or`.

### `ast-doctor-80-1423`

**KEEP** — Targets static_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `static_checks`; observed DETECTED; detects 11 cases.

- Line 80: `(Path(p).name.startswith('.env.') and Path(p).name != '.env.example')]` becomes `((Path(p).name.startswith('.env.') or Path(p).name != '.env.example'))]`.

### `ast-doctor-90-1448`

**KEEP** — Targets static_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `static_checks`; observed DETECTED; detects 1 cases.

- Line 90: `'check local environment and Compose syntax privately', warn=self.static and not env.is_file())` becomes `'check local environment and Compose syntax privately', warn=(self.static or not env.is_file()))`.

### `ast-doctor-112-1479`

**KEEP** — Targets inspect through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `inspect`; observed DETECTED; detects 17 cases.

- Line 112: `if any(bindings is not None and (` becomes `if any((bindings is not None or (not isinstance(bindings, list) or any((not isinstance(binding, dict) for binding in bindings))))`.
- Line 113: `not isinstance(bindings, list)` becomes `for bindings in ports.values()):`.
- Line 114: `or any(not isinstance(binding, dict) for binding in bindings))` becomes `return None`.

### `ast-doctor-128-1493`

**KEEP** — Targets runtime_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `runtime_checks`; observed DETECTED; detects 18 cases.

- Line 128: `info = self.inspect(container) if ids.returncode == 0 and re.fullmatch(r'[a-f0-9]{12,64}', container) else None` becomes `info = self.inspect(container) if (ids.returncode != 0) and re.fullmatch(r'[a-f0-9]{12,64}', container) else None`.

### `ast-doctor-141-1553`

**KEEP** — Targets runtime_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `runtime_checks`; observed DETECTED; detects 17 cases.

- Line 141: `self.report(prefix + '-LIMITS', host.get('Memory') == memory and host.get('NanoCpus') == cpus,` becomes `self.report(prefix + '-LIMITS', (host.get('Memory') != memory) and host.get('NanoCpus') == cpus,`.

### `ast-doctor-141-1554`

**KEEP** — Targets runtime_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `runtime_checks`; observed DETECTED; detects 17 cases.

- Line 141: `self.report(prefix + '-LIMITS', host.get('Memory') == memory and host.get('NanoCpus') == cpus,` becomes `self.report(prefix + '-LIMITS', host.get('Memory') == memory and (host.get('NanoCpus') != cpus),`.

### `ast-doctor-144-1563`

**KEEP** — Targets runtime_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `runtime_checks`; observed DETECTED; detects 16 cases.

- Line 144: `self.report(prefix + '-LOGS', log.get('Type') == 'json-file' and log.get('Config', {}).get('max-size') == '10m'` becomes `self.report(prefix + '-LOGS', (log.get('Type') != 'json-file') and log.get('Config', {}).get('max-size') == '10m'`.

### `ast-doctor-144-1564`

**KEEP** — Targets runtime_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `runtime_checks`; observed DETECTED; detects 16 cases.

- Line 144: `self.report(prefix + '-LOGS', log.get('Type') == 'json-file' and log.get('Config', {}).get('max-size') == '10m'` becomes `self.report(prefix + '-LOGS', log.get('Type') == 'json-file' and (log.get('Config', {}).get('max-size') != '10m')`.

### `ast-doctor-145-1565`

**KEEP** — Targets runtime_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `runtime_checks`; observed DETECTED; detects 16 cases.

- Line 145: `and log.get('Config', {}).get('max-file') == '3', 'logs bounded', 'restore 10m / 3 log rotation')` becomes `and (log.get('Config', {}).get('max-file') != '3'), 'logs bounded', 'restore 10m / 3 log rotation')`.

### `ast-doctor-147-1571`

**KEEP** — Targets runtime_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `runtime_checks`; observed DETECTED; detects 13 cases.

- Line 147: `matching = [m for m in mounts if m.get('Destination') == destination]` becomes `matching = [m for m in mounts if (m.get('Destination') != destination)]`.

### `ast-doctor-148-1579`

**KEEP** — Targets runtime_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `runtime_checks`; observed DETECTED; detects 15 cases.

- Line 148: `self.report(prefix + '-VOLUME', bool(project) and len(matching) == 1 and matching[0].get('Type') == 'volume'` becomes `self.report(prefix + '-VOLUME', bool(project) and (len(matching) != 1) and matching[0].get('Type') == 'volume'`.

### `ast-doctor-148-1580`

**KEEP** — Targets runtime_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `runtime_checks`; observed DETECTED; detects 14 cases.

- Line 148: `self.report(prefix + '-VOLUME', bool(project) and len(matching) == 1 and matching[0].get('Type') == 'volume'` becomes `self.report(prefix + '-VOLUME', bool(project) and len(matching) == 1 and (matching[0].get('Type') != 'volume')`.

### `ast-doctor-149-1581`

**KEEP** — Targets runtime_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `runtime_checks`; observed DETECTED; detects 14 cases.

- Line 149: `and matching[0].get('Name') == f'{project}_{service}_data',` becomes `and (matching[0].get('Name') != f'{project}_{service}_data'),`.

### `ast-doctor-152-1591`

**KEEP** — Targets runtime_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `runtime_checks`; observed DETECTED; detects 17 cases.

- Line 152: `self.report(prefix + '-UID', uid.returncode == 0 and uid.stdout.strip() == '999',` becomes `self.report(prefix + '-UID', (uid.returncode != 0) and uid.stdout.strip() == '999',`.

### `ast-doctor-152-1592`

**KEEP** — Targets runtime_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `runtime_checks`; observed DETECTED; detects 18 cases.

- Line 152: `self.report(prefix + '-UID', uid.returncode == 0 and uid.stdout.strip() == '999',` becomes `self.report(prefix + '-UID', uid.returncode == 0 and (uid.stdout.strip() != '999'),`.

### `ast-doctor-160-1612`

**KEEP** — Targets runtime_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `runtime_checks`; observed DETECTED; detects 24 cases.

- Line 160: `self.report('REDIS-' + key.upper(), result.returncode == 0 and result.stdout.splitlines() == [key, value],` becomes `self.report('REDIS-' + key.upper(), (result.returncode != 0) and result.stdout.splitlines() == [key, value],`.

### `ast-doctor-160-1613`

**KEEP** — Targets runtime_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `runtime_checks`; observed DETECTED; detects 24 cases.

- Line 160: `self.report('REDIS-' + key.upper(), result.returncode == 0 and result.stdout.splitlines() == [key, value],` becomes `self.report('REDIS-' + key.upper(), result.returncode == 0 and (result.stdout.splitlines() != [key, value]),`.

### `ast-doctor-177-1671`

**KEEP** — Targets host_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `host_checks`; observed DETECTED; detects 7 cases.

- Line 177: `accepted = positive.returncode == 0 and positive.stdout.strip() == '1'` becomes `accepted = (positive.returncode != 0) and positive.stdout.strip() == '1'`.

### `ast-doctor-177-1672`

**KEEP** — Targets host_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `host_checks`; observed DETECTED; detects 7 cases.

- Line 177: `accepted = positive.returncode == 0 and positive.stdout.strip() == '1'` becomes `accepted = positive.returncode == 0 and (positive.stdout.strip() != '1')`.

### `ast-doctor-178-1675`

**KEEP** — Targets host_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `host_checks`; observed DETECTED; detects 1 cases.

- Line 178: `rejected = negative.returncode != 0 and 'password authentication failed' in negative.stderr.lower()` becomes `rejected = (negative.returncode == 0) and 'password authentication failed' in negative.stderr.lower()`.

### `ast-doctor-180-1684`

**KEEP** — Targets host_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `host_checks`; observed DETECTED; detects 1 cases.

- Line 180: `self.report('HOST-PG-NEGATIVE', accepted and rejected, 'host TCP wrong password explicitly rejected',` becomes `self.report('HOST-PG-NEGATIVE', (accepted or rejected), 'host TCP wrong password explicitly rejected',`.

### `ast-doctor-208-1760`

**KEEP** — Targets postgres_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `postgres_checks`; observed DETECTED; detects 5 cases.

- Line 208: `self.report('PG-CLUSTER', valid and (self.expect_cluster is None or observed == self.expect_cluster),` becomes `self.report('PG-CLUSTER', valid and ((self.expect_cluster is not None) or observed == self.expect_cluster),`.

### `ast-doctor-208-1761`

**KEEP** — Targets postgres_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `postgres_checks`; observed DETECTED; detects 2 cases.

- Line 208: `self.report('PG-CLUSTER', valid and (self.expect_cluster is None or observed == self.expect_cluster),` becomes `self.report('PG-CLUSTER', valid and (self.expect_cluster is None or (observed != self.expect_cluster)),`.

### `ast-doctor-80-1859`

**KEEP** — Targets static_checks through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `static_checks`; observed DETECTED; detects 12 cases.

- Line 80: `(Path(p).name.startswith('.env.') and Path(p).name != '.env.example')]` becomes `(Path(p).name.startswith('.env.') and (Path(p).name == '.env.example'))]`.

### `ast-doctor-112-1907`

**KEEP** — Targets inspect through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `inspect`; observed DETECTED; detects 2 cases.

- Line 112: `if any(bindings is not None and (` becomes `if any((bindings is None) and (`.

### `ast-doctor-113-1908`

**KEEP** — Targets inspect through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/doctor.py`; responsible function: `inspect`; observed DETECTED; detects 1 cases.

- Line 113: `not isinstance(bindings, list)` becomes `(not isinstance(bindings, list) and any((not isinstance(binding, dict) for binding in bindings))))`.
- Line 114: `or any(not isinstance(binding, dict) for binding in bindings))` becomes `for bindings in ports.values()):`.
- Line 115: `for bindings in ports.values()):` becomes `return None`.

### `ast-prd_lint-181-88`

**IMPROVE** — Reversed import/main guard causes CLI parsing before tests. Not a detected implementation fault. Move to explicit CLI-isolation regression; never credit INVALID as effectiveness.

Source: `tools/prd_lint.py`; responsible function: `module entry point`; observed INVALID; detects 0 cases.

- Line 181: `if __name__ == "__main__":` becomes `if (__name__ != '__main__'):`.

### `ast-prd_lint-36-136`

**KEEP** — Targets document_root through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/prd_lint.py`; responsible function: `document_root`; observed DETECTED; detects 1 cases.

- Line 36: `if folder.name == "planning" and folder.parent.name == "docs":` becomes `if (folder.name == 'planning' or folder.parent.name == 'docs'):`.

### `ast-prd_lint-148-212`

**KEEP** — Targets main through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/prd_lint.py`; responsible function: `main`; observed DETECTED; detects 3 cases.

- Line 148: `if folder.name == "docs":` becomes `if (folder.name != 'docs'):`.

### `ast-prd_lint-36-268`

**KEEP** — Targets document_root through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/prd_lint.py`; responsible function: `document_root`; observed DETECTED; detects 2 cases.

- Line 36: `if folder.name == "planning" and folder.parent.name == "docs":` becomes `if (folder.name != 'planning') and folder.parent.name == "docs":`.

### `ast-prd_lint-36-269`

**KEEP** — Targets document_root through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/prd_lint.py`; responsible function: `document_root`; observed DETECTED; detects 1 cases.

- Line 36: `if folder.name == "planning" and folder.parent.name == "docs":` becomes `if folder.name == "planning" and (folder.parent.name != 'docs'):`.

### `ast-prd_lint-53-286`

**KEEP** — Targets local_link_errors through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/prd_lint.py`; responsible function: `local_link_errors`; observed DETECTED; detects 15 cases.

- Line 53: `if fence is not None:` becomes `if (fence is None):`.

### `ast-prd_lint-55-288`

**KEEP** — Targets local_link_errors through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/prd_lint.py`; responsible function: `local_link_errors`; observed DETECTED; detects 1 cases.

- Line 55: `if path.suffix == ".md":` becomes `if (path.suffix != '.md'):`.

### `ast-prd_lint-154-425`

**KEEP** — Targets main through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/prd_lint.py`; responsible function: `main`; observed DETECTED; detects 1 cases.

- Line 154: `if len(v) > 1:` becomes `if (len(v) <= 1):`.

### `ast-prd_lint-157-431`

**KEEP** — Targets main through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/prd_lint.py`; responsible function: `main`; observed DETECTED; detects 2 cases.

- Line 157: `if len(v) > 1:` becomes `if (len(v) <= 1):`.

### `ast-prd_lint-162-438`

**KEEP** — Targets main through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/prd_lint.py`; responsible function: `main`; observed DETECTED; detects 2 cases.

- Line 162: `if missing and len(days) > 5:` becomes `if (missing or len(days) > 5):`.

### `ast-prd_lint-46-491`

**KEEP** — Targets local_link_errors through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/prd_lint.py`; responsible function: `local_link_errors`; observed DETECTED; detects 7 cases.

- Line 46: `marker = re.match(r"^\s*(\`{3,}|~{3,})(.*)$", line) if path.suffix == ".md" else None` becomes `marker = re.match(r"^\s*(\`{3,}|~{3,})(.*)$", line) if (path.suffix != '.md') else None`.

### `ast-prd_lint-48-495`

**KEEP** — Targets local_link_errors through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/prd_lint.py`; responsible function: `local_link_errors`; observed DETECTED; detects 13 cases.

- Line 48: `if fence is None:` becomes `if (fence is not None):`.

### `ast-prd_lint-65-524`

**KEEP** — Targets local_link_errors through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/prd_lint.py`; responsible function: `local_link_errors`; observed DETECTED; detects 1 cases.

- Line 65: `if parsed.scheme or parsed.netloc or not parsed.path:` becomes `if (parsed.scheme and parsed.netloc and (not parsed.path)):`.

### `ast-prd_lint-94-550`

**KEEP** — Targets lint_file through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/prd_lint.py`; responsible function: `lint_file`; observed DETECTED; detects 1 cases.

- Line 94: `if SPRINT_PART.match(path.name) and re.match(r"^DAY\s+\d+", line, re.I):` becomes `if (SPRINT_PART.match(path.name) or re.match('^DAY\\s+\\d+', line, re.I)):`.

### `ast-prd_lint-108-568`

**KEEP** — Targets lint_file through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/prd_lint.py`; responsible function: `lint_file`; observed DETECTED; detects 1 cases.

- Line 108: `if kid and h.group(2).lower().startswith(("sk-", "skill")):` becomes `if (kid or h.group(2).lower().startswith(('sk-', 'skill'))):`.

### `ast-prd_lint-120-593`

**KEEP** — Targets lint_file through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/prd_lint.py`; responsible function: `lint_file`; observed DETECTED; detects 1 cases.

- Line 120: `if lvl <= level:` becomes `if (lvl > level):`.

### `ast-prd_lint-162-690`

**KEEP** — Targets main through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/prd_lint.py`; responsible function: `main`; observed DETECTED; detects 2 cases.

- Line 162: `if missing and len(days) > 5:` becomes `if missing and (len(days) <= 5):`.

### `ast-prd_lint-50-752`

**KEEP** — Targets local_link_errors through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/prd_lint.py`; responsible function: `local_link_errors`; observed DETECTED; detects 2 cases.

- Line 50: `elif marker.group(1)[0] == fence[0] and len(marker.group(1)) >= len(fence) and not marker.group(2).strip():` becomes `elif (marker.group(1)[0] == fence[0] or len(marker.group(1)) >= len(fence) or (not marker.group(2).strip())):`.

### `ast-prd_lint-85-801`

**KEEP** — Targets lint_file through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/prd_lint.py`; responsible function: `lint_file`; observed DETECTED; detects 2 cases.

- Line 85: `elif m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence) and not m.group(2).strip():` becomes `elif (m.group(1)[0] == fence[0] or len(m.group(1)) >= len(fence) or (not m.group(2).strip())):`.

### `ast-prd_lint-111-834`

**KEEP** — Targets lint_file through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/prd_lint.py`; responsible function: `lint_file`; observed DETECTED; detects 1 cases.

- Line 111: `d = DAY_ENTRY.match(h.group(2)) if SPRINT_PART.match(path.name) and len(h.group(1)) == 2 else None` becomes `d = DAY_ENTRY.match(h.group(2)) if (SPRINT_PART.match(path.name) or len(h.group(1)) == 2) else None`.

### `ast-prd_lint-161-927`

**KEEP** — Targets main through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/prd_lint.py`; responsible function: `main`; observed DETECTED; detects 5 cases.

- Line 161: `dupes = {d: v for d, v in days.items() if len(v) > 1}` becomes `dupes = {d: v for d, v in days.items() if (len(v) <= 1)}`.

### `ast-prd_lint-50-979`

**KEEP** — Targets local_link_errors through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/prd_lint.py`; responsible function: `local_link_errors`; observed DETECTED; detects 3 cases.

- Line 50: `elif marker.group(1)[0] == fence[0] and len(marker.group(1)) >= len(fence) and not marker.group(2).strip():` becomes `elif (marker.group(1)[0] != fence[0]) and len(marker.group(1)) >= len(fence) and not marker.group(2).strip():`.

### `ast-prd_lint-50-980`

**KEEP** — Targets local_link_errors through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/prd_lint.py`; responsible function: `local_link_errors`; observed DETECTED; detects 2 cases.

- Line 50: `elif marker.group(1)[0] == fence[0] and len(marker.group(1)) >= len(fence) and not marker.group(2).strip():` becomes `elif marker.group(1)[0] == fence[0] and (len(marker.group(1)) < len(fence)) and not marker.group(2).strip():`.

### `ast-prd_lint-85-1027`

**KEEP** — Targets lint_file through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/prd_lint.py`; responsible function: `lint_file`; observed DETECTED; detects 7 cases.

- Line 85: `elif m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence) and not m.group(2).strip():` becomes `elif (m.group(1)[0] != fence[0]) and len(m.group(1)) >= len(fence) and not m.group(2).strip():`.

### `ast-prd_lint-85-1028`

**KEEP** — Targets lint_file through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/prd_lint.py`; responsible function: `lint_file`; observed DETECTED; detects 7 cases.

- Line 85: `elif m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence) and not m.group(2).strip():` becomes `elif m.group(1)[0] == fence[0] and (len(m.group(1)) < len(fence)) and not m.group(2).strip():`.

### `ast-prd_lint-87-1032`

**KEEP** — Targets lint_file through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/prd_lint.py`; responsible function: `lint_file`; observed DETECTED; detects 1 cases.

- Line 87: `if lang in CODE_LANGS and n > MAX_CODE_LINES:` becomes `if (lang in CODE_LANGS or n > MAX_CODE_LINES):`.

### `ast-prd_lint-111-1079`

**KEEP** — Targets lint_file through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/prd_lint.py`; responsible function: `lint_file`; observed DETECTED; detects 2 cases.

- Line 111: `d = DAY_ENTRY.match(h.group(2)) if SPRINT_PART.match(path.name) and len(h.group(1)) == 2 else None` becomes `d = DAY_ENTRY.match(h.group(2)) if SPRINT_PART.match(path.name) and (len(h.group(1)) != 2) else None`.

### `ast-prd_lint-87-1260`

**KEEP** — Targets lint_file through the concrete changed condition/statement below. Existing detections establish a sensitive oracle; keep for this operational/planning contract, not as application-domain security proof.

Source: `tools/prd_lint.py`; responsible function: `lint_file`; observed DETECTED; detects 8 cases.

- Line 87: `if lang in CODE_LANGS and n > MAX_CODE_LINES:` becomes `if lang in CODE_LANGS and (n <= MAX_CODE_LINES):`.

📚 Learn first: [Existing case-level evidence](../case-effectiveness-evidence/python-cases.md).
↩ Return: inspect the full JSON for exact fixture/functions and detection IDs; approve reductions by preserved requirements, not raw mutation percentages.
