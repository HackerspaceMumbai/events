# Hackmum sync activation (maintainers)

Operationalize the events → Hackmum rebuild pipeline.

Full contract: [architecture-and-contracts.md § Hackmum website sync](./architecture-and-contracts.md#hackmum-website-sync).  
Blog consumption: [hackerspaceMumbai/blog docs/events-archive-sync.md](https://github.com/hackerspaceMumbai/blog/blob/main/docs/events-archive-sync.md) (land with the companion blog PR if not on `main` yet).

## Checklist

1. Confirm at least one past-event page on Hackmum sets `archiveLinks` to this archive (September Dev Days is the pilot).
2. In Netlify (hackmum.in site) → **Build hooks** → create `events-archive-sync`.
3. In this repo → Settings → Secrets → Actions → add `HACKMUM_SYNC_WEBHOOK` = Build Hook URL.
4. Actions → **Notify website sync** → Run workflow (`workflow_dispatch`).
5. Confirm Netlify starts a deploy.
6. Merge a speaker resource change (or wait for one) under `speakers/<handle>/speaker.md` with `slides` / `repository` / `recording` URLs.
7. After notify + rebuild, open the past-event page and confirm the new resource appears without editing blog frontmatter.

Community-only merges must **not** rebuild Hackmum.
