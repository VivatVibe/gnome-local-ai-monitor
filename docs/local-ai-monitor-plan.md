# Local AI Monitor GNOME Extension plan

Build a GNOME Shell extension that monitors local AI services and GPU VRAM usage.
The extension serves developers and operators running local large language models on Linux.
It polls Ollama APIs and hardware telemetry asynchronously without blocking the compositor.
Five sequential PRs deliver scaffolding, client networking, hardware telemetry, UI assembly, and packaging.

## How to read this

One box is one unit of work. Every box names the evidence that checks it. A nested box is a sub-step of the box above it. Check a box only when its evidence exists, a file, a log line, a screenshot, a test run, or a SHA. The body is a how-to. The appendices explain and record.

The program runs `pstack/skills/poteto-mode/playbooks/autopilot-stack.md`. The operator reviews review-gated PRs and lands the stack.

Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked.

## Program checklist

### Arm the program

- [ ] State the protocol and this plan to the operator, then stop. Start execution only on the operator's explicit go.
- [ ] Read these from trunk at program start. Re-read them at every tick.
  - [ ] `git show origin/main:pstack/skills/poteto-mode/playbooks/autopilot-stack.md`
  - [ ] `git show origin/main:pstack/skills/swarm/SKILL.md`
  - [ ] `git show origin/main:pstack/skills/poteto-mode/playbooks/opening-a-pr.md`
  - [ ] `git show origin/main:pstack/skills/principle-model-the-domain/SKILL.md`
  - [ ] `git show origin/main:pstack/skills/principle-sequence-verifiable-units/SKILL.md`
  - [ ] `git show origin/main:pstack/skills/principle-prove-it-works/SKILL.md`
- [ ] On the operator's go, arm the audit tick as `/loop 1h` with the tick prompt below. Never leave the cadence to memory.
- [ ] Use this tick prompt, verbatim. "Re-read the execution playbook from trunk. Audit the operation against it and fix drift in this tick. Probe every active lane and judge progress by side effects only. Stand down a stuck lane and dispatch its replacement now. Then post a short status message to the operator in chat only when the audit found a tracked change that no earlier status message reported, such as a PR opened, a code-ready head, a round launched or closed, a verdict, a merge, a stuck agent and the action taken, a blocker added or cleared, or a decision only the operator can make. Name every such change and nothing else. Do not repeat a table, the merged list, or an unchanged blocker. If the audit found none, end the turn with no reply text. Either way, log this tick's row in your decision trail. The row names the items reported, or none."
- [ ] On the operator's hold or stand-down, send every owner a zero-writes order at once.

### Spawn owners

- [ ] Spawn one owner per PR with the full lifecycle the execution playbook names.
- [ ] Follow this dependency graph. Start dependent work only after its parent merges, or base it on the parent branch when the execution playbook stacks.
  - [ ] PR 1 is independent and first. Branches from `main`.
  - [ ] PR 2 after PR 1.
  - [ ] PR 3 after PR 1.
  - [ ] PR 4 after PR 2 and PR 3.
  - [ ] PR 5 after PR 4.
- [ ] Hold the file boundaries. PR 1 touches metadata and schema files. PR 2 touches Ollama client logic. PR 3 touches GPU telemetry. PR 4 touches UI indicator and menu widgets. PR 5 touches preferences and packaging scripts.
- [ ] Hold the review gate. PR 4 and PR 5 change an interaction. They wait for the operator's review in chat with screenshots and a video before merge.

### PR mechanics, for every PR

- [ ] Resolve the forge once. Default to `gh`; if `command -v origin` succeeds and Origin can resolve the repository, use `origin pr` for every PR operation. Record any fallback to `gh`. Never require `gt`.
- [ ] Open the PR ready, never draft, per **Opening a PR**. Use the run's built-in PR tool when it has one, else `origin pr create --status open --base <base-branch>` or `gh pr create --base <base-branch>` according to the resolved forge. A stack child targets its parent branch.
- [ ] Run the repo's lint and typecheck once before the PR-facing push. Push with hooks on.
- [ ] Run `/deslop` before each commit and `/no-comments` before review.
- [ ] Triage every Bugbot and security-reviewer comment per `../references/bugbot-triage.md`.
- [ ] Rebase onto current trunk before the code-ready report and babysit. Keep that merge base in fix rounds. Rebase again only at merge prep, on a `git merge-tree` conflict with trunk, on a CI failure that comes from a change on trunk, or when a known concurrent change to the same files lands.

### Verdict and merge, for every PR

- [ ] A full swarm runs once, at the code-ready head. Another full swarm runs only for new behavior, a redesign, or a large new diff. A rebase, a merge-conflict resolution, or a minor fix gets a single verifier at the new head, and a wording-only change gets none. Run each full swarm per `pstack/skills/swarm/SKILL.md`. One gates lane. The ten live lanes from the PR's **Verify, live** block. The perf lane from its **Verify, perf** block. Two or more audit lanes, each with its own focus, that read the diff and the receipts and distrust the PR body. The root audits the receipts in the merge-ready report before the verdict.
- [ ] Judge every finding by the execution playbook's blocking rule. The verdict is clean when none blocks. A failure on trunk behavior in a lane marked `Regression lane against trunk.` is recorded against trunk and does not block the PR. A new head gets a fresh verdict, except for results that stay valid under the patch-id rule in `playbooks/shipping.md`.
- [ ] The owner reports merge-ready to the root. The operator lands the stack bottom-up after review.

### Boot recipe, for every live lane

Each live lane runs on its own test environment at the PR head. Drive through `gjs` and GNOME extensions CLI tools.

- [ ] `git fetch origin <head-branch> && git checkout <head SHA>`.
- [ ] Validate syntax with `gjs -m` and compile schemas with `glib-compile-schemas`.
- [ ] Deliver input only through test harness scripts and GNOME Shell IPC calls.
- [ ] Save every screenshot to `/tmp/swarm-<pr-id>/worker-<n>/<slug>.png` and return the paths with the report.

## Scaffold extension metadata and schemas (PR 1)

**Depends on.** None.

**Files.**

- [ ] Create `extension/metadata.json`.
- [ ] Create `extension/stylesheet.css`.
- [ ] Create `extension/schemas/org.gnome.shell.extensions.local-ai-monitor.gschema.xml`.
- [ ] Create `tests/test_scaffold.sh`.

**Build.**

- [ ] Define extension UUID `local-ai-monitor@local-ai.mrnv` and supported shell versions 45 through 51 in `extension/metadata.json`.

**You see.**

- [ ] Schema compiles cleanly with `glib-compile-schemas extension/schemas/` producing `gschemas.compiled`.

**Verify, unit.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked.

- [ ] JSON and XML lint test in `tests/test_scaffold.sh`. Run `bash tests/test_scaffold.sh`.

**Verify, live.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked. Ten lanes on `grok-4.7-xhigh-fast` at the PR head, per the boot recipe.

- [ ] Lane 1. Regression lane against trunk. Verify that trunk has no schema collisions with existing extensions. Save `scaffold-lane1.png`. Pass when schema ID is unique.
- [ ] Lane 2. Schema compilation verification. Save `scaffold-lane2.png`. Pass when compile exit code is zero.
- [ ] Lane 3. Metadata validation with gnome-extensions tool. Save `scaffold-lane3.png`. Pass when tool parses UUID.
- [ ] Lane 4. Shell version array boundary test. Save `scaffold-lane4.png`. Pass when 45 through 51 are present.
- [ ] Lane 5. CSS stylesheet parser check. Save `scaffold-lane5.png`. Pass when file is non-empty and valid CSS.
- [ ] Lane 6. Extension path resolution test. Save `scaffold-lane6.png`. Pass when relative imports locate metadata.
- [ ] Lane 7. Default settings key lookup test. Save `scaffold-lane7.png`. Pass when poll-interval key defaults to 3 seconds.
- [ ] Lane 8. Ollama endpoint setting lookup test. Save `scaffold-lane8.png`. Pass when endpoint key defaults to localhost.
- [ ] Lane 9. Schema uninstall cleanly removes compiled file. Save `scaffold-lane9.png`. Pass when clean script removes binary.
- [ ] Lane 10. Metadata strict schema check. Save `scaffold-lane10.png`. Pass when required fields name and uuid exist.

**Verify, perf.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked.

- [ ] Metric. Schema compilation elapsed wall-clock duration in milliseconds.
- [ ] Probe. Run `glib-compile-schemas extension/schemas/` ten times and compute average duration.
- [ ] Baseline. Record 15 milliseconds as the initial baseline.
- [ ] Rule. Compilation must finish within 50 milliseconds.

**Review gate.** None. PR 1 is not review-gated.

**Merge.**

- [ ] Root clean verdict at the exact head SHA.
- [ ] Rebased onto current trunk after the verdict, patch-id unchanged.
- [ ] Root appends PR 1 to base stack.

## Implement Ollama client and polling state machine (PR 2)

**Depends on.** PR 1.

**Files.**

- [ ] Create `extension/lib/types.js`.
- [ ] Create `extension/lib/ollamaClient.js`.
- [ ] Create `tests/test_ollama_client.js`.

**Build.**

- [ ] Implement `OllamaClient` class using `Soup 3.0` async calls for `/api/version`, `/api/tags`, and `/api/ps` in `extension/lib/ollamaClient.js`.

**You see.**

- [ ] Client emits structured state object with server status, loaded models array, and available models array.

**Verify, unit.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked.

- [ ] Test client against local Ollama service in `tests/test_ollama_client.js`. Run `gjs -m tests/test_ollama_client.js`.

**Verify, live.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked. Ten lanes on `grok-4.7-xhigh-fast` at the PR head, per the boot recipe.

- [ ] Lane 1. Regression lane against trunk. Verify that trunk has no Ollama poller running. Save `client-lane1.png`. Pass when port 11434 query returns online.
- [ ] Lane 2. Version API endpoint test. Save `client-lane2.png`. Pass when version string is non-empty.
- [ ] Lane 3. Loaded models endpoint `/api/ps` test. Save `client-lane3.png`. Pass when loaded models array parses.
- [ ] Lane 4. Available models endpoint `/api/tags` test. Save `client-lane4.png`. Pass when available models list matches installed models.
- [ ] Lane 5. Offline fallback test with invalid port. Save `client-lane5.png`. Pass when state transitions cleanly to OFFLINE without crashing.
- [ ] Lane 6. Response body UTF-8 decoding test. Save `client-lane6.png`. Pass when TextDecoder handles multibyte chunks.
- [ ] Lane 7. Request cancellation test. Save `client-lane7.png`. Pass when aborting in-flight message triggers cancellable handler.
- [ ] Lane 8. Polling timer interval tick test. Save `client-lane8.png`. Pass when periodic callback fires on cadence.
- [ ] Lane 9. Unload model API payload generation test. Save `client-lane9.png`. Pass when keep_alive duration zero payload is valid JSON.
- [ ] Lane 10. Concurrent requests deduplication test. Save `client-lane10.png`. Pass when duplicate poll cycles drop overlapping calls.

**Verify, perf.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked.

- [ ] Metric. Round-trip latency for local Ollama query in milliseconds.
- [ ] Probe. Measure latency across twenty consecutive `/api/tags` queries via Soup session.
- [ ] Baseline. Record 12 milliseconds as local loopback baseline.
- [ ] Rule. Query duration must remain under 100 milliseconds on local interface.

**Review gate.** None. PR 2 is not review-gated.

**Merge.**

- [ ] Root clean verdict at the exact head SHA.
- [ ] Rebased onto current trunk after the verdict, patch-id unchanged.
- [ ] Root appends PR 2 to base stack.

## Implement GPU VRAM telemetry reader (PR 3)

**Depends on.** PR 1.

**Files.**

- [ ] Create `extension/lib/gpuTelemetry.js`.
- [ ] Create `tests/test_gpu_telemetry.js`.

**Build.**

- [ ] Implement `GpuTelemetry` class executing `nvidia-smi` asynchronously via `Gio.Subprocess` in `extension/lib/gpuTelemetry.js`.

**You see.**

- [ ] Reader parses GPU model name, VRAM used, VRAM total, and GPU compute utilization into numeric fields.

**Verify, unit.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked.

- [ ] Test telemetry parser against live hardware in `tests/test_gpu_telemetry.js`. Run `gjs -m tests/test_gpu_telemetry.js`.

**Verify, live.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked. Ten lanes on `grok-4.7-xhigh-fast` at the PR head, per the boot recipe.

- [ ] Lane 1. Regression lane against trunk. Verify that trunk has no GPU poller running. Save `gpu-lane1.png`. Pass when `nvidia-smi` produces telemetry output.
- [ ] Lane 2. Process spawn argument validation test. Save `gpu-lane2.png`. Pass when CSV format flags are passed correctly.
- [ ] Lane 3. Memory parsing precision test. Save `gpu-lane3.png`. Pass when used and total VRAM parse as integers.
- [ ] Lane 4. GPU utilization percentage test. Save `gpu-lane4.png`. Pass when utilization is between zero and one hundred.
- [ ] Lane 5. Subprocess non-blocking behavior test. Save `gpu-lane5.png`. Pass when MainLoop processes events during command run.
- [ ] Lane 6. Missing binary graceful degradation test. Save `gpu-lane6.png`. Pass when non-existent binary returns null without unhandled exception.
- [ ] Lane 7. Output line splitting and whitespace trimming test. Save `gpu-lane7.png`. Pass when trailing newlines are stripped.
- [ ] Lane 8. Telemetry state update event test. Save `gpu-lane8.png`. Pass when listener receives parsed metrics object.
- [ ] Lane 9. Resource cleanup on dispose test. Save `gpu-lane9.png`. Pass when subprocess streams close cleanly.
- [ ] Lane 10. Memory calculation ratio test. Save `gpu-lane10.png`. Pass when percentage calculation handles division correctly.

**Verify, perf.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked.

- [ ] Metric. Asynchronous subprocess execution time in milliseconds.
- [ ] Probe. Time twenty asynchronous executions of `nvidia-smi` query command.
- [ ] Baseline. Record 28 milliseconds as command execution baseline.
- [ ] Rule. Execution duration must remain under 120 milliseconds.

**Review gate.** None. PR 3 is not review-gated.

**Merge.**

- [ ] Root clean verdict at the exact head SHA.
- [ ] Rebased onto current trunk after the verdict, patch-id unchanged.
- [ ] Root appends PR 3 to base stack.

## Assemble panel indicator widget and quick settings menu (PR 4)

**Depends on.** PR 2 and PR 3.

**Files.**

- [ ] Create `extension/ui/indicator.js`.
- [ ] Create `extension/ui/menu.js`.
- [ ] Create `extension/extension.js`.

**Build.**

- [ ] Implement `Extension` class subclassing `Extension` from GNOME Shell extensions API, mounting panel button with status badge and dropdown menu.

**You see.**

- [ ] Top panel button displays robot icon and current VRAM usage badge. Clicking opens dropdown with server status, active model, and loaded model list.

**Verify, unit.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked.

- [ ] Unit syntax and ESM module import resolution test. Run `gjs -m -c "import './extension/extension.js';"`.

**Verify, live.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked. Ten lanes on `grok-4.7-xhigh-fast` at the PR head, per the boot recipe.

- [ ] Lane 1. Regression lane against trunk. Verify that trunk does not mount local AI indicator. Save `ui-lane1.png`. Pass when indicator mounts on panel.
- [ ] Lane 2. Panel button icon visibility test. Save `ui-lane2.png`. Pass when symbolic icon renders.
- [ ] Lane 3. Label text update test when model loads. Save `ui-lane3.png`. Pass when label displays active model name.
- [ ] Lane 4. Dropdown menu open on click test. Save `ui-lane4.png`. Pass when popup menu expands.
- [ ] Lane 5. Server status row styling test. Save `ui-lane5.png`. Pass when online status shows green accent class.
- [ ] Lane 6. Active model card display test. Save `ui-lane6.png`. Pass when model name and parameter size are visible.
- [ ] Lane 7. VRAM progress bar rendering test. Save `ui-lane7.png`. Pass when progress bar width matches memory ratio.
- [ ] Lane 8. Unload model button action test. Save `ui-lane8.png`. Pass when clicking sends unload request to Ollama client.
- [ ] Lane 9. Extension enable and disable cycle test. Save `ui-lane9.png`. Pass when disable destroys panel button with zero leaks.
- [ ] Lane 10. Re-enable lifecycle idempotency test. Save `ui-lane10.png`. Pass when re-enabling extension restores UI cleanly.

**Verify, perf.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked.

- [ ] Metric. UI label update render overhead in milliseconds.
- [ ] Probe. Interleaved render timing during rapid telemetry updates.
- [ ] Baseline. Record 2 milliseconds per label update tick.
- [ ] Rule. UI update tick must not exceed 8 milliseconds on main thread.

**Review gate.** The operator reviews before merge.

- [ ] Copy lane 4 screenshots into `media/pr4-review-menu.png`.
- [ ] Record a 30 to 60 second video of panel interaction. Save it as `media/pr4-review.mp4`.
- [ ] Post screenshots and video in chat. Stop at merge-ready. Wait for operator click.

**Merge.**

- [ ] Root clean verdict at the exact head SHA.
- [ ] Rebased onto current trunk after the verdict, patch-id unchanged.
- [ ] Root appends PR 4 to base stack.

## Add preferences dialog and package bundle (PR 5)

**Depends on.** PR 4.

**Files.**

- [ ] Create `extension/prefs.js`.
- [ ] Create `scripts/package.sh`.
- [ ] Create `scripts/verify.sh`.
- [ ] Create `README.md`.

**Build.**

- [ ] Implement `ExtensionPreferences` class using `Adw.PreferencesWindow` and shell script bundling extension zip for distribution.

**You see.**

- [ ] Preferences window displays polling interval slider and Ollama endpoint text input. Package script generates `local-ai-monitor@local-ai.mrnv.shell-extension.zip`.

**Verify, unit.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked.

- [ ] Bundle verification test in `scripts/verify.sh`. Run `bash scripts/verify.sh`.

**Verify, live.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked. Ten lanes on `grok-4.7-xhigh-fast` at the PR head, per the boot recipe.

- [ ] Lane 1. Regression lane against trunk. Verify that trunk has no packaging script. Save `prefs-lane1.png`. Pass when zip bundle builds.
- [ ] Lane 2. Preferences window launch test. Save `prefs-lane2.png`. Pass when `gnome-extensions prefs` opens dialog.
- [ ] Lane 3. Polling interval preference binding test. Save `prefs-lane3.png`. Pass when changing value writes to GSettings.
- [ ] Lane 4. Ollama host endpoint preference input test. Save `prefs-lane4.png`. Pass when updating string persists.
- [ ] Lane 5. Extension zip archive structure test. Save `prefs-lane5.png`. Pass when zip root contains metadata.json directly.
- [ ] Lane 6. Review guidelines compliance check. Save `prefs-lane6.png`. Pass when no forbidden imports exist.
- [ ] Lane 7. Clean build artifact test. Save `prefs-lane7.png`. Pass when temporary files are excluded from zip.
- [ ] Lane 8. Local manual installation test. Save `prefs-lane8.png`. Pass when `gnome-extensions install` succeeds.
- [ ] Lane 9. Extension info inspection test. Save `prefs-lane9.png`. Pass when `gnome-extensions info` outputs version 1.
- [ ] Lane 10. Complete end-to-end user workflow test. Save `prefs-lane10.png`. Pass when extension runs smoothly on desktop.

**Verify, perf.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked.

- [ ] Metric. Zip archive compression time in milliseconds and archive size in kilobytes.
- [ ] Probe. Time execution of `scripts/package.sh` and read output file size.
- [ ] Baseline. Record 45 milliseconds compression time and 40 kilobytes archive size.
- [ ] Rule. Archive must be under 200 kilobytes and compress within 200 milliseconds.

**Review gate.** The operator reviews before merge.

- [ ] Copy lane 2 screenshots into `media/pr5-review-prefs.png`.
- [ ] Record a 30 to 60 second video of preferences dialog and packaged extension. Save it as `media/pr5-review.mp4`.
- [ ] Post screenshots and video in chat. Stop at merge-ready. Wait for operator click.

**Merge.**

- [ ] Root clean verdict at the exact head SHA.
- [ ] Rebased onto current trunk after the verdict, patch-id unchanged.
- [ ] Root appends PR 5 to base stack.

## Close the program

- [ ] Every box above is checked with its evidence.
- [ ] Reply to the operator with the report the execution playbook names.

## Appendix A. Prototype evidence

Two empirical questions were tested before writing this plan.

1. Soup 3.0 asynchronous networking in GJS.
A standalone prototype script `/tmp/test-soup.js` sent an asynchronous `GET` request to `http://127.0.0.1:11434/api/tags`.
The script observed `TAGS SUCCESS` with valid model list JSON from local Ollama.
The call succeeded without blocking the main event loop.

2. Asynchronous subprocess execution for NVIDIA GPU telemetry.
A standalone prototype script `/tmp/test-gpu.js` invoked `nvidia-smi` through `Gio.Subprocess`.
The script observed `GPU SUCCESS` with RTX 3060 Laptop GPU memory and compute metrics.
The call retrieved GPU device name, memory used, total memory, and compute utilization asynchronously.

## Appendix B. Alternatives rejected

1. Synchronous HTTP and shell execution.
Executing `curl` or synchronous network requests directly in GNOME Shell extension code blocks the Mutter compositor.
Blocking Mutter freezes the entire desktop UI and causes frame drops.
All network and process calls must use `Soup.Session.send_and_read_async` and `Gio.Subprocess.communicate_utf8_async`.

2. Direct C-library NVML bindings via GObject Introspection.
Binding directly to `libnvidia-ml.so` requires custom typelibs or low-level FFI.
This crashes on machines running AMD GPUs or Intel integrated graphics.
Spawning `nvidia-smi` with fallback handling allows graceful degradation when NVIDIA drivers are absent.

## Appendix C. Risks

1. Ollama daemon stopped or unreachable.
Mitigated in PR 2 by catching connection errors in Soup async callback and transitioning to an OFFLINE state without throwing unhandled exceptions.

2. Mutter main loop stalls from polling too frequently.
Mitigated in PR 1 and PR 5 with a configurable polling interval defaulting to 3 seconds, and skipping new polls if an existing poll is still in flight.

## Appendix D. Links and reading list

1. GNOME Shell Extension Documentation. `https://gjs.guide/extensions/`
2. Ollama REST API Reference. `https://github.com/ollama/ollama/blob/main/docs/api.md`
3. GNOME Extensions Review Guidelines. `https://gjs.guide/extensions/review-guidelines/review-guidelines.html`
