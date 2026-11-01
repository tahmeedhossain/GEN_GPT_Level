# Nonclassicality Network — catalog v2.6: round 4 and scope corrections

Date: 2026-11-01. Data: `data/network_v2.6.json` (page `v26.html`). Base: v2.4 (`data/network_v2.json`, page `v2.html`, both unchanged).
The same results, with the same proofs, are in Sec. 8.7 of the combined paper *The Great Epistemic Network* (T. Hossain, 2026).

## Method of this round

A relation that the compiled literature establishes is recorded as an edge, so an unconnected pair of nodes is a question the
compiled literature does not answer. For every pair below the literature was **searched before a proof was attempted**:

- a result found in the literature is recorded as a literature edge (status `theorem`) and counted as a correction of the curation;
- a result not found is proved and recorded with status `derived` and the search date — "not found on 2026-11-01", never a priority claim.

The pairs were chosen by judgement, not by a script. Starting points: the registered problems SG1 and SG5, and the pairs flagged as
natural next questions in v2.4 — (`p-filter`, `e-ctx`) and (`p-cov`, `s-magic`); (`s-athermal`, `e-ctx`) was not attempted. Further
pairs arose while closing these. The proofs were checked by a separate AI instance that had not written them; that check is a
mitigation, not an expert referee's verification.

Census v2.4 → v2.6: 148 → 156 edges (98 → 101 possibility, 40 → 45 no-go, 10 open); 4056 → 4049 unconnected node pairs of 4186;
witness-matrix cells settled 445 → 469 of 3094 (w-magicw gains the blindness records of U4/U5); gap records 21 → 23.

## Conventions

- **Operational equivalence.** (a) *Accessible-fragment convention*: preparations are equivalent when every measurement in the fragment
  gives them the same statistics; effects when every preparation in the fragment gives them the same probability. (b) *Tomographically
  complete convention*: equivalence is judged against all preparations and measurements of the theory (in quantum theory: density
  operators and POVM elements). Mixtures of procedures are represented by mixtures of their distributions or response functions.
- **TTS / covariant.** `U_t = exp(−iHt)`, spectral projectors `Π_k`; `X` is TTS iff `[X,H] = 0`; `T` is covariant iff
  `T(U_t X U_t†) = U_t T(X) U_t†`; dephasing `D(X) = Σ_k Π_k X Π_k` (= the time average of `U_t X U_t†`).
- **Dephasing lemma.** (i) `D(X) = X` iff `X` is TTS; (ii) for nondegenerate `H` the TTS operators are the operators diagonal in the
  energy basis; (iii) if `T` is covariant then `T†(U_t† E U_t) = U_t† T†(E) U_t`, so `T†` maps TTS effects to TTS effects.

---

## U1 — the covariant fragment is noncontextual iff H is nondegenerate (closes SG1; refines N1)

**Theorem.** Let `H` have eigenspaces `H_k` of dimensions `d_k`. Let `F_H` be the prepare–measure fragment whose preparations are all
states and whose effects are `T†(E)` with `T` covariant and `E` TTS.

1. `Tr(E T(ρ)) = Tr(E T(D(ρ)))` for every `ρ`, and the effects of `F_H` are exactly the TTS effects; so `F_H` has the statistics of
   quantum theory on each `H_k` with a classical label `k`.
2. `F_H` admits a generalized-noncontextual model (under (a) or (b)) iff every `d_k = 1`, i.e. iff `H` is nondegenerate.
3. If some `d_k ≥ 2`, preparation contextuality is exhibited with `T = id` by six pure states and three TTS projective measurements
   inside `H_k`.

**Proof.** (i) The proof of N1(i) uses only lemma parts (i) and (iii), valid for every `H`. Every TTS effect `F` is `T†(F)` with
`T = id`. A TTS operator is block diagonal, so `Tr(Fρ) = Tr(F D(ρ))` with `D(ρ) = Σ_k p_k ρ_k`.

(ii) "If": under (b) this is N1(ii). Under (a), two preparations are equivalent iff they have the same energy-basis diagonal, and two
TTS effects iff they have the same diagonal; the quotient is the classical simplex on `d` points with all its effects. "Only if" is (iii).

(iii) Take a 2-dimensional `V ⊆ H_k` with basis `|0⟩, |1⟩`, and `|ψ_j⟩ = cos(θ_j/2)|0⟩ + sin(θ_j/2)|1⟩`, `θ_j = (j−1)π/3`,
`P_j = |ψ_j⟩⟨ψ_j|`, `j = 1..6`. Then `|⟨ψ_i|ψ_j⟩|²` is 0 for `j = i±3`, 3/4 for `j = i±1`, 1/4 for `j = i±2` (mod 6).
The measurements `M_ℓ = {P_ℓ, P_{ℓ+3}, 1 − Π_V}`, `ℓ = 1,2,3`, consist of TTS effects (`H` is a scalar on `H_k`). The three mixtures
`½(P_1+P_4) = ½(P_2+P_5) = ½(P_3+P_6) = Π_V/2` are the same operator, hence equivalent under (b), and under (a) because every TTS effect
is in the fragment. In a preparation-noncontextual model put `ν = ½(μ_1+μ_4) = ½(μ_2+μ_5) = ½(μ_3+μ_6)`. Since
`∫ξ_{P_ℓ} dμ_ℓ = 1` and `∫ξ_{P_ℓ} dμ_{ℓ+3} = 0`, the sets `S_ℓ = {ξ_{P_ℓ} = 1}` and `S_{ℓ+3} = {ξ_{P_ℓ} = 0}` are disjoint,
`μ_ℓ(S_ℓ) = μ_{ℓ+3}(S_{ℓ+3}) = 1`, and `ν(S_ℓ ∪ S_{ℓ+3}) = 1`; so `a = 1_{S_1}`, `b = 1_{S_2}`, `c = 1_{S_3}` are binary random
variables on `(Λ, ν)`. Then `ν(a=b=1) = ½μ_1(S_2) = ½Tr(P_2P_1) = 3/8` and `ν(a=b=0) = ½μ_4(S_5) = ½Tr(P_5P_4) = 3/8`, so
`ν(a=b) = 3/4`; likewise `ν(b=c) = 3/4` and `ν(a=c) = ½[Tr(P_3P_1) + Tr(P_6P_4)] = 1/4`. But `ν(a≠c) ≤ ν(a≠b) + ν(b≠c)`, i.e.
`3/4 ≤ 1/4 + 1/4` — a contradiction. Only preparation noncontextuality is used. (Six-state proof: Spekkens, PRA 71, 052108 (2005);
Mazurek et al., Nat. Commun. 7, 11780 (2016).) ∎

**Reading.** Time-translation symmetry hides exactly the contextuality carried by coherences *between* eigenspaces and none *inside* an
eigenspace. Search 2026-11-01: no prior statement found; the ingredients are standard.

---

## U2 — local filters cannot create or destroy generalized contextuality (pair `p-filter`–`e-ctx`; closes SG5 at the level of models)

**Theorem.** Let `S` be a convex set of states and `A` invertible; `S_A = {AσA†/Tr(AσA†) : σ ∈ S}`. Under (b), `(S, all POVMs)` has a
preparation-and-measurement noncontextual model iff `(S_A, all POVMs)` does. Hence for invertible local filters `A ⊗ B` the
remote-preparation scenario `(Λ_A(ρ'), all POVMs)` of the filtered state is contextual iff that of `ρ` is.

**Proof.** A noncontextual model is `(μ_σ, ξ_E)` with `μ` affine in `σ`, `ξ` affine in `E` (hence extendable to a positive linear map
on the positive cone), `ξ_1 = 1`, `∫ξ_E dμ_σ = Tr(Eσ)`. Let `n(σ) = Tr(A†Aσ) > 0`. For `σ' = AσA†/n(σ)` define
`μ'_{σ'} = ξ_{A†A} μ_σ / n(σ)` and `ξ'_M = ξ_{A†MA}/ξ_{A†A}` where `ξ_{A†A} > 0` (`Tr(M)/dim` elsewhere). `μ'` is a probability
measure; `0 ≤ ξ_{A†MA} ≤ ξ_{A†A}` gives `ξ'_M ∈ [0,1]`; `ξ'` is affine with `ξ'_1 = 1`; statistics: `∫ξ'_M dμ'_{σ'} =
Tr(A†MAσ)/Tr(A†Aσ) = Tr(Mσ')`. Affinity of `μ'` on `S_A`: a mixture `pσ'_1 + (1−p)σ'_2` equals `AωA†/n(ω)` with
`ω = [(p/n_1)σ_1 + ((1−p)/n_2)σ_2]/t`, `t = p/n_1 + (1−p)/n_2`, `n(ω) = 1/t`, and `μ'` of it is `pμ'_1 + (1−p)μ'_2`. Measurement
noncontextuality: `ξ'_M` depends only on `M`. Converse: apply with `A⁻¹`. Remote preparation: `Tr_B[(1⊗E_B)ρ'] =
A Tr_B[(1⊗B†E_B B)ρ] A†/N`, and `E_B ↦ B†E_B B` is a bijection of the positive cone, so `Λ_A(ρ') = Λ_A(ρ)_A`. ∎

**Corollary U2′.** For states that are local for all POVMs yet become CHSH-violating after an invertible local filter (Hirsch,
Quintino, Bowles, Brunner, PRL 111, 160402 (2013)), the remote-preparation scenario is contextual before and after filtering
(Plávala–Gühne, PRL 132, 100201 (2024), Thm. 1): hidden nonlocality is visible as contextuality without a filter.

**What filters can change** is which fixed witness detects contextuality (Kumari, Patra, arXiv:2504.18045: a parity-oblivious
random-access-code witness switches under filtering) — a witness-level statement, registered as SG7. The hypothesis "all measurements"
is essential. Search 2026-11-01: invariance statement not found.

---

## U3 — the odd-dimensional stabilizer subtheory is EPR-steerable (pair `m-stab-odd`–`e-steer`)

**Proposition.** For odd `d ≥ 3`, the stabilizer subtheory contains a state, Alice measurements and Bob effects (all stabilizer
objects) whose assemblage has no local-hidden-state model with quantum hidden states, although the subtheory has a nonnegative,
noncontextual representation (Gross; edge C5).

**Proof.** `|Φ⟩ = d^{-1/2} Σ_j |jj⟩`; Alice measures `Z` (basis `|a⟩`) or `X` (basis `|x_b⟩ = d^{-1/2} Σ_j ω^{bj}|j⟩`). Bob's
conditional states: `σ_{a|Z} = |a⟩⟨a|/d`, `σ_{b|X} = |x_{−b}⟩⟨x_{−b}|/d`. The functional
`S = Σ_a Tr(σ_{a|Z}|a⟩⟨a|) + Σ_b Tr(σ_{b|X}|x_{−b}⟩⟨x_{−b}|) = 2`, while any LHS model gives
`S ≤ max_{a,b} λ_max(|a⟩⟨a| + |x_b⟩⟨x_b|) = 1 + 1/√d < 2`. ∎ (The argument works for every `d ≥ 2`; oddness is needed only for the
nonnegative representation.)

**Reading.** The Gross representation is itself an LHS model with phase-space points as hidden states; steering is relative to the
class of hidden states admitted. DV companion of F2 (Gaussian QM). Search 2026-11-01: not found as a property of the noncontextual subtheory.

---

## U4 — symmetric states are magic-free iff H is nondegenerate with a stabilizer eigenbasis (pair `s-tts`–`s-magic`)

**Proof.** Nondegenerate `H`: TTS states are mixtures of eigenprojectors — in STAB if all eigenvectors are stabilizer states; if one
is not, its projector is a TTS magic state (a pure state in a finite convex hull equals a vertex). Degenerate `H`: an eigenspace of
dimension ≥ 2 holds a continuum of pure TTS states and only finitely many stabilizer states. ∎

## U5 — covariant probing is blind to magic; covariant dynamics creates it (pair `p-cov`–`s-magic`)

**Proposition.** For `H` nondegenerate with a stabilizer eigenbasis: (i) every experiment of covariant transformations and TTS effects
has the statistics of the stabilizer state `D(ρ)` (U1(i) + U4), so no such magic witness certifies magic; (ii) covariant dynamics
creates magic: `H = Z` on a qubit, `exp(−iZπ/8) ∝ T` maps `|+⟩` to Bloch vector `(1,1,0)/√2`, outside the octahedron `|x|+|y|+|z| ≤ 1`. ∎

## U5b — literature fill: thermal operations generate magic (pair `p-thermalops`–`s-magic`; instance IV: edge C20)

de Oliveira Junior, Macedo, Czartowski, Brask, Chaves, *Trading athermality for nonstabiliserness*, arXiv:2511.13839 (2025): for a
qubit prepared in a stabilizer state and coupled to a heat bath: a necessary and sufficient condition for nonstabiliserness to be
generated under thermal operations, an analytic characterisation of the reachable nonstabiliser states with bounds on their
nonstabiliserness, the Hamiltonians that maximise generation, and the critical temperatures at which it emerges; for energy-diagonal
inputs, a Hamiltonian aligned with a stabilizer direction generates no magic (consistent with U4; for a coherent stabilizer input this
cannot hold, since `exp(−iZπ/8)` is itself a thermal operation, U5(ii)). arXiv record and text checked 2026-11-01.

*Relation to QP5 of the resource network (ours, elementary).* Complete thermalisation is a thermal operation, so the Gibbs-state
statement QP5 lies within the question of the preprint: the Gibbs state of `H = −(ω/2) n̂·σ⃗`, `n̂ = (1,1,1)/√3`, has Bloch vector
`tanh(βω/2) n̂` and is a magic state iff `tanh(βω/2) > 1/√3`. This statement was not found in explicit form in the preprint.
(A first version of this record, 2026-11-01, attributed to the preprint a free-energy bound and this Gibbs-state threshold; neither
is in its main text.)

---

## U6 — zero discord on the steered side gives an exactly noncontextual remote-preparation scenario (pair `s-zerodisc`–`e-ctx`; literature + direct proof)

If `ρ_AB = Σ_i p_i |i⟩⟨i| ⊗ τ_i`, then `Tr_B[(1⊗E_B)ρ] = Σ_i p_i Tr(E_B τ_i)|i⟩⟨i|` is diagonal, and the P2 model (ontic `i`,
`μ_σ(i) = ⟨i|σ|i⟩`, `ξ_E(i) = ⟨i|E|i⟩`) is noncontextual under (b). Case of Plávala–Gühne Thm. 2. Under (a) the statement fails
(a classical–classical example on C⁴⊗C⁴ with a square of remote preparations exists).

## U7 — among separable states, remote-preparation contextuality requires but is not implied by steered-side discord (pair `s-discord`–`e-ctx`; counterexample)

Under (b): (i) contextual ⇒ discord on A (contrapositive of U6). (ii) `½(|0⟩⟨0|⊗|0⟩⟨0| + |+⟩⟨+|⊗|1⟩⟨1|)` is discordant on A, but
`Λ_A` is the segment `[|0⟩⟨0|, |+⟩⟨+|]`, simplex-embeddable via `ι = (p, 1−p)`, `κ(E) = (⟨0|E|0⟩, ⟨+|E|+⟩)`. (iii) Plávala–Gühne's
Eq. (4) state gives `Λ_A = conv{0,1,+,−}`: encode `00,11,01,10 ↦ 0,1,+,−` (parity-oblivious since `½(P_0+P_1) = ½(P_+ + P_−)`);
measuring `(Z±X)/√2` wins with `cos²(π/8) > 3/4`, the preparation-noncontextual bound (Spekkens et al., PRL 102, 010401 (2009)).
New gap **SG6**: a structural criterion for which steered-side sets are simplex-embeddable.

---

## Scope corrections recorded in v2.6 (combined paper, corrections C7–C13)

| Record | Correction |
|---|---|
| A5 | Kind `excludes` (biconditional "contextual ⇔ not simplicial") → `forbids` ("contextual ⇒ not simplicial"); the toy theory is non-simplicial and noncontextual. v1 had `equiv`, same overstatement. (C13) |
| D2 | Holds under (b); diagonal *states* suffice; fails under (a): four diagonal states with commuting effects `P1+P2`, `P1+P3` are preparation contextual. (C7) |
| N1 | Noncontextuality claim under (b); converse appended (U1): sharp for nondegenerate `H`. (C7) |
| R2 | The clause "commutativity reproves N1's blindness" holds under (b) only. (C7) |
| GN5 | Proved as necessity (quadratic generators preserve Wigner positivity), not "exactly the generators". (C8) |
| R1 | Coherence and entanglement live in degeneracy blocks; discord does not. (C10) |
| R6 | `I3 = 0` in Sorkin's setting only; SG4 concerns the binary toy theory. (C11) |
| A7 (P1) | Status note: a one-step composition of two published theorems — a composed corollary, not a new result. |

## Gap records changed

- **SG1** closed by U1. **SG5** closed at the level of models by U2. **P4** gains the DV instance U3.
- **SG6** (new): separable states with contextual remote-preparation scenarios — a structural criterion.
- **SG7** (new): witness-level activation of contextuality by filters — how robustness depends on the filter.
