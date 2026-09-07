#!/usr/bin/env python3
"""Fail speaker PRs that touch files outside speakers/<github-handle>/."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

PROTECTED_EVENT_FILES = {
    "readme.md",
    "agenda.md",
    "recap.md",
    "contributors.md",
    "event.yml",
}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def posix(path: str) -> str:
    return path.replace("\\", "/").strip()


def speaker_handle(path: str) -> str | None:
    parts = posix(path).split("/")
    try:
        index = parts.index("speakers")
    except ValueError:
        return None
    if index + 1 >= len(parts):
        return None
    handle = parts[index + 1]
    if handle.startswith(".") or handle.lower() == "readme.md":
        return None
    return handle


def is_speakers_path(path: str) -> bool:
    return "speakers" in posix(path).split("/")


def codeowners_handles(path: Path) -> set[str]:
    handles: set[str] = set()
    if not path.is_file():
        return handles
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.split("#", 1)[0].strip()
        if not stripped:
            continue
        for token in stripped.split():
            if token.startswith("@"):
                handles.add(token[1:].split("/", 1)[-1].lower())
    return handles


def parse_labels(raw: str) -> set[str]:
    return {item.strip().lower() for item in raw.split(",") if item.strip()}


def validate(actor: str, files: list[str], labels: set[str], maintainers: set[str]) -> list[str]:
    actor_l = actor.lower()
    if "organizer" in labels or actor_l in maintainers:
        return []

    changed = [posix(path) for path in files if posix(path)]
    if not changed:
        return []

    speaker_changes = [path for path in changed if is_speakers_path(path)]
    if not speaker_changes:
        return []

    errors: list[str] = []
    for path in changed:
        handle = speaker_handle(path)
        if handle is None or handle.lower() != actor_l:
            errors.append(
                f"`{path}` is outside `speakers/{actor}/**`. "
                "Speaker PRs may only modify that folder."
            )
            continue
        name = Path(path).name.lower()
        if name in PROTECTED_EVENT_FILES and "speakers/" not in posix(path).lower():
            errors.append(f"`{path}` is a shared event file and cannot be changed in a speaker PR.")

    if errors:
        errors.append(
            "Speakers must not modify README.md, agenda.md, recap.md, contributors.md, "
            "event.yml, or peer speaker folders. Organizers should label the PR `organizer`."
        )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--actor", required=True)
    parser.add_argument("--files", help="Newline-separated changed paths")
    parser.add_argument("--files-from", type=Path, help="File containing newline-separated changed paths")
    parser.add_argument("--labels", default="")
    parser.add_argument("--codeowners", type=Path, default=repo_root() / ".github" / "CODEOWNERS")
    args = parser.parse_args()

    raw_files = args.files or ""
    if args.files_from is not None:
        raw_files = args.files_from.read_text(encoding="utf-8")
    files = [line.strip() for line in raw_files.splitlines() if line.strip()]
    labels = parse_labels(args.labels)
    maintainers = codeowners_handles(args.codeowners)

    errors = validate(args.actor, files, labels, maintainers)
    if errors:
        print("Speaker PR contract failed:\n", file=sys.stderr)
        for error in errors:
            print(f" - {error}", file=sys.stderr)
        return 1

    print("Speaker PR contract passed.")
    return 0


if __name__ == "__main__":
    os.chdir(repo_root())
    raise SystemExit(main())
