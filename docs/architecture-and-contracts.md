# Architecture and contracts

This repository is the canonical public archive for Hackerspace Mumbai events.

## System boundaries

```text
GitHub  = Community Archive
Hackmum = Community Website
Bethuya = Community Operations Platform
```

### GitHub (this repository)

Owns event metadata, agendas, speaker profiles, recaps, resource links, community contributions (photos, notes, stories, highlights, social), and community recognition.

Supports Pull Requests, reviews, and community ownership.

### Hackmum.in

Public presentation layer. It should consume `event.yml` and the markdown artifacts in each event folder to display past events, speakers, resources, recaps, gallery links, and relative visual asset paths (`assets.cover`, speaker `card`).

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
| `assets` | object | Relative paths to organizer visual identity files (see [Visual Assets Archival Standard](#visual-assets-archival-standard)) |

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

Session binaries and link-first resources are distinct from curated visual identity files. See [Visual Assets Archival Standard](#visual-assets-archival-standard) for cover images and speaker cards (tighter size limits, finals only).

## Visual Assets Archival Standard

Final published branding documents how an event was promoted and how speakers were presented. Preserve those artifacts in-repo without turning GitHub into a media CDN or introducing shared marketing folders that break the Speaker PR contract.

### Rationale

Visual assets archive:

- Event branding
- Speaker promotion
- Community history
- Sponsor participation context (when present on published artwork)
- Evolution of Hackerspace Mumbai over time

Store only the **final published** artifact for each role. Do not commit design sources, drafts, or export variants.

### Ownership boundaries

| Owner | Location | Examples |
| --- | --- | --- |
| Organizers, volunteers, official photographers, and speakers contributing official assets | `media/` | Official photos, videos/recording links, social posts, `cover.jpg`, optional `banner.jpg` |
| Speakers | `speakers/<github-handle>/` | `card.jpg` beside `speaker.md` |
| Community | `community/photos/<github-handle>/`, `community/social/<github-handle>.md` | Curated attendee photos and public social links (see [Community contributions](community-contributions.md)) |

Invalid (creates ownership ambiguity and merge conflicts):

```text
marketing/speaker-cards/
shared-assets/
event-root/card.jpg
```

### Official event media assets

```text
media/
├── photos/      # official event photography
├── videos/      # official recording and playlist links
├── social/      # official Hackerspace Mumbai posts and assets
├── cover.jpg    # strongly recommended
└── banner.jpg   # optional
```

- Use `.jpg` or `.webp`.
- `cover.jpg` is the primary event identity graphic (registration art, official promotional cover).
- `banner.jpg` is optional (sponsor announcements, secondary promotional strips).
- This is the canonical official event media archive for hackmum.in.
- Maintained by organizers, volunteers, official photographers, and speakers contributing official event assets.
- Community perspectives and attendee-created content belong under `community/`, not `media/`.

### Speaker assets (speaker-owned)

```text
speakers/<github-handle>/
├── speaker.md
└── card.jpg      # optional, strongly encouraged
```

- `card.jpg` is the final published speaker promotional card.
- Supported formats: `.jpg` or `.webp` (prefer `card.jpg` or `card.webp`).
- Referenced from speaker frontmatter; stored only in that speaker's folder.
- Session slides and other binaries still belong in `assets/` when a public URL is unavailable (see Resource policy).

### Speaker PR compatibility

`card.jpg` lives under `speakers/<github-handle>/`, so it remains inside the Atomic Speaker PR path:

```text
speakers/<github-handle>/**
```

Speakers must not edit `media/`, `event.yml` `assets`, or another speaker's card. Organizers scaffolding multiple speaker folders should label the PR `organizer`.

### Size and compression

| Target | Limit |
| --- | --- |
| Recommended | ≤ 500 KB per visual asset |
| Maximum | ≤ 1 MB per visual asset |

Compress before commit (Squoosh, TinyPNG, `cwebp`). Prefer finals that stay near the recommended size.

### Not allowed

- Canva / Figma / Photoshop / Illustrator project files
- Raw camera files
- Multiple export variants (`speaker-v1.png`, `speaker-v3-final.png`)
- Draft revisions and temporary design assets
- Photo galleries as bulk uploads under organizer `media/` (use optional `gallery` URI for external albums, or curated attendee sets under `community/photos/<github-handle>/`)

### Machine-readable metadata

Paths are relative to the event folder (or speaker folder for `card`) and portable for static-site generation and hackmum.in:

```yaml
# event.yml
assets:
  cover: media/cover.jpg
  banner: media/banner.jpg   # optional
```

```yaml
# speakers/<handle>/speaker.md frontmatter
card: card.jpg
```

Consumers resolve `assets.cover` / `assets.banner` against the event directory, and `card` against the speaker directory containing `speaker.md`.

### Target layout

```text
events/YYYY/YYYY-MM-DD-event-slug/
├── event.yml
├── README.md
├── agenda.md
├── recap.md
├── contributors.md
├── media/
│   ├── cover.jpg
│   └── banner.jpg
├── speakers/
│   └── <github-handle>/
│       ├── speaker.md
│       └── card.jpg
├── resources/
└── community/
    ├── photos/<github-handle>/
    ├── notes/<github-handle>.md
    ├── stories/<github-handle>.md
    ├── highlights/<github-handle>.md
    └── social/<github-handle>.md
```

This shape scales across recurring meetups, conference-style events, Hacktoberfest, Dev Days, and one-off community gatherings without shared marketing directories.

## Community PR contract

Design goal: an attendee only modifies their own community paths, so parallel community PRs do not conflict.

### Allowed paths for community PRs

```text
community/photos/<github-handle>/**
community/notes/<github-handle>.md
community/stories/<github-handle>.md
community/highlights/<github-handle>.md
community/social/<github-handle>.md
```

`<github-handle>` should equal the Pull Request author's GitHub username.

Contributors may also add their own recognition line under **Community Contributors** in `contributors.md` (or a maintainer can do so after merge).

### Guidelines

- Prefer links and markdown over large binaries.
- Community photos: ≤ 20 recommended; ≤ 500 KB preferred per image (maximum 1 MB); `.jpg` or `.webp`.
- Social contributions: public links only (LinkedIn, X/Twitter, blogs, videos, galleries); no file uploads required.
- No private attendee data.

CI does not yet enforce this contract (unlike the Speaker PR contract). A future `verify-community-pr` check may mirror the speaker enforcer. Until then, reviewers rely on the PR checklist and [Community contributions](community-contributions.md).

## Recaps and contributors

`recap.md` is a first-class artifact for completed events.

`contributors.md` recognizes organizers, volunteers, photography, A/V, registration, community hosts, speakers, and **Community Contributors** (Photos, Notes, Stories, Highlights, Social Contributions).

Community photos, notes, stories, highlights, and social contributions under `community/` are first-class event artifacts alongside speakers and resources. See [Community contributions](community-contributions.md).

## Future Hackmum consumption

Hackmum may later:

- Walk `events/**/event.yml`
- Render event pages from `README.md`, `agenda.md`, `recap.md`, and `speakers/*/speaker.md`
- Surface resource links and gallery URLs
- Resolve relative `assets.cover` / `assets.banner` from `event.yml` and `card` from speaker frontmatter for static-site and CDN-friendly image URLs
- Feature community stories from `community/stories/`
- Build event galleries from `community/photos/`
- Surface community highlights from `community/highlights/`
- Enhance event recaps with attendee notes and perspective from `community/notes/`
- Surface community social links from `community/social/`

**Status: documented only. Do not implement website consumption from this repository.**

The notify workflow [`.github/workflows/notify-website-sync.yml`](../.github/workflows/notify-website-sync.yml) is a stub. It no-ops until `HACKMUM_SYNC_WEBHOOK` is configured. No website integration is implemented in this repository.
