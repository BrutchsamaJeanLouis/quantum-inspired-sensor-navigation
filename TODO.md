# QIWM — TODO

## Active PO session (2026-09-25 PM): applications section + repo tidy + GitHub + Zenodo + PDF

- [ ] **TODO 1 — Applications section in the paper** (docs/PAPER.md; confirmed it is the only paper; RESULTS.md is the appendix, readme.md is the plan)
  - Add a `## Applications` section (ranked most→least impactful) covering: (1) drop-in exploration channel for local-greedy nav agents (AMRs, game NPCs, multi-agent, routing); (2) the "is your baseline really a baseline?" instrument-forensics eval method; (3) sensor-vs-controller decomposition; (4) "completeness not directness" product framing; (5) coupling-liability auto-tune rule; (6) honest-nulls "when NOT to use" boundaries; (7) teaching/demo artifact; (8) reproducible benchmark. Tie each to the actual finding + a concrete deliverable.

- [ ] **TODO 2 — tidy repo + push to GitHub as `quantum-inspired-sensor-navigation`** (public, for SEO/research-discovery)
  - [ ] Tidy loose temp files: root has ~13 stray CSVs, 5 PNGs, 3 GIFs, 2 mp4s, logs, `__pycache__`, `.aider.*`, `.pytest_cache`, `.claude`, `.pi`, `.playwright-mcp`. Decide: keep the headline result artifacts (demo_video.mp4, the tunnel gifs) referenced in the paper; move scratch/temp out or gitignore; remove pure-temp (empty logs, __pycache__).
  - [ ] Create public GitHub repo `quantum-inspired-sensor-navigation` (browser, logged in), `git remote add origin`, `git push -u origin master` (GCM auth).

- [ ] **TODO 3 — generate paper.pdf + upload to Zenodo with SEO tags + cross-links**
  - [ ] Generate `docs/PAPER.pdf` (pandoc + xelatex, via pypandoc_binary) with the GitHub repo link in it.
  - [ ] Upload to Zenodo (browser, logged in): tags (quantum-inspired, navigation, robotics, path-planning, machine-learning, world-model, ablation, pilot-wave, ...), link GitHub repo, attach PAPER.pdf.
  - [ ] Cross-link: Zenodo DOI in the paper + GitHub repo in the paper + GitHub link on Zenodo.
  - [ ] Re-generate PDF after adding the Zenodo DOI link (so the PDF cites its own DOI), commit + push + update Zenodo.

## Prior sessions (all [x])
- [x] 2026-09-24: LLM tick controls (TimelinePlayer, --shot/--replay, slider) + render fixes; 120 tests.
- [x] 2026-09-25 AM: exhaustive tick verification (1a matrix, 1b live seek, 1c rewind consistency) + QUANTUM_ASSUMPTIONS_HISTORY.md (11-row assumption ledger). 120 tests.
