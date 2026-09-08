# Event taxonomy

This archive supports monthly meetups, one-off gatherings, workshops, event series, and multi-day conferences.

## Valid event types

CI rejects any `eventType` that is not in this list.

| `eventType` | Meaning | Examples |
| --- | --- | --- |
| `meetup` | Recurring community meetup | `#mumtechup` |
| `workshop` | Hands-on learning session | AI Workshop, Open Source Fridays |
| `conference` | Named conference or developer day | GitHub Copilot Dev Days Mumbai, Global Azure Mumbai, Build //localhost Mumbai |
| `hackathon` | Timed collaborative building event | Hacktoberfest Mumbai (when run as a hackathon) |
| `community-day` | Partner or community day | Community Days editions |
| `series` | Parent folder for a multi-stop tour or regional initiative | Mangaluru Dev Days, Hacktoberfest Mumbai (as a series) |
| `summit` | Named summit | Conference / Summit branded days |

## Folder shapes

### Single event (meetup, workshop, one-off, conference, summit, hackathon)

```text
events/
└── 2026/
    └── 2026-09-05-github-copilot-dev-days-mumbai/
        ├── event.yml
        ├── README.md
        ├── agenda.md
        ├── recap.md
        ├── contributors.md
        ├── media/
        │   ├── photos/
        │   ├── videos/
        │   │   ├── README.md
        │   │   ├── session-recordings.md
        │   │   └── playlists.md
        │   ├── social/
        │   │   ├── linkedin.md
        │   │   ├── twitter.md
        │   │   ├── recap-posts.md
        │   │   └── assets/
        │   ├── cover.jpg
        │   └── banner.jpg
        ├── speakers/
        │   └── <github-handle>/
        │       ├── speaker.md
        │       └── card.jpg
        └── resources/
```

- Folder: `YYYY-MM-DD-slug`
- `event.yml` `date` must equal `YYYY-MM-DD`
- `event.yml` `slug` must equal the kebab-case suffix
- Multi-day events still use the **start date** in the folder name and may set optional `endDate`

### Event series (tours, regional initiatives, multi-stop programs)

```text
events/
└── 2026/
    └── 2026-02-mangaluru-dev-days-tour/
        ├── README.md
        ├── event.yml
        ├── stop-01-sahyadri/
        ├── stop-02-nmamit/
        └── stop-03-...
```

- Parent folder: `YYYY-MM-slug` (year and month of the series start; no day component)
- Parent `eventType` must be `series`
- Each stop is `stop-NN-name/` and may include its own `event.yml` plus the usual markdown files
- Stops can be meetups, workshops, or conferences in their own metadata

### Multi-day conferences

Use the single-event folder shape with:

- `date`: first day
- `endDate`: last day
- `eventType`: `conference` or `summit`

Do not split one conference across multiple date-prefixed folders unless the days are independently published events.

## Choosing a type

- Monthly `#mumtechup` → `meetup`
- A standalone named gathering → `conference` (or `summit` if that is the public brand)
- A hands-on lab with a small agenda → `workshop`
- A parent that only exists to group stops → `series`
- If Hacktoberfest is a city-wide season with multiple nights, prefer a `series` parent; if it is one hack night, use `hackathon`

When unsure, prefer the type that matches how the event is presented on [hackmum.in](https://hackmum.in).
