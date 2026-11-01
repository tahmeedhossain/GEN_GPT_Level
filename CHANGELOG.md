# Changelog — Nonclassicality Network (GEN_GPT_Level)

Every released version stays online unchanged; a correction is a new version alongside. Content versions
change the network; presentation variants change only how it is read.

## v2.6 — 2026-11-01 (current; `v26.html`, `data/network_v2.6.json`)

Round 4, run for the combined paper *The Great Epistemic Network* with the literature searched **before**
each proof (proofs: `catalog/network_catalog_v2.6_round4.md`).

- New edges (8): **U1** `p-cov → e-ctx` (implies, derived; the covariant/TTS fragment is noncontextual iff H is
  nondegenerate; closes SG1), **U2** `p-filter → e-ctx` (not_implies, derived; contextuality with all measurements
  is invariant under invertible filters; closes SG5 at the level of models), **U3** `m-stab-odd → e-steer`
  (implies, derived), **U4** `s-tts → s-magic` (forbids, derived), **U5** `p-cov → s-magic` (hides, derived),
  **U5b** `p-thermalops → s-magic` (implies, theorem: de Oliveira Junior et al., arXiv:2511.13839),
  **U6** `s-zerodisc → e-ctx` (forbids, theorem: Plávala–Gühne Thm. 2, with a direct proof),
  **U7** `s-discord → e-ctx` (not_implies, counterexample).
- Corrected kind: **A5** `excludes` → `forbids` (contextual ⇒ not simplicial; the biconditional is refuted by the toy theory).
- Appended scope notes: **D2**, **R2**, **N1** (tomographically complete convention; N1 converse = U1), **GN5** (necessity only),
  **R1** (coherence and entanglement, not discord, are confined to degeneracy blocks), **R6** (Sorkin's setting; SG4 = binary toy theory),
  **A7** (status note: composed corollary), **P7** (reference: Hirsch et al. 2013).
- Witness records: `w-magicw` blind on `s-tts` and `p-cov` (H nondegenerate with a stabilizer eigenbasis; U4, U5);
  `w-ncineq` blindness note on `p-cov` extended to the degenerate case (U1).
- Gaps: SG1 closed; SG5 closed at the level of models; P4 note (DV instance U3); SG4 scope; new **SG6**, **SG7**.
- Census: 156 edges (101 possibility, 45 no-go, 10 open); 469 / 3,094 witness-matrix cells settled; 4,049 of 4,186 node pairs unconnected.
- Landing page and README: the stale polarity census 35 / 96 / 10 (the v2.3 counts) corrected to 40 / 98 / 10 for v2.4;
  v1 described as 84 edge records (10 of them open problems) instead of "81 edges".

## 2.5 — 2026-10-23 (citation-file release; `v1b.html`, `v2b.html`)

Presentation variants of v1 and v2.4: plain-language readings with conditions on every edge
(`data/plain_readings.json`); on v2b, state → process → witness pathway overlays, a path finder, the pathway rows
K11 and K18, and the round-3 before/after toggle (141 ↔ 148 edges). Networks unchanged.

## v2.4 — 2026-10-23 (`v2.html`, `data/network_v2.json`)

Round 3: edges R1–R6 (seven records, R4 in two parts) generated from uncharted cells; gaps SG4–SG5. 148 edges; 445 / 3,094 cells settled.

## v2.2–2.3 — 2026-10-21

Signed semantics: the exclusion kind (X ⇔ ¬Y) and the hosting kind; impossibility edges drawn with flat-bar terminators
and polarity filters; machine-readable polarity metadata. 141 edges.

## v2.0 — 2026-10-21

Layered form: seven node types (genesis axioms, models, state clusters, process clusters, witnesses, effects, tasks);
structured witness records; the state × process verdict matrix; N1, N2; genesis edges; gaps SG1–SG3.

## v1 — 2026-10-20 (`v1.html`, `data/network_v1.json`)

Flat graph: five node types, 84 edge records (10 of them registered open problems occupying an edge), propositions
P1–P4, gaps G1–G10.
