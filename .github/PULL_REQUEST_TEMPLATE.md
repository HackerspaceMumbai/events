## Change type

Select all that apply, then complete the relevant checklist below.

- [ ] **Organizer** — event metadata, agenda, recap, or structure
- [ ] **Speaker** — files in my `speakers/<my-github-handle>/` folder
- [ ] **Community** — photos, notes, stories, highlights, social links, resources, contributors, or docs

## Summary

<!-- What does this PR add, update, or fix? -->

## Event

<!-- Event path under events/YYYY/, or “Not event-specific.” -->

## Speaker checklist

Complete this section for speaker contributions.

- [ ] My folder name matches my GitHub username.
- [ ] This PR only changes `speakers/<my-github-handle>/**`.
- [ ] I have not edited `event.yml`, `README.md`, `agenda.md`, `recap.md`, `contributors.md`, or another speaker's folder.
- [ ] Hackmum resources are in `speaker.md` YAML frontmatter: `slides:`, `repository:`, and/or `recording:` use durable `https://` URLs.
- [ ] Any PDF or PPTX is in `speakers/<my-github-handle>/assets/`, not beside `speaker.md`; `slides:` still points to a durable URL.
- [ ] Any local file is 25 MB or smaller.

> Hackmum reads resource URLs from YAML frontmatter; links in the Markdown body alone are not published.

## Organizer checklist

Complete this section for event setup or organizer updates.

- [ ] `event.yml` uses a documented `eventType`.
- [ ] The event folder follows `YYYY-MM-DD-slug` or the series folder follows `YYYY-MM-slug`.
- [ ] The event includes `agenda.md`, `recap.md`, and `contributors.md`.
- [ ] A new event includes the `community/` contribution folders.
- [ ] If this PR includes speaker files alongside organizer changes, it is labeled `organizer` (unless my org membership or collaborator status bypasses the speaker path check).

## Community checklist

Complete this section for community contributions.

- [ ] My changes are under my own handle in the event's `community/` folder:
  - Photos: `community/photos/<my-github-handle>/**`
  - Notes: `community/notes/<my-github-handle>.md`
  - Stories: `community/stories/<my-github-handle>.md`
  - Highlights: `community/highlights/<my-github-handle>.md`
  - Social links: `community/social/<my-github-handle>.md`
- [ ] Photos are public-shareable and curated (20 or fewer recommended; 500 KB preferred per image, 1 MB maximum).
- [ ] Social links are public and not gated.
- [ ] I have not included attendee lists, email addresses, or other private data.
- [ ] New links are public and durable.
- [ ] I added myself to **Community Contributors** in `contributors.md`, or a maintainer will add me.

## Review

- [ ] I have requested at least one reviewer.
