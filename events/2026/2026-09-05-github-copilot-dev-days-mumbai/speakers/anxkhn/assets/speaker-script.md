# One Interface, Infinite Agents: Using Copilot with Omnigent

## Complete 25 minute speaker script

**Speaker:** Anas Khan  
**Event:** GitHub DevDays Mumbai  
**Talk duration:** Slides 1 to 17, 00:00 to 25:00  
**Q&A duration:** Slide 18, 25:00 to 30:00  
**Live demo:** Slide 11, 07:00 to 12:45  

Words in quotation marks are spoken aloud. Directions in square brackets are staging cues and physical actions. Keep to the slide transitions even if a section finishes slightly ahead of schedule. Speak at a deliberate, conversational engineering pace, around 140 words per minute.

## Stage and environment setup

- Open the 18 slide deck on slide 1 in full screen mode.
- Open the clean shopping cart fixture in a large terminal window with high contrast.
- Run `node --test` once before the talk to confirm it fails, then reset the fixture to the clean bug state.
- Test that `omnigent run --harness copilot` launches cleanly from the fixture directory.
- Open `DEMO_FALLBACK.html` at frame 1 in a background browser tab as insurance.
- Set the browser window for the live demo to 150 percent zoom so code remains readable from the back row.
- Disable all system notifications, close personal tabs, and mute chat clients.
- Start your personal timer the second you speak your first sentence on slide 1.

## Slide 1: One Interface, Infinite Agents

**Time:** 00:00 to 00:30 (30 seconds)

[Walk to center stage. Stand still. Let the audience look at the title slide for two seconds before speaking.]

"Good morning, Mumbai.

Most of us writing software with AI today juggle multiple tools. We have terminal windows running local agents, browser tabs open with frontier models, and editor extensions on the side. When we move between them, we act as a human clipboard bus. We copy test failures from one window, paste them into another, copy the diff back, and hope important context survived the round trip.

Today, we are going to look at a cleaner approach. I will run GitHub Copilot inside a single terminal through an open meta-harness called Omnigent to solve a concrete bug. We will attach to that exact running session in a browser without restarting the process. Then we will fork the session history over to OpenAI Codex for an independent review.

Pay close attention to what transfers over the wire, what remains local to the machine, and what the receiving agent still has to verify for itself."

**Transition:** "Before opening the terminal, let me introduce who I am and why I work on this problem."

[Advance to slide 2 at 00:30.]

## Slide 2: About Anas

**Time:** 00:30 to 01:15 (45 seconds)

"I am Anas Khan. By day, I work as a Software Engineer at Microsoft focusing on backend systems and applied AI. Earlier in my journey, I worked as a Google DeepMind contributor through Google Summer of Code, building open source tools around machine learning systems.

Over the past few months, I have also been an active open source contributor to Omnigent. When I first submitted the proposal for this talk, I had twenty merged pull requests in the project. Today that count is twenty-two, including six core pull requests on the GitHub Copilot SDK harness integration.

I share those numbers because the technical mechanisms, the failure modes, and the integration boundaries I am discussing today come directly from writing adapter code, debugging dropped event streams, and handling session serialization in the repository.

My views here are entirely my own. This talk reflects personal technical work rather than an official endorsement from Microsoft, GitHub, Google DeepMind, or the Omnigent team."

**Transition:** "The contribution count grew, and the systems challenge behind this talk remains urgent."

[Advance to slide 3 at 01:15.]

## Slide 3: Why developers juggle tools

**Time:** 01:15 to 02:05 (50 seconds)

[Look across the room. Raise one hand.]

"Quick show of hands. In the last forty-eight hours, who here has copied a git diff, a stack trace, or a failing unit test out of one AI tool and pasted it into another?"

[Wait three seconds for hands to go up.]

"Most of the room has their hands up.

Here is why developers do this every day. Frontier labs heavily subsidize their first-party coding agent subscriptions. Tools like GitHub Copilot, Claude Code, and ChatGPT Plus or Pro for Codex bundle massive token allowances, prompt caching, and high rate limits into flat monthly plans. Calling raw frontier APIs with an API key gets expensive fast when an agent loops through forty file reads, compile runs, and test executions.

So developers naturally jump between these subsidized tools. You start in Copilot, hit an hourly rate limit or reach a task where another model excels, and want to continue in Codex or Claude Code.

Opening that second tool takes three seconds. Rebuilding the state of your work takes twenty minutes. The second tool needs the original goal, the constraints, the files modified, the exact shell commands executed, the exit codes, and the risks that remain untested.

Copying the last prompt passes a headline while leaving the underlying investigation behind."

**Transition:** "To build reliable bridges across these tools, we need to separate the stack into distinct engineering layers."

[Advance to slide 4 at 02:05.]

## Slide 4: Demystifying the stack

**Time:** 02:05 to 03:15 (1 minute 10 seconds)

[Point to each layer on screen as you name it.]

"In modern software discussions, people often blend the terms model, harness, and agent together. Keeping them distinct clarifies systems architecture. For this talk, I use four layers.

First is the model. The model provides raw token prediction. It evaluates inputs and generates tokens representing text or structured tool calls. It lacks filesystem access, process tables, and network sockets.

Second is the harness. The harness is the software runtime wrapped around the model. It takes proposed tool calls, opens a pseudo-terminal, executes shell commands, reads repository files, runs tests, inspects git diffs, manages context window compaction, and presents approval dialogs. Claude Code is a harness. GitHub Copilot's CLI backend is a harness. OpenCode is a harness.

Third is the agent. An agent is the working system produced when a model operates through a harness with an explicit goal, an execution loop, and maintained state across turns. In our demo, Copilot functions as our implementation agent, and Codex functions as our review agent.

Fourth is the meta-harness. A meta-harness operates above individual harnesses. It coordinates sessions, persists normalized event history, manages multi-client access, routes execution to runner hosts, and enforces stateful policies across disparate agent runtimes.

People often ask whether tools like OpenCode or GitHub Copilot are meta-harnesses because they let you pick between Claude, GPT, or local models. They are single harnesses that dispatch to multiple models. They run their own internal execution loop and tool engine. OpenCode cannot take an active session and hand it off natively to Claude Code or Copilot. It lacks an agent-to-agent protocol to coordinate with external harnesses.

In contrast, a meta-harness sits above multiple harnesses. T3 Code calls itself an agent harness control surface: it lets you operate local coding agents through web, desktop, and mobile clients. Omnigent focuses on persisted sessions, explicit forks, and lineage across coding-agent harnesses.

Remember the mnemonic: Model proposes. Harness acts. Agent pursues. Meta-harness coordinates. This provides a practical engineering decomposition."

**Transition:** "With those definitions clear, let us look at how Omnigent implements that coordination layer."

[Advance to slide 5 at 03:15.]

## Slide 5: Meet Omnigent

**Time:** 03:15 to 04:05 (50 seconds)

"Omnigent began inside Databricks as an internal engineering system called Isaac. The Databricks team had thousands of engineers using Claude Code and Cursor, followed quickly by Codex. Engineers were hitting subscription rate limits, copying context between terminal panes, writing custom markdown integrations in Obsidian, and trying to keep remote development machines alive overnight so agents could finish long tasks.

To solve that fragmentation, they built and open sourced Omnigent under the Apache 2.0 license.

The architecture separates into two components: a central server and a distributed runner. The server persists the conversation DAG, message events, tool inputs, stdout results, token metrics, and branch lineage in Postgres. The runner executes your selected harness on whatever host you choose, including your local laptop, an SSH development server, or a Docker container.

Because the server stores the canonical record, multiple clients can connect simultaneously: your terminal, a web browser, a native desktop shell, or a mobile client.

Keep your expectations grounded. Omnigent labels itself alpha. It provides a shared, addressable session plane while leaving vendor billing accounts and harness internals distinct."

**Transition:** "Now examine the four concrete ways Omnigent connects to different coding agents."

[Advance to slide 6 at 04:05.]

## Slide 6: How harnesses connect

**Time:** 04:05 to 05:00 (55 seconds)

[Point to the four quadrants on slide 6.]

"Different coding agents expose completely different interfaces to the outside world. Omnigent unifies them using four integration patterns.

First, Direct Python SDK. For GitHub Copilot, Omnigent embeds `github-copilot-sdk` directly in the Python runner process, communicating with Copilot's bundled background CLI daemon over local IPC.

Second, Native SDK. For Claude Code, Omnigent uses `claude-sdk` via `claude_agent_sdk` to directly drive Anthropic's agent loop, tool calls, and turn streaming.

Third, Native CLI Bridges. For OpenAI Codex, Cursor, OpenCode, Pi, Antigravity, Kimi, and Kiro, Omnigent uses native app-server daemons and terminal pseudo-terminal wrappers with model catalog discovery.

Fourth, Agent Client Protocol over stdio. For Devin, Grok Build, Gemini CLI, Qwen Code, and Goose, Omnigent communicates through the open Agent Client Protocol, or ACP. The agent executes as a child process of the runner, exchanging JSON-RPC messages across standard input and output streams. The ACP stack handles capability negotiation, session initialization, and tool delegation. Omnigent includes a generic ACP harness: you point it at a command like `gemini --experimental-acp` or `qwen --acp`, and Omnigent drives it with full session persistence and governance without writing custom adapter code.

Direct SDKs, native CLIs, and open ACP agents become one addressable session stream."

**Transition:** "Now let us understand what happens when a session moves or branches."

[Advance to slide 7 at 05:00.]

## Slide 7: Forks preserve complete history

**Time:** 05:00 to 05:55 (55 seconds)

"When I launch an agent in my terminal and open the emitted URL in a browser, both clients connect over WebSockets to the exact same server session ID. The runner on my laptop continues to own execution. If I send an instruction from the browser, the terminal updates. If the terminal prints a tool output, the browser renders the diff. That is client continuity.

A session fork performs a different operation.

When you fork a session, Omnigent clones the persisted conversation DAG up to a chosen checkpoint into a brand new session entity with its own lineage.

There are four practical reasons developers fork conversations:

One, harness capabilities. Harness A might have specialized local AST manipulation or browser automation that Harness B lacks.  
Two, model specialization. You might use a fast model for initial code generation, then fork to a frontier reasoning model to diagnose a subtle concurrency bug.  
Three, independent adversarial review. Having the same agent review its own patch introduces confirmation bias. Forking to a second harness provides an uncompromised evaluation.  
Four, rate limit rotation. When you exhaust your hourly allowance on one subsidized subscription, you can fork your active task to another provider without starting over.

A session fork clones the message history into a separate database branch. It still requires an explicit host and workspace to reach code on disk."

**Transition:** "When you fork to a different model, there is another operational reality you must understand: token cache cold starts."

[Advance to slide 8 at 05:55.]

## Slide 8: Cache cold starts across forks

**Time:** 05:55 to 06:40 (45 seconds)

[Point to the Warm vs Cold comparison on slide 8.]

"Look at how prompt caching works under the hood.

In our original Copilot session, subsequent turns enjoy high cache hit rates, often around ninety percent. The provider caches key-value tensors for the prompt prefix. Cached input tokens process faster and cost a fraction of standard input tokens.

Now look at what happens when you fork to OpenAI Codex.

Omnigent duplicates the conversation text history in Postgres. But provider-level KV caches are strictly bound to a specific model checkpoint and tokenizer. OpenAI cannot read Anthropic or Copilot cache tensors.

Therefore, turn one on the new model is always a cache cold start. The entire conversation history must be fully re-tokenized and processed at standard input rates.

Session history is portable across databases. Model prompt cache resets at the provider boundary."

**Transition:** "Now let us look at the exact path GitHub Copilot takes through the SDK adapter."

[Advance to slide 9 at 06:40.]

## Slide 9: Copilot enters through the SDK

**Time:** 06:40 to 07:25 (45 seconds)

[Point to the pipeline diagram on slide 9.]

"Omnigent integrates Copilot through GitHub's official Python `github-copilot-sdk`.

Inside the Omnigent runner process, a Python executor initializes the SDK. The SDK package internally bundles and manages its own CLI backend daemon, communicating across a local IPC channel.

The SDK manages the multi-turn session lifecycle with GitHub's remote Copilot infrastructure, streams tool proposals, and returns execution results. Omnigent defaults Copilot to `mai-code-1.1-flash`.

My contributions to this harness focused on making that adapter production grade. In real engineering environments, capturing raw text is insufficient. The system must record operational events accurately. I implemented support for provider-reported AI credit accounting, token cache hit metrics, reasoning effort tracking, clean sub-process interruption during cancellations, context compaction event logging, and policy hooks that evaluate tool proposals before the daemon executes them on your machine.

An adapter delivers value by capturing high fidelity execution evidence."

**Transition:** "With the integration mechanics established, let us set the contract for the live demo."

[Advance to slide 10 at 07:25.]

## Slide 10: Watch the boundary, not the bug

**Time:** 07:25 to 08:00 (35 seconds)

"The demo task involves a shopping cart calculation with an arithmetic bug in `src/cart.js`. The test expects subtotal minus discount plus shipping. The bug omits the discount subtraction.

I selected this bug because it is simple. Any engineer can spot it immediately. A complex distributed systems bug would distract the room into analyzing algorithms.

Keep your attention on the boundaries. Track four specific observations:

One, Copilot executing in the terminal.  
Two, the browser connecting to that exact same live session.  
Three, the operational usage and credit evidence attached to the session record.  
Four, the fork to OpenAI Codex, with explicit host and workspace binding.

Copilot implements. Codex performs a single bounded review. There is no third turn."

**Transition:** "Let us switch over to the terminal and run the workflow live."

[Advance to slide 11 at 08:00. Switch display to terminal window.]

## Slide 11: Live demo

**Time:** 08:00 to 13:45 (5 minutes 45 seconds)

### Phase 1: Launch Copilot via Omnigent (08:00 to 08:45)

[In the terminal, show the prompt inside the test fixture directory.]

```bash
omnigent run --harness copilot
```

"I execute `omnigent run --harness copilot`.

The runner boots our Python harness, initializes `github-copilot-sdk`, launches the backing daemon, and connects to the Omnigent server. The server registers a new conversation session ID and emits a local session URL.

Both the runner and server operate locally on my laptop right now. Model inference and authentication requests flow upstream to GitHub's Copilot cloud service."

[Point to the generated session ID and URL on screen.]

### Phase 2: Reproduce and patch the bug (08:45 to 10:15)

[Paste the prepared implementation prompt into the terminal:]

```text
Work only in the current directory. Run node --test to reproduce the bug.
Make the smallest correct fix in src/cart.js. Do not install dependencies,
browse the web, commit, delete files, or change the test. Run node --test
again and summarize the cause, the one-line change, and the final result.
```

"This prompt defines strict boundaries: work strictly in the current directory, keep the test suite unchanged, leave git state intact, and use `node --test` to verify before and after the edit.

When Copilot asks for approval to run the shell command, I press `a` to approve shell commands for this session. Notice that read-only file inspections are auto-approved, preventing approval card collisions.

Watch the tool call sequence streaming in.

First, Copilot invokes the bash tool to run `node --test`. The test fails: expected ninety-five, received one hundred and ten. The fifteen dollar discount was omitted.

Second, Copilot reads `src/cart.js` and `tests/cart.test.js`.

Third, Copilot issues an edit tool call, replacing that expression with subtotal minus discount plus shipping.

Fourth, Copilot runs `node --test` a second time. The test passes with zero failures.

Copilot provides a concise summary of the cause, the diff, and the passing test result."

### Phase 3: Inspect the live session in the browser (10:15 to 11:00)

[Switch to the browser tab. Navigate directly to the emitted session URL.]

"Now I switch to the browser and open the exact session URL printed by the terminal.

The browser client established a WebSocket connection to the server, loaded the active session record, and rendered the conversation tree.

In the browser, we see the full visual diff of `src/cart.js`. We see every tool invocation, the command line arguments, the stdout responses, and Copilot's final message.

The terminal and the browser observe the exact same server-backed session entity. The runner remained on the local machine. My git workspace stayed intact."

### Phase 4: Inspect operational usage evidence (11:00 to 11:45)

[Click on the session tools and policies drawer. Expand token usage and cost metrics.]

"Now examine the operational metrics recorded alongside the chat.

Because of our work in the Python SDK adapter, Omnigent records the exact token breakdown for each turn: prompt tokens, completion tokens, cache hits, and the provider-reported AI credit usage.

Usage records provide operational telemetry for tracking context and latency. Monthly accounting depends on the provider invoice.

This telemetry allows engineering teams to identify whether prompts are bloating context windows or whether context compaction activated unexpectedly."

### Phase 5: Fork the session to Codex with explicit binding (11:45 to 12:45)

[Hover over Copilot's final passing response. Click `Fork from here`. In the modal, select `Codex` from the harness dropdown. Show the host selection and working directory input.]

"Now we perform the handoff. I click `Fork from here` directly on Copilot's completed message.

Look closely at this modal. I select OpenAI Codex as the target harness. Observe the two fields below it: the execution host and the working directory.

Omnigent clones the message sequence and tool records into a new session branch. Codex needs access to the physical files to review code effectively.

I explicitly bind this fork to my local runner host and the exact working directory path where `src/cart.js` resides.

I click `Clone and start`."

### Phase 6: Bounded adversarial review and lineage stop (12:45 to 13:45)

[In the newly created Codex session, paste the review prompt:]

```text
Independent review only. Do not edit files. Read the copied conversation and
the current src/cart.js and tests/cart.test.js, then run node --test. Do not
browse the web, install anything, commit, or change git state. Report exactly:

VERDICT: PASS or FAIL
RATIONALE: one sentence
RESIDUAL RISK: one sentence
```

"I instruct Codex to perform an independent review without editing files, to inspect current files on disk, to rerun `node --test`, and to return a structured verdict.

Codex reads `src/cart.js` and `tests/cart.test.js` directly. It runs `node --test` itself.

Look at the output:
VERDICT: PASS.  
RATIONALE: The implementation subtracts the discount from the subtotal before adding shipping charges, satisfying the test assertion.  
RESIDUAL RISK: The function does not validate whether discounts greater than the subtotal produce negative totals.

Now look at the lineage tree at the top of the screen.

We have our primary Copilot implementation branch, and branching off it at turn four, we have our Codex review session. We stop here. The review task was bounded and complete, the test ran independently, and the lineage is recorded."

[Switch display back to slides. Advance to slide 12 at 13:45.]

## Slide 12: What crossed the boundary?

**Time:** 13:45 to 15:15 (1 minute 30 seconds)

"Let us examine what actually crossed that boundary from a systems standpoint. Look at the ledger on screen.

The left column lists what was available to Codex:

First, the persisted conversation history up to the fork point. Codex received the prompt, the file contents Copilot inspected, the stdout from the initial test failure, and Copilot's proposed diff.  
Second, the explicit commands and results.  
Third, the fork lineage, recording parentage in the session database.  
Fourth, the recorded usage metadata.  
Fifth, the current filesystem state, which was accessible because we explicitly bound the fork to a runner host and workspace holding those files.

The right column lists what did not cross the boundary:

Codex did not receive Copilot's hidden reasoning tokens. It did not share Copilot's prompt cache or token embeddings. It did not inherit Copilot's private session runtime state or authentication tokens. It maintained separate billing accounts. If we had bound the fork to a different machine, the repository files would have stayed on the original host.

The files were accessible through host binding rather than transcript serialization.

Handoffs across models are useful and inherently lossy. Recognizing what is lost tells you what must be verified."

**Transition:** "Now let us examine how the network traffic and credentials are secured across these distributed boundaries."

[Advance to slide 13 at 15:15.]

## Slide 13: Wire security and payload encryption

**Time:** 15:15 to 16:30 (1 minute 15 seconds)

[Point to the encrypted reasoning diagram and trade-offs on slide 13.]

"Let us examine how payloads and reasoning tokens are secured across the architecture.

Look at the sealed reasoning flow on the left:

Frontier reasoning models generate internal chain-of-thought tokens that arrive sealed as `encrypted_content`. Omnigent preserves these encrypted payloads directly inside the session DAG without attempting to decrypt or modify them. On subsequent turns, the runner passes the sealed payload back upstream to the provider, proving valid reasoning continuity.

Now consider the engineering trade-offs on the right:

The benefits are clear. The system cryptographically guarantees reasoning integrity. It maintains multi-turn context across sessions without leaking proprietary model scratchpads, internal prompts, or sensitive code in plaintext.

The trade-off is opacity. In client UIs, developers see a 'Thinking…' indicator rather than raw chain-of-thought tokens. You cannot inspect or debug the raw scratchpad locally.

Sealed payloads preserve cryptographic verification without exposing internal scratchpads across client screens."

**Transition:** "Because private state remains on the host, the record passed to the next agent must take the form of verifiable empirical claims."

[Advance to slide 14 at 16:30.]

## Slide 14: Evidence the next agent can check

**Time:** 16:30 to 18:00 (1 minute 30 seconds)

"This slide shows the structure of a high signal work record.

Look at the fields:
Goal: Fix cart total calculation.  
Constraint: Change `src/cart.js` only, keep tests unchanged.  
File changed: `src/cart.js`.  
Diff: subtotal minus discount plus shipping.  
Command: `node --test`.  
Observed result: one pass, zero fail.  
Unresolved risk: Invalid or oversized discounts are unhandled.

Notice the label: observed result. This records empirical evidence from running a specific command against a specific commit.

When Codex received this task, it avoided parsing fifty conversational paragraphs. It had a concrete diff to inspect, an exact command to reproduce, and an explicit test output to evaluate.

Notice that final entry: unresolved risk. Teams under deadline pressure often omit the risk statement. That omission frequently causes regression bugs. When an agent reports a fix, it rarely highlights that a discount exceeding the subtotal produces a negative total.

You can apply this structure inside a pull request description, a GitHub issue comment, or a Markdown file in your repository. Omnigent automates the recording."

**Transition:** "To protect your systems while running these agents, you need a clear model of execution topology and containment."

[Advance to slide 15 at 18:00.]

## Slide 15: Know where it runs and what contains it

**Time:** 18:00 to 20:30 (2 minutes 30 seconds)

[Point to the topology diagram and features on slide 15.]

"Let us examine Omnigent's execution architecture and containment boundaries.

Look at the physical tiers:
Tier one is the client: the terminal, the browser, or a mobile device.  
Tier two is the session record server: the central Postgres database, the WebSocket hub, and the policy coordinator.  
Tier three is the runner host: the machine where the Python process executes, where shell commands run, and where files are modified.

Notice the execution features across the bottom:
Multi-host runners let you execute on your local laptop, an SSH development box, or a dedicated cloud container while steering from anywhere.  
Contextual policies dynamically protect sensitive data and enforce live budget caps.  
Kernel sandboxing applies Docker, Bubblewrap, seccomp filters, or Kubernetes pod isolation underneath the runner.

Now examine the three levels of safety:

Level one is the prompt. In our demo, I gave Codex the instruction: `Do not edit files. Independent review only.` That instruction guided model intent. Prompts express desired behavior. If a model hallucinates or encounters an untrusted instruction in a file, it can still issue an edit tool call.

Level two is policy. A policy operates inside the harness or runner runtime. It intercepts tool proposals before execution. A policy can allow an action, request human approval, or deny it. Omnigent supports stateful, contextual policies. If an agent reads a sensitive credentials file earlier in a session, the policy engine can block subsequent outbound network requests. Policy provides workflow control within the application layer.

Level three is the sandbox. A sandbox operates beneath the agent at the operating system and kernel level. It uses Linux cgroups, namespaces, seccomp filters, Docker containers, or microVMs to enforce filesystem, process, and network boundaries.

Prompts express intent to the model. Policies intercept tool requests in the software runtime. Sandboxes use kernel primitives to isolate the process. These three mechanisms operate at entirely different layers of the computing stack."

**Transition:** "Understanding those boundaries establishes the operational rule for building agent workflows."

[Advance to slide 16 at 20:30.]

## Slide 16: Use the smallest workflow that works

**Time:** 20:30 to 22:45 (2 minutes 15 seconds)

"When teams discover meta-harnesses, they often try to construct complex multi-agent pipelines immediately. They place four agents in a debate loop, run recursive review cycles, and spend substantial token budgets on straightforward tasks.

Apply the rule on screen: use the smallest workflow that works.

Step one: Keep Copilot primary when it fits. If GitHub Copilot handles the task within your existing workflow, finish the work there. Introduce additional harnesses only when you hit a concrete limitation.

Step two: Give another harness one named job. In our demo, Codex had a single responsibility: independent adversarial review. It inspected the code, ran the test, and returned a three line verdict.

Step three: Bind the correct host and workspace. Confirm which machine and directory will execute tools before initiating a fork.

Step four: Verify after every session fork. Prompt the receiving agent to run tests, inspect diffs, and return concrete execution evidence.

Step five: Stop when the task is solved. Once tests pass and the review succeeds, close the session.

Treat token and cost metrics as operational telemetry for monitoring context growth. Omnigent labels itself alpha. Build your production systems around simple, verifiable patterns."

**Transition:** "Let us synthesize the core takeaways from the session."

[Advance to slide 17 at 22:45.]

## Slide 17: Keep the evidence portable

**Time:** 22:45 to 25:00 (2 minutes 15 seconds)

[Step to center stage. Speak slowly and deliberately.]

"As we close, think about how meta-harnesses empower software engineers, especially young developers and students entering the field.

First, subsidized access. Flat-rate coding subscriptions make frontier reasoning models accessible to developers who cannot afford thousands of dollars in raw API token bills. A meta-harness lets you build real production systems on top of those subsidized plans.

Second, zero re-learning. Instead of mastering ten different CLI tools, five bespoke configuration files, and proprietary prompt templates, you handle all context in a single reproducible session. When you want to try a new model or harness, you change a flag rather than rewriting your workflow.

Third, collaborative views. You can invite a teammate or mentor into a running session, comment directly on live diffs, and inspect transparent session DAG lineage together.

One interface coordinates separate runtimes without unifying the underlying models.

Keep the agent that fits the task. When work must move, carry evidence, not confidence.

Thank you very much."

[Hold for applause. Advance to slide 18 at exactly 25:00.]

## Slide 18: Questions

**Time:** 25:00 to 30:00 (5 minutes)

[Leave slide 18 on screen. It displays the simplified topology diagram, open discussion topics, and the resource link.]

"We have five minutes for open discussion. Questions regarding the Copilot SDK integration, session DAG persistence, ACP protocol communication, and wire security are all welcome."

### Question and answer handling playbook

Repeat each audience question into your microphone before answering. Keep responses direct, technical, and under 45 seconds.

#### Question 1: How does Omnigent communicate with ACP agents like Devin or Gemini?
"Omnigent connects to ACP agents through the Agent Client Protocol over standard input and output streams. The agent CLI (such as Devin, Grok Build, Gemini, or Qwen) runs as a child process of the runner, exchanging JSON-RPC messages. Omnigent provides an ACP client that maps tool requests, prompts, and streaming deltas into normalized Omnigent session events."

#### Question 2: Why don't prompt cache hits carry over when forking from Copilot to Codex?
"Provider prompt caching (like Anthropic ephemeral caching or OpenAI prefix caching) operates on the model's exact tokenizer and KV cache state in GPU memory. When you fork a session to another model, the conversation text is copied into Postgres, but the new provider's tokenizer must parse and re-embed the tokens from scratch. The first turn on the new model is always a cold start."

#### Question 3: How does Omnigent communicate with Copilot without a separate CLI?
"Omnigent uses GitHub's official Python `github-copilot-sdk`. Inside the harness runner, our Python adapter initializes the Copilot client. The SDK package internally bundles its own CLI backend server and launches it as an IPC child process. The Python process exchanges JSON-RPC messages across that channel and maps the stream into normalized Omnigent events. No standalone Copilot CLI installation is required on your path."

#### Question 4: Is a session fork equivalent to a git branch?
"No. A git branch tracks a DAG of repository commits on disk. A session fork tracks a DAG of conversational messages, prompts, and tool invocations in the database. You can fork a session while remaining on the same git branch, or fork a session and instruct the runner to check out a new git branch. They represent separate state dimensions."

#### Question 5: How are credentials and payloads secured between the runner and server?
"The runner connects to the server over an outbound WebSocket tunnel encrypted with TLS (WSS) and authenticated using runner tokens. Upstream calls to Copilot or OpenAI use TLS with tokens stored only on the runner host. Sensitive credentials never serialize into the central conversation database."

[At 29:40, wrap up the session.]

"We are at time. Thank you for the questions. The presentation slides, detailed architecture notes, and demo fixtures are available at `anaskhan.me`. Enjoy the rest of DevDays Mumbai!"

## Demo fallback language

Use `DEMO_FALLBACK.html` if there is an unexplained delay greater than 12 seconds or an unrecoverable network failure. State the transition plainly.

### General fallback transition
"The live network connection is experiencing latency, so I am switching over to our verified static execution trace. The architectural boundaries are what matter today, rather than network conditions."

### Copilot authentication or SDK failure
"The local Copilot daemon failed to establish its session with the service, so I am switching to the verified static trace. It shows the identical Python SDK execution sequence, session ID, and emitted URL."

### Browser client reconnect failure
"The browser WebSocket client encountered a local connection issue, so we will use the matching static view. The terminal and browser address the exact same session ID, with the runner on the local host."

### Fork or Codex failure
"OpenAI Codex is experiencing API latency, so I am advancing to the prepared fork frames. Here you see the Codex harness selection, host binding, workspace file inspection, and the passing verdict."

## Timing checkpoint guide

| Elapsed time | Slide | Action |
| --- | --- | --- |
| 00:00 | Slide 1 | Start talk, open with human clipboard hook |
| 00:30 | Slide 2 | Introduce Anas, Microsoft, GSoC, 22 merged PRs |
| 01:15 | Slide 3 | Hand raise, frontier subsidies, cost of rebuilding work state |
| 02:05 | Slide 4 | Four layers: model, harness, agent, meta-harness, OpenCode distinction |
| 03:15 | Slide 5 | Meet Omnigent, Databricks origin, server vs runner |
| 04:05 | Slide 6 | How harnesses connect: direct SDK, native CLI, ACP over stdio |
| 05:00 | Slide 7 | Same session across clients vs session fork, four reasons to fork |
| 05:55 | Slide 8 | Cache cold starts across forks, prompt caching mechanics |
| 06:40 | Slide 9 | Copilot Python SDK architecture and event pipeline |
| 07:25 | Slide 10 | Demo contract, trivial bug in `src/cart.js`, four boundaries |
| 08:00 | Slide 11 | Launch live demo in terminal |
| 10:15 | Slide 11 | Switch to browser view of same session |
| 11:00 | Slide 11 | Show operational usage metrics and credit breakdown |
| 11:45 | Slide 11 | Fork to Codex with explicit host and workspace binding |
| 12:45 | Slide 11 | Run bounded Codex review, show lineage tree |
| 13:45 | Slide 12 | Return to slides, break down the boundary ledger |
| 15:15 | Slide 13 | Wire security and payload encryption, WSS tunnel, credential isolation |
| 16:30 | Slide 14 | Structured portable work record and unresolved risk |
| 18:00 | Slide 15 | Systems topology, Prompt vs Policy vs Sandbox |
| 20:30 | Slide 16 | The smallest workflow that works, governance rules |
| 22:45 | Slide 17 | Closing synthesis, evidence over confidence |
| 25:00 | Slide 18 | Begin Q&A, hold until 30:00 |

## Verification and facts checklist

- Primary implementation harness: GitHub Copilot using Python's `github-copilot-sdk`.
- Secondary review harness: OpenAI Codex performing a single bounded verification.
- Contribution count: 22 merged pull requests (submitted count was 20).
- Session semantics: Same session ID across clients; forks create a new branch in the Postgres session DAG.
- Workspace requirement: A session fork copies conversation history; access to repository files requires explicit runner host and working directory binding.
- Safety hierarchy: Prompts express desired behavior; policies intercept tool proposals in software; sandboxes enforce kernel-level isolation.
- Architecture: Central server (Postgres, WebSockets, policies) and distributed runner (local machine, SSH dev box, or Docker container).
- Operational records: Usage metrics provide operational telemetry, separate from the provider invoice.
