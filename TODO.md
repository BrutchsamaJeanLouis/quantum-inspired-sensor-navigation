# TODO.md — QIWM

## Active PO session (2026-09-25): exhaustive tick verification + quantum-history analysis
- [x] TODO 1a: exhaustive headless matrix — `--shot`/`--replay` across scenarios (default, maze) × tick regions (0, 1, 5, 50, 120, 300, 500) × seeds (42, 7): every frame valid, non-degenerate, correct state; determinism pairs pixel-identical
  - `examples/verify_tick_matrix.py` → **MATRIX PASS** (28 in-process frames all valid+divergent; cross-seed t0 identical; 8 CLI determinism pairs pixel-identical). Re-confirmed 2026-09-25.
- [x] TODO 1b: live GUI via API (PostMessage keys, works): multiple demos (default/maze) seeked to specific ticks (Home, arrows, slider-max region) → computer_screenshot crop of tick line at each stage; verify state changes (agents, field) across tick regions and scenarios
  - `examples/live_seek_verify.py` (self-contained: launches its own demo, drives PostMessage keys, captures, diffs vs `--shot`) → **LIVE-SEEK PASS** both scenarios, seed 42, ticks 0/120/300. Tick readouts exact: default `Tick:0/120/300 (paused)`, Avg Steps 0/120/300, Avg Energy 100→235→430 (state changes across regions); maze `Tick:0/120/300 (paused)` (agents deterministically die at t=250 → 0 alive at t=300). All `--shot` rc=0, ESC exit 0. Seek uses reliable plain-+1 PostMessage (extended-key bit 24 set; the SDL2 Shift-mod ×10 path is racy).
- [x] TODO 1c: rewind consistency check: live-seeked tick N frame content vs `--shot N` frame (same scenario/seed) — visual/structural match
  - Proven at the WORLD-DATA level (DPI/render-agnostic), the definitive criterion: `examples/verify_rewind_consistency.py` → **REWIND-CONSISTENCY PASS** for 28 (scenario,seed,tick) triples; three independent reach paths (seek(N) == step(1)×N == play-then-HOME-then-scrub) give bit-identical field (maxdiff 0.0), agent (x,y,energy,steps) AND full trail arrays for {default,maze}×{seed 42,7}×{t 0,1,5,50,120,300,500}.
  - Pixel-level cross-check: field heatmap matches (per-pixel diff 0–8, only gradient dithering); the full-frame maxdiff=255 is a capture artifact — the live window (PrintWindow, real 125% display) vs the headless `--shot` (SDL dummy driver) render the alpha-128 agent-trail overlay at different intensities. Not a world-state difference.
- [x] TODO 2 (significant analysis): new `docs/QUANTUM_ASSUMPTIONS_HISTORY.md` — full repo history of the quantum calculation from first commit to now: what changed in assumptions/code/math, and what evidence indicated each change (v1→v2 forensics, §4i re-scope, ablations, instrument bugs)
  - **Written** `docs/QUANTUM_ASSUMPTIONS_HISTORY.md` (5 sections + 11-row assumption ledger A1–A11). Traces the calc across all 15 commits: Era 0 classical baseline (`cc80b63`) → Era 1 v1 pilot-wave embedded in `ToyWorld`, raw `grid + 0.3*pilot_wave`, fatal "q=0 is a classical baseline" assumption (`616d613`, aider) → Era 2 v2 instrument calibration (`5928b5c`: extracted `QuantumInspiredWorld`, `guidance = grid + q·3000·normalize(pilot)`, prewarm 2000, collapse-ON, true classical argmax → honest 0–45% not 70–98%, null rejected 4/5) → Era 3 robustness (ε-greedy `49d90e6`, crossing taxonomy `c0abc3c`, closed-boundary `2971739`) → Era 4 Φ re-scope / 1.5× retraction (`b82d2b1`, §4i, ratio 0.874, direction reversed) → Era 5 paper (`a597baa`) → Era 6 LLM tick controls (`77003ed`, determinism consequence, REWIND-CONSISTENCY PASS). Central instrument-bug lesson + exact stable formulas as of HEAD + stable-vs-instrument-dependent split. Every cited number cross-checked against source (prewarm 2000, 70–98%, moving 0% vs 45%, 400-run grid, ε-sweep, path-eff 0.495, Φ 1.000/0.874).

## Prior session (2026-09-24): LLM-driven tick control + render fixes
- [x] `src/core/timeline.py` — TimelinePlayer (deterministic step/seek/rebuild; seek(n) ≡ live tick n)
- [x] `main.py` CLI: `--scenario {default,maze}`, `--seed`, `--replay T1 T2...`, `--shot TICK --out FILE`
- [x] Visualizer: bottom tick slider (0..500), Space pause/resume, ←/→ scrub (Shift ×10), Home seek 0, L/U coupling
- [x] Render bug fixes: energy-source radius `strength^0.5*scale*0.5`; field normalization p1..p99 percentiles
- [x] Tests: `tests/test_timeline.py` (8) + `tests/test_tick_slider.py` (5) → **120 passed** (was 107)
- [x] Headless `--shot 120 --out` verified: deterministic (same seed ⇒ identical pixels), white ratio 87%→4.3%, 1197 colors
- [x] Live GUI pause + keyboard scrub verified earlier (zero pixel-diff while paused; 6628↔6633 step)
- [x] Live GUI: pause (zero pixel-diff), keyboard scrub (6628↔6633), ESC clean shutdown (exit 0), full-window render (PrintWindow: info panel + both sliders + fixed field) verified live; seek wiring proven by 5 deterministic unit tests on the exact live handlers (`_handle_mouse_down`→`_set_tick_from_x`→`player.seek`→`_sync_player`). Live PostMessage click/drag dispatched (window 800×800 logical, DPI-virtualized to 1000×1000 phys; GetClientRect=800×800 ⇒ logical coords correct); on this SDL2/Windows env PostMessage'd keys reach pygame but mouse events don't register — environmental, not code (see scrapbook 2026-09-24)
- [x] Update scrapbook.md (2026-09-24 session entry)
- [x] git commit (M main.py, M visualizer.py, ?? timeline.py, tests, postkey/postmouse)
- [x] Final smoke test: `--shot 120` ×2 independent runs → pixel-identical (max diff 0,0,0); pytest → 120 passed

## Prior session (2026-09-21): Phi re-scope (P7)
- [x] compute_phi_agents re-scope, ExperimentConfig.phi_agent_in_loop, tests 102→107
- [x] phi_rescope.py audit, docs/RESULTS.md §4i, PAPER.md update
- Honest result: 1.5× threshold formally retracted; re-scoped Φ is a coupling diagnostic, not a gap metric
