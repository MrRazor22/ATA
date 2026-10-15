"""PFD Skill Sync — installs and syncs the PFD skill triad with Antigravity.

Usage:
  python sync-pfd.py install     Install skills from this repo into Antigravity (~/.gemini/config/skills)
  python sync-pfd.py update-repo Pull live skills from Antigravity into this repo (for committing)
  python sync-pfd.py check       Check if repo and Antigravity skills are in sync
"""

from pathlib import Path
import hashlib, shutil, sys

SKILLS = ("pfd", "pfd-audit", "pfd-iterate")

def antigravity_dir() -> Path:
    return Path.home() / ".gemini" / "config" / "skills"

def repo_skills_dir(repo: Path) -> Path:
    return repo / "skills"

def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else ""

def sync_tree(src: Path, dst: Path, check_only: bool) -> bool:
    if not src.exists():
        print(f"  [SKIP] Source directory missing: {src}")
        return True

    dst.mkdir(parents=True, exist_ok=True)
    in_sync = True

    # Check/copy files from source to destination
    for src_file in sorted(src.rglob("*")):
        if not src_file.is_file():
            continue
        rel = src_file.relative_to(src)
        dst_file = dst / rel

        if file_hash(src_file) != file_hash(dst_file):
            in_sync = False
            if check_only:
                status = "NEW" if not dst_file.exists() else "CHANGED"
                print(f"  [{status}] {rel}")
            else:
                dst_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_file, dst_file)
                print(f"  [SYNCED] {rel}")

    # Remove extra files in destination that no longer exist in source (when not check_only)
    for dst_file in sorted(dst.rglob("*")):
        if not dst_file.is_file():
            continue
        rel = dst_file.relative_to(dst)
        if not (src / rel).exists():
            in_sync = False
            if check_only:
                print(f"  [REMOVED IN SOURCE] {rel}")
            else:
                dst_file.unlink()
                print(f"  [DELETED] {rel}")

    if in_sync:
        print("  [OK] In sync")
    return in_sync

def main():
    repo = Path(__file__).resolve().parent.parent
    cmd = sys.argv[1].lower() if len(sys.argv) > 1 else "install"

    if cmd in ("-h", "--help", "help"):
        print(__doc__.strip())
        return 0

    agy_dir = antigravity_dir()
    repo_dir = repo_skills_dir(repo)

    if cmd in ("install", "publish"):
        print(f"Installing PFD skills: repo -> Antigravity ({agy_dir})\n")
        src_root, dst_root = repo_dir, agy_dir
        check_only = False
    elif cmd in ("update-repo", "export", "pull"):
        print(f"Updating repo skills: Antigravity ({agy_dir}) -> repo\n")
        src_root, dst_root = agy_dir, repo_dir
        check_only = False
    elif cmd in ("check", "status", "diff"):
        print(f"Checking sync status: repo <-> Antigravity ({agy_dir})\n")
        src_root, dst_root = repo_dir, agy_dir
        check_only = True
    else:
        print(f"Unknown command: '{cmd}'. Use 'install', 'update-repo', or 'check'.")
        return 1

    all_synced = True
    for name in SKILLS:
        print(f"  [{name}]")
        synced = sync_tree(src_root / name, dst_root / name, check_only)
        all_synced = all_synced and synced
        print()

    if check_only:
        print("All skills in sync." if all_synced else "Skills mismatch detected. Run 'install' or 'update-repo'.")
    else:
        print("Operation completed successfully.")

    return 0 if all_synced or not check_only else 1

if __name__ == "__main__":
    sys.exit(main())
