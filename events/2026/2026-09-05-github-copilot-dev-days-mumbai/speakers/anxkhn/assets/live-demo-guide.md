```bash
uv tool install --python 3.12 "omnigent[copilot]==0.12.0"
omnigent --version
codex --version
gh auth token >/dev/null
codex login status
```

```bash
export OMNIGENT_FEATURES=usage_page
omnigent start
```

```bash
omnigent server status
open http://localhost:6767
open DEMO_FALLBACK.html
```

```bash
rm -rf demo-cart
unzip demo-cart.zip
cd demo-cart
node --test
omnigent run --harness copilot
```

```text
Work only in the current directory. Run node --test to reproduce the bug.
Make the smallest correct fix in src/cart.js. Do not install dependencies,
browse the web, commit, delete files, or change the test. Run node --test
again and summarize the cause, the one-line change, and the final result.
```

```bash
omnigent usage --limit 3
```

```text
Independent review only. Do not edit files. Read the copied conversation and
the current src/cart.js and tests/cart.test.js, then run node --test. Do not
browse the web, install anything, commit, or run commands that change git state.
Report exactly:

VERDICT: PASS or FAIL
RATIONALE: one sentence
RESIDUAL RISK: one sentence
```
