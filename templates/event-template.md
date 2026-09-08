# Event title

> Copy this file to `events/YYYY/YYYY-MM-DD-slug/README.md` and replace the placeholders.
> Also add `event.yml` from `templates/event.yml.example`.

## About

Short public summary of the gathering.

- **Date:** YYYY-MM-DD
- **Venue:** Venue name, city
- **Type:** meetup | workshop | conference | hackathon | community-day | summit
- **Series:** series-id or standalone
- **Website:** https://hackmum.in

## Visual identity

Organizers archive final published branding under [media/](media/):

- `media/cover.jpg` — strongly recommended event cover / registration graphic
- `media/banner.jpg` — optional secondary promotional banner

Use `.jpg` or `.webp`. Keep each file at or below **500 KB** when possible (maximum **1 MB**). Compress with Squoosh, TinyPNG, or `cwebp` before committing. Reference paths from `event.yml`:

```yaml
assets:
  cover: media/cover.jpg
```

Do not commit design sources, drafts, or multiple export variants. See [Visual Assets Archival Standard](../docs/architecture-and-contracts.md#visual-assets-archival-standard).

## Agenda

See [agenda.md](agenda.md).

## Speakers

Speakers add their own folders under [speakers/](speakers/). See [CONTRIBUTING.md](../CONTRIBUTING.md).

## Community

Attendees contribute photos, notes, stories, highlights, and social links under [community/](community/). See [Community contributions](../docs/community-contributions.md).

Already shared publicly? Links to LinkedIn posts, X/Twitter threads, blogs, videos, and public photo albums are welcome — no file uploads required.

```text
community/
├── photos/
├── notes/
├── stories/
├── highlights/
└── social/
```

## Recap

See [recap.md](recap.md).

## Contributors

See [contributors.md](contributors.md). Include a **Community Contributors** section (Photos, Notes, Stories, Highlights, Social Contributions).

## Resources

Prefer links. Local files belong in [resources/](resources/) only when necessary (25 MB maximum).
