# Contributing

Thank you for helping preserve Hackerspace Mumbai's community knowledge.

This repository is the public event archive. Registrations, attendee lists, and capacity management belong in Bethuya, not here.

Please read the [Code of Conduct](CODE_OF_CONDUCT.md) before contributing.

## Organizer workflow

Create the event, add the agenda, add speakers, then publish.

1. **Create the event**
   - Copy [templates/event-template.md](templates/event-template.md) and [templates/event.yml.example](templates/event.yml.example).
   - For tours or multi-stop initiatives, start from [templates/series-template.md](templates/series-template.md).
   - Place the folder at `events/YYYY/YYYY-MM-DD-slug/` (single or multi-day) or `events/YYYY/YYYY-MM-slug/` (series).
   - Fill `event.yml` with required metadata. Use a documented `eventType` from [docs/event-taxonomy.md](docs/event-taxonomy.md).

2. **Add the agenda**
   - Edit `agenda.md` with sessions, times, and rooms as they become public.
   - Link each session to `speakers/<github-handle>/` once the speaker folder exists.

3. **Add speakers**
   - Speakers should open their own PRs (see below) so merges stay conflict-free.
   - Organizers scaffolding an event that includes speaker folders should label the PR `organizer`.

4. **Publish**
   - Open a Pull Request.
   - After the event, complete `recap.md` and `contributors.md`.
   - Prefer links over binaries in `resources/`.
   - Archive final event branding under `media/` (`cover.jpg` strongly recommended; `banner.jpg` optional). Reference them from `event.yml` `assets`. Keep visual assets ≤ 500 KB when possible (maximum 1 MB). See [Visual Assets Archival Standard](docs/architecture-and-contracts.md#visual-assets-archival-standard).

## Speaker workflow

Find the event, create your folder, add resources, submit a PR.

1. **Find the event** under `events/YYYY/`.
2. **Create your folder** at `speakers/<your-github-handle>/`.
   - The folder name must match your GitHub username.
   - Copy [templates/speaker-template.md](templates/speaker-template.md) to `speaker.md`.
3. **Add resources**
   - Link slides, source, and recordings in frontmatter when possible.
   - Optional: add the final published speaker card as `card.jpg` (or `card.webp`) and set `card:` in frontmatter. Target ≤ 500 KB (maximum 1 MB).
   - Other local session files belong in `assets/` only when a durable public URL does not exist (≤ 25 MB; CI warns above that size).
   - Do not edit organizer `media/` or shared marketing folders.
4. **Submit a PR** that modifies **only** `speakers/<your-github-handle>/**`.
   - Do not edit `README.md`, `agenda.md`, `recap.md`, `event.yml`, `contributors.md`, `media/`, or another speaker's folder.

CI enforces this contract so maintainers can merge many speaker submissions without conflicts.

## Community workflow

Suggest improvements, share links, and help maintain knowledge.

- Fix typos, add missing resource URLs, and improve recaps.
- Record organizers, volunteers, photography, A/V, registration, and hosts in `contributors.md`.
- Open an issue with the event-proposal or speaker-resource templates when you are not ready to send a PR.
- Keep personal data out of this archive. Do not commit attendee lists, emails, or registration exports.

## Pull request labels

| Label | Meaning |
| --- | --- |
| `organizer` | Maintainer or organizer work that may touch shared event files and speaker folders |
| `speaker` | Speaker-owned folder only |
| `community` | Recaps, links, docs, and other knowledge-base improvements |

## Questions

Open a GitHub issue, or write to [community@hackmum.in](mailto:community@hackmum.in).
