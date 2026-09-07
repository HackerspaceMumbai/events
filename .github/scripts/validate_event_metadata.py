#!/usr/bin/env python3
"""Validate events/**/event.yml against the archive contract."""

from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import sys
from pathlib import Path
from typing import Any

import yaml

VALID_EVENT_TYPES = {
    "meetup",
    "workshop",
    "conference",
    "hackathon",
    "community-day",
    "series",
    "summit",
}

REQUIRED_FIELDS = (
    "title",
    "slug",
    "date",
    "city",
    "country",
    "eventType",
    "series",
    "community",
    "venue",
    "website",
    "eventPage",
    "resourcesAvailable",
)

OPTIONAL_STATUS = {"upcoming", "completed", "cancelled"}

SINGLE_FOLDER = re.compile(r"^(\d{4}-\d{2}-\d{2})-([a-z0-9]+(?:-[a-z0-9]+)*)$")
SERIES_FOLDER = re.compile(r"^(\d{4}-\d{2})-([a-z0-9]+(?:-[a-z0-9]+)*)$")
STOP_FOLDER = re.compile(r"^stop-\d{2}-([a-z0-9]+(?:-[a-z0-9]+)*)$")
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
TIME = re.compile(r"^\d{2}:\d{2}$")
MAX_BYTES = 25 * 1024 * 1024


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def load_yaml(path: Path) -> tuple[Any | None, str | None]:
    try:
        with path.open(encoding="utf-8") as handle:
            data = yaml.safe_load(handle)
    except yaml.YAMLError as exc:
        return None, f"invalid YAML: {exc}"
    return data, None


def parse_date(value: object) -> str | None:
    if isinstance(value, dt.date) and not isinstance(value, dt.datetime):
        return value.isoformat()
    if isinstance(value, dt.datetime):
        return value.date().isoformat()
    if isinstance(value, str) and DATE.match(value):
        try:
            dt.date.fromisoformat(value)
            return value
        except ValueError:
            return None
    return None


def is_nonempty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def looks_like_uri(value: object) -> bool:
    return isinstance(value, str) and value.startswith(("http://", "https://"))


def folder_kind(name: str) -> str:
    if STOP_FOLDER.match(name):
        return "stop"
    if SINGLE_FOLDER.match(name):
        return "single"
    if SERIES_FOLDER.match(name):
        return "series"
    return "unknown"


def validate_event(path: Path, events_root: Path) -> list[str]:
    errors: list[str] = []
    data, yaml_error = load_yaml(path)
    rel = path.as_posix()
    if yaml_error:
        return [f"{rel}: {yaml_error}"]
    if not isinstance(data, dict):
        return [f"{rel}: root must be a mapping"]

    for field in REQUIRED_FIELDS:
        if field not in data:
            errors.append(f"{rel}: missing required field `{field}`")
        elif field != "series" and data[field] is None:
            errors.append(f"{rel}: missing required field `{field}`")

    for field in ("title", "city", "country", "community", "venue"):
        if field in data and data[field] is not None and not is_nonempty_string(data[field]):
            errors.append(f"{rel}: `{field}` must be a non-empty string")

    slug = data.get("slug")
    if slug is not None and not (isinstance(slug, str) and SLUG.match(slug)):
        errors.append(f"{rel}: `slug` must be kebab-case")

    event_date = parse_date(data.get("date")) if "date" in data else None
    if "date" in data and data["date"] is not None and event_date is None:
        errors.append(f"{rel}: `date` must be YYYY-MM-DD")

    event_type = data.get("eventType")
    if event_type is not None and event_type not in VALID_EVENT_TYPES:
        errors.append(
            f"{rel}: unknown eventType `{event_type}`. "
            f"Valid types: {', '.join(sorted(VALID_EVENT_TYPES))}"
        )

    series = data.get("series")
    if series is not None and series != "" and not isinstance(series, str):
        errors.append(f"{rel}: `series` must be a string or null")

    if "resourcesAvailable" in data and data["resourcesAvailable"] is not None:
        if not isinstance(data["resourcesAvailable"], bool):
            errors.append(f"{rel}: `resourcesAvailable` must be a boolean")

    for uri_field in ("website", "eventPage", "gallery"):
        if uri_field in data and data[uri_field] not in (None, "") and not looks_like_uri(
            data[uri_field]
        ):
            errors.append(f"{rel}: `{uri_field}` must be an http(s) URL")

    if "status" in data and data["status"] is not None:
        if data["status"] not in OPTIONAL_STATUS:
            errors.append(f"{rel}: `status` must be one of {sorted(OPTIONAL_STATUS)}")

    if "endDate" in data and data["endDate"] is not None:
        if parse_date(data["endDate"]) is None:
            errors.append(f"{rel}: `endDate` must be YYYY-MM-DD")

    if "startTime" in data and data["startTime"] is not None:
        if not (isinstance(data["startTime"], str) and TIME.match(data["startTime"])):
            errors.append(f"{rel}: `startTime` must be HH:MM")

    if "hashtags" in data and data["hashtags"] is not None:
        if not isinstance(data["hashtags"], list) or not all(
            is_nonempty_string(item) for item in data["hashtags"]
        ):
            errors.append(f"{rel}: `hashtags` must be a list of strings")

    try:
        relative = path.parent.relative_to(events_root)
    except ValueError:
        errors.append(f"{rel}: event.yml must live under events/")
        return errors

    parts = relative.parts
    if len(parts) < 2:
        errors.append(f"{rel}: expected events/YYYY/<event-folder>/event.yml")
        return errors

    year_dir, event_folder = parts[0], parts[1]
    kind = folder_kind(event_folder)
    is_stop = len(parts) >= 3 and folder_kind(parts[-1]) == "stop"

    if not year_dir.isdigit() or len(year_dir) != 4:
        errors.append(f"{rel}: year folder `{year_dir}` must be YYYY")

    if is_stop:
        return errors

    if event_type == "series":
        if kind != "series":
            errors.append(
                f"{rel}: series events must use folder `YYYY-MM-slug`, found `{event_folder}`"
            )
        match = SERIES_FOLDER.match(event_folder)
        if match and slug and match.group(2) != slug:
            errors.append(
                f"{rel}: folder slug `{match.group(2)}` does not match metadata slug `{slug}`"
            )
        if match and event_date and not event_date.startswith(match.group(1)):
            errors.append(
                f"{rel}: date `{event_date}` does not match series folder month `{match.group(1)}`"
            )
        if match and year_dir != match.group(1).split("-")[0]:
            errors.append(f"{rel}: year folder `{year_dir}` does not match series folder")
        return errors

    if kind != "single":
        errors.append(
            f"{rel}: expected folder `YYYY-MM-DD-slug` for non-series events, found `{event_folder}`"
        )
        return errors

    match = SINGLE_FOLDER.match(event_folder)
    if not match:
        return errors
    folder_date, folder_slug = match.group(1), match.group(2)
    if slug and folder_slug != slug:
        errors.append(f"{rel}: folder slug `{folder_slug}` does not match metadata slug `{slug}`")
    if event_date and folder_date != event_date:
        errors.append(f"{rel}: folder date `{folder_date}` does not match metadata date `{event_date}`")
    if year_dir != folder_date.split("-")[0]:
        errors.append(f"{rel}: year folder `{year_dir}` does not match event date")
    return errors


def warn_large_files(root: Path, files: list[Path] | None) -> int:
    targets = files if files is not None else [
        path for path in root.rglob("*") if path.is_file()
    ]
    warnings = 0
    for path in targets:
        try:
            size = path.stat().st_size
        except OSError:
            continue
        if size > MAX_BYTES:
            rel = path.as_posix()
            mb = size / (1024 * 1024)
            print(f"::warning file={rel}::File is {mb:.1f} MB; prefer links over binaries above 25 MB")
            warnings += 1
    return warnings


def collect_event_files(events_root: Path) -> list[Path]:
    return sorted(events_root.rglob("event.yml"))


def parse_changed_files(raw: str | None) -> list[Path] | None:
    if not raw:
        return None
    files = []
    for line in raw.splitlines():
        line = line.strip()
        if line:
            files.append(Path(line))
    return files


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root())
    parser.add_argument(
        "--changed-files",
        help="Newline-separated paths; used for the 25 MB warning on PRs",
    )
    parser.add_argument(
        "--changed-files-from",
        type=Path,
        help="File containing newline-separated changed paths",
    )
    args = parser.parse_args()
    root = args.root.resolve()
    events_root = root / "events"
    if not events_root.is_dir():
        print("No events/ directory found; nothing to validate.")
        return 0

    errors: list[str] = []
    event_files = collect_event_files(events_root)
    if not event_files:
        print("No event.yml files found.")
    for path in event_files:
        errors.extend(validate_event(path, events_root))

    changed_raw = args.changed_files
    if args.changed_files_from is not None:
        changed_raw = args.changed_files_from.read_text(encoding="utf-8")
    changed = parse_changed_files(changed_raw)
    if changed is not None:
        existing = [root / path for path in changed if (root / path).is_file()]
        warn_large_files(root, existing)
    else:
        warn_large_files(events_root, None)

    if errors:
        print("Event metadata validation failed:\n", file=sys.stderr)
        for error in errors:
            print(f" - {error}", file=sys.stderr)
        return 1

    print(f"Validated {len(event_files)} event.yml file(s).")
    return 0


if __name__ == "__main__":
    os.chdir(repo_root())
    raise SystemExit(main())
