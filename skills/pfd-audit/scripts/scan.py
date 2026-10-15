"""PFD Mechanical Violation Scanner — scans source files for automatable PFD rule violations."""

from dataclasses import dataclass, field
from pathlib import Path
import re, sys

# ── Data ──────────────────────────────────────────────────────────────────────

@dataclass
class Violation:
    rule: int
    path: str
    line: int
    message: str

@dataclass
class FileMetrics:
    path: str
    lines: int
    private_methods: int = 0
    interfaces: dict[str, int] = field(default_factory=dict)  # name → method count

@dataclass
class ScanResult:
    files_scanned: int = 0
    total_lines: int = 0
    previous_lines: int | None = None
    violations: list[Violation] = field(default_factory=list)
    metrics: list[FileMetrics] = field(default_factory=list)

# ── Configuration (cross-language patterns — the "policies") ──────────────────

EXTENSIONS = {'.cs', '.py', '.rs', '.ts', '.tsx', '.go', '.java', '.kt', '.cpp', '.hpp', '.h', '.swift', '.dart'}
SKIP = {'bin', 'obj', 'node_modules', '.git', '.vs', '__pycache__', 'target', 'dist', '.idea', 'build', 'out'}
BANNED = {'manager', 'service', 'helper', 'utils', 'common', 'utility', 'components', 'helpers',
          'services', 'managers', 'base', 'impl', 'dto', 'dtos', 'models', 'types', 'contract',
          'contracts', 'schema', 'interface', 'factories'}

PRIVATE_METHOD = [
    re.compile(r'^\s*private\s+(?!class|struct|enum|interface|record).*\w+\s*\('),  # C#/Java/Kotlin
    re.compile(r'^\s*def\s+_[^_]\w*\s*\('),                                         # Python _method
    re.compile(r'^\s*fn\s+_[^_]'),                                                   # Rust convention
]
UNTYPED = [
    re.compile(r'[:(]\s*Any\b'),             re.compile(r'->\s*Any\b'),              # Python/Swift
    re.compile(r'[:(]\s*any\b'),             re.compile(r'=>\s*any\b'),              # TypeScript
    re.compile(r'[:(]\s*object\b'),          re.compile(r'->\s*object\b'),           # C# param/return
    re.compile(r'\bdynamic\b'),                                                      # C#/Dart
    re.compile(r'\binterface\s*\{\s*\}'),                                            # Go empty
    re.compile(r'\bvoid\s*\*'),                                                      # C/C++
    re.compile(r'[Dd]ict\[str,\s*Any\]'),                                            # Python dict[str, Any]
]
CALLBACK = [
    re.compile(r'\b(?:Action|Func|EventHandler)\s*[<(]'),                            # C# delegates
    re.compile(r'\bdelegate\b'),             re.compile(r'\bevent\s+\w'),            # C# delegate/event
    re.compile(r'\bCallable\b'),             re.compile(r'callback\s*[:(]', re.I),   # General
]
UTILITY_CLASS = [re.compile(r'static\s+class\s+\w*(Utils|Helper|Common|Utility)', re.I)]
INTERFACE_DECL = [
    re.compile(r'^\s*(?:public\s+)?interface\s+(\w+)'),                              # C#/Java/TS/Kotlin/Go
    re.compile(r'^\s*(?:pub\s+)?trait\s+(\w+)'),                                     # Rust
    re.compile(r'^\s*class\s+(\w+)\s*\(\s*(?:Protocol|ABC)\s*\)'),                   # Python
    re.compile(r'^\s*protocol\s+(\w+)'),                                             # Swift
]
COMMENT = re.compile(r'^\s*(//|#|\*|/\*|"""|\'\'\')')

# ── Scanning ──────────────────────────────────────────────────────────────────

def should_skip(path: Path, root: Path) -> bool:
    return any(p in SKIP or p.startswith('.') for p in path.relative_to(root).parts)

def scan_names(root: Path) -> list[Violation]:
    violations = []
    for p in root.rglob('*'):
        if should_skip(p, root): continue
        name = (p.stem if p.is_file() else p.name).lower()
        if name not in BANNED: continue
        rel = str(p.relative_to(root))
        kind = "directory" if p.is_dir() else "file"
        violations.append(Violation(36, rel, 0, f"Banned meta-name {kind}: '{p.name}'"))
    return violations

def match_any(line: str, patterns: list[re.Pattern]) -> bool:
    return any(p.search(line) for p in patterns)

def scan_file(path: Path, root: Path) -> tuple[FileMetrics, list[Violation]]:
    try: lines = path.read_text(encoding='utf-8', errors='replace').splitlines()
    except Exception: return FileMetrics(str(path.relative_to(root)), 0), []

    rel = str(path.relative_to(root))
    violations: list[Violation] = []
    metrics = FileMetrics(rel, len(lines))
    current_iface, brace_depth, iface_depth = None, 0, 0

    if len(lines) > 150:
        violations.append(Violation(11, rel, 0, f"{len(lines)} lines (limit: ~150)"))

    is_py = path.suffix == '.py'
    iface_indent = 0

    for i, line in enumerate(lines, 1):
        if COMMENT.match(line) or not line.strip(): continue

        indent = len(line) - len(line.lstrip())

        # Track interface declarations and count their methods
        for pat in INTERFACE_DECL:
            m = pat.match(line)
            if m:
                current_iface, iface_depth, iface_indent = m.group(1), brace_depth, indent
                metrics.interfaces[current_iface] = 0
                break

        brace_depth += line.count('{') - line.count('}')

        if current_iface:
            if is_py:
                if indent <= iface_indent and not any(pat.match(line) for pat in INTERFACE_DECL):
                    current_iface = None
                elif re.match(r'^\s+def\s+\w+', line):
                    metrics.interfaces[current_iface] += 1
            else:
                if brace_depth <= iface_depth and '}' in line:
                    current_iface = None
                elif re.match(r'^\s+\w.*\(.*\)', line) and '{' not in line:
                    metrics.interfaces[current_iface] += 1

        # Skip imports for pattern checks
        if line.strip().startswith(('import ', 'from ')):
            continue

        # Pattern violations (one check per line, first match wins to avoid noise)
        if match_any(line, PRIVATE_METHOD):
            metrics.private_methods += 1
            violations.append(Violation(13, rel, i, f"Private method: {line.strip()[:80]}"))
        elif match_any(line, UNTYPED):
            violations.append(Violation(4, rel, i, f"Untyped escape hatch: {line.strip()[:80]}"))
        elif match_any(line, CALLBACK):
            violations.append(Violation(6, rel, i, f"Callback/delegate/hook: {line.strip()[:80]}"))
        elif match_any(line, UTILITY_CLASS):
            violations.append(Violation(20, rel, i, f"Static utility class: {line.strip()[:80]}"))

    for iface, count in metrics.interfaces.items():
        if count > 5:
            violations.append(Violation(2, rel, 0, f"Interface '{iface}' has {count} methods (limit: 4-5)"))

    return metrics, violations

def scan(root: Path) -> ScanResult:
    result = ScanResult()
    result.violations.extend(scan_names(root))
    for path in sorted(root.rglob('*')):
        if not path.is_file() or path.suffix not in EXTENSIONS or should_skip(path, root): continue
        metrics, violations = scan_file(path, root)
        result.files_scanned += 1
        result.total_lines += metrics.lines
        result.metrics.append(metrics)
        result.violations.extend(violations)
    return result

# ── Reporting ─────────────────────────────────────────────────────────────────

def report(result: ScanResult, root: Path):
    print(f"\n{'='*60}")
    print(f"  PFD MECHANICAL SCAN — {root}")
    print(f"{'='*60}")
    print(f"  Files: {result.files_scanned}  |  Total LOC: {result.total_lines}")
    if result.previous_lines is not None:
        delta = result.total_lines - result.previous_lines
        sym = "[+]" if delta > 0 else ("[-]" if delta < 0 else "[=]")
        print(f"  Previous: {result.previous_lines}  |  Delta: {sym} {abs(delta)} lines")
        if delta > 0: print(f"  !! CODE ECONOMY VIOLATION: Lines went UP -- PFD not correctly applied")

    print(f"\n{'-'*60}\n  FILE LINE COUNTS\n{'-'*60}")
    for m in sorted(result.metrics, key=lambda x: x.lines, reverse=True):
        flag = " <- OVER" if m.lines > 150 else ""
        print(f"  {m.lines:>4} | {m.path}{flag}")

    ifaces = [(m.path, n, c) for m in result.metrics for n, c in m.interfaces.items()]
    if ifaces:
        print(f"\n{'-'*60}\n  INTERFACE METHOD COUNTS\n{'-'*60}")
        for path, name, count in sorted(ifaces, key=lambda x: x[2], reverse=True):
            flag = " <- OVER" if count > 5 else ""
            print(f"  {count:>2} methods | {name} ({path}){flag}")

    privates = [(m.path, m.private_methods) for m in result.metrics if m.private_methods > 0]
    if privates:
        print(f"\n{'-'*60}\n  PRIVATE METHOD COUNTS\n{'-'*60}")
        for path, count in sorted(privates, key=lambda x: x[1], reverse=True):
            print(f"  {count:>2} private | {path}")

    if not result.violations:
        print(f"\n  CLEAN -- Zero mechanical violations.\n")
        return

    grouped: dict[int, list[Violation]] = {}
    for v in result.violations: grouped.setdefault(v.rule, []).append(v)
    print(f"\n{'-'*60}\n  VIOLATIONS ({len(result.violations)} total)\n{'-'*60}")
    for rule in sorted(grouped):
        items = grouped[rule]
        print(f"\n  Rule {rule} -- {len(items)} violation(s):")
        for v in items:
            loc = f":{v.line}" if v.line > 0 else ""
            print(f"    {v.path}{loc} -- {v.message}")
    print(f"\n  FAILED: {len(result.violations)} violation(s) across {len(grouped)} rule(s)\n")

# ── Entry ─────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python scan.py <path> [previous_line_count]")
        sys.exit(1)
    root = Path(sys.argv[1]).resolve()
    if not root.is_dir():
        print(f"Error: '{root}' is not a directory"); sys.exit(1)
    result = scan(root)
    if len(sys.argv) >= 3:
        try: result.previous_lines = int(sys.argv[2])
        except ValueError: pass
    report(result, root)
    sys.exit(1 if result.violations else 0)
