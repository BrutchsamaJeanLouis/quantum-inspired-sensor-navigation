# QIWM Scrapbook

## 2026-09-25 PM: PO session — Applications section + repo publish + GitHub + Zenodo (all TODOs [x])

- **Paper §5 Applications** added to `docs/PAPER.md` (8 ranked subsections 5.1–5.8, most→least impact: UUV/autonomy, planetary/rover, SAR/RF nav, indoor SLAM, swarm/underwater, embodied-LLM planning, biology-inspired research, education). Ranked by where a *locally-greedy* policy is most costly.
- **Repo tidy + publish:** loose CSVs→`data/`, PNGs→`media/`, scratch→`scratch/`; `.gitignore` updated. Public GitHub `BrutchsamaJeanLouis/quantum-inspired-sensor-navigation` created; pushed (final `07de126`). Cross-links: paper→GitHub + DOI; README→DOI + author.
- **Author fix:** paper/README/PDF now show **"Author: Brutchsama Jean-Louis"**; PDF `pdfauthor` metadata set to match (was "QIWM").
- **PAPER.pdf:** pypandoc + xelatex + `docs/paper_header.tex` (newtxtext/T1 for ε≈≥≤≡). ~79KB, self-referential DOI.
- **Zenodo flow (RDM API):** `POST /api/records/{id}/versions` → new recid; `PUT /draft` metadata (needs `publisher`, `person_or_org.given_name/family_name`); `POST /draft/actions/publish` → 202. Version 4 = **active DOI `10.5281/zenodo.22964117`** (v1 22961527 / v3 22963620 superseded but stay live; concept 22961526→latest). File drop = manual drag-and-drop (AGENTS.md rule), not setInputFiles.
- **DOI resolution:** doi.org 404 right after publish is *expected* DataCite handle-registration lag (verified vs Zenodo/EPrints docs); concept DOI→latest version, version DOI→that version. Concept DOI handle was `responseCode:100` (registered, no URL yet) = in-progress, not failure.
- **Env:** GCM OAuth token `gho_…` works for token-URL push; the `ghp_` PAT went stale. Zenodo CSRF via `csrftoken` cookie + `X-XSRF-TOKEN`/`X-CSRFToken` from a zenodo.org page. `related_identifiers[].relation_type` is a broken required-field in this RDM build → keep `[]`, put GitHub URL in description.

## 2026-09-25: PO session — exhaustive tick verification + quantum-history analysis (all TODOs [x])

- **TODO 1a — headless matrix:** `examples/verify_tick_matrix.py` → **MATRIX PASS**. 28 in-process `--shot`-equivalent frames (default,maze)×(seed 42,7)×{t 0,1,5,50,120,300,500} all valid + divergent across t; cross-seed t0 identical; 8 CLI `--shot` determinism pairs pixel-identical. Re-confirmed today.
- **TODO 1b — live GUI via API:** `examples/live_seek_verify.py` (self-contained: launches its own demo, drives PostMessage keys, PrintWindow-captures, diffs vs `--shot`) → **LIVE-SEEK PASS** both scenarios, seed 42, ticks 0/120/300. Tick readouts exact (default `Tick:0/120/300`, Avg Steps 0/120/300, Avg Energy 100→235→430; maze `Tick:0/120/300`, agents die at t=250 → 0 alive at t=300). All `--shot` rc=0, ESC exit 0. Seek uses reliable plain-+1 PostMessage. **Root cause of earlier key-drops:** SDL2 2.28's `WindowsScanCodeToSDLScanCode` remaps non-extended VKs to numpad scancodes unless bit 24 (extended) is set in lParam → set it for arrows/home. **×10 (Shift+Right) is racy** (posted Shift-keyup processed out of order, clears KMOD before RIGHT) → use +1 in the driver.
- **TODO 1c — rewind consistency:** `examples/verify_rewind_consistency.py` → **REWIND-CONSISTENCY PASS**, the definitive (DPI/render-agnostic) criterion. 28 (scenario,seed,tick) triples, three reach paths bit-identical: `seek(N)` ≡ `step(1)×N` ≡ play-then-HOME-then-scrub, on field (maxdiff 0.0) + agents (x,y,energy,steps) + full trail arrays. Pixel cross-check: field heatmap matches (diff 0–8, gradient dithering only); full-frame maxdiff=255 is a capture artifact (live PrintWindow @125% vs headless `SDL_VIDEODRIVER=dummy` render the alpha-128 trail overlay at different intensities) — **not** a world-state difference.
- **TODO 2 — quantum-history analysis:** `docs/QUANTUM_ASSUMPTIONS_HISTORY.md` (new) — forensic history of the quantum calc across all 15 commits: v1 (pilot-wave embedded in `ToyWorld`, raw `grid+0.3*pilot_wave`, the fatal "q=0 is a classical baseline" assumption, `616d613`) → v2 instrument calibration (`5928b5c`: `QuantumInspiredWorld` extracted, `guidance = grid + q·3000·normalize(pilot)`, prewarm 2000, collapse-ON, true classical argmax → honest 0–45% not 70–98%, null rejected 4/5) → robustness (`49d90e6` ε-greedy, `c0abc3c` crossing taxonomy, `2971739` closed-boundary) → Φ re-scope / 1.5× retraction (`b82d2b1`, §4i, ratio 0.874 direction reversed) → paper → LLM tick controls. 11-row assumption ledger (A1–A11: introduced / killing-or-keeping evidence / status) + central instrument-bug lesson + exact stable formulas as of HEAD + stable-vs-instrument-dependent split. Every cited number cross-checked against source.
- **Verification:** `pytest tests -q` → **120 passed** (43 s). All three new example scripts run clean. `nul` artifact removed. Tree clean after commit.

## 2026-09-24: PO session — LLM-driven tick controls + render fixes (all TODOs [x])

- **`src/core/timeline.py`** (new): `TimelinePlayer` — deterministic scrubbable tick engine. `step(n)`; `seek(n)` = fast-forward if ahead, else re-seed + re-step n (rebuild world+swarm from factory, fixed seed ⇒ seek(n) ≡ live tick n); `rebuild()`, `stats()`, `guidance_field()`.
- **`main.py` CLI**: `--scenario {default,maze}`, `--seed`, `--replay T1 T2…` (hop-and-screenshot), `--shot TICK --out FILE` (headless single frame = clean LLM bash primitive). Smoke: two `--shot 120` runs pixel-identical (max diff 0,0,0).
- **Visualizer**: bottom tick slider (0..500) + tick label; Space pause/resume; ←/→ scrub (Shift ×10); Home seek 0; L/U coupling. `_sync_player()` re-points viz world/swarm after rewind. Render fixes: energy-source radius `strength^0.5*scale*0.5` (was covering the field); field normalization p1..p99 percentiles (min/max flattened heatmap).
- **Tests**: `tests/test_timeline.py` (8) + `tests/test_tick_slider.py` (5: click-seek+arm-drag, drag-updates-tick, edges→0/max, slider click doesn't add energy, rewind re-points world) → **120 passed** (was 107). `examples/postkey.py`/`postmouse.py` (PostMessage key/mouse helpers — SendInput blocked in this env).
- **Live GUI verification**: pause (zero pixel-diff 3 s), keyboard scrub (6628↔6633), ESC clean exit (exit 0, "Simulation Complete") all verified via PostMessage keys + PrintWindow captures. Window geometry decoded: GetClientRect=800×800 logical, DWM frame 1002×1040 physical (DPI-unaware/virtualized 1.25×) ⇒ PostMessage mouse coords in logical 800-space. PostMessage'd **keys reach pygame, mouse events don't register** on this SDL2/Windows/DPI-virtualized window (clicks at both y=774 and y=968 didn't seek; tick kept playing) — environmental, not code; the slider mouse→seek chain is the 5 unit-tested path.
- **Env gotchas learned**: PrintWindow(PW_RENDERFULLCONTENT) renders the window regardless of virtual desktop but goes all-black after PostMessage mouse events; ImageGrab sees wallpaper when the window is on another Windows virtual desktop; demos launched via interactive_shell self-exit within minutes (20/20 alive, exit 0) — treat as short-lived, verify fast. Matplotlib deprecation warnings in visualizer.py:65-66 (`get_cmap`) — cosmetic, pre-existing.

## 2026-09-22: PO session — research paper + demo video + repo polish (all TODOs [x])

- **`docs/PAPER.md`** (new): 8–12 pp research paper — Abstract + 7 sections
  (intro, method, experimental design incl. v1→v2 instrument forensics,
  results §4.1–4.9, discussion, limitations, conclusion, data/code
  availability). Every number traced to a committed CSV. §4.8 ε-sweep table
  corrected to exact per-config values from `epsilon_sweep_tunnel.csv`
  (ε ∈ {0.05,0.1,0.2,0.3}; quantum q=0.3; median 1st-crossing latency 2.0 vs
  7.0–21.5 for the ε-arms; parity 100% never reached).
- **`examples/make_demo_video.py`** (new): headless tunnel sim → 3-segment
  video: (A) classical|quantum A/B, (B) P-key coherence/Φ overlay, (C) headline
  summary card → `demo_video.mp4` (21 s, h264) + `.gif` (both gitignored, like
  the tunnel GIFs). All 3 segments visually inspected.
- **Repo polish:** CLAUDE.md (phases 1–4 status, real module tree, key classes
  incl. `compute_phi_agents`, correct ablation cmd `run_ablation_study.py
  --runs 10`, null-hyp status = rejected 4/5), readme.md (deliverable
  checklist all [x], fresh start_here), QUICKSTART.md, PROJECT_STRUCTURE.md
  (module tree + phase status).
- **Verification:** compileall clean; `pytest tests -q` → **107 passed**; UI
  interactive (15 s headless, exit 124 = ran to timeout) + export (exit 0).
  No git remote configured, so push is a no-op. Tree clean.
- **PO decision:** the project's two headline deliverables (paper + demo video)
  are now DONE, on top of the settled phi story (§4i). Scope is closed except
  optional push (needs `git remote add origin …`) and future-work items
  (Numba JIT, larger worlds) that are documented, not in-scope.

## 2026-09-21 (2): PO session — Phi re-scope (P7) → §4i, formally retracted

- `compute_phi_agents` (src/core/coherence.py): re-scoped agent-in-the-loop,
  agent-localised Φ. Per agent, a (2·r+1)² window (r=4) around its *current*
  position; forward-sim `steps`=5 WITH the whole swarm stepping
  (sense/decide/move/collapse); max(0, corr(t0_R,t1_R) − corr(boundary_t0_R,t1_R))
  on the guidance field the agent perceives, averaged over agents. Deep-copies
  (world, agents). Wired behind `ExperimentConfig.phi_agent_in_loop` (default OFF
  → 400-run v2 dataset byte-identical). 5 new unit tests; suite 102→107 green.
- `examples/phi_rescope.py` → `phi_rescope.csv` (default, n=10, 500 steps,
  collapse ON). **RESULT: classical pinned 1.0000 (±0.0000); quantum 0.8740
  ±0.0125 (0.8546–0.8883). Ratio 0.874 — NOT MET vs 1.5×, DIRECTION REVERSED
  (quantum lower).** Moving scenario: classical 1.0000, quantum 0.4630±0.1965
  — same direction. Direction consistent across 3 probe designs (field-only
  1.000 §4e; swarm-centroid quantum-lower §4e; agent-local quantum-lower §4i).
- Instrument property (documented, not a finding): classical=1.0000 in every
  scenario because its perceived field is the deterministic potential, locally
  STATIC over the 5-step horizon → t0_R≡t1_R → self-predictability 1.0 (ceiling).
  Quantum <1.0 because the perceived guidance field adds the diffusive pilot-wave
  channel (gain 3000·normalize(pilot)), evolving → less self-predictable over 5
  steps. Magnitude partly a ceiling effect; DIRECTION is the robust signal.
- PO decision: **formally retract the "quantum Φ is 1.5× classical" threshold as
  stated; retain re-scoped Φ as a clean agent–world-coupling diagnostic**
  (instrumentation improvement — the original measured field self-organization,
  1.000, not coupling). Documented HONESTLY in RESULTS.md §4i + readme
  (threshold status + repro row). Paper carries it as an honest negative with a
  fixed instrument + consistent direction, not a silent null.

## 2026-09-21: PO session — ε-sweep curve (§4h) + tunnel demo GIFs

- `examples/epsilon_sweep_tunnel.py` → `epsilon_sweep_tunnel.csv`
  (7 arms × 10 seeds, tunnel/torus/v2 instrument): alive 0 → 48.0±7.8 →
  66.5±11.6 → 79.0±12.6 → 83.5±12.3 (ε→0.3). Parity with quantum
  (100±0, 20/20) NOT reached; latency quantum med 2.2 vs 11–28 ε-arms
  (5–12×); ε-taxonomy stable (77–84% wall walk-throughs, seam flat
  ~2/run, 2-cell jumps 0.3→1.6/run); interaction arm q=0.3/ε=0.1 benign
  (100%, 20/20 seam, med 2.7, overlapping seed ranges). Paper framing:
  the tradeoff is *route for the same price*, not parity. RESULTS.md
  §4h + §4b pointer.
- `examples/tunnel_demo_gif.py`: headless (SDL dummy) WorldVisualizer
  frame capture → animated GIF + optional PNG frames; configs quantum
  (q=0.3) / classical (q=0.0), v2 constants, 20 agents corner spawn,
  prewarm 2000. Final-frame check: quantum 20/20 alive @750 steps vs
  classical 0/20 — the A/B centerpiece. Artifacts:
  tunnel_demo_{quantum,classical}.gif (150f @12fps). pillow →
  requirements.
- **Bootstrap 95% CIs (P7 closed):** analyze_results.py gains
  bootstrap_ci/delta_ci (2000 resamples, fixed seed); the 95% CI column
  is on every summary alive-rate row and the Δ-mean 95% CI on all
  U-test comparisons (alive/energy/crossings). docs/RESULTS.md
  regenerated (interpretation §4a–§4h preserved).
- **Repro quickstart (P7 closed):** readme “Reproducing the headline
  numbers” table — every headline claim → exact command → CSV/section.
  All commands executed: 6 audit CSVs md5-stable on re-run; v2 + n50
  reproduce every headline rate (dead-end 0/194/132/77; §4a curve to
  3rd decimal). ε-sweep CLI → argparse; phase4_full_demo sys.path fix.
- **CI + energy budget + interactive UI (P7/P4 closed):**
  .github/workflows/ci.yml (pytest, SDL-dummy 15s smoke rc=124,
  --export; steps verified locally); energy_budget.py →
  energy_budget.csv (break-even net = h·S−50 per 50-step window);
  visualizer: L/R click-to-add, draggable coupling slider (live),
  K_r double-bind fix.
- Tests 81→102; UI smoke (interactive rc=124 + --export rc=0) clean.
  Remaining: phi re-scope; paper + demo video (dedicated sessions).

## 2026-08-20 (compressed): closed boundary + late metrics

- **Closed boundaries (§4g):** no channel penetrates an impenetrable
  barrier — without the torus seam quantum crosses 0/20 (0% alive);
  ε0.1 walk-throughs at 25% alive. Quantum value = exhaustive non-local
  exploration of locally invisible routes.
- **Path efficiency (§4f, 15% NOT MET):** quantum 0.5055 vs classical
  1.0207 (default); maze: classical 0/20 reached, quantum 20/20 @0.894.
- **Phi (§4e, 1.5× NOT MET):** ratio 1.000; phi measures field
  self-organization, not agent-world coupling.
- **Maze route audit (§4d):** quantum 20/20 reach via 100% edge wraps —
  same global-route mechanism.
- **Anticipation (§4c, honest null):** nobody anticipates; quantum
  monotonically reduces lag (index −4.09→−1.39, frac ahead 0→0.10).

## 2026-08-19 (compressed): the null hypothesis is dead

- v1 flat ablations = broken instrument (2%/step dissipation; q=0 agents
  ran the quantum sampler; unreachable dead-end trap). v2 instrument
  (gain 3000, dt 0.2, diss 0.9999, prewarm 2000, q=0 argmax guard):
  tunnel 0%→100% alive (p≤2.4e-5); maze/single_source 0%→100%; default
  45%→90%.
- Re-scoped (§4b): quantum tunnel crossings are 100% seam wraps —
  separates *determinism vs exploration*; ε-greedy leaks too. Moving:
  real monotone coupling-liability curve at n=50 (0.679@q=0.05 →
  baseline by q≥0.2) — interior optimum at weak coupling.
- Caveat: advantage magnitude instrument-dependent; 0%→100% contrast is
  not (structural −1e6 wall).
