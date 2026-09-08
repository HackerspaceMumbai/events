---
name: Anshul Bansal
sessionTitle: "Your Server-Rendered App Doesn't Know Who It's Talking To"
github: anshul2209
card: card.jpg
linkedin: https://www.linkedin.com/in/anshul2209
twitter: https://x.com/anshulbansal09
---

# Your Server-Rendered App Doesn't Know Who It's Talking To

## Abstract

A production Node SSR fleet serving 35M monthly users was growing independently of human traffic. Profiling showed ~75% of the expensive render work was bots and crawlers, and HPA was ratcheting capacity up on those surges. This session covers traffic-aware SSR patterns — edge offload, bot/human classification, and differential caching — that cut OLX India's origin footprint by ~80% while making good AI crawlers affordable instead of something to block.

## Key Takeaways

- Profile the client, not just the path: know who is asking before you decide what a request costs you.
- Kill the human-router assumption: SSR that treats every request as a browser user will over-render for crawlers and AI agents.
- Differential caching by traffic type: humans get short TTLs; bots share a long-TTL variant so origin is hit once per window.
- Consolidate cache keys: whitelist params that change the page; collapse every crawler into one `traffic_type=bot` bucket.
- Protect the autoscaling floor: never let bot bursts set baseline capacity — stop junk at the edge first.
- Cache only successful, non-personalized renders: fail toward freshness, purge by tag, and bypass logged-in traffic entirely.
- Caching flips the bot policy: good crawlers can be welcomed back at near-zero origin cost; bad bots stay blocked at the edge.

## Resources

Download the slides from here: [Download](./dev-days-mumbai-deck.pdf)
