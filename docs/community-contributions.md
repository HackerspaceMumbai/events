# Community contributions

Events are moments. Communities are journeys.

Speakers contribute knowledge. Attendees contribute perspective. The Events Archive preserves both.

Community artifacts live under each event’s `community/` folder and are first-class alongside speakers, recaps, and resources.

## Folder layout

```text
community/
├── photos/
│   └── <github-handle>/
│       ├── README.md
│       └── photos/
├── notes/
│   └── <github-handle>.md
├── stories/
│   └── <github-handle>.md
├── highlights/
│   └── <github-handle>.md
└── social/
    └── <github-handle>.md
```

Starters:

- [templates/community-photo-readme-template.md](../templates/community-photo-readme-template.md)
- [templates/community-notes-template.md](../templates/community-notes-template.md)
- [templates/community-story-template.md](../templates/community-story-template.md)
- [templates/community-highlight-template.md](../templates/community-highlight-template.md)
- [templates/community-social-template.md](../templates/community-social-template.md)

## What to share

- Session notes
- Event photos
- Learning reflections
- Interesting resources
- Follow-up projects
- Community stories
- Links to demos and experiments
- Short highlights (favorite session, demo, discussion)
- Public social posts, blogs, videos, and photo albums

## What not to share

- Personal contact information
- Private attendee details
- Non-event-related content
- Promotional spam
- Large batches of duplicate or blurry media

Keep secrets, emails, phone numbers, and registration exports out of git.

## Community photos

Structure:

```text
community/photos/<github-handle>/
├── README.md
└── photos/
```

`README.md` should include frontmatter:

```yaml
---
contributor:
github:
event:
---
```

Capture talks, networking, workshops, community interactions, and venue atmosphere.

**Quality over quantity.** Recommend at most **20 photos** per contributor. Prefer ≤ **500 KB** per image (maximum **1 MB**). Use `.jpg` or `.webp`.

Do not upload blurry images, duplicates, or massive dumps.

## Community notes

Path: `community/notes/<github-handle>.md`

Useful topics: session takeaways, key concepts, useful resources, workshop notes.

## Community stories

Path: `community/stories/<github-handle>.md`

Capture attendee experience and community impact — why you came, what you learned, people you met, and what happens next.

## Community highlights

Path: `community/highlights/<github-handle>.md`

Short-form memories: favorite session, demo, resource, or discussion.

## Social Contributions

Already shared your experience publicly?

You can contribute links to:

- LinkedIn posts
- X/Twitter threads
- Blog posts
- YouTube videos
- Public photo galleries

No file uploads required.

Simply submit a Pull Request containing links.

This is the recommended contribution path for attendees who already posted content elsewhere.

Path: `community/social/<github-handle>.md`

Start from [templates/community-social-template.md](../templates/community-social-template.md). Include frontmatter:

```yaml
---
contributor: your-github-handle
event: event-slug
---
```

## How to contribute

1. Find the event under `events/YYYY/`.
2. Add files only under your own GitHub handle paths (see [Community PR contract](architecture-and-contracts.md#community-pr-contract)).
3. Optionally add yourself under **Community Contributors** in that event’s `contributors.md`.
4. Open a Pull Request (label `community`).

If you need help, open an issue with:

- [Community photo submission](../.github/ISSUE_TEMPLATE/community-photo-submission.yml)
- [Community notes submission](../.github/ISSUE_TEMPLATE/community-notes-submission.yml)
- [Community story submission](../.github/ISSUE_TEMPLATE/community-story-submission.yml)
- [Community social submission](../.github/ISSUE_TEMPLATE/community-social-submission.yml)

See also [CONTRIBUTING.md](../CONTRIBUTING.md) and [Event messaging](event-messaging.md) for closing-slide and email copy.

## Recognition

Everyone who contributes should be listed in the event’s `contributors.md` under **Community Contributors** (Photos, Notes, Stories, Highlights, Social Contributions). Contributors are recognized regardless of whether they uploaded files or shared links.
