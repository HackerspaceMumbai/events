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
└── highlights/
    └── <github-handle>.md
```

Starters:

- [templates/community-photo-readme-template.md](../templates/community-photo-readme-template.md)
- [templates/community-notes-template.md](../templates/community-notes-template.md)
- [templates/community-story-template.md](../templates/community-story-template.md)
- [templates/community-highlight-template.md](../templates/community-highlight-template.md)

## What to share

- Session notes
- Event photos
- Learning reflections
- Interesting resources
- Follow-up projects
- Community stories
- Links to demos and experiments
- Short highlights (favorite session, demo, discussion)

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
contributor:
github:
event:
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

## How to contribute

1. Find the event under `events/YYYY/`.
2. Add files only under your own GitHub handle paths (see [Community PR contract](architecture-and-contracts.md#community-pr-contract)).
3. Optionally add yourself under **Community Contributors** in that event’s `contributors.md`.
4. Open a Pull Request (label `community`).

If you need help, open an issue with:

- [Community photo submission](../.github/ISSUE_TEMPLATE/community-photo-submission.yml)
- [Community notes submission](../.github/ISSUE_TEMPLATE/community-notes-submission.yml)
- [Community story submission](../.github/ISSUE_TEMPLATE/community-story-submission.yml)

See also [CONTRIBUTING.md](../CONTRIBUTING.md) and [Event messaging](event-messaging.md) for closing-slide and email copy.

## Recognition

Everyone who contributes should be listed in the event’s `contributors.md` under **Community Contributors** (Photos, Notes, Stories, Highlights).
