# QIWM TODO

## Active — PO session (2026-09-21): Phi re-scope (P7)

**PO decision:** the one open scientific question is the phi threshold (§4e, ratio
1.000 vs 1.5×). Root cause (diagnosed, not fudge): `compute_phi` runs an
*agent-less* forward sim on a *fixed central region* the agents never occupy →
it measures FIELD self-organization, not agent–world coupling. Implement the
principled re-scope the backlog names (agent-in-the-loop + agent-localized),
define it BEFORE looking at the number, run the n=10 audit, report direction
honestly (met, or formally retracted as a clean diagnostic). Keep the 400-run
v2 dataset untouched (new config flag, default OFF).

- [x] `compute_phi_agents(world, agents, local_radius, steps)` in src/core/coherence.py
      — agent-in-the-loop forward sim (agents sense/decide/move/collapse), per-agent
      localized probe regions, averaged. Deep-copies (world, agents) pair.
- [x] `ExperimentConfig.phi_agent_in_loop` (default False) + `phi_agent_samples` metric
      in src/core/experiments.py; wire `phi_agent_mean`/`phi_agent_final` into to_dict().
- [x] Unit test in tests/test_coherence.py (5 new, suite 102→107).
- [x] `examples/phi_rescope.py` audit (default scenario, q=0 vs q=0.3, n=10, 500 steps,
      sample every 100) → `phi_rescope.csv`; print ratio + direction vs 1.5× threshold.
- [x] Run smoke (1 seed) then full audit; record result.
- [x] Update docs/RESULTS.md (new §4i) + readme + TODO + scrapbook HONESTLY.
- [x] Full test suite (107 green) + UI smoke clean; commit.

**RESULT (honest):** Re-scoped agent–world-coupling Φ — classical pinned 1.0000
(its perceived field is locally static → self-predictability 1.0, an instrument
property), quantum 0.8740±0.0125 (default) / 0.4630±0.1965 (moving). Ratio
0.874, **NOT MET** vs 1.5×, **direction REVERSED** (quantum lower). Consistent
across 3 probe designs. 1.5× "quantum higher" threshold **formally retracted as
stated**; re-scoped Φ retained as a clean coupling diagnostic (instrumentation
improvement — it now measures coupling, not field self-organization 1.000).

## Deferred (dedicated sessions)
- [x] Research paper (8-12 pages) → `docs/PAPER.md` (draft complete, ~4.2k words,
      Abstract + 7 sections + data/code availability; ε-sweep table verified
      against epsilon_sweep_tunnel.csv). Story: forensics → tunnel → collapse
      ablation → moving null → phi re-scope (§4i).
- [x] Demo video → `examples/make_demo_video.py` → `demo_video.mp4` (21s, h264,
      250 frames) + `demo_video.gif`. 3 segments: (A) tunnel A/B classical|quantum,
      (B) P-key coherence/Φ overlay, (C) headline summary card. Verified all 3
      frames render correctly.
- [x] GitHub repo polish: CLAUDE.md (status/phases/structure/classes/commands/
      refs/null-hyp), readme.md (deliverable checklist [x], start_here),
      QUICKSTART.md (What's Working/Next), PROJECT_STRUCTURE.md (module tree +
      phase status). All referenced docs verified to exist; ablation cmd fixed
      to `run_ablation_study.py --runs 10 --output ablation_results_v2.csv`.

## Completed
(see git log; prior sessions) — Phases 1–5 code, v2 ablations (null H₀ rejected 4/5),
tunnel ε-sweep, tunnel demo GIFs, bootstrap CIs, CI workflow, energy budget,
interactive UI, repro quickstart. **Phi re-scope (this session, §4i):** agent-in-
the-loop, agent-localised coupling Φ — formally retracted the 1.5× "quantum higher"
threshold (direction reversed, quantum 0.874 vs classical 1.000 default). 107 tests green.
