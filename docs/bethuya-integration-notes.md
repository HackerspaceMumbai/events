# Bethuya integration notes

**Status: documented only. Do not implement from this repository.**

Bethuya is Hackerspace Mumbai's community operations platform. It owns registrations, attendee management, curation, capacity, notifications, and community intelligence.

This archive owns public knowledge after (and around) the event: metadata, agendas, speakers, recaps, and resources.

## Boundary

| Belongs in Bethuya | Belongs in this archive |
| --- | --- |
| RSVPs and waitlists | `event.yml` public metadata |
| Attendee PII | Speaker profiles the speaker chose to publish |
| Curation and fairness decisions | Agendas and recaps |
| Capacity and check-in | Resource links and slides |
| Operational notifications | Contributor recognition |

Never copy attendee lists, emails, phone numbers, or curation notes into git.

## Potential future flows

These ideas would be initiated by Bethuya (or a maintainer bot), reviewed by humans, and merged through Pull Requests. They are not built here.

### Auto-create event folders

After an event is approved in Bethuya, a draft PR could:

1. Create `events/YYYY/YYYY-MM-DD-slug/`
2. Add `event.yml`, `README.md`, `agenda.md`, `recap.md`, and `contributors.md` from templates
3. Leave `speakers/` and `resources/` empty for the community

### Auto-generate metadata

Bethuya already knows title, date, venue, and series. A future job could fill required `event.yml` fields and keep Hackmum's public copy in sync — still via PR, not a silent push to `main`.

### Auto-request speaker resources

After a session is confirmed, Bethuya could open a GitHub issue from [`.github/ISSUE_TEMPLATE/speaker-resource-submission.yml`](../.github/ISSUE_TEMPLATE/speaker-resource-submission.yml) or comment on a tracking issue asking the speaker to add `speakers/<handle>/`.

Speakers would still submit their own PRs so the speaker path contract remains conflict-free.

## Principles if this is ever built

- AI drafts, humans approve, community owns.
- Public artifacts only.
- Prefer Pull Requests over direct writes.
- Keep Hackmum as the presentation layer; keep this repo as the source of truth for published event content.
