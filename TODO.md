# TODO.md — QIWM

## Active PO session (2026-09-24): LLM-driven tick control + render fixes
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
