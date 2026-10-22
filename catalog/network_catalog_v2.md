# Nonclassicality Network II — structural catalog (v2 addendum)

**2026-10-21. Companion to the v2 interactive page and `gpt_effects_network_v2.json`. The v1 artifact, `network_catalog.md` and `gpt_effects_network.json` are unchanged and remain the reference for the v1 edge set; v2 carries all v1 edges forward (re-homed where layers changed) and adds the structure below.**

## 1. What changed from v1 to v2

| v1 | v2 |
|---|---|
| 5 layers (axiom / model / state-property / effect / task) | 7 layers: **axiom → model → state-operator cluster → process-operator cluster → witness → effect → task** |
| effects and witnesses conflated | **witness layer**: operator-valued tests (functionals, inequality operators, SDP/LP tests, protocols), each paired 1–1 with the effect it detects; every witness node carries structured `requires {model, state, process}` and `blind` lists |
| state properties flat | intra-state containments and implications (entangled ⇒ coherent in every product basis; entangled ⇒ discordant; thermal ⊂ TTS; Wigner-negative ⇒ magic in odd d; Hudson; CC ⊂ separable) |
| no process layer | 13 process clusters with their own structure (TO ⊂ covariant; Clifford/Gaussian ⊂ unitary; free-operation "forbids-generation" edges; filter/weak/TPM protocol clusters) |
| genesis implicit | **genesis axioms**: symplectic/Poisson structure, epistemic restriction, Moyal lift, complex unit *i*, ħ — with `generates` edges to models and resources |
| — | **witness-algebra matrix**: 14 state clusters × 13 process clusters per witness; verdicts fires / hidden / blind from 17 referenced combo rows; gray cells auto-listed as uncharted candidate edges (the automation hook) |

Node/edge count (v2.2, 2026-10-21 revision): 92 nodes, 141 edges, 17 structured witness records, 17 combo rows, 19 gap/proposition cards. Revision after review: (i) new signed edge kind `excludes` (X holds iff Y FAILS) carries the polarity of the four classicality equivalences on the drawn edge itself - A1 incompatibility, A2 no-broadcasting, A3 entangleability, A5 contextuality are all 'classical <=> NOT X'; (ii) new kind `hosts` (model contains state cluster) with edges MH1-MH4 (quantum, Gaussian, odd-d stabilizer, boxworld all host entangled states), grounding the generative chain m-quantum -> s-ent -> e-bell; (iii) E8 retargeted to superquantum correlations - it is a ceiling (Tsirelson from local structure), not the source of Bell violations.

## 2. The witness–effect correspondence, made exact

Adopted design principle (user's): *no effect without a witness*. Every effect node now has a `pairs` edge from exactly one witness node:

| Witness (operator object) | Detects | Canonical references |
|---|---|---|
| CHSH functional | Bell violation (and, by thresholds 2 / 2√2 / 4: the quantum boundary and PR correlations) | CHSH 1969; Tsirelson 1980; PR 1994 |
| Steering inequalities / LHS SDP | EPR steering | Cavalcanti–Skrzypczyk, RPP 80, 024001 (2017) |
| Joint-measurability SDP | incompatibility | Designolle–Farkas–Kaniewski, NJP 21, 113053 (2019) |
| Entanglement witness operator / PPT map | entanglement (state property) | Horodecki³ 1996; Terhal 2000 |
| NC inequalities / simplex-embedding LP | generalized contextuality | SSWKS, PRX Quantum 2, 010331 (2021); arXiv:2204.11905 |
| SI-C sets (Peres–Mermin, Yu–Oh) | state-independent KS contextuality | Cabello, PRL 101, 210401 (2008); Yu–Oh, PRL 108, 030402 (2012) |
| KCBS pentagon | state-dependent KS contextuality | KCBS, PRL 101, 020403 (2008) |
| Displaced parity / phase-point operators | Wigner negativity | Royer, PRA 15, 449 (1977); Gross, JMP 47, 122107 (2006) |
| KD direct-measurement scheme | KD nonpositivity | Kirkwood 1933; Dirac 1945; Lundeen, Nature 474, 188 (2011) |
| Weak-value protocol | anomalous weak values | AAV, PRL 60, 1351 (1988); Pusey, PRL 113, 200401 (2014) |
| Work-quasiprobability protocol | anomalous work/heat | Allahverdyan, PRE 90, 032137 (2014); Lostaglio, PRL 120, 040602 (2018) |
| Magic monotones (robustness, mana, extent) | magic | Veitch et al., NJP 16, 013009 (2014); Howard–Campbell, PRL 118, 090501 (2017) |
| Coherence monotones / event-graph tests | coherence | Baumgratz–Cramer–Plenio, PRL 113, 140401 (2014); Wagner–Camillini–Galvão, Quantum 8, 1240 (2024) |
| Local-broadcasting test | discord | Piani–Horodecki–Horodecki, PRL 100, 090502 (2008) |
| Cloning-fidelity bound | no-broadcasting | Bužek–Hillery 1996; Gisin–Massar 1997; Barnum et al. 1996 |
| Fringe visibility | second-order interference | Greenberger–Yasin 1988; Englert, PRL 77, 2154 (1996) |
| Sorkin I₃ estimator | higher-order interference | Sorkin 1994; Sinha et al., Science 329, 418 (2010) |

Two recorded qualifications to strict 1–1:
1. **Threshold stratification.** CHSH is one functional detecting three nested effects (local bound 2, Tsirelson 2√2, algebraic 4). The pairing is 1–1 up to such filtrations; formalizing witness families as filtrations is new gap SG2.
2. **Witness incompleteness is itself tracked**: the PPT test is blind exactly on the bound-entangled cluster (witnesses exist by Hahn–Banach but no efficient universal one, NP-hardness); distillability has no known witness (NPT bound entanglement open); quantum-set membership has no algorithmic witness at all (MIP* = RE). So "no effect without a witness" holds as a principle, while *efficient* or *complete* witnesses fail in catalogued places — your original "sometimes we lack a proper witness" is encoded as properties of witness nodes rather than as missing nodes.

## 3. New propositions (TTS structure) — the user's claim, adjudicated and sharpened

Your claim was: *"tts states/thermal states may correspond to contextuality, but the processes don't, rather they hide contextuality. the same go for coherence in case of tts states and processes."* Verified status: **correct in its asymmetry, after one correction of scope**, and it splits into one derived proposition and one assembled theorem.

### N1 (derived here). Covariant/TTS fragments hide contextuality
**Statement.** Let H be nondegenerate. Consider any prepare–measure–transform fragment whose transformations T are time-translation covariant (T(U_t ρ U_t†) = U_t T(ρ) U_t†) and whose effects E are TTS ([E, H] = 0). Then the fragment is simplex-embeddable — noncontextual, KD-positive and coherence-blind — for **every** input state, energy-coherent states included.

**Proof.** For TTS effects, U_t† E U_t = E, so Tr(E T(U_t ρ U_t†)) = Tr(U_t† E U_t T(ρ)) = Tr(E T(ρ)). Averaging over t: Tr(E T(D(ρ))) = Tr(E T(ρ)), where D is the energy-dephasing (time-averaging) map. Hence the fragment's statistics are invariant under pre-dephasing and factor through D. For nondegenerate H, D maps into the commutative diagonal algebra; TTS effects are diagonal; covariant T preserves the diagonal subspace (T∘D is a stochastic map on populations). A commutative fragment embeds in the simplex over energy labels with its dual effects — the SSWKS simplex embedding. Noncontextuality follows (PRX Quantum 2, 010331); KD distributions over energy-basis chains are genuine probabilities; no coherence monotone is estimable from the fragment's statistics. ∎

**Reading.** TTS processes do not *lack* access to contextuality — they **hide** it: the hiding map is exactly D, and the statistics of a coherent input are indistinguishable from those of its dephased shadow. Lostaglio's noncontextual TPM fluctuation theorem (PRL 120, 040602 (2018)) is the special case T = id, E = energy projectors. Adjacent recent work: contextuality dissipation under decoherence (arXiv:2605.09558).

**Sharpness (degenerate H).** If H has degenerate eigenspaces, D dephases only between distinct energies; each degeneracy block remains a full matrix algebra, and covariant fragments can stay contextual inside blocks (extreme case H ∝ 𝟙: every process is covariant, nothing is hidden). This failure mode is new gap SG1.

### N2 (assembled from published results). Thermal states witness contextuality; the resource is process-side
Every state — Gibbs and maximally mixed included — violates state-independent contextuality inequalities: Cabello's Peres–Mermin inequality (two qubits, PRL 101, 210401 (2008)) and the Yu–Oh 13-ray inequality (qutrit, PRL 108, 030402 (2012)). Hence **the state-blind set of contextuality witnesses is empty**, while by N1 the **process-blind set contains the entire covariant/TTS cluster** (nondegenerate H). Corollary of N1: any SI-C measurement set necessarily contains non-TTS elements when H is nondegenerate.

### The contrast your claim pointed at, now exact
- **Contextuality:** blindness is *process-side only*. TTS/thermal states still witness it (N2) — but only through non-TTS measurements; TTS processes hide it for all states (N1).
- **Coherence (energy-basis):** blindness is *two-sided*. TTS states carry none (definitional, S8); covariant processes create none (Marvian–Spekkens asymmetry non-generation, P2) and TPM readout erases it (Perarnau-Llobet et al., PRL 118, 070601 (2017), K2).

So the corrected version of your sentence is: *thermal/TTS states can exhibit contextuality (under SI witnesses) but never energy coherence; TTS processes hide both.* This two-column contrast is encoded in the witness-algebra matrix (rows s-tts, s-thermal, s-cohE × columns p-cov, p-projE, p-weak, p-pauli).

### Also corrected in v2 (carried from your message)
- *"an entangled state also has coherences"* — true only basis-relatively, and the correct invariant statement is edge S1: **an entangled state is coherent with respect to every product basis** (if ρ is diagonal in a product basis it is manifestly separable). Every ρ is diagonal in *some* basis (spectral theorem), so basis-free "has coherence" is empty; the state-cluster node `s-coh` carries this warning in its definition.
- Entangled ⇒ discordant (S2, Ollivier–Zurek / Henderson–Vedral); entangled states may or may not be Wigner-negative — the clusters are logically independent (Gaussian entangled states are Wigner-positive; single-system Fock states are Wigner-negative and unentangled). The matrix shows this as independent rows rather than one merged "nonclassical state" node.

## 4. Genesis decomposition: what comes from where (model level)

The user's question — what is generated by the lift from Poisson to commutator, what comes from *i*, what from ħ — is answered by the GN edge family. Each line below is one or more edges with references in the JSON.

**(a) Poisson structure alone (ax-symplectic → m-classical).** Unrestricted classical statistical mechanics: the simplex. No incompatibility, no cloning obstruction, nothing.

**(b) Poisson + epistemic restriction (ax-epirestrict → m-spekkens, m-gaussian, m-stab-odd).** The *entire noncontextual-but-nonclassical shell* is classical mechanics plus a knowledge-balance restriction — this is the "classical epistemic model structure" you asked to see as one construction:
- discrete: Spekkens toy theory (PRA 75, 032110 (2007); quasi-quantization arXiv:1409.5041);
- continuous: epistricted Liouville mechanics = **Gaussian QM exactly** (Bartlett–Rudolph–Spekkens, PRA 86, 012103 (2012));
- ℤ_d: epistricted discrete mechanics = **odd-d stabilizer subtheory** = Gross's nonnegative Wigner representation, which is its unique noncontextual model (Gross 2006; Catani–Browne 2017; Schmid–Du–Selby–Pusey, PRL 129, 120403 (2022)).
This shell already shows: incompatibility, no-cloning, interference phenomenology, steering phenomenology, teleportation/dense-coding analogues, BB84. It never shows: negativity, generalized contextuality, Bell violation, anomalous weak values, computational speedup.
**Anomaly (GN3):** the qubit stabilizer subtheory is *not* reachable by any epistemic restriction — state-independently contextual (even-d result, Schmid et al. 2022). The even/odd split is the cleanest known boundary of the epistricted construction.

**(c) The Poisson → commutator lift (ax-moyal).** Groenewold–van Hove: there is no exact Lie-algebra morphism from Poisson brackets to commutators beyond quadratic observables (Groenewold, Physica 12, 405 (1946)), so the lift is necessarily a *deformation*: the Moyal bracket = Poisson bracket + O(ħ²) higher-derivative corrections (Moyal 1949; BFFLS, Ann. Phys. 111 (1978); Kontsevich, Lett. Math. Phys. 66, 157 (2003)). GN5 (derived, assembled from published pieces): **the beyond-Poisson terms are exactly the generators of Wigner negativity** — quadratic Hamiltonians have Moyal = Poisson, generate Gaussian unitaries, and preserve Wigner positivity (free cluster of non-Gaussianity resource theories, Takagi–Zhuang PRA 97, 062337 (2018)); pure Wigner-positive states are precisely Gaussian (Hudson 1974); CV universality and negativity generation need cubic-or-higher generators (Lloyd–Braunstein, PRL 82, 1784 (1999)). Via the CV equivalence negativity ⇔ contextuality (Booth–Chabaud–Emeriau, PRL 129, 230401 (2022)), *the deformation terms are what generate contextuality*. In the network: everything the middle shell lacks enters through ax-moyal.

**(d) The complex unit i (ax-complex).** Three separable contributions, each with its own edge:
- **Algebraic:** i[A,B] is Hermitian, so observables close as a Lie algebra and coincide with generators of dynamics (Stone's theorem) — the quantum observable–generator (Noether) link; real QM breaks it (Stueckelberg, Helv. Phys. Acta 33, 727 (1960)).
- **Compositional:** complex QM is the locally tomographic choice; real QM violates local tomography (Araki, CMP 75, 1 (1980); Wootters 1990; Hardy–Wootters, Found. Phys. 42, 454 (2012)).
- **Operational:** imaginarity is a resource (Wu et al., PRL 126, 090401 (2021)); real-amplitude QM is experimentally falsified in network Bell tests (Renou et al., Nature 600, 625 (2021); PRL 128, 040402 & 040403 (2022)); KD *imaginarity* exists only because of i (w-kd requires ax-complex).

**(e) ħ (ax-hbar).** Not a structure but the *scale* of both prior items: it sets the epistemic cell of the restriction that generates the middle shell (BRS 2012) and is the deformation parameter of the Moyal lift; ħ → 0 contracts star product to pointwise product, Moyal to Poisson, negativity to zero — the simplex limit (BFFLS 1978). In GPT terms ħ does not change which cone you are in; it quantifies the uncertainty/incompatibility trade-off within it.

## 5. Cluster algebra (state × process → witness verdicts)

The 17 referenced combo rows (K1–K17 in the JSON; rendered as the matrix) — condensed:

| # | State × Process | Verdicts | Anchor |
|---|---|---|---|
| K1 | TTS × covariant (+TTS effects, nondeg. H) | all contextuality/coherence/KD/work witnesses **blind** | N1; Lostaglio 2018 |
| K2 | energy-coherent × TPM | coherence/KD/work/WV **hidden** (resource present, dephased at readout) | Perarnau-Llobet 2017 |
| K3 | energy-coherent × weak measurement | KD, work-quasiprob, weak values, NC inequalities **fire** | Lundeen 2011; Lostaglio 2018; Pusey 2014 |
| K4 | thermal × SI-C sets | SI contextuality **fires** on every state (N2); KCBS state-dependent — β, H dependent | Cabello 2008; Yu–Oh 2012 |
| K5 | Gaussian × Gaussian ops | negativity/contextuality/Bell **blind**; steering & entanglement witnesses **fire** | BRS 2012; WJD 2007 |
| K6 | Gaussian(entangled) × non-Gaussian meas. | CHSH **fires** with state-Wigner positive — the needed negativity sits in the measurement representation | Banaszek–Wódkiewicz 1998 |
| K7 | stabilizer × Clifford/Pauli (odd d) | everything **blind**; efficiently simulable | Gross 2006; Veitch 2012; Schmid et al. 2022 |
| K8 | stabilizer × Pauli (qubits) | SI contextuality **fires** for every state (Mermin square) | Mermin 1990; Cabello 2008 |
| K9 | magic × Pauli (odd prime d) | state-dependent contextuality **fires iff Wigner-negative** | Howard et al. 2014 |
| K10 | bound magic × Clifford | negativity witness **blind**, magic witnesses **fire** | Veitch et al. 2012 |
| K11 | Werner-entangled × incompatible meas. (single copy) | CHSH **blind** (LHV even for POVMs) | Werner 1989; Barrett 2002 |
| K12 | same states × local filter then CHSH | CHSH **fires** (hidden nonlocality) | Gisin 1996; Hirsch 2013 |
| K13 | separable × local ops | Bell/steering/entanglement witnesses **blind** forever | WJD 2007 |
| K14 | bound entangled × LOCC | PPT test blind, tailored witnesses **fire**, some violate Bell; undistillable | Vértesi–Brunner 2014 |
| K15 | discordant × local broadcasting | broadcasting failure **fires** | Piani et al. 2008 |
| K16 | entangled × LOCC | monotones non-increasing: free ops only **hide** | Horodecki RMP 2009 |
| K17 | energy-coherent × covariant | asymmetry monotones decay: **hidden**, never amplified | Marvian–Spekkens 2014 |

The matrix fills 14 × 13 cells per witness from these rows plus each witness's blind lists; the remaining gray cells are the **uncharted set** — the operational form of "automatize research by finding missing/impossible edges" (gap SG3). Counts are shown live per witness on the page.

## 6. New gaps (beyond v1's P1–P4, G1–G10, all kept)

- **SG1 — covariant contextuality in degeneracy blocks.** N1's exact failure mode: classify witnesses surviving covariant-only probing inside degenerate eigenspaces (links: quantum reference frames, noiseless subsystems). Concrete start: U(1)-covariant channels on a twofold-degenerate doublet.
- **SG2 — threshold stratification.** Which witness families are filtrations of a single functional (CHSH: 2 / 2√2 / 4; CSW theta-function analogues for contextuality)? Is there a general witness-filtration theorem tied to the NPA hierarchy?
- **SG3 — the uncharted-cell program.** Each gray matrix cell is a candidate theorem: derive from monotone/free-operation structure, locate in the literature, or register as open. Many cells are trivially derivable (do that first); the residue is a genuine research list.

## 7. Reference honesty

- v1's modern load-bearing citations were search-verified on 2026-10-20; they carry over unchanged.
- v2's *added* citations (Hudson 1974; Groenewold 1946; Moyal 1949; BFFLS 1978; Kontsevich 2003; Stone 1932; Stueckelberg 1960; Araki 1980; Hardy–Wootters 2012; Yu–Oh 2012; Cabello 2008; Mermin 1990/Peres 1991; AAV 1988; Lundeen 2011; Allahverdyan 2014; Perarnau-Llobet 2017; Baumgratz 2014; Ollivier–Zurek/Henderson–Vedral 2001; Piani 2008; Bužek–Hillery 1996; Gisin–Massar 1997; Gisin 1996; Gottesman 1998/Aaronson–Gottesman 2004; Lloyd–Braunstein 1999; Takagi–Zhuang 2018; Albarelli 2018; Designolle–Farkas–Kaniewski 2019; Cavalcanti–Skrzypczyk 2017; Howard–Campbell 2017; Royer 1977; Kirkwood 1933; Dirac 1945; Greenberger–Yasin 1988; Englert 1996) are standard results cited from knowledge, not re-searched today; verify page numbers before quoting them in a manuscript.
- `derived` items (N1; GN5; P1–P3 from v1) are proved or assembled here and **not** claimed to appear in the literature; N1's closest published neighbors are Lostaglio's TPM result and decoherence-dissipation-of-contextuality work (arXiv:2605.09558). Before publishing N1 or GN5 as new, run a dedicated literature pass.

## 8. File map

- v2 interactive page — layered graph, witness panels (requires / blind / combos), witness-algebra matrix with uncharted cells, edge catalog, gaps.
- `gpt_effects_network_v2.json` — machine-readable: 92 nodes, 137 edges, 17 witness records, 17 combos, 19 gap cards.
- `network_catalog_v2.md` — this file.
- v1 artifact + `gpt_effects_network.json` + `network_catalog.md` — unchanged, kept as the flat edge reference.

---

# Round 3 (v2.4, 2026-10-23): edges generated from uncharted cells

Method demonstration: each item below occupies a cell or node pair that previously carried NO edge (neither connecting nor disconnecting theorem recorded). Items marked *derived* are proved here; *composed* items are corollaries of recorded edges; the literature fill closes a cell with existing results.

## R1 (derived; possibly folklore). TTS states of generic noninteracting pairs carry only classical correlations
**Statement.** Let H = H_A + H_B with nondegenerate total spectrum (all E_i^A + E_j^B distinct). Then every TTS state ([rho,H]=0) is classical–classical: zero discord, hence separable, unsteerable and Bell-local. Entangled or discordant TTS states exist iff the total spectrum is degenerate, and their quantum correlations live entirely inside degeneracy blocks.
**Proof.** Nondegenerate total spectrum forces the eigenbasis of H to be the (unique) product basis |E_i^A> x |E_j^B>; [rho,H]=0 then makes rho diagonal in it, i.e. rho = sum_ij p_ij |ij><ij| — a classical–classical state. Zero discord (Ollivier–Zurek/Henderson–Vedral), separability, and the WJD hierarchy do the rest. Degenerate case: two equal-gap qubits give the TTS Bell state (|01>+|10>)/sqrt 2 in the {|01>,|10>} block. QED.
**Consistency.** The Micadei et al. (Nat. Commun. 10, 2456 (2019)) arrow-of-time reversal uses initial correlations in exactly such a degenerate block (equal-frequency qubits, |01><10| coherence) — the experiment sits precisely where R1 says symmetric quantum correlations must live. Refines gap SG1 into a classification.

## R2 (derived lemma). Time-translation-symmetric measurements have no incompatibility
**Statement.** For nondegenerate H, all TTS sharp observables commute (each is a function of H), and every TTS POVM is a classical post-processing of the energy measurement; the TTS measurement cluster is jointly measurable in toto.
**Proof.** [A,H]=0 with H nondegenerate forces A diagonal in the H-basis; two diagonal matrices commute. A POVM with all effects diagonal, E_k = sum_i e_k|i Pi_i, is realized by measuring H and sampling k with probability e_k|i. QED.
**Corollaries.** No incompatibility -> no steering (B6) and no Bell violation (Fine, B7) from TTS probes; and the fragment is commutative, giving a one-line alternative proof of the N1 blindness column. Slogan: symmetry of the probe set collapses the effect layer to classical stochastics.

## R3 (composed corollary; A8 o B3). Bell-local yet contextual scenarios
Plavala–Guhne Theorem 1 (PRL 132, 100201 (2024)): a preparation-and-measurement noncontextual model for the steered states together with ALL measurements implies separability. Contrapositive applied to Werner-region entangled states with LHV models for all single-copy measurements (Werner 1989; Barrett 2002): their derived sequential scenario is contextual while no Bell inequality can be violated. Contextuality is thus a strictly finer composite-nonclassicality detector than Bell violation. Checked against the PG paper (2026-10-23): the theorem supports the inference; the Werner corollary is NOT stated there explicitly — flagged as derived, novelty pass required. Scope note: the contextual fragment contains ALL measurements on the steered side; restricted fragments (e.g. stabilizer-only, MH3) can remain noncontextual — no contradiction.

## R4 (counterexamples). Magic and discord are logically independent
(a) Magic without discord: |T> x |0> is a pure product state (all correlation measures zero) and magic. (b) Discord without magic: rho = 1/2(|0><0| x |0><0| + |+><+| x |+><+|) lies in the stabilizer polytope (non-magic) yet is discordant on both sides. Proof of (b): [rho, A x I]=0 gives [P0,A] x P0 = -[P+,A] x P+; since P0, P+ are linearly independent operators, both commutators vanish, so A commutes with P0 and P+, which generate the full qubit operator algebra, so A ∝ I; hence no nontrivial local observable commutes with rho and rho is not classical-quantum on either side. QED. Consequence: no unconditional edge can ever connect s-magic and s-discord — the cell is closed in both directions.

## R5 (literature fill). The KD-Hudson boundary
Pure KD-classical states are characterized by support-uncertainty / complete-incompatibility conditions: De Bievre, PRL 127, 190404 (2021) [citation confirmed via arXiv:2210.02876, which proves De Bievre's DFT conjecture: pure KD-classical iff n_A(psi) n_B(psi) = d]; noncommutation alone is insufficient for KD nonpositivity (Arvidsson-Shukur, Drori, Yunger Halpern, J. Phys. A 54, 284001 (2021)).

## R6 (inheritance + new sub-gap SG4). Sorkin order of epistricted theories
Gaussian QM and the odd-d stabilizer subtheory are literal quantum subtheories, hence inherit I3 = 0 identically. The discrete toy(-field) theory is not a quantum subtheory (it fails GHZ-type stabilizer statistics), so its Sorkin order is open (SG4): define its three-path interferometer and compute I3. New gap SG5: do local filters, which activate hidden nonlocality, also amplify the sequential-scenario contextuality of R3?

## Remaining examples of fully uncharted pairs (no theorem either way, as of this writing)
- s-athermal x e-ctx: is there a free-energy cost or budget to contextuality under thermal operations?
- p-filter x e-ctx (SG5): hidden-contextuality activation.
- p-cov x s-magic: can covariant dynamics generate or must it degrade magic (H outside the Clifford frame)?
- m-aq x witness layer: which witnesses are even definable for the almost-quantum set without a no-restriction GPT carrier?
Census (v2.4): 445 of 3,094 witness-matrix cells settled; 2,649 uncharted.
