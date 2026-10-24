"""Conservative Python fault scope: retain every baseline case and dependent test.

Unknown targets, dynamic imports, opaque subprocesses and uncertain fixture
configuration fall back to the full Python collection. This never caches results
or removes a fault. MERLIN_PYTHON_FAULT_SCOPE=all preserves the all-pairs audit.
"""
import ast
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# Changed or new test modules use every fault until their scope is reviewed.
REVIEWED_TESTS = {'tests/test_note_rules_and_maintenance.py': '0a3dcf4b2e7c9b07e93d9e33f25d444b3b4b309f7020d075840617c28a6fa4ef', 'tests/test_database_connectivity_probe.py': 'ba296ed12baab295aea9b44c5915a88082fe163968ea9a2596ac82ca380a3063', 'tests/test_prd_lint.py': '04a66d2ac906235b4bd727b6fb87ce475dd2f6ba51c5ba910b2c945996082344', 'tests/test_doctor_failure_cases.py': '6c8c06d6285fe2950912692838ae692763b5c28f4e9454f83af4b200a3c8df97', 'tools/test_doctor.py': '25522e95c32b8ceea080984ee800b2b8a82c3a0c169cac52e9732c0fce3d44b7'}
# Reviewed API subprocess imports only the two explicitly imported API modules.
REVIEWED_TESTS['tests/test_health_api.py'] = '3dc8727b03097a757a26b7f5981f3e678caf50a867e0ddc2ef8c08d2c71f0b9a'
REVIEWED_TESTS['tests/test_local_provider.py'] = 'fe78680b5ef16bf94579870023cd93440e11c6f95c5f87fee6e6479da06cc56a'
REVIEWED_TESTS['tests/test_notes_repository.py'] = 'f9edec997747c8d6a8c20514bbe92dae5faf72ae71f8c9d82ef9c156e85bcbec'
# Reviewed doctor launches setup clients only; changing it restores full scope.
REVIEWED_DOCTOR = '4cf276effb197aad39ce94f652e01a558ca39ad3bbebe8af5ce9ce4693fae26f'
TARGETS = {'app/local_provider.py', 'app/health_api.py', 'app/health_server.py', 'tests/test_health_api.py',
           'app/note_rules.py', 'app/notes_maintenance.py',
           'app/notes_repository.py',
           'app/database_connectivity_probe.py', 'tools/doctor.py', 'tools/prd_lint.py'}


def resolve(name):
    if name == 'doctor':
        name = 'tools.doctor'
    base = ROOT.joinpath(*name.split('.'))
    for candidate in [base.with_suffix('.py'), base / '__init__.py']:
        if candidate.is_file():
            return candidate.relative_to(ROOT).as_posix()
    return None


def dependencies(file, visited=None):
    visited = set() if visited is None else visited
    if file in visited:
        return visited, False
    visited.add(file)
    tree = ast.parse((ROOT / file).read_text())
    uncertain = False
    package = file.split('/')[:-1]
    imports = set()
    aliases = {}
    subprocess_calls = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name for alias in node.names)
            aliases.update({alias.asname or alias.name.split('.')[0]: alias.name for alias in node.names})
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                if node.level > len(package):
                    uncertain = True
                    continue
                parent = package[:len(package) - node.level + 1]
                prefix = '.'.join(parent + ([node.module] if node.module else []))
            else:
                prefix = node.module or ''
            aliases.update({alias.asname or alias.name: prefix + '.' + alias.name for alias in node.names})
            imports.add(prefix)
            imports.update(prefix + '.' + alias.name for alias in node.names)
        elif isinstance(node, ast.Call):
            function = ast.unparse(node.func)
            if function in {'__import__', 'eval', 'exec'} or any(
                    name in function for name in ['import_module', 'run_path', 'run_module', 'spec_from_file_location']):
                uncertain = True
            first, separator, remainder = function.partition('.')
            canonical = aliases.get(first, first) + (separator + remainder if separator else '')
            if canonical in {'subprocess.run', 'subprocess.Popen', 'subprocess.call',
                             'subprocess.check_call', 'subprocess.check_output',
                             'subprocess.getoutput', 'subprocess.getstatusoutput'}:
                subprocess_calls.append(node)
        elif isinstance(node, ast.Name) and node.id == 'pytest_plugins':
            uncertain = True
    if subprocess_calls:
        # This reviewed helper invokes only the project's linter. A changed or
        # additional subprocess call automatically makes this module uncertain.
        allowed = file == 'tests/test_prd_lint.py' and len(subprocess_calls) == 1
        call = subprocess_calls[0]
        allowed = allowed and ast.unparse(call.func) == 'subprocess.run' and bool(call.args)
        allowed = allowed and ast.unparse(call.args[0]) == '[sys.executable, str(LINTER), str(folder)]'
        definitions = [node for node in ast.walk(tree) if isinstance(node, ast.Assign)
                       and any(isinstance(target, ast.Name) and target.id=='LINTER' for target in node.targets)]
        expected = "Path(__file__).resolve().parents[1] / 'tools' / 'prd_lint.py'"
        allowed = allowed and len(definitions)==1 and ast.unparse(definitions[0].value)==expected
        if (file == 'tests/test_health_api.py' and len(subprocess_calls) == 1
                and hashlib.sha256((ROOT / file).read_bytes()).hexdigest() == REVIEWED_TESTS.get(file)
                and ast.unparse(call.func) == 'subprocess.run'
                and call.args and ast.unparse(call.args[0]) == "[sys.executable, '-c', script]"):
            allowed = True
        if file == 'tools/doctor.py' and hashlib.sha256((ROOT / file).read_bytes()).hexdigest() == REVIEWED_DOCTOR:
            allowed = True
        if not allowed:
            uncertain = True
    for name in imports:
        local = resolve(name)
        if local:
            _, opaque = dependencies(local, visited)
            uncertain |= opaque
    return visited, uncertain


def scopes(baseline):
    files = sorted({row['file'] for row in baseline['cases'].values()})
    fixtures = list(ROOT.glob('tests/**/conftest.py'))
    if fixtures:
        # Shared fixture effects require explicit proof before narrowing scope.
        return {target: files for target in TARGETS}
    graph = {file: dependencies(file) for file in files}
    unreviewed = {file for file in files if hashlib.sha256((ROOT / file).read_bytes()).hexdigest()
                  != REVIEWED_TESTS.get(file)}
    result = {}
    for target in TARGETS:
        selected = [file for file, (edges, uncertain) in graph.items() if target in edges or uncertain or file in unreviewed]
        result[target] = selected or files
    return result
