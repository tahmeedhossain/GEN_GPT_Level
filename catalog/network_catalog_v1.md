# Epistemic network of quantum foundations: GPT axioms, models, state properties, observable effects

**Companion catalog to `gpt_effects_network.json` and the interactive network page. 2026-10-20.**

Scope: quantum foundations, quantum information, quantum thermodynamics and resource theories, organized as a typed graph in the style of the project's observable–model–state networks:

- **Axiom nodes** (model-level assumptions on a generalized probabilistic theory, GPT): no-signalling, local tomography, purification, no-restriction, information causality, macroscopic locality, local orthogonality, Sorkin truncation, decoherence-to-classical.
- **Model nodes** (specific theories/subtheories): classical, quantum, real-amplitude QM, boxworld, Spekkens/epistricted theories, odd-d and even-d stabilizer subtheories, Gaussian QM, separable quantum theory, the almost-quantum set.
- **State-property nodes**: entanglement, bound entanglement, Wigner negativity, magic, coherence/superposition, discord, athermality, asymmetry, ψ-epistemic status.
- **Effect nodes** (operational phenomena): Bell violation, steering, incompatibility, KS contextuality (state-independent and state-dependent), generalized (Spekkens) contextuality, no-broadcasting, second- and higher-order interference, anomalous weak values, Kirkwood–Dirac nonpositivity, anomalous work/heat, PR correlations.
- **Task nodes** (operational witnesses/advantages): DI and 1sDI cryptography, BB84, parity-oblivious multiplexing/RACs, universal QC by state injection/MBQC, state discrimination, postselected metrology, entanglement witnessing, deciding the quantum set, second laws/work extraction.

Edge kinds: `implies`, `equiv`, `necessary` (target requires source), `not_implies` (counterexample), `enables`, `forbids`, `witness`, `open`. Statuses: `theorem` (published, verified here against the literature), `partial` (holds under stated conditions), `counterexample`, `example`, `derived` (proved in §3 below from cited theorems), `conjecture`/`open`.

Honesty note: every `theorem` edge carries a citation that I checked against the literature during compilation (titles/venues verified by search on 2026-10-20 for the 2020–2026 results and for all load-bearing older ones). Where I was not fully certain of a page number I cite journal+year and/or arXiv ID. `derived` items are proved below and are **not** claimed to be in the literature — adjacent known results are cited for each.

---

## 1. The backbone: what "classical" means, once and for all

The modern consensus, which the network is organized around, is that all of the following are **equivalent characterizations of nonclassicality of a single GPT system**, each discovered separately and later unified:

| # | Nonclassicality criterion | Equivalence theorem |
|---|---|---|
| 1 | State space is not a simplex | definition |
| 2 | Incompatible measurements exist | Plávala, PRA 94, 042108 (2016); Kuramochi (arXiv:1912.00563) |
| 3 | Broadcasting is impossible (no-cloning) | Barnum–Barrett–Leifer–Wilce, PRL 99, 240501 (2007) |
| 4 | "Superposition" (strong incompatibility) exists | Aubrun–Lami–Palazuelos–Plávala (ALPP), PRL 128, 160402 (2022) |
| 5 | The system can be **entangled** with any other nonclassical system | ALPP, Geom. Funct. Anal. 31, 181 (2021) — "entangleability of cones" |

Crucially, **generalized (Spekkens) contextuality is strictly stronger** than 1–5: it is equivalent to failure of *simplex-embeddability* (Schmid–Selby–Wolfe–Kunjwal–Spekkens, PRX Quantum 2, 010331 (2021)), and a GPT can be nonsimplicial yet simplex-embeddable (Spekkens' toy theory). So the network has **two concentric classicality boundaries**:

```
simplex  ⊂  simplex-embeddable (noncontextual)  ⊂  all GPTs
   |                 |                                  |
 no incompatibility, toy theory, Gaussian QM,        quantum,
 no entangleability, odd-d stabilizer live here      boxworld, ...
 no superposition
```

Everything in the inner shell has *no* incompatibility, cloning, entangleability or superposition. Everything in the middle shell can have incompatibility, superposition, entanglement-like correlations, ensemble steering, interference, no-cloning, teleportation analogues — **and still be noncontextual**. Only outside the middle shell do negativity, generalized contextuality, anomalous weak values, computational speedup (in the state-injection sense) and Bell violations live.

This two-boundary picture is what resolves most of the "does X imply Y?" questions below.

## 2. Verified edge catalog (selection, grouped)

The full machine-readable list with statements is in `gpt_effects_network.json`; here are the clusters with commentary.

### 2.1 GPT-level equivalences and preconditions

- **Incompatibility ⇔ nonclassical** (Plávala 2016; Kuramochi 2020 for the infinite-dimensional Choquet case).
- **No-broadcasting ⇔ nonclassical** (BBLW 2007); refined 2024: **no-broadcasting characterizes operational contextuality** (PRL 133, 240201 (2024); arXiv:2406.07305) — broadcastability of the accessed fragment corresponds exactly to the existence of a noncontextual model. These are different theorems at different granularities (theory-level vs fragment-level), and the network keeps both edges.
- **Entangleability of cones** (ALPP, GAFA 2021): min⊗ = max⊗ iff one cone is classical. Physical reading: *any two nonclassical systems can be entangled*. Strengthened (ALPP, PRL 2022): nonclassicality ⇔ strong incompatibility ("superposition") ⇔ entangleability (entangled states **or** entangled measurements), and superposition alone suffices to run BB84.
- **Noncontextual ⇔ simplex-embeddable** (SSWKS, PRX Quantum 2021; Shahandeh, PRX Quantum 2, 010330 (2021)); ⇔ **existence of a nonnegative quasiprobability representation** (Spekkens, PRL 101, 020401 (2008); structure theorem arXiv:2005.07161). Dimension bounds that make this a finite linear program: Selby–Wolfe–Schmid–Sainz–Rossi (arXiv:2204.11905) and accessible-fragment theory (arXiv:2112.04521).
- **Contextuality is a precondition for entanglement** (Plávala–Gühne, PRL 132, 100201 (2024)): entanglement in a nonlocal scenario exists only if the remote-state-preparation sequential scenario is preparation-and-measurement contextual; noncontextuality inequalities ↔ entanglement witnesses. (Complementary converse-direction corollary derived in §3.1.)
- **Incompatibility is neither necessary nor sufficient for generalized contextuality** (Selby–Schmid–Wolfe–Sainz–Kunjwal–Spekkens, PRL 130, 230201 (2023); single-projective-measurement CV version arXiv:2601.14067). But **with all quantum states available, incompatibility ⇔ steering ⇔ contextuality** (Tavakoli–Uola, PRR 2, 013011 (2020)). The apparent tension is scoping: fragment-relative vs full-state-space statements. Both edges are kept, with conditions.

### 2.2 Quantum correlation hierarchy

- Bell ⊊ steering ⊊ entanglement (Wiseman–Jones–Doherty, PRL 98, 140402 (2007)).
- Pure entangled ⇒ Bell-violating (Gisin, PLA 154, 201 (1991); Popescu–Rohrlich, PLA 166, 293 (1992)); mixed entangled ⇏ (Werner, PRA 40, 4277 (1989); Barrett, PRA 65, 042302 (2002) for POVMs); but all entangled states win semiquantum games (Buscemi, PRL 108, 200401 (2012)); activation by filtering (Popescu PRL 74, 2619 (1995); Hirsch et al., PRL 111, 160402 (2013)) and by copies (Palazuelos, PRL 109, 190401 (2012)).
- Steering ⇔ incompatibility of the steering party's measurements (Quintino–Vértesi–Brunner, PRL 113, 160402 (2014); Uola–Moroder–Gühne, PRL 113, 160403 (2014); one-to-one: Uola et al., PRL 115, 230402 (2015)).
- Incompatibility necessary for Bell (Fine, PRL 48, 291 (1982)); any incompatible dichotomic *pair* violates CHSH (Wolf–Pérez-García–Fernández, PRL 103, 230402 (2009)); incompatible *sets* need not violate anything (Bene–Vértesi, NJP 20, 013021 (2018); Hirsch–Quintino–Brunner, PRA 97, 012129 (2018)).
- Bound entanglement: PPT ⇒ undistillable (Horodecki³, PRL 80, 5239 (1998)); **Peres conjecture false** — PPT states violating Bell inequalities exist (Vértesi–Brunner, Nat. Commun. 5, 5297 (2014)); PPT states can steer (Moroder et al., PRL 113, 050404 (2014)). **NPT bound entanglement: open since 1998.**
- Witness/complexity layer: witnesses complete by Hahn–Banach (Horodecki³ 1996; Terhal 2000) but separability is NP-hard (Gurvits, STOC 2003); quantum set not closed (Slofstra, Forum Math. Pi 2019); MIP* = RE ⇒ approximating quantum values undecidable, Tsirelson's problem and Connes embedding negative (Ji–Natarajan–Vidick–Wright–Yuen 2020).
- Composite-KS: multiqubit logical KS proofs need entangled measurements, statistical ones need entangled states (Wright–Kunjwal, Quantum 7, 900 (2023)); invertible Bell↔contextuality scenario map (Wright–Farkas, PRL 131, 220202 (2023)); contextuality→nonlocality conversions (Cabello, PRL 127, 070401 (2021)); contextuality–nonlocality monogamy (Kurzyński–Cabello–Kaszlikowski, PRL 112, 100401 (2014)).

### 2.3 Negativity, magic, contextuality, computation

- **Odd prime d**: state-dependent contextuality w.r.t. stabilizer measurements ⇔ discrete Wigner negativity (Howard–Wallman–Veitch–Emerson, Nature 510, 351 (2014)). **CV**: contextuality ⇔ Wigner negativity for CV Pauli/quadrature measurements (Booth–Chabaud–Emeriau, PRL 129, 230401 (2022)). *This is the user's "Wigner negativity creates state-dependent contextuality" edge — it is a theorem, with these exact scopes.*
- Nonnegative Wigner ⇒ efficient classical simulation (Veitch et al., NJP 14, 113011 (2012); Mari–Eisert, PRL 109, 230503 (2012)); magic necessary for state injection (Bravyi–Kitaev, PRA 71, 022316 (2005); resource theory: Veitch et al., NJP 16, 013009 (2014)).
- **Stabilizer classification** (Schmid–Du–Selby–Pusey, PRL 129, 120403 (2022)): odd d — unique nonnegative diagram-preserving representation = Gross Wigner = Spekkens epistricted theory (so noncontextuality *singles out one classical model*); even d — none exists, the qubit stabilizer subtheory is generalized-contextual. Corollary: **generalized contextuality is necessary for universal QC in the state-injection model**, all dimensions.
- **Caveat edge** (Zurel–Okay–Raussendorf, PRL 125, 260404 (2020); + Heimendahl, Quantum 8, 1323 (2024)): a nonnegative probabilistic hidden-variable model *does* cover universal QCM for qubits and all qudits. No contradiction: the model is not diagram-preserving/noncontextual. Lesson encoded in the network: *negativity is representation-relative; generalized contextuality is the invariant notion.*
- KD nonpositivity ⇒ contextuality within its validity scope; anomalous weak values are proofs of contextuality (Pusey, PRL 113, 200401 (2014)); scope caveats for generalized KD representations (Schmid–Baldijão–Yīng–Wagner–Selby, arXiv:2405.04573); KD review: Arvidsson-Shukur et al., NJP 2024 (arXiv:2403.18899); KD negativity → postselected metrology (Arvidsson-Shukur et al., Nat. Commun. 11, 3775 (2020)); claimed necessary for quantum computing (arXiv:2506.08092).
- Contextuality → tasks: POM (Spekkens et al., PRL 102, 010401 (2009)), state discrimination (Schmid–Spekkens, PRX 8, 011015 (2018)), MBQC (Raussendorf, PRA 88, 022322 (2013); Anders–Browne, PRL 102, 050502 (2009)), shallow circuits (Bravyi–Gosset–König, Science 362, 308 (2018)), entanglement-assisted one-shot communication (Kunjwal, Quantum 6, 839 (2022)).

### 2.4 Coherence (and the correction to the second proposed edge)

The user proposed: *"coherence in states ensures state-dependent contextuality and vice versa."* The verified status is asymmetric:

- **Necessity holds** (and is made precise as Proposition P2 in §3.2): any contextual prepare–measure fragment must contain basis-independent coherence of its state set; quantitative witnesses exist in interferometric scenarios (Wagner–Camillini–Galvão, Quantum 8, 1240 (2024); set-coherence ⇔ contextuality-confirmation relations, arXiv:2601.14067).
- **Sufficiency fails**: epistricted theories (toy theory, Gaussian QM, odd-d stabilizer) have superposition-like structure and reproduce the full textbook two-path interference phenomenology — double slit, Elitzur–Vaidman bomb test, delayed choice, quantum eraser — while being exactly noncontextual (Spekkens, PRA 75, 032110 (2007); Bartlett–Rudolph–Spekkens, PRA 86, 012103 (2012); Catani–Leifer–Schmid–Spekkens, Quantum 7, 1119 (2023)). Only *specific further aspects* of interference are genuinely nonclassical (Catani–Leifer–Scala–Schmid–Spekkens, PRA 2023; "What is nonclassical about uncertainty relations?", PRL 2022).
- **No threshold**: contextuality can be made maximally robust to dephasing, i.e. witnessed with vanishing coherence (Rossi–Schmid–Selby–Sainz, PRA 2023; arXiv:2212.06856). So the coherence *amount* is not the resource; its *non-erasability across the whole fragment* is.
- Within quantum theory, coherence converts faithfully to entanglement (Streltsov et al., PRL 115, 020403 (2015)) and to discord (Ma et al., PRL 116, 160407 (2016)); unspeakable coherence = asymmetry (Marvian–Spekkens, Nat. Commun. 5, 3821 (2014); PRA 94, 052324 (2016)); at the GPT level superposition ⇔ entangleability (ALPP, PRL 2022). Imaginarity is a further, independent resource: real-amplitude QM is experimentally falsified in network Bell tests (Renou et al., Nature 600, 625 (2021); Li et al., PRL 128, 040402 (2022); Chen et al., PRL 128, 040403 (2022)).

### 2.5 Axioms → effects

- No-signalling alone: PR boxes allowed (Popescu–Rohrlich 1994); boxworld realizes them with only trivial reversible dynamics (Gross–Müller–Colbeck–Dahlsten, PRL 104, 080402 (2010)) — nonlocality without teleportation/swapping.
- Information causality ⇒ Tsirelson (Pawłowski et al., Nature 461, 1101 (2009)); macroscopic locality ⇒ Q1 (Navascués–Wunderlich 2010); local orthogonality kills PR boxes and recovers the KCBS quantum bound (Fritz et al., Nat. Commun. 4, 2263 (2013); Cabello, PRL 110, 060402 (2013); CSW, PRL 112, 040401 (2014)). **None singles out the quantum set**: the almost-quantum set survives and, remarkably, **cannot come from any GPT obeying no-restriction** (Navascués et al., Nat. Commun. 6, 6288 (2015); Sainz–Guryanova–Acín–Navascués, PRL 120, 200402 (2018)).
- Purification ⇒ entanglement, no-cloning, ensemble steering, probabilistic teleportation, reversible dilation; with further informational axioms ⇒ quantum theory (CDP, PRA 81, 062348 (2010); PRA 84, 012311 (2011); Masanes–Müller, NJP 13, 063001 (2011); Hardy, quant-ph/0101012).
- Local quantum structure + no-signalling ⇒ quantum bipartite correlations (Barnum–Beigi–Boixo–Elliott–Wehner, PRL 104, 140401 (2010)).
- Sorkin truncation: QM is exactly second order (Sorkin 1994; bounds: Sinha et al., Science 329, 418 (2010)); higher order excluded by purity principles (Barnum–Müller–Ududec, NJP 16, 123029 (2014)); density cubes realize third order (Dakić–Paterek–Brukner, NJP 16, 023028 (2014)).
- Decoherence-to-classical ⇒ entanglement must exist (Richens–Selby–Al-Safi, PRL 119, 080503 (2017)).
- ψ-ontology: PBR (Nat. Phys. 8, 475 (2012)); maximal ψ-epistemicity impossible for d ≥ 3 (Barrett–Cavalcanti–Lal–Maroney, PRL 112, 250403 (2014); Leifer–Maroney, PRL 110, 120401 (2013)); ψ-epistemic models without preparation independence exist (Lewis et al., PRL 109, 150404 (2012)).

### 2.6 Model rows (what each theory does and does not exhibit)

| Model | incompat. | interference | ensemble steering | entanglement | Bell | neg./ctx | notes |
|---|---|---|---|---|---|---|---|
| Classical (simplex) | – | – | – | – | – | – | unique fully classical GPT |
| Spekkens toy / epistricted | ✓ | ✓ | ✓ | ✓(toy analogues) | – | – | steering phenomenology without contextuality (Spekkens 2007; Kar–Ghosh–Choudhary–Banik, Mathematics 4, 52 (2016)) |
| Gaussian QM | ✓ | ✓ | ✓ (two-mode squeezing, operational LHS-failure) | ✓ | – (with Gaussian meas.; non-Gaussian meas. needed: Banaszek–Wódkiewicz, PRA 58, 4345 (1998)) | – (epistricted embedding: BRS, PRA 86, 012103 (2012)) | steering strictly weaker than negativity |
| Odd-d stabilizer | ✓ | ✓ | ✓ | ✓ | ✓ (GHZ-type? — Bell violations with stabilizer measurements exist for multiqudit stabilizer states) | – (unique NC model = Gross/epistricted) | nonlocal yet noncontextual fragment-wise; see Schmid et al. 2022 |
| Qubit stabilizer | ✓ | ✓ | ✓ | ✓ | ✓ (GHZ/Mermin) | ✓ (generalized-contextual) | even-d anomaly |
| Boxworld | ✓ | n/a | ✓ | ✓ | ✓✓ (PR) | ✓ (nonclassical) | trivial reversible dynamics |
| Separable QT (min⊗) | ✓ | ✓ | – | – | – | ✓ (quantum marginals) | negativity/contextuality **without** entanglement; purification fails |
| Real QM | ✓ | ✓ | ✓ | ✓ | ✓ but bounded differently in networks | ✓ | falsified experimentally (2021–22) |
| Quantum (ℂ) | ✓ | ✓ | ✓ | ✓ | ✓ (≤ Tsirelson) | ✓ | — |

(The odd-d stabilizer Bell entry deserves care: the *subtheory as a whole* admits the nonnegative Gross representation, which is a local-hidden-variable model for all its space-like statistics; GHZ-type refutations use even-d/qubit Paulis. So: odd-d stabilizer = no Bell violation inside the subtheory; qubit stabilizer = Bell-violating. This is the row the network encodes.)

### 2.7 Thermodynamics

- Second laws: α-Rényi free energies govern (block-diagonal) conversion under thermal operations (Brandão–Horodecki–Oppenheim–Renes–Spekkens, PNAS 112, 3275 (2015)).
- Coherence is an independent constraint family (time-translation covariance; coherence cannot be created, must decay): Lostaglio–Jennings–Rudolph, Nat. Commun. 6, 6383 (2015); Lostaglio–Korzekwa–Jennings–Rudolph, PRX 5, 021001 (2015); Ćwikliński et al., PRL 115, 210403 (2015). Work-locking: coherence yields no work without a reference (Korzekwa et al., NJP 18, 023045 (2016)).
- **Thermodynamic witnesses of contextuality**: fluctuation theorems compatible with TPM on classical states either carry a work quasiprobability or fail on contextual protocols; its negativity is a contextuality signature (Lostaglio, PRL 120, 040602 (2018); no-go: Perarnau-Llobet et al., PRL 118, 070601 (2017)). Noncontextual bounds on average work/heat in sequential-measurement protocols; non-real entropy production signals contextuality; anomalous heat flow as a contextuality witness (KD review arXiv:2403.18899; "Contextuality in anomalous heat flow", arXiv:2406.09715 (2024)). Arrow-of-time reversal from initial correlations observed (Micadei et al., Nat. Commun. 10, 2456 (2019)); interferometric KD work distributions (Hernández-Gómez et al., npj QI 10 (2024)).
- **GPT thermodynamics**: in *sharp theories with purification*, microcanonical thermodynamics is well-posed, conversion is majorization-governed, and the three resource theories of purity are **dual to pure-state entanglement** — the entanglement–thermodynamics duality is not specifically quantum (Chiribella–Scandolo, NJP 17, 103027 (2015); NJP 19, 123043 (2017); arXiv:1608.04459). Thermodynamic consistency as an axiom source: Krumm–Barnum–Barrett–Müller, NJP 19, 043025 (2017).

---

## 3. Derived propositions (this work)

These are stated because the network showed the edge missing or implicit. Each is a short corollary of cited theorems; none is claimed to appear verbatim in the literature (nearest neighbors cited).

### P1. Contextuality implies entangleability

**Proposition.** Let a GPT system A possess a (tomographically complete) prepare–measure fragment that fails generalized noncontextuality. Then for every nonclassical system B (of this or any other GPT) there exists a consistent composite AB containing entangled states or entangled measurements. Equivalently: a universe in which no composite can ever support entanglement is a universe in which every system is noncontextual, nonnegative-representable, Wigner-positive, compatibility-only, steering-free and Bell-local.

**Proof.** Contextual ⇒ not simplex-embeddable (SSWKS, PRX Quantum 2, 010331 (2021)) ⇒ the state cone of A is not simplicial (a simplicial GPT trivially simplex-embeds). By entangleability of cones (ALPP, GAFA 31, 181 (2021); PRL 128, 160402 (2022)), min⊗ ≠ max⊗ for the pair (A,B) whenever B is also nonclassical, and the max (or any beyond-min) composite is a consistent no-signalling theory containing entangled elements. ∎

**Sharpness.** (i) Converse fails: Spekkens' toy theory is nonsimplicial (hence entangleable) yet noncontextual — entangleability does not require contextuality. (ii) The only escape is *postulating* the minimal tensor product: separable quantum theory (P3) keeps contextual marginals with no entangled states. (iii) Complementary known result in the opposite direction: entanglement requires contextuality of the associated sequential scenario (Plávala–Gühne, PRL 132, 100201 (2024)); and nonclassicality+decoherence forces entanglement (Richens–Selby–Al-Safi, PRL 119, 080503 (2017)). Together: **contextuality and entanglement are mutually entangled across the single/composite divide**, with the tensor-product choice as the sole hinge.

### P2. Coherence is necessary (never sufficient, with no threshold) for contextuality

**Proposition.** Let F be a prepare–measure fragment of quantum theory in which all states and all effects are diagonal in a single orthonormal basis (more generally: generate a commutative algebra). Then F is simplex-embeddable, hence noncontextual. Consequently every proof of generalized contextuality requires *basis-independent coherence of the state-plus-effect set* (no common diagonalizing basis).

**Proof.** Diagonal states are probability vectors over basis labels; diagonal effects are response functions on those labels; the identity maps embed the fragment into the d-simplex and its dual with inner products preserved — exactly the SSWKS simplex-embedding. ∎

**Status of the converse and the quantitative question.** Sufficiency fails (epistricted counterexamples; interference phenomenology is noncontextually reproducible — Catani et al., Quantum 7, 1119 (2023)). No coherence threshold exists (contextuality with vanishing coherence — Rossi et al. 2023). What exists quantitatively: event-graph/MZI inequalities tying basis-independent coherence to noncontextuality bounds (Wagner–Camillini–Galvão, Quantum 8, 1240 (2024)) and set-coherence ⇔ contextuality-confirmation statements (arXiv:2601.14067). **The user's proposed biconditional "coherence ⇔ state-dependent contextuality" is therefore false as stated; the correct edge is: coherence necessary, not sufficient, no threshold, with scenario-specific quantitative witnesses — and closing the general quantitative gap is research target G2 below.**

### P3. Negativity without entanglement — the user's example, realized and localized

**Proposition.** Separable quantum theory QT_sep (single systems = full quantum systems; composite state cone = separable cone, effect cone its dual; dynamics = non-entangling channels) is a consistent no-signalling GPT in which: (a) Wigner negativity, magic, anomalous weak values and generalized contextuality of single systems persist; (b) there are no entangled states, no steerable assemblages and no Bell violations; (c) purification fails.

**Proof sketch.** (a) Marginal theory is unrestricted quantum mechanics. (b) No entangled states by construction; every assemblage produced from a separable ρ = Σ p_i σ_i ⊗ τ_i admits the local-hidden-state model (λ = i, hidden state τ_i), so no steering and a fortiori no Bell violation (Fine/WJD hierarchy). (c) Any purification of a mixed separable marginal is entangled in standard QM and absent here; so the purification axiom fails, consistently with P1 — it is precisely the axiom whose removal decouples single-system negativity from composite entanglement. ∎

This answers the user's "a GPT shows Wigner negativity but not entanglement" hypothetical **affirmatively and sharply**: possible, and possible *only* by adopting the minimal tensor product / dropping purification. If any beyond-minimal composite is allowed, P1 forces entangled elements. The known complementary chain (odd prime d): Wigner negativity ⇒ state-dependent contextuality (Howard et al. 2014, under the unique-representation theorem of Schmid et al. 2022) ⇒ (P1) entangleability.

### P4. Steering sits strictly between the two classicality boundaries

**Observation (assembled, with one derived direction).** Ensemble-steering phenomenology exists inside noncontextual theories (toy theory; Gaussian QM operational steering with quadratures), while Bell violation and negativity do not. Hence in the network: steering ⇏ contextuality; steering ⇒ incompatibility (Banik, J. Math. Phys. 56, 052101 (2015), for tensor-product GPT classes; quantum: UMG/QVB 2014); contextuality ⇏ steering (QT_sep is contextual and unsteerable). Steering is thus logically *independent* of contextuality in both directions at the GPT level — which is why no "steering analogue of entangleability of cones" exists yet (gap G4).

---

## 4. Research gaps surfaced by missing edges (ordered by my estimate of tractability × payoff)

**G1 — Steering analogue of entangleability of cones.** Known: purification ⇒ steering (CDP 2010); steering ⇒ incompatibility in tensor-product classes (Banik 2015; Jenčová–Plávala, PRA 98, 012133 (2018)); restricted-theory steering↔contextuality connections (2024). Missing: a characterization of exactly which (A, B, composite-cone) triples admit steerable states. Conjecture (from P1/P4): every beyond-min composite of nonclassical, tomographically complete GPTs containing a *pure* entangled state is steerable; the open content is the mixed/no-purification case. Concrete first step: test on boxworld's max-tensor composites and on QT_sep-type interpolations (cones between min and max).

**G2 — Quantitative coherence → contextuality.** Wanted: conditions (candidates: tomographic completeness of two mutually unbiased fragments; saturation of an uncertainty relation, cf. Catani et al. PRL 2022) under which a coherence monotone lower-bounds contextuality robustness, with the epistricted theories sitting exactly at the boundary. The event-graph machinery (Wagner et al. 2024) plus the linear-program robustness (arXiv:2204.11905) make this a computable program: sweep fragments interpolating from the stabilizer fragment to full QM and map coherence vs contextual robustness — the shape of that Pareto frontier is unknown.

**G3 — Even-dimensional magic ⇔ contextuality.** The odd-d iff (Howard et al.) has no qubit counterpart: state-independent Pauli contextuality and the ZOR Λ-polytope model block naive statements. Known necessary direction: generalized contextuality for state injection (Schmid et al. 2022). Missing: a state-dependent *measure-level* iff — which qubit states inject contextuality beyond the state-independent baseline, and does some monotone over the Λ-polytope coincide with a contextuality robustness?

**G4 — Completeness of thermodynamic contextuality witnesses.** Known: work-quasiprobability negativity ⇔ contextual protocols in specific schemas (Lostaglio 2018); noncontextual bounds on heat/work; anomalous heat flow witnesses (2024). Missing: a completeness theorem — within thermal operations, is every contextual state/process detectable by some work/heat/entropy-production statistic? A no-go in either direction would be significant: either thermodynamics is a universal contextuality detector, or there is "thermally invisible contextuality" (then characterize it).

**G5 — Higher-order interference vs contextuality.** Nothing is known about Sorkin-level-3 theories' contextuality quantifiers; even the contextuality status of density cubes (Dakić et al. 2014) is open. A simplex-embedding analysis of the density-cube state space is a self-contained, publishable first computation.

**G6 — Thermodynamic axiomatics converse.** Chiribella–Scandolo derive thermodynamics *from* purification-type axioms; Krumm et al. partially reverse this. Open: which minimal thermodynamic demands (well-posed microcanonics, Landauer, second laws) *force* purification or spectrality? A counterexample theory with good thermodynamics but no purification would be as valuable as a derivation.

**G7 — Monogamy calculus contextuality ↔ nonlocality.** The Wright–Farkas invertible scenario map plus KCK monogamy suggest a single resource whose "budget" splits between sequential (contextuality) and spatial (nonlocality) scenarios. No such conserved quantity is known.

**G8 — NPT bound entanglement** (classic, hard, 28 years open); and thermodynamics of bound entanglement (work-extraction signature under LOCC-thermal constraints) — essentially untouched.

**G9 — The quantum set from principles.** Still open; the Sainz et al. no-restriction obstruction means any almost-quantum theory needs a principled measurement-restriction rule — nobody has proposed a natural one. A concrete program: classify restriction rules compatible with the self-duality the almost-quantum set *does* enjoy.

**G10 — Witnessability of effects (the user's "no proper witness" theme).** The infrastructure exists piecewise: contextuality is LP-testable on accessible fragments robustly to noise, detector inefficiency, no incompatibility needed, tomographic-incompleteness loophole addressed ("shadows and subsystems", arXiv:2409.13024; Mazurek et al. 2016; Müller–Garner, PRX 13, 041001 (2023)); entanglement witnessing is NP-hard in general; quantum-set membership is undecidable. Missing: the same meta-analysis for steering and for thermodynamic witnesses — i.e., a complexity-theoretic column for the whole network.

---

## 5. How this network answers the user's seed questions

1. *"A GPT shows Wigner negativity but not entanglement?"* — Yes: QT_sep (P3). And this is the **only** way: with any beyond-minimal composite, negativity ⇒ contextuality (odd-d/CV equivalences) ⇒ entangleability (P1). The axiom carrying the burden is purification / the composition rule, not the local structure.
2. *"Any GPT state with effect X shows effect Y?"* — The verified implication lattice is: Bell ⇒ steering ⇒ entanglement ⇒ (preconditioned by) contextuality (Plávala–Gühne) ⇒ non-simplex-embeddability ⇒ nonclassicality ⇔ incompatibility ⇔ no-broadcasting ⇔ superposition ⇔ entangleability. Negativity-type effects (Wigner, KD, anomalous weak values, work-quasiprobability) all collapse onto generalized contextuality as the invariant core (Spekkens 2008 + the 2022–24 equivalences), with representation-relative exceptions flagged (ZOR).
3. *"Wigner negativity creates state-dependent contextuality"* — theorem, with scope: odd prime d w.r.t. stabilizer measurements (Howard et al. 2014) and CV w.r.t. quadrature-displacement measurements (Booth et al. 2022); for qubits the statement must be replaced by the generalized-contextuality necessity of Schmid et al. (2022) — gap G3.
4. *"Coherence ⇔ state-dependent contextuality"* — false as a biconditional; corrected to: necessary (P2), not sufficient (epistricted/interference counterexamples), no threshold (vanishing-coherence contextuality), quantitative only scenario-wise — gap G2 is the open residue.
5. *"Failure to distinguish states blurs effects"* — encoded as: epistemic restrictions (the middle shell of §1) erase exactly {negativity, contextuality, Bell} while preserving {incompatibility, interference, steering phenomenology, no-cloning}; tomographic incompleteness as a witness loophole is now addressable (arXiv:2409.13024); and undecidability/NP-hardness results bound what witnesses can ever decide (Gurvits; Slofstra; MIP*=RE).

## 6. File map

- `gpt_effects_network.json` — machine-readable nodes/edges/statements/references (the artifact embeds the same data).
- Interactive page — typed graph with filters by node type, edge kind and status; click any edge for its statement and references; "Gaps" panel lists G1–G10 and the derived propositions P1–P4.
