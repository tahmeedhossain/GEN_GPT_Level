# Hypergraph form of the Nonclassicality Network (v3.0, 2026-11-26): definitions, transfer rules, proofs

Status: generated with AI assistance (Claude, Anthropic) on 2026-11-26; not yet reviewed by the author.
Scope: this note defines the hypergraph form in general terms (Sections 1 to 6 do not depend on the physics),
then records what the form changes in this network (Sections 7 to 9). The hyperedges themselves are listed in
`catalog/hyperedges_v3.md`; the data are in `data/hypergraph_v3.json`; the engine is `tools/hyperclosure.py`.
Versions v1, v1b, v2 (v2.4), v2b and v2.6 are unchanged.

## 1. Why a graph is not enough

An edge of v2.6 joins two nodes. Three kinds of record do not fit that form.

1. A statement with two premises. P3 reads "LOCC rules out entangled states". The theorem is that LOCC cannot
   create an entangled state from a separable one. The premise "separable input" is a node of the network
   (Separable states) but not an endpoint of the edge.
2. Two statements on the same pair with opposite signs. N1 (Covariant processes rule out contextuality) and U1
   (Covariant processes imply contextuality) differ by a hypothesis on the Hamiltonian. On a graph they are two
   opposite edges on one pair.
3. A verdict of the witness matrix. "Entangled states with incompatible local measurements fire the
   entanglement witness" is a statement about a state cluster and a process cluster together. In v2 it is a row
   of a side table (K11), not an edge.

In all three cases the object is one relation among more than two nodes. A hyperedge is that object.

## 2. Definitions

**Definition 1 (epistemic hypergraph).** An epistemic hypergraph is a triple (V, λ, E). V is a finite set of
nodes; λ assigns to each node its layer (here: axiom, model, state cluster, process cluster, witness, effect,
task). Each element e of E is a hyperedge with

- a nonempty tail T(e) ⊆ V, the joint premises;
- a nonempty head H(e) ⊆ V, disjoint from the tail, the conclusions;
- a modality μ(e) (Section 3), which fixes the polarity: possibility or no-go;
- a status (theorem, partial, counterexample, derived, definition, open), as in v2;
- a guard: text for the conditions that are not nodes;
- a scope: a finite set of tokens for the standing hypotheses under which the record holds
  (for example `odd-d`, `cv`, `nondeg-H`), with a fixed list of incompatible pairs of tokens.

The signature of e is the pair of multisets of layers of its tail and of its head. A hyperedge with several
heads abbreviates the hyperedges with the same tail and one head each.

A binary edge is a hyperedge with one premise and one conclusion. So the graph v2.6 is the sub-hypergraph of
(1,1)-hyperedges, and it is kept as it is. In the terminology of Gallo, Longo, Pallottino and Nguyen [1] a
hyperedge with one head is a B-arc and a hyperedge with one tail is an F-arc. The "AND routes" of the reader
graphs and of the particle-physics graph of this project are B-arcs. The "requires" lists of the witness
records of v2 are F-arcs: one witness, several necessary conditions.

**Three values.** As for edges: a tuple of nodes carries a possibility hyperedge, a no-go hyperedge, or none.
None means unsettled.

## 3. Instance semantics of three signatures

A transfer rule needs to know what a record asserts. For three signatures this is fixed as follows.

**Arrangements.** An arrangement inside a process cluster P is a finite prepare, transform and measure scheme
all of whose transformations and measurements belong to P. Two conventions, which the rows of v2 used
implicitly, are made explicit.

- (R) A cluster given as a set of channels is completed by its reference measurement: the energy measurement
  (TTS effects) for covariant and thermal operations, the incoherent basis for incoherent operations, Pauli
  measurements for Clifford operations, homodyne detection for Gaussian operations, local measurements for
  LOCC, a fixed sharp measurement for unitary dynamics.
- (L) For witnesses of composite systems (Bell, steering, entanglement, discord) the processes act locally.
  A global entangling operation is a transformation of the state and is recorded by a transformation
  hyperedge.

**Firing.** For a witness w paired with a state cluster (entanglement witness, Wigner estimator, magic,
coherence and discord witnesses), w fires on a pair (ρ, A) of a state and an arrangement when the statistics
of A on ρ violate a criterion of class w whose bound holds for every state outside the detected cluster under
the same arrangement. For a witness paired with an effect (Bell, steering, noncontextuality, Kirkwood-Dirac,
...), the bound is that of the classical model class of the effect (local hidden variables, local hidden
states, noncontextual models, nonnegative distributions). Write Φ(w) for the set of pairs on which w fires.

**Definition 2 (detection modalities).** For a state cluster S, a process cluster P and a witness w:

| modality | statement | polarity |
|---|---|---|
| fires | there are ρ in S and an arrangement A inside P with (ρ, A) in Φ(w) | possibility |
| fires_all | for every ρ in S there is an arrangement A inside P with (ρ, A) in Φ(w) | possibility |
| blind | for every ρ in S and every arrangement A inside P, (ρ, A) is not in Φ(w) | no-go |
| hidden | blind, and S lies in the cluster that w detects | no-go |
| not_always | there is ρ in S such that (ρ, A) is not in Φ(w) for every arrangement A inside P | no-go |

"blind" is the negation of "fires", and "not_always" is the negation of "fires_all". Hence for every tuple
(S, P; w) exactly one of fires and blind is true, and exactly one of fires_all and not_always. An uncharted
tuple is therefore a question with a yes or no answer. For nonempty S, fires_all implies fires and blind
implies not_always.

A unary record "blind on S" means blind(S, P; w) for the cluster P of all arrangements, and "blind on P" the
same with S the cluster of all states. A record at the level of a model (B.I3.QT) holds for all clusters of
that model.

**Definition 3 (transformation and task modalities).** can_create(S, P; S′): some channel inside P maps some
state of S into S′. cannot_create is its negation. achieves(S, P; t): some protocol with inputs from S and
operations inside P achieves the task t. cannot_achieve is its negation.

**Requirement.** "w requires the state cluster c" means: (ρ, A) in Φ(w) implies ρ in c. "w requires the
process cluster c" means: (ρ, A) in Φ(w) implies that A contains a member of c.

**Order.** s ⊑ S (recorded inclusion): every state of s is a state of S; for process clusters, every
arrangement inside s is an arrangement inside S. S ⟂ S′ (recorded exclusion): no state belongs to both; for
process clusters p ⟂ c, no arrangement inside p contains a member of c. The inclusions used are binary edges
of v2.6 (S1, S2, S3, S4, S5, S7, S10, P1, P5), each with the scope under which it is a set inclusion. The
exclusions are S6, S8, S9, R1, U4, the definitional complements X1 to X5, and X6 (Lemma R2 read as an
exclusion: TTS effects are jointly measurable for nondegenerate H).

## 4. Transfer rules

**Proposition 1 (transfer).** Let S, S′ be state clusters, P, P′ process clusters, w a witness.

- (a) If fires(S, P; w), S ⊑ S′ and P ⊑ P′, then fires(S′, P′; w).
- (b) If fires_all(S, P; w), S′ ⊑ S and P ⊑ P′, then fires_all(S′, P′; w).
- (c) If blind(S, P; w), S′ ⊑ S and P′ ⊑ P, then blind(S′, P′; w). The same holds for hidden.
- (d) If not_always(S, P; w), S ⊑ S′ and P′ ⊑ P, then not_always(S′, P′; w).

*Proof.* (a) The pair (ρ, A) given by the hypothesis has ρ in S ⊆ S′ and A inside P, hence inside P′.
(b) Every ρ in S′ is in S, so it has an arrangement inside P, hence inside P′, on which w fires.
(c) A state of S′ is a state of S and an arrangement inside P′ is an arrangement inside P, so the pair is not
in Φ(w); for hidden, S′ ⊆ S lies in the detected cluster. (d) The state ρ given by the hypothesis is in S′,
and every arrangement inside P′ is inside P. ∎

Possibility moves to larger clusters and no-go to smaller ones; fires_all and not_always move in opposite
directions in the two slots.

**Proposition 2 (requirement and exclusion).** If w requires c, c ⊑ c′ and x ⟂ c′, then w is blind on x.

*Proof.* State side: if (ρ, A) is in Φ(w) then ρ is in c ⊆ c′, so ρ is not in x. Process side: A contains a
member of c, which is a member of c′, so A is not an arrangement inside x. ∎

**Proposition 3 (transformation and task).** can_create and achieves transfer to larger clusters in every
slot (for can_create also in the output slot); cannot_create and cannot_achieve transfer to smaller clusters
in every slot.

*Proof.* As for (a) and (c). For the positive statements the witnessing state and channel remain inside the
larger input and process clusters, and Λ(ρ) in S′ ⊑ S″ gives Λ(ρ) in S″. For the negative statements a
state and a channel that violate the statement for the smaller clusters violate it for the larger ones. ∎

**Scopes.** A record holds under its scope. A derivation holds under the union of the scopes of the records
and inclusions it uses; if the union contains an incompatible pair of tokens, the derivation is discarded
(its hypotheses cannot hold together).

**Definition 4 (classes of a tuple).** Collect all derivations of a tuple.

- conflict: a positive derivation (fires or fires_all) and a blind or hidden derivation with compatible
  scopes, or fires_all and not_always with compatible scopes;
- split: positive and blind derivations, all pairs with incompatible scopes;
- blind, hidden: only such derivations;
- mixed: fires and not_always, no blind;
- fires_all; fires; not_always: only such derivations;
- uncharted: no derivation.

**Proposition 4 (consistency).** If every record is true under its scope, no tuple is in the class conflict.

*Proof.* By Propositions 1 and 2 every derivation is a true statement under its scope. Under a compatible
union of scopes both statements would hold together, and fires contradicts blind, fires_all contradicts
not_always. ∎

Read in the other direction: a conflict proves that a record is false or that its modality was mis-recorded.
This is a check of the data base that needs no physics. The calculus is sound and not complete: it moves
recorded verdicts along recorded inclusions and proves nothing else.

**Mixed and split tuples.** A mixed tuple is a true statement: the cluster contains states that fire and
states that never fire. It names a missing node, the sub-cluster on which the verdict is uniform. A split
tuple names a hypothesis on which the verdict depends.

## 5. Hyperpaths

**Definition 5 (B-connection, [1]).** A node t is B-connected to a set X of nodes if t is in X, or there is
a hyperedge with t in its head whose tail nodes are all B-connected to X. The set of nodes B-connected to X
is computed by forward chaining; for Horn formulae, to which this is equivalent, linear-time algorithms are
classical [3], and [1, 2] give the hypergraph versions. The page uses a plain fixed-point loop.

A B-path is a pathway in the structural sense: every step is a recorded statement and holds under its own
conditions. The steps need not be about the same system. The next proposition says when they are.

**Proposition 5 (two-step pathway).** If can_create(S1, P1; S2), S2 ⊑ S and fires_all(S, P2; w), then there
are a state ρ in S1, a channel Λ inside P1 and an arrangement A inside P2 such that w fires on (Λ(ρ), A).
With fires in place of fires_all the conclusion does not follow.

*Proof.* Take ρ and Λ with Λ(ρ) in S2 ⊆ S; fires_all gives A for the state Λ(ρ). For the last sentence: the
state of S that fires need not be one that can be created. ∎

**Corollary (created but unseen).** If can_create(S1, P; S2), P ⊑ P′, w requires S2 and w is blind on P′,
then operations inside P create states of the cluster that w detects, and no arrangement inside P′, in
particular none inside P, certifies them.

The forward-chaining tool of the page follows the possibility hyperedges and those binary edges for which an
occurrence of the source gives an occurrence of the target without a further premise: containments,
witness-effect pairings, hostings, generations, enablements of tasks, and the implications B1, B1b, C10, C14,
S1, S2, S5. It does not follow a binary edge that a hyperedge restates with explicit premises, nor partial,
open or counterexample edges, nor W1b (the threshold exception of the CHSH functional) and P4 (its premise,
an incoherent input, is not a node).

## 6. The census, generalised

For a signature with tail layers L1, ..., Lk and head layer L, the tuples are the elements of
V(L1) × ... × V(Lk) × V(L). A tuple is charted if the calculus gives it a class other than uncharted. The
census of v2 (unconnected pairs, gray matrix cells) is the case of the signatures (1,1) and
(state, process → witness) without transfer.

## 7. Application to network v2.6

Numbers are produced by `tools/build_v3.py` and repeated in `catalog/hyperedges_v3.md`.

**Lift.** 92 nodes and 156 binary edges are unchanged. 101 hyperedge records are added:

| signature | count | source |
|---|---|---|
| detection: state + process → witness | 36 | the rows K1 to K18 (K16 excepted) split by modality; K19 to K25 lifted from B2, B6, B7, C1, R3, U1, U6, U7; K26 to K29 read off the pairings W4, W8, W13, W16; HG1, HG2, HG2b, HG3 (Section 9) |
| unary detection: cluster → witness | 31 | the blind lists of the witness records (4 of 35 retyped) |
| requirement: witness → clusters | 10 | the pairings, the hierarchy edges B1 and B1b, and B6, B7, R5 |
| complements and exclusions | 6 | definitions of the clusters; Lemma R2 |
| transformation: state + process → state | 7 | P2, P3, P10, P11, D1, U5b, and the non-generation content of a witness record |
| task: state + process → task | 4 | P6, C3, C4, G1 |
| genesis and logic | 7 | GN1, GN2, GN4, GN7, E6, E8, E12, A11, B12 |

No lifted record adds physics: each states an existing record with its premises as tail nodes and names the
records it comes from. The four rows of Section 9 are the exception and are marked as such.

**What the hyperedge form resolves.**

- N1 and U1 become K1 and K25, the same tuple (TTS states, Covariant processes; NC-LP) with the scopes
  `nondeg-H` and `deg-H`: a split tuple instead of two opposite edges.
- A10 (incompatibility does not imply contextuality) and A11 (it does, when all quantum states are available)
  are separated by a second tail node: L7 has the tail {Measurement incompatibility, Quantum theory}.
- P6 (Clifford operations rule out universal computation) and C4 (magic is necessary for it) are the two
  hyperedges Q1 (Stabilizer states + Clifford operations cannot achieve it) and Q2 (Magic states + Clifford
  operations achieve it).

**Consistency check of the released records.** Reading the v2.6 and v2b records literally (blind and hidden
universal, fires existential) the calculus finds conflicts on 3 tuples, from 2 pairs of records:

1. K16 (Entangled states × LOCC → EW: hidden) against K14 (Bound entangled states × LOCC → EW: fires) with
   S10 (bound entangled states are entangled states).
2. The entry "MagicW blind on Clifford operations" against K10 (Magic states × Clifford operations → MagicW:
   fires).

In both, the negative record states that free operations do not increase the resource. That is a statement
about the output state, i.e. a transformation hyperedge (T2, T4), not a detection verdict. Five further
records are retyped because their own notes state a narrower claim; the list with reasons is in
`catalog/hyperedges_v3.md`, Section 3. After retyping there is no conflict.

**Transfer.**

| | charted tuples of 3,094 |
|---|---|
| v2.6 rule on the v2.6 records (reproduced) | 469 |
| v3 records, no transfer | 632 |
| v3 records with transfer | 981 |

Of the 632, 182 are the single record B.I3.QT (the Sorkin term vanishes in quantum theory), which the v2.6
rule did not apply because its premise is a model. Without that column the three numbers are 469, 450 and 799.
The 349 tuples added by transfer use only the inclusions thermal ⊑ TTS, classical-classical ⊑ separable,
bound entangled ⊑ entangled ⊑ discordant, entangled ⊑ coherent (product basis), energy-coherent ⊑ coherent
(energy basis), Wigner-negative ⊑ magic (odd d), thermal operations ⊑ covariant, Clifford ⊑ unitary, and the
requirement rule. Classes after transfer: blind 914, hidden 7, fires_all 19, fires 33, mixed 5, split 2,
not_always 1; uncharted 2,113.

**Cross-checks that come out of the calculus.**

- 13 of the 16 state-side blindness records kept from v2.6 are re-derived by Proposition 2 from a pairing and an
  exclusion; 3 rest on their own note (KD and CohW on TTS states, CloneF on classical-classical states).
- T7 (thermal operations create magic from a stabilizer state) transferred along P1 gives "covariant
  operations create magic from a stabilizer state", which is statement (ii) of U5; with the record
  "MagicW blind on Covariant processes" the corollary of Proposition 5 gives U5 itself.
- T6 (D1) transferred along S2 gives "incoherent operations create discord from coherence", the second
  sentence of D1.
- The mixed tuple (Discordant states, Incompatible sets; NC-LP) is the registered problem SG6. The mixed
  tuple (Entangled states, Incompatible sets; CHSH) is hidden nonlocality. The mixed tuple (Magic states,
  KS sets; KCBS) is bound magic.
- A derived statement not recorded before: for H nondegenerate with a stabilizer eigenbasis in odd dimension,
  the Wigner estimator is blind on TTS states (REQ.Parity, S5, U4): TTS states are then stabilizer mixtures.
  It is an immediate consequence of U4 and S9.

**Two-step pathways (Proposition 5).** Six are found, among them: coherent state, incoherent operation,
entangled state, incompatible local measurements, entanglement witness fires (T6, K11-fires); stabilizer
state, thermal operation, magic state, Clifford operations with Pauli measurements, magic witness fires
(T7, K10-fires).

## 8. Limits

1. Guards are text. Scopes are twelve tokens chosen by hand with five incompatible pairs. A condition that is
   neither a node nor a token is invisible to the calculus.
2. The instance semantics is fixed for the detection, transformation and task signatures. The genesis and
   logic hyperedges are recorded and drawn; no rule is applied to them.
3. Conventions (R) and (L) are part of the semantics. Under another convention some unary records change.
4. Only recorded inclusions are used. For example a Kochen-Specker set is an incompatible set, but
   "KS sets ⊑ incompatible sets" is not recorded, because the rows on incompatible sets concern local
   measurements on a wing and the rows on KS sets measurements of the whole system.
5. A cluster-level verdict says nothing about a given state except through fires_all and blind.
6. The 2,113 uncharted tuples are uncharted relative to the records. Many will be settled by statements that
   are known and simply not recorded.

## 9. Rows added in this round

Retyping removed four unary records and so left cells without a verdict although the answer is elementary or
in the literature. By the standing rule of the project (a relation that the literature establishes must be an
edge) they are recorded.

**HG1** (Stabilizer states + KS sets → KCBS: fires). Let v1, ..., v5 be unit vectors of a qutrit with
v_i orthogonal to v_{i+1} (indices mod 5) in the configuration of Klyachko et al. [4]; the operator
A = Σ |v_i⟩⟨v_i| has largest eigenvalue √5 with eigenvector a. For a pure state ψ take a unitary U with
Ua = ψ. The vectors Uv_i satisfy the same orthogonality relations and Σ |⟨Uv_i|ψ⟩|² = √5 > 2. This holds for
the stabilizer state |0⟩. The rays Uv_i are not stabilizer measurements, so K7 (blind inside the stabilizer
subtheory, odd d) is not contradicted.

**HG2** (Coherent states + Incoherent operations → CohW: fires; scope `io`). Qubit, incoherent basis
{|0⟩, |1⟩}, |±⟩ = (|0⟩ ± |1⟩)/√2. K1 = |0⟩⟨+| and K2 = |1⟩⟨−| satisfy K1†K1 + K2†K2 = 1, and
K_n |i⟩⟨i| K_n† is proportional to |0⟩⟨0| or |1⟩⟨1|, so the channel is an incoherent operation in the sense of
Baumgratz, Cramer and Plenio [5]. Followed by a measurement in the incoherent basis it gives outcome 0 with
probability ⟨+|ρ|+⟩, which is 1/2 for every incoherent ρ and 1 for |+⟩. Compare Yadin et al. [6], who single
out the strictly incoherent operations as those that do not use coherence.

**HG2b** (Incoherent operations → CohW: blind; scope `dio`). Let D be the dephasing map, Λ a channel with
DΛ = ΛD, and E an effect with D(E) = E. Then Tr(E Λ(ρ)) = Tr(D(E) Λ(ρ)) = Tr(E D(Λ(ρ))) = Tr(E Λ(D(ρ))).
The statistics are those of the incoherent state D(ρ). HG2 and HG2b make the tuple split: the node
"Incoherent / dephasing-covariant ops" is a union of two clusters with different verdicts.

**HG3** (Wigner-negative states + Gaussian operations → Parity: fires; scope `cv`). Homodyne tomography
reconstructs the Wigner function from quadrature statistics; Lvovsky et al. [7] reconstructed a negative
Wigner function of the single-photon Fock state in this way. The witness record of the Wigner estimator
already notes that "homodyne alone gives W only via tomography".

## References

[1] G. Gallo, G. Longo, S. Pallottino, S. Nguyen, Directed hypergraphs and applications, Discrete Applied
Mathematics 42, 177-201 (1993). doi:10.1016/0166-218X(93)90045-P
[2] G. Ausiello, L. Laura, Directed hypergraphs: Introduction and fundamental algorithms - A survey,
Theoretical Computer Science 658, 293-306 (2017). doi:10.1016/j.tcs.2016.03.016
[3] W. F. Dowling, J. H. Gallier, Linear-time algorithms for testing the satisfiability of propositional Horn
formulae, The Journal of Logic Programming 1, 267-284 (1984). doi:10.1016/0743-1066(84)90014-1
[4] A. A. Klyachko, M. A. Can, S. Binicioğlu, A. S. Shumovsky, Simple Test for Hidden Variables in Spin-1
Systems, Phys. Rev. Lett. 101, 020403 (2008). doi:10.1103/PhysRevLett.101.020403
[5] T. Baumgratz, M. Cramer, M. B. Plenio, Quantifying Coherence, Phys. Rev. Lett. 113, 140401 (2014).
[6] B. Yadin, J. Ma, D. Girolami, M. Gu, V. Vedral, Quantum Processes Which Do Not Use Coherence,
Phys. Rev. X 6, 041028 (2016). doi:10.1103/PhysRevX.6.041028
[7] A. I. Lvovsky, H. Hansen, T. Aichele, O. Benson, J. Mlynek, S. Schiller, Quantum State Reconstruction of
the Single-Photon Fock State, Phys. Rev. Lett. 87, 050402 (2001). doi:10.1103/PhysRevLett.87.050402

References [1] to [4], [6], [7] were checked against Crossref on 2026-11-26 (title, authors, journal, volume,
pages or article number, year). [5] is the reference already carried by edge P4 of v2.6. The physics
references of the lifted hyperedges are those of the v2.6 records they come from.
