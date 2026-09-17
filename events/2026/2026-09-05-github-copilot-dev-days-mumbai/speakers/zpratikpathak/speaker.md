---
name: Pratik Pathak
sessionTitle: "You Shouldn't Prompt GitHub Copilot Agent, You Should Make a System to Prompt Itself"
github: zpratikpathak
card: card.jpg
slides: https://raw.githubusercontent.com/HackerspaceMumbai/events/main/events/2026/2026-09-05-github-copilot-dev-days-mumbai/speakers/zpratikpathak/assets/Self_Prompt_PPT.pdf
---

# You Shouldn't Prompt GitHub Copilot Agent, You Should Make a System to Prompt Itself

## Abstract

Developers often spend significant time acting as the bridge between tools and AI systems, manually collecting logs, stack traces, and diagnostics. This session explores **Closed-Loop Agentic Architecture** and **Context Engineering**, demonstrating how GitHub Copilot can use feedback from compilers, tests, and diagnostics to iteratively improve its own output, reducing manual intervention and prompt fatigue.

## Key Takeaways

- Kill the "Human Router" Anti-Pattern: Stop copy-pasting terminal stack traces into chatboxes; conversational micromanagement wastes time and pollutes context.
- Harness Over Prompt Engineering: Shift from writing prose prompts to building programmatic, headless feedback loops between Copilot CLI and your toolchain.
- Context Engineering Sets the Guardrails: Use .github/copilot-instructions.md to passively enforce typing rules, schemas, and architectural boundaries on every run.
- The Compiler Is the Ultimate Prompt: Replace fuzzy natural language with strict type systems and invariant tests that give the agent an exact, binary finish line.
- Synthesize AST Diagnostics: Strip framework noise to pass only high-density error vectors, cutting token waste by up to 68%.
- Enforce Hard Circuit Breakers: Cap iteration budgets at 3 retries and lock test directories to prevent runaway loops or modified test assertions.
- From Typist to Invariant Architect: Your job is to define bulletproof acceptance criteria and review final green diffs, not babysit compilation loops.

## Resources

Download the slides from here: [Download](./assets/Self_Prompt_PPT.pdf)
