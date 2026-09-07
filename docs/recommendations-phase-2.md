# Phase 2 Recommendations

## Executive Summary

Phase 1 delivered a coherent archive foundation: folder taxonomy, `event.yml` contracts, JSON Schema, templates, speaker path CI, CODEOWNERS, issue/PR forms, and boundary docs for Hackmum and Bethuya.

Operational maturity is still early. The only published event — `events/2026/2026-09-05-github-copilot-dev-days-mumbai/` — is marked `status: completed` and `resourcesAvailable: true`, yet has no `speakers/` tree, placeholder agenda/recap/contributors sections, and no `resources/` artifacts. Schema rules are duplicated in Python rather than loaded by CI. Series stop folders skip folder-alignment checks. Workflows lack least-privilege `permissions`. Branch protection is not documented in-repo.

Phase 2 should harden what exists and close quality loops before **Hacktoberfest Mumbai 2026** volume arrives — without redesigning metadata models, schemas, validators, folder layout, or workflows.

Architectural invariants remain:

```text
GitHub  = Community Archive
Hackmum = Community Website
Bethuya = Community Operations Platform
```

## Current Maturity Assessment

| Area | Maturity | Evidence |
| --- | --- | --- |
| Repository structure | Strong | `events/YYYY/…`, templates, schema, docs |
| Event metadata contract | Strong (docs) / Medium (enforcement) | Required fields documented; CI reimplements schema; empty URI strings pass |
| Speaker contribution path | Strong (contract) / Weak (content) | Path CI + templates + issue form; zero speaker folders published |
| Shared event artifacts | Designed, underfilled | README present; agenda/recap/contributors mostly placeholders |
| Contributor recognition | Designed, empty | Role sections exist; only “Hackerspace Mumbai” under organizers |
| Series / stops | Documented only | Templates + taxonomy; no live series in `events/` |
| Governance | Partial | CODEOWNERS + templates; no documented branch protection; workflows unhardened |
| Hackmum readiness | Stub | `notify-website-sync.yml` no-ops without `HACKMUM_SYNC_WEBHOOK` |
| Bethuya readiness | Notes only | `docs/bethuya-integration-notes.md` correctly forbids implementation here |

**Verdict:** well-structured archive scaffolding; not yet a durable, complete community knowledge platform.

---

## P0 Recommendations

## Complete the Copilot Dev Days archive record

### Current State

`events/2026/2026-09-05-github-copilot-dev-days-mumbai/` contains valid `event.yml` (`status: completed`, `resourcesAvailable: true`), a filled README, and scaffold files for agenda, recap, and contributors. There is no `speakers/` directory and no tracked `resources/` content. Agenda lists a TBD row; recap and contributors retain italic placeholders.

### Gap

A “completed” event with `resourcesAvailable: true` publishes an incomplete public record. There is no quality bar for Hacktoberfest organizers to copy.

### Business Value

Establishes the canonical example of a finished archive entry before high-volume contribution season. Improves Hackmum consumption readiness and community trust.

### Complexity

Medium

### Priority

P0

### Recommendation

Treat this event as the Phase 2 quality bar:

1. Collect session titles, times, and speaker GitHub handles; update `agenda.md` and open or merge speaker PRs under `speakers/<handle>/speaker.md` using `templates/speaker-template.md`.
2. Fill `recap.md` (summary, highlights, resource links, photos/videos, thank-yous).
3. Replace placeholders in `contributors.md` for volunteers, photography, A/V, registration, and hosts (names/handles only — no attendee PII).
4. Add `gallery` to `event.yml` when a public album exists.
5. Set `resourcesAvailable` to `false` until at least one durable speaker resource link or `resources/` file exists; flip to `true` when that lands.
6. Prefer external durable URLs in speaker frontmatter over binaries, per the existing resource policy in `docs/architecture-and-contracts.md`.

Do not invent a new folder layout or metadata model.

---

## Require branch protection and CI checks on main

### Current State

`.github/CODEOWNERS` assigns `@HackerspaceMumbai` to shared event files, `.github/`, `schema/`, and `docs/`. Two PR-gate workflows exist: `Validate event metadata` and `Verify speaker PR`. There is no in-repo documentation of GitHub branch protection or rulesets.

### Gap

Without required status checks and review rules, invalid `event.yml` or path-contract violations can reach `main` if checks are skipped or ignored.

### Business Value

Operational safety for the archive before Hacktoberfest PR volume. Protects the canonical knowledge base.

### Complexity

Low

### Priority

P0

### Recommendation

In GitHub repository settings (not new workflow logic):

1. Protect `main`: require a pull request; dismiss stale reviews on new commits.
2. Require status checks: **Validate event metadata** / job `event.yml and binary size`, and **Verify speaker PR** / job `speakers may only edit their own folder`.
3. Require review from CODEOWNERS for changes touching shared paths (already expressed in `.github/CODEOWNERS`).
4. Document this checklist in `CONTRIBUTING.md` or a short maintainer note under `docs/` so future admins can re-apply settings after org moves.

Do not replace CODEOWNERS or the existing validators.

---

## Publish a post-event completion checklist

### Current State

`CONTRIBUTING.md` tells organizers to complete `recap.md` and `contributors.md` after the event. Architecture docs call recaps and contributors first-class. There is no step-by-step completion checklist tied to `status`, `resourcesAvailable`, speaker chase, or gallery.

### Gap

Completion is implied, not operationalized. Incomplete “completed” events are easy to leave behind.

### Business Value

Archive quality and event completeness before and during Hacktoberfest. Reduces maintainer ambiguity.

### Complexity

Low

### Priority

P0

### Recommendation

Add `docs/event-completion-checklist.md` (and link it from `CONTRIBUTING.md` under organizer “Publish”):

1. Confirm folder naming and required `event.yml` fields still pass CI.
2. Set `status` to `completed` (or `cancelled`) when the gathering ends.
3. Finalize public `agenda.md` (or note cancellations).
4. Open speaker-resource issues via `.github/ISSUE_TEMPLATE/speaker-resource-submission.yml` for missing folders.
5. Fill `recap.md` and `contributors.md`.
6. Set `resourcesAvailable` and optional `gallery` to match reality.
7. Open an organizer-labeled PR for shared-file updates.

Keep logistics, RSVPs, and attendee follow-up in Bethuya. This checklist is archive-only.

---

## Scaffold Hacktoberfest Mumbai 2026 in the archive early

### Current State

`docs/event-taxonomy.md` already guides Hacktoberfest as either a `hackathon` (single night) or `series` (multi-stop season). Templates exist for single events and series parents. No 2026 Hacktoberfest folder exists yet.

### Gap

Without an early scaffold, speakers and community contributors lack a target path; last-minute folder creation increases merge risk.

### Business Value

Contributor workflows and archive readiness for the named P0 milestone.

### Complexity

Low

### Priority

P0

### Recommendation

Before the season opens:

1. Decide `eventType` using existing taxonomy (`series` vs `hackathon`).
2. Create the folder from `templates/event-template.md` / `templates/series-template.md` and `templates/event.yml.example`.
3. Seed `agenda.md`, empty `recap.md` / `contributors.md`, and `status: upcoming`.
4. Pre-create GitHub labels used by CONTRIBUTING (`organizer`, `speaker`, `community`, `event`) if missing.
5. Open tracking issues for speaker resources as sessions confirm.

Do not change taxonomy or invent a Hacktoberfest-specific layout.

---

## Harden existing GitHub Actions workflows

### Current State

Three workflows under `.github/workflows/` (`validate-event-metadata.yml`, `verify-speaker-pr.yml`, `notify-website-sync.yml`) use `actions/checkout@v4` and (where needed) `actions/setup-python@v5`. None declare top-level `permissions:` or `concurrency:` groups.

### Gap

Default `GITHUB_TOKEN` permissions are broader than needed for read-only validation. Stale PR runs are not cancelled.

### Business Value

Operational safety with minimal change — hardening, not replacement.

### Complexity

Low

### Priority

P0

### Recommendation

For each existing workflow:

1. Add `permissions: contents: read` (and only add write permissions later if a future job truly needs them).
2. Add a `concurrency` group keyed by workflow + ref with `cancel-in-progress: true` for pull_request jobs.
3. Keep triggers, scripts, and job names stable so branch-protection required checks do not break.

Do not replace PyYAML validation with a new CI stack in this step.

---

## Finish contributor recognition for the live event

### Current State

`contributors.md` for Copilot Dev Days defines roles for organizers, volunteers, photography, A/V, registration, and community hosts. Only organizers lists “Hackerspace Mumbai”; other sections are placeholders. Speakers section points at a missing `speakers/` tree.

### Gap

Non-speaker contributors are invisible in the public archive despite an explicit recognition model.

### Business Value

Community culture and archive integrity; signals that volunteer labor is part of the knowledge record.

### Complexity

Low

### Priority

P0

### Recommendation

Organizer or community PR (label `community` or `organizer`):

1. Replace placeholders with public names or GitHub handles for each role that applied.
2. Keep registration team as handles/names only — never attendee lists or emails.
3. As speaker folders land, list sessions under Speakers.
4. Cross-link Thank Yous in `recap.md` to `contributors.md` (already scaffolded).

Do not add a parallel recognition system (for example all-contributors bot) until this per-event model is routinely filled.

---

## P1 Recommendations

## Load JSON Schema inside the metadata validator

### Current State

`schema/event.schema.json` (JSON Schema 2020-12) documents the `event.yml` contract. `.github/scripts/validate_event_metadata.py` reimplements required fields, enums, and URI heuristics with PyYAML. CI installs PyYAML only; it never loads the schema file.

### Gap

Schema and Python rules can drift. Documentation points contributors at the schema while CI enforces a separate copy of the rules.

### Business Value

Metadata quality and long-term maintainability without replacing either artifact.

### Complexity

Medium

### Priority

P1

### Recommendation

Extend the existing validator:

1. Add a pinned `jsonschema` dependency in CI (and optionally a small `requirements.txt` under `.github/scripts/`).
2. After YAML load, validate the mapping against `schema/event.schema.json`.
3. Keep folder-naming, year alignment, and series/stop layout checks in Python (schema cannot express path rules).
4. Align empty-string URI handling: either reject empty `website`/`eventPage` in both schema and script, or document empty as intentionally allowed — pick one and enforce consistently.
5. Add a few unit tests for required-field and folder-mismatch cases.

Do not rewrite the schema from scratch or delete the Python path checks.

---

## Close the series stop folder-alignment gap

### Current State

For paths under `stop-*`, `validate_event_metadata.py` runs field validation, then returns after the year-folder check (`is_stop` early return). It does not verify stop folder naming against `slug`, parent series layout, or date consistency with the stop folder.

### Gap

Series stops — the shape Hacktoberfest may use — are under-validated relative to single events.

### Business Value

Metadata quality and automation safety before year-end series growth.

### Complexity

Medium

### Priority

P1

### Recommendation

In `validate_event_metadata.py` only:

1. When `is_stop`, require the parent folder to be a series-shaped `YYYY-MM-slug` with `eventType: series` on the parent `event.yml` if present.
2. Match stop folder `stop-NN-name` naming via the existing `STOP_FOLDER` regex; align `slug` with the stop name segment where the contract expects it (document the rule in `docs/architecture-and-contracts.md` if not already explicit).
3. Continue validating required fields for stop `event.yml` (already done before the early return).
4. Cover with a fixture path in tests (synthetic tree under test fixtures — live golden series can wait for P2).

Do not replace the series folder convention.

---

## Completed-event artifact and resourcesAvailable consistency checks

### Current State

CI validates `event.yml` and warns on files over 25 MB. Presence of `README.md`, `agenda.md`, `recap.md`, and `contributors.md` is expected by docs and PR checklists but not enforced. `resourcesAvailable: true` does not require any speaker links or `resources/` files.

### Gap

Completed events can merge while structurally hollow; the Copilot Dev Days record demonstrates this.

### Business Value

Archive integrity and honest metadata for Hackmum listings.

### Complexity

Medium

### Priority

P1

### Recommendation

Extend `validate_event_metadata.py` (same workflow):

1. When `status` is `completed`, emit errors (or start as warnings for one release, then errors) if any of `README.md`, `agenda.md`, `recap.md`, `contributors.md` is missing beside `event.yml`.
2. When `resourcesAvailable` is `true`, warn (then later fail) if no `speakers/*/speaker.md` contains a non-empty `slides`, `repository`, or `recording` frontmatter URL and no files exist under `resources/`.
3. Keep 25 MB as warning unless abuse appears; document the policy remains soft.

Do not require binaries in git; prefer links.

---

## Lint speaker frontmatter in CI

### Current State

`templates/speaker-template.md` defines frontmatter fields (`name`, `sessionTitle`, `github`, `linkedin`, `slides`, `repository`, `recording`). Speaker path CI enforces folder ownership only. No machine check of frontmatter content. No speaker files exist yet.

### Gap

Invalid or mismatched `github` handles and broken URL shapes will only be caught in human review.

### Business Value

Speaker experience and metadata quality for resource discovery.

### Complexity

Medium

### Priority

P1

### Recommendation

Add a focused check to the existing validate workflow (or a small sibling script invoked by the same workflow):

1. For each `events/**/speakers/*/speaker.md`, parse YAML frontmatter.
2. Require `name`, `sessionTitle`, and `github`.
3. Require `github` to equal the parent folder name (case rules as documented).
4. If `slides` / `repository` / `recording` / `linkedin` are present and non-empty, require `http://` or `https://` prefixes (same heuristic as event URIs today).
5. Fail the job on violations.

Do not replace the speaker path contract workflow.

---

## Add external link durability checks

### Current State

Resource policy prefers durable public URLs. There is no automated check that `website`, `eventPage`, `gallery`, or speaker resource URLs still resolve.

### Gap

Link rot will silently degrade the archive once resources are published.

### Business Value

Resource durability and long-term archive trust.

### Complexity

Medium

### Priority

P1

### Recommendation

1. Add a scheduled workflow (for example weekly) and optional PR-scoped mode that collects URLs from `event.yml` and speaker frontmatter.
2. Perform HTTP HEAD (fallback GET) with timeouts; report non-2xx/3xx as check annotations or a summary comment.
3. Start as non-blocking (`continue-on-error` or warnings) for external false positives; tighten once noise is understood.
4. Do not mirror binary assets into this repo as a substitute for link health; do not move link checking into Bethuya or Hackmum.

---

## Publish an events discoverability index

### Current State

Events live under `events/YYYY/…`. README diagrams mention `2027/` though only `2026/` exists. There is no machine- or human-friendly index of title/date/status/slug for consumers.

### Gap

Archive discoverability for contributors and for future Hackmum walks of the tree.

### Business Value

Discoverability and Hackmum compatibility (archive readiness only).

### Complexity

Low

### Priority

P1

### Recommendation

Add `events/README.md` listing each event: year, folder slug, `title`, `date`, `status`, `eventType`, path. Prefer generating it in CI from `event.yml` files and failing if the committed index is stale — or document hand maintenance until generation exists. Keep Hackmum as the public presentation layer; this index is for archive navigation and consumption readiness.

---

## Issue template config and label hygiene

### Current State

Issue forms exist for event proposals and speaker resource submissions. CONTRIBUTING documents labels `organizer`, `speaker`, and `community`. There is no `.github/ISSUE_TEMPLATE/config.yml` for contact links or blank-issue policy. Labels are not created by repo config.

### Gap

Contributors may file unstructured issues; labels may be missing on a fresh fork/org transfer, breaking organizer bypass documentation.

### Business Value

Contributor workflow clarity.

### Complexity

Low

### Priority

P1

### Recommendation

1. Add `.github/ISSUE_TEMPLATE/config.yml` with `contact_links` to `community@hackmum.in` and optionally hackmum.in; disable blank issues or point them at the forms.
2. Ensure labels `organizer`, `speaker`, `community`, `event`, and `speaker` form labels exist in the GitHub UI (or document creation in the maintainer checklist).
3. Do not change the speaker path contract’s reliance on the `organizer` label.

---

## Dependabot for GitHub Actions

### Current State

Workflows pin actions to moving major tags (`@v4`, `@v5`). PyYAML is installed unpinned via `pip install pyyaml`. No Dependabot or Renovate config exists.

### Gap

Supply-chain and breakage risk as action majors advance; unreproducible pip installs.

### Business Value

Operational safety and automation hygiene.

### Complexity

Low

### Priority

P1

### Recommendation

1. Add `.github/dependabot.yml` for the `github-actions` ecosystem (weekly).
2. Pin Python packages used in CI (`pyyaml`, and later `jsonschema`) to versions in a requirements file referenced by the workflow.
3. Optionally migrate action tags to full commit SHAs after Dependabot is in place — incremental, not a workflow rewrite.

---

## P2 Recommendations

## Document archive export expectations for Bethuya

### Current State

`docs/bethuya-integration-notes.md` describes future Bethuya-initiated scaffold PRs, metadata fill, and speaker-resource issue creation. Status is documented-only; do not implement from this repository.

### Gap

Bethuya implementers lack a concise, stable “read these paths/fields” contract beyond narrative notes.

### Business Value

Interop readiness without responsibility drift — Bethuya remains operations; GitHub remains the archive.

### Complexity

Low

### Priority

P2

### Recommendation

Extend `docs/bethuya-integration-notes.md` with an **Archive export surface** section listing:

- Glob patterns: `events/**/event.yml`, speaker paths, shared markdown filenames.
- Required `event.yml` fields Bethuya may pre-fill.
- PR-first principle and forbidden data (attendee PII).
- Pointers to issue forms for speaker chase.

Do not implement bots, webhooks, or write APIs in this repository.

---

## Hackmum sync activation checklist

### Current State

`notify-website-sync.yml` POSTs `{"repository","sha","ref"}` when `secrets.HACKMUM_SYNC_WEBHOOK` is set; otherwise exits 0 as a stub. Architecture docs describe Hackmum walking `event.yml` and markdown.

### Gap

No maintainer checklist for enabling the secret, verifying payload handling, or confirming archive completeness before relying on sync.

### Business Value

Clean handoff when Hackmum is ready to consume — without implementing Hackmum here.

### Complexity

Low

### Priority

P2

### Recommendation

Add a short checklist to `docs/architecture-and-contracts.md` under Future Hackmum consumption:

1. At least one completed event meets the quality bar (speakers/recap/contributors filled).
2. Configure `HACKMUM_SYNC_WEBHOOK` in repo secrets.
3. Run `workflow_dispatch` on Notify website sync and confirm Hackmum receives the JSON body.
4. Confirm Hackmum reads `event.yml` fields already in the schema (do not add Hackmum-only fields here without updating schema + validator together).

No website code in this repo.

---

## Series golden fixture after stop validation

### Current State

Series layout is documented and templated; README shows a Mangaluru tour example that is not in the tree. Stop validation is incomplete (see P1).

### Gap

CI and contributors lack a real series+stop example to prove layout and validation.

### Business Value

Archive discoverability and automation confidence for multi-stop seasons.

### Complexity

Medium

### Priority

P2

### Recommendation

After P1 stop validation ships, add either:

- a minimal real series under `events/` when one exists in the community calendar, or
- a documented fixture used only in validator unit tests.

Prefer a real public series over synthetic production data. Do not change series naming rules.

---

## Optional speaker frontmatter schema

### Current State

Speaker fields live only in the markdown template and CONTRIBUTING prose.

### Gap

If frontmatter lint (P1) proves valuable, there is still no versioned schema artifact parallel to `event.schema.json`.

### Business Value

Metadata consistency for advanced consumers.

### Complexity

Low

### Priority

P2

### Recommendation

Only after speaker lint is stable: add `schema/speaker.schema.json` mirroring linted fields, and load it from the same CI path. Do not introduce this before speakers actually publish folders.

---

## Resource preservation policy notes

### Current State

Policy prefers durable links; local files allowed up to 25 MB with CI warnings. No guidance on archival copies (for example Internet Archive) when a host disappears.

### Gap

Critical slides and recordings remain single-host dependent.

### Business Value

Long-term resource durability without turning GitHub into a media CDN or Bethuya into an asset store for public knowledge.

### Complexity

Low

### Priority

P2

### Recommendation

Document in `docs/architecture-and-contracts.md` Resource policy:

1. Prefer stable hosts (SpeakerDeck, YouTube, GitHub repos).
2. For irreplaceable materials, optionally add an `archiveUrl` (or note in speaker.md body) pointing at a public web archive snapshot.
3. Keep binaries in `resources/` or `assets/` only when no durable URL exists; retain the 25 MB warning.

Do not build in-repo mirroring infrastructure in Phase 2.

---

## Repository Health Risks

### Risk

Incomplete “completed” events (`resourcesAvailable: true` without speakers, resources, filled recap, or recognition)

### Impact

Public archive misrepresents availability; Hackmum and contributors inherit hollow pages; trust erodes before Hacktoberfest.

### Likelihood

High

### Mitigation

P0 complete Copilot Dev Days record; P0 completion checklist; P1 consistency checks in CI.

---

### Risk

Schema and Python validator drift

### Impact

Docs/`schema/event.schema.json` disagree with CI; contributors follow the wrong contract.

### Likelihood

Medium

### Mitigation

P1 load JSON Schema in `validate_event_metadata.py`; keep path rules in Python only.

---

### Risk

Under-validated series stop `event.yml` folder alignment

### Impact

Invalid stop trees merge ahead of Hacktoberfest multi-stop use; harder to fix later.

### Likelihood

Medium

### Mitigation

P1 close stop early-return gap; P2 golden fixture or tests.

---

### Risk

Missing branch protection / non-required CI checks

### Impact

Broken metadata or speaker path violations reach `main`.

### Likelihood

Medium

### Mitigation

P0 require both validation workflows on `main`; document settings for maintainers.

---

### Risk

Contributor invisibility beyond speakers

### Impact

Volunteers, photography, A/V, registration, and hosts remain absent from the knowledge record despite `contributors.md` design.

### Likelihood

High

### Mitigation

P0 recognition push on the live event; completion checklist includes contributors.

---

### Risk

External link rot after resources publish

### Impact

Dead slides/recording links; archive decay.

### Likelihood

Medium

### Mitigation

P1 link durability workflow; P2 preservation notes for critical assets.

---

### Risk

Archive decay under Hacktoberfest volume without operational process

### Impact

Many scaffolds created; few completed; quality bar never enforced.

### Likelihood

High

### Mitigation

P0 early Hacktoberfest scaffold + completion checklist + branch protection; P1 completed-event checks.

---

### Risk

Soft 25 MB resource policy (warn-only)

### Impact

Large binaries can inflate the git history if ignored.

### Likelihood

Low

### Mitigation

Retain warn-only for now; revisit hard fail if abuse appears; keep preferring external durable URLs.

---

## Recommended Implementation Order

1. Complete Copilot Dev Days (speakers, agenda, recap, contributors, honest `resourcesAvailable`).
2. Enable branch protection + required checks; harden workflow `permissions` / concurrency.
3. Publish event completion checklist; scaffold Hacktoberfest 2026 from existing templates.
4. Finish live-event contributor recognition in parallel with speaker collection.
5. Load JSON Schema in the validator; fix stop-folder alignment validation.
6. Add completed-event artifact / `resourcesAvailable` consistency checks and speaker frontmatter lint.
7. Add link durability checks; events index; issue template config; Dependabot + pinned pip deps.
8. Document Bethuya export surface and Hackmum sync activation; optional series fixture, speaker schema, preservation notes.

## Long-Term Outlook

This repository should evolve from a **well-structured archive** into a **durable community knowledge platform**: complete event records, reliable metadata enforcement, visible non-speaker contributors, and link-healthy resources — still contributed through Pull Requests.

Hackmum remains the presentation layer that consumes `event.yml` and markdown. Bethuya remains the operations platform that may later open scaffold PRs and speaker-resource issues. Neither boundary should absorb the other’s responsibilities.

Incremental Phase 2 work — quality bar, governance, validator depth, and discoverability — is enough to support Hacktoberfest Mumbai 2026 and year-end archive growth without a redesign.
