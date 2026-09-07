# Architecture and contracts

This repository is the canonical public archive for Hackerspace Mumbai events.

## System boundaries

```text
GitHub  = Community Archive
Hackmum = Community Website
Bethuya = Community Operations Platform
```

### GitHub (this repository)

Owns event metadata, agendas, speaker profiles, recaps, resource links, and community recognition.

Supports Pull Requests, reviews, and community ownership.

### Hackmum.in

Public presentation layer. It should consume `event.yml` and the markdown artifacts in each event folder to display past events, speakers, resources, recaps, and gallery links.

This repository does not generate website pages. See [Future Hackmum consumption](#future-hackmum-consumption).

### Bethuya

Owns registrations, attendee management, curation, capacity, notifications, and community intelligence.

Attendee data, waitlists, and operational workflows are **out of scope** for this archive. Future ideas are documented in [bethuya-integration-notes.md](bethuya-integration-notes.md) and are not implemented here.

## Event metadata contract

Every event folder (and each series stop that is itself an event) must contain `event.yml`.

### Required fields

| Field | Type | Notes |
| --- | --- | --- |
| `title` | string | Public event name |
| `slug` | string | kebab-case; must match the folder slug |
| `date` | date | `YYYY-MM-DD` (start date for multi-day events) |
| `city` | string | |
| `country` | string | |
| `eventType` | enum | See [event-taxonomy.md](event-taxonomy.md) |
| `series` | string | Series id, or `null` / empty for standalone events |
| `community` | string | Usually `Hackerspace Mumbai` |
| `venue` | string | Public venue name only |
| `website` | URI | Community site, typically `https://hackmum.in` |
| `eventPage` | URI | Canonical public event or past-events URL |
| `resourcesAvailable` | boolean | Whether slides, recordings, or other resources exist |

Unknown `eventType` values fail CI.

### Optional fields (Hackmum-ready)

| Field | Type | Notes |
| --- | --- | --- |
| `status` | string | `upcoming` \| `completed` \| `cancelled` |
| `endDate` | date | Required in practice for multi-day events |
| `timezone` | string | IANA tz, e.g. `Asia/Kolkata` |
| `startTime` | string | `HH:MM` 24-hour local time |
| `hashtags` | string[] | e.g. `[mumtechup, DevDaysMumbai]` |
| `description` | string | Short public summary |
| `gallery` | URI | Public photo/video album |

The JSON Schema lives at [`schema/event.schema.json`](../schema/event.schema.json).

### Folder naming

- Single, one-off, and multi-day events: `events/YYYY/YYYY-MM-DD-slug/`
- Series and tours: `events/YYYY/YYYY-MM-slug/` with `stop-NN-name/` children
- Year directory must match the event year
- `slug` in `event.yml` must match the folder slug (`YYYY-MM-DD-slug` or `YYYY-MM-slug`)
- `date` must match the `YYYY-MM-DD` prefix for single events

CI rejects mismatches.

## Speaker PR contract

Design goal: a speaker only modifies their own folder, so parallel speaker PRs do not conflict.

### Allowed paths for speaker PRs

```text
speakers/<github-handle>/**
```

`<github-handle>` must equal the Pull Request author's GitHub username.

### Forbidden for speaker PRs

```text
README.md
agenda.md
recap.md
contributors.md
event.yml
peer speaker folders
any path outside speakers/<github-handle>/
```

### CI behavior

Workflow: [`.github/workflows/verify-speaker-pr.yml`](../.github/workflows/verify-speaker-pr.yml)

- If a PR changes any `**/speakers/**` path, **every** changed file must be under `**/speakers/<github.actor>/**`.
- Violations fail the check.
- Skip when the PR has the `organizer` label, or when the author is listed in [`.github/CODEOWNERS`](../.github/CODEOWNERS).

## Resource policy

Prefer durable public links over binaries:

```yaml
slides: https://speakerdeck.com/...
repository: https://github.com/...
recording: https://youtube.com/...
```

Allow local files (`slides.pdf`, `slides.pptx`, and similar) only when a public host is not available.

Maximum recommended size: **25 MB**. CI emits a warning when an added or changed file exceeds that size. It does not fail the build.

Keep secrets, attendee lists, and private contact data out of git.

## Recaps and contributors

`recap.md` is a first-class artifact for completed events.

`contributors.md` recognizes organizers, volunteers, photography, A/V, registration, and community hosts — not only speakers.

## Future Hackmum consumption

Hackmum may later:

- Walk `events/**/event.yml`
- Render event pages from `README.md`, `agenda.md`, `recap.md`, and `speakers/*/speaker.md`
- Surface resource links and gallery URLs

The notify workflow [`.github/workflows/notify-website-sync.yml`](../.github/workflows/notify-website-sync.yml) is a stub. It no-ops until `HACKMUM_SYNC_WEBHOOK` is configured. No website integration is implemented in this repository.
