#!/usr/bin/env python3
"""build_v3.py - lift the binary network v2.6 to the hypergraph v3 and run the transfer calculus.

Inputs : data/network_v2.6.json, data/plain_readings.json, tools/v3_template.html
Outputs: data/hypergraph_v3.json, catalog/hyperedges_v3.md, v3.html

Run from the repository root:  python3 tools/build_v3.py
"""
import json, os, sys, re
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import hyperclosure as hc

net = json.load(open(os.path.join(ROOT, "data", "network_v2.6.json"), encoding="utf-8"))
plain = json.load(open(os.path.join(ROOT, "data", "plain_readings.json"), encoding="utf-8"))
NODE = {n["id"]: n for n in net["nodes"]}
EDGE = {e["id"]: e for e in net["edges"]}
short = lambda i: NODE[i].get("s") or {"m-quantum": "QT"}.get(i, NODE[i]["label"])
STATES = [n["id"] for n in net["nodes"] if n["type"] == "state"]
PROCS = [n["id"] for n in net["nodes"] if n["type"] == "process"]
WITS = [n["id"] for n in net["nodes"] if n["type"] == "witness"]

# ----------------------------------------------------------------------------- scopes
SCOPE_TOKENS = {
    "cv": "continuous variables",
    "odd-d": "odd (prime) dimension",
    "even-d": "qubits (even dimension)",
    "nondeg-H": "nondegenerate Hamiltonian (composites: noninteracting, nondegenerate total spectrum)",
    "deg-H": "H has an eigenvalue of multiplicity at least 2",
    "stab-eigenbasis": "H nondegenerate with a stabilizer eigenbasis",
    "tts-readout": "readout by TTS effects ([E, H] = 0)",
    "remote-prep": "remote-preparation scenario, all measurements on the steered side, tomographically complete convention",
    "energy-basis": "coherence taken with respect to the energy eigenbasis",
    "product-basis": "coherence taken with respect to a product basis",
    "io": "general incoherent operations (IO)",
    "dio": "dephasing-covariant operations with incoherent readout",
}
IMPLIED = {"stab-eigenbasis": ["nondeg-H"]}
INCOMPATIBLE = [("cv", "odd-d"), ("cv", "even-d"), ("odd-d", "even-d"), ("nondeg-H", "deg-H"), ("io", "dio")]
SC = hc.Scopes(IMPLIED, INCOMPATIBLE)

# ----------------------------------------------------------------------------- plain readings for the round-4 edges
plain.update({
    "U1": {"r": "When the Hamiltonian has a degenerate level, an observer restricted to covariant operations and energy-compatible measurements can still exhibit contextuality: inside a degenerate eigenspace the full quantum structure survives.",
           "c": "H has an eigenvalue of multiplicity at least 2. Sharpens N1, which covers nondegenerate H."},
    "U2": {"r": "Local filtering neither creates nor destroys generalized contextuality when all measurements are available: the scenario is contextual after an invertible filter exactly when it was before.",
           "c": "Convex state set, invertible filter, all POVMs in the scenario. Bell nonlocality behaves differently: filters can activate it (P7)."},
    "U3": {"r": "The odd-dimensional stabilizer subtheory shows EPR steering although it is noncontextual.",
           "c": "Steering judged against local hidden quantum states; maximally entangled stabilizer state with Z and X measurements."},
    "U4": {"r": "No time-translation-symmetric state is a magic state when every energy eigenstate is a stabilizer state.",
           "c": "H nondegenerate with a stabilizer eigenbasis. For degenerate H, or with a non-stabilizer eigenvector, TTS magic states exist."},
    "U5": {"r": "Covariant processing with energy-compatible readout cannot certify magic, although covariant dynamics can create it (the T gate is covariant for H = Z).",
           "c": "H nondegenerate with a stabilizer eigenbasis; readout by TTS effects."},
    "U5b": {"r": "Thermal operations can turn a stabilizer state into a magic state.",
            "c": "Qubit coupled to a heat bath; necessary and sufficient condition in de Oliveira Junior et al. (arXiv:2511.13839). For energy-diagonal inputs with H along a stabilizer axis no magic is generated."},
    "U6": {"r": "A state that is classical on the steered side - in particular any classical-classical state - gives a noncontextual remote-preparation scenario.",
           "c": "Remote-preparation scenario with all measurements; operational equivalences judged against all of quantum theory (tomographically complete convention)."},
    "U7": {"r": "Among separable states, discord on the steered side is needed for contextuality of the remote-preparation scenario but is not enough: an explicit discordant separable state gives a noncontextual scenario.",
           "c": "Separable states; remote-preparation scenario with all measurements; tomographically complete convention."},
})

# ----------------------------------------------------------------------------- hyperedges
H = []          # all hyperedge records beyond the 156 binary edges
def refs_of(*ids):
    out = []
    for i in ids:
        for r in EDGE[i]["refs"]:
            if r not in out and not r.lower().startswith("derived"):
                out.append(r)
    return out

def hyper(id, sig, tail, head, mod, status, reading, guard="", scope=(), frm=(), refs=(), note=""):
    for n in list(tail) + list(head):
        assert n in NODE, (id, n)
    for t in scope:
        assert t in SCOPE_TOKENS, (id, t)
    H.append({"id": id, "sig": sig, "tail": list(tail), "head": list(head), "mod": mod, "status": status,
              "scope": list(scope), "guard": guard, "reading": reading, "from": list(frm), "refs": list(refs), "note": note})

COMBO = {c["id"]: c for c in net["combos"]}
def crefs(k):
    return list(COMBO[k]["refs"])

# --- (1) detection hyperedges: state x process -> witness -------------------------------------
N1G = "Nondegenerate H; readout by TTS effects (N1)."
hyper("K1", "detect", ["s-tts", "p-cov"], ["w-ncineq", "w-sic", "w-kcbs", "w-cohw", "w-kd", "w-workq", "w-weakval"], "blind", "derived",
      "A time-translation-symmetric state probed only by covariant operations and energy-compatible measurements shows no contextuality, no Kirkwood-Dirac negativity, no anomalous weak value, no negative work quasiprobability and no coherence signal.",
      N1G + " The same blindness holds for every input state (unary records on Covariant processes).", ["nondeg-H", "tts-readout"], ["K1", "N1"], crefs("K1"))
hyper("K2", "detect", ["s-cohE", "p-projE"], ["w-cohw", "w-kd", "w-workq", "w-weakval", "w-ncineq"], "hidden", "theorem",
      "An energy-coherent state probed by the two-point projective energy measurement gives the statistics of its dephased version: the coherence is there, its witnesses stay silent.",
      "Two-point measurement scheme; the first measurement is projective in the energy eigenbasis.", [], ["K2", "P8"], crefs("K2"))
hyper("K3", "detect", ["s-cohE", "p-weak"], ["w-kd", "w-workq", "w-weakval", "w-ncineq"], "fires", "theorem",
      "An energy-coherent state probed by weak or direct sequential measurements can show Kirkwood-Dirac negativity, a negative work quasiprobability and anomalous weak values; each of these is a proof of generalized contextuality.",
      "Existence statement: suitable state, observables and coupling (C9, C10, G4).", [], ["K3", "P9"], crefs("K3"))
hyper("K4", "detect", ["s-thermal", "p-pauli"], ["w-sic", "w-ncineq"], "fires_all", "theorem",
      "Every thermal state, the maximally mixed state included, violates state-independent contextuality inequalities when it is measured with a Kochen-Specker set.",
      "Dimension at least 3 (Yu-Oh) or two qubits (Peres-Mermin). The KCBS functional is state dependent and is not covered.", [], ["K4", "N2"], crefs("K4"))
hyper("K5-blind", "detect", ["s-gauss", "p-gaussU"], ["w-wig", "w-ncineq", "w-bell", "w-kcbs"], "blind", "theorem",
      "Gaussian states processed by Gaussian operations and read out by homodyne detection form an epistricted theory, noncontextual and Wigner-positive: no negativity witness, no noncontextuality inequality, no KCBS functional and no Bell inequality fires.",
      "Continuous variables; all preparations, transformations and measurements Gaussian.", ["cv"], ["K5", "F2"], crefs("K5"))
hyper("K5-fires", "detect", ["s-gauss", "p-gaussU"], ["w-steer", "w-entw"], "fires", "theorem",
      "The same Gaussian resources violate steering inequalities and entanglement witnesses: a two-mode squeezed state with quadrature measurements.",
      "Continuous variables; existence statement (two-mode squeezed vacuum).", ["cv"], ["K5", "F2", "MH2"], crefs("K5"))
hyper("K6", "detect", ["s-gauss", "p-nongauss"], ["w-bell"], "fires", "theorem",
      "A Gaussian entangled state violates the CHSH inequality once displaced-parity (non-Gaussian) measurements are used; the Wigner function of the state stays positive.",
      "Continuous variables; existence statement (Banaszek-Wodkiewicz).", ["cv"], ["K6"], crefs("K6"))
hyper("K7", "detect", ["s-stab", "p-clifford"], ["w-ncineq", "w-kcbs", "w-wig", "w-magicw"], "blind", "theorem",
      "Inside the odd-dimensional stabilizer subtheory (stabilizer states, Clifford operations, Pauli measurements) no contextuality, Wigner-negativity or magic witness fires.",
      "Odd dimension; all operations and measurements are stabilizer operations.", ["odd-d"], ["K7", "C5"], crefs("K7"))
hyper("K8", "detect", ["s-stab", "p-pauli"], ["w-sic", "w-ncineq"], "fires_all", "theorem",
      "For qubits, stabilizer states measured in Pauli contexts (Mermin square) violate state-independent contextuality inequalities; every two-qubit state does.",
      "Qubits; two or more of them.", ["even-d"], ["K8", "C6"], crefs("K8"))
hyper("K9", "detect", ["s-magic", "p-pauli"], ["w-kcbs", "w-magicw"], "fires", "theorem",
      "A magic state measured with stabilizer (Pauli) measurements can violate a noncontextuality inequality, and it fires magic witnesses.",
      "Odd prime dimension. The contextuality witness fires exactly on the Wigner-negative magic states (C1; K24, K9-not).", ["odd-d"], ["K9", "C1"], crefs("K9"))
hyper("K9-not", "detect", ["s-magic", "p-pauli"], ["w-kcbs"], "not_always", "theorem",
      "Not every magic state does: bound-magic states (Wigner-positive, non-stabilizer) violate no noncontextuality inequality built from stabilizer measurements.",
      "Odd prime dimension; stabilizer measurements.", ["odd-d"], ["K9", "C1", "S5"], crefs("K9") + ["Veitch et al., NJP 14, 113011 (2012)"])
hyper("K10-fires", "detect", ["s-magic", "p-clifford"], ["w-magicw"], "fires_all", "theorem",
      "Every magic state is detected by a magic witness evaluated with stabilizer operations and Pauli measurements: the robustness of magic exceeds 1 exactly outside the stabilizer polytope.",
      "Robustness of magic is faithful (W12); Clifford processing cannot increase it.", [], ["K10", "W12"], crefs("K10") + ["Howard, Campbell, PRL 118, 090501 (2017)"])
hyper("K10-not", "detect", ["s-magic", "p-clifford"], ["w-wig"], "not_always", "theorem",
      "Some magic states are invisible to the Wigner-negativity witness: bound-magic states have a nonnegative discrete Wigner function.",
      "Odd dimension.", ["odd-d"], ["K10", "S5"], crefs("K10"))
hyper("K11-not", "detect", ["s-ent", "p-incompset"], ["w-bell"], "not_always", "counterexample",
      "Incompatible local measurements do not always reveal nonlocality: Werner states are entangled and yet have a local hidden variable model for all local measurements.",
      "Single copy, no pre-processing; projective measurements (Werner) and POVMs (Barrett).", [], ["K11", "B3"], crefs("K11"))
hyper("K11-fires", "detect", ["s-ent", "p-incompset"], ["w-entw"], "fires_all", "theorem",
      "Every entangled state violates some entanglement witness, and the witness can be evaluated from incompatible local measurement settings.",
      "The witness is decomposed into local observables; enough local settings are measured.", [], ["K11", "B10", "W4"], refs_of("B10"))
hyper("K12", "detect", ["s-ent", "p-filter"], ["w-bell"], "fires", "theorem",
      "Local filtering before the Bell test can make a Bell-local entangled state violate CHSH (hidden nonlocality).",
      "Existence statement; stochastic local operations with postselection.", [], ["K12", "P7", "B5"], crefs("K12"))
hyper("K13", "detect", ["s-sep", "p-locc"], ["w-bell", "w-steer", "w-entw"], "blind", "theorem",
      "A separable state under local operations and classical communication never violates a Bell inequality, a steering inequality or an entanglement witness.",
      "", [], ["K13"], crefs("K13"))
hyper("K14", "detect", ["s-bound", "p-locc"], ["w-entw", "w-bell"], "fires", "theorem",
      "Bound entangled states are detected by suitable entanglement witnesses measured locally, and some of them violate a Bell inequality.",
      "For the Bell functional an existence statement (Vertesi-Brunner state).", [], ["K14", "B9"], crefs("K14"))
hyper("K15", "detect", ["s-discord", "p-locc"], ["w-discw"], "fires_all", "theorem",
      "Every discordant state fails the local-broadcasting test.",
      "Local broadcasting is possible exactly for classical-classical states.", [], ["K15", "G7", "W14"], crefs("K15"))
hyper("K17", "detect", ["s-cohE", "p-cov"], ["w-cohw"], "hidden", "theorem",
      "Energy coherence processed by covariant operations and read out by energy-compatible measurements is present but undetectable.",
      N1G + " With general effects the surviving coherence remains detectable.", ["nondeg-H", "tts-readout", "energy-basis"], ["K17", "P2", "N1"], crefs("K17"))
hyper("K18", "detect", ["s-ent", "p-cov"], ["w-entw", "w-steer", "w-bell"], "blind", "derived",
      "An entangled state probed only by covariant operations and energy-compatible measurements never violates an entanglement witness, a steering inequality or a Bell inequality.",
      "Nondegenerate noninteracting H (nondegenerate total spectrum); TTS effects. Composition N1 + R1 + R2.", ["nondeg-H", "tts-readout"], ["K18", "N1", "R1", "R2"], ["N1 + R1 + R2 (this network; Corollary K18 of the concept paper)"])
# pathway rows lifted from binary theorems of v2.6 (no new physics: the premises are made explicit)
hyper("K19", "detect", ["s-ent", "p-incompset"], ["w-steer"], "fires", "theorem",
      "An entangled state with an incompatible set of measurements on the steering side can violate a steering inequality; every incompatible set does so with a suitable state.",
      "Quantum theory (B6).", [], ["B6"], refs_of("B6"))
hyper("K20", "detect", ["s-ent", "p-incompset"], ["w-bell"], "fires", "theorem",
      "An entangled state with incompatible measurements on both wings can violate a Bell inequality: every pure entangled state does, and every incompatible pair of two-outcome measurements does with a suitable state and partner.",
      "Existence statement; K11-not records the entangled states that never do.", [], ["B2", "B7"], refs_of("B2", "B7"))
hyper("K21", "detect", ["s-ent", "p-incompset"], ["w-ncineq"], "fires_all", "derived",
      "Every entangled state gives a contextual prepare-and-measure scenario when states are prepared remotely on one wing and all measurements are allowed there.",
      "Remote-preparation scenario; all measurements on the steered side; tomographically complete convention. R3 = A8 o B3.", ["remote-prep"], ["R3", "A8"], refs_of("R3"))
hyper("K22", "detect", ["s-zerodisc", "p-incompset"], ["w-ncineq"], "blind", "theorem",
      "A classical-classical state gives a noncontextual remote-preparation scenario whatever is measured.",
      "Remote-preparation scenario; tomographically complete convention (U6).", ["remote-prep"], ["U6"], refs_of("U6"))
hyper("K23", "detect", ["s-discord", "p-incompset"], ["w-ncineq"], "not_always", "counterexample",
      "Discord on the steered side does not guarantee a contextual remote-preparation scenario: an explicit discordant separable state gives a simplex-embeddable scenario.",
      "Remote-preparation scenario, all measurements, tomographically complete convention (U7). Together with K21 transferred to discordant states this is the open problem SG6.", ["remote-prep"], ["U7"], refs_of("U7"))
hyper("K24", "detect", ["s-wneg", "p-pauli"], ["w-kcbs"], "fires_all", "theorem",
      "Every Wigner-negative state violates a noncontextuality inequality built from stabilizer measurements.",
      "Odd prime dimension; the inequality is built from two-qudit stabilizer projectors, the state being paired with an ancilla qudit (C1).", ["odd-d"], ["C1"], refs_of("C1"))
hyper("K25", "detect", ["s-tts", "p-cov"], ["w-ncineq"], "fires", "derived",
      "If H has a degenerate level, time-translation-symmetric states probed by covariant operations and energy-compatible measurements can violate a noncontextuality inequality: six states inside a two-dimensional subspace of the degenerate eigenspace with three TTS projective measurements.",
      "H has an eigenvalue of multiplicity at least 2 (U1). Opposite to K1, which needs nondegenerate H.", ["deg-H", "tts-readout"], ["U1"], refs_of("U1"))
# canonical firing rows read off the witness-effect pairings and witness records
hyper("K26", "detect", ["s-wneg", "p-nongauss"], ["w-wig"], "fires_all", "definition",
      "Every Wigner-negative state is detected by the displaced-parity estimator, which measures the Wigner function point by point.",
      "Continuous variables; parity or photon-counting measurement, which is non-Gaussian (W8).", ["cv"], ["W8"], refs_of("W8"))
hyper("K27", "detect", ["s-ent", "p-locc"], ["w-entw"], "fires_all", "theorem",
      "Every entangled state is detected by some entanglement witness, and the witness can be evaluated with local measurements and classical communication.",
      "Completeness of witnesses (B10) and their local decomposition (witness record of EW). Replaces the verdict 'hidden' of row K16; see the retyped records.", [], ["B10", "W4", "K14"], refs_of("B10"))
hyper("K28", "detect", ["s-coh", "p-weak"], ["w-cohw"], "fires", "definition",
      "A coherent state fires coherence witnesses in interferometric or sequential circuits.",
      "Coherence relative to the basis probed by the circuit; existence statement (W13).", [], ["W13"], refs_of("W13"))
hyper("K29", "detect", ["s-coh", "p-unitary"], ["w-vis"], "fires", "definition",
      "A path-coherent state shows fringe visibility in an interferometer built from beam splitters and phases.",
      "Visibility detects interference phenomenology and does not certify nonclassicality (D3).", [], ["W16"], refs_of("W16"))
# rows generated in this round: cells left uncharted by the retyping, closed by elementary arguments or the literature
hyper("HG1", "detect", ["s-stab", "p-pauli"], ["w-kcbs"], "fires", "derived",
      "A stabilizer state can violate the KCBS inequality when the five projectors are not stabilizer measurements: for every pure qutrit state there is a pentagon of rays that reaches the quantum maximum sqrt(5).",
      "Qutrit; general KS ray sets. Proof: the KCBS operator, the sum of the five projectors, has largest eigenvalue sqrt(5); a unitary carrying its top eigenvector to the given pure state carries the pentagon to another pentagon with the same orthogonalities. K7 concerns stabilizer measurements only, so there is no contradiction.", [], ["C14", "K7"],
      ["Klyachko, Can, Binicioglu, Shumovsky, PRL 101, 020403 (2008)"])
hyper("HG2", "detect", ["s-coh", "p-incoh"], ["w-cohw"], "fires", "derived",
      "Incoherent operations with a readout in the incoherent basis can detect coherence: the incoherent channel with Kraus operators |0><+| and |1><-| copies the populations of the +/- basis into the incoherent basis.",
      "General incoherent operations (IO): each Kraus operator maps incoherent states to incoherent states. Proof: K1 = |0><+|, K2 = |1><-| satisfy K1*K1 + K2*K2 = 1 and K_n |i><i| K_n* is proportional to an incoherent state; the outcome probability <+|rho|+> equals 1/2 for every incoherent input and 1 for |+>. Not valid for dephasing-covariant operations (HG2b).", ["io"], ["P4", "W13"],
      ["Baumgratz, Cramer, Plenio, PRL 113, 140401 (2014) (definition of incoherent operations)"])
hyper("HG2b", "detect", ["p-incoh"], ["w-cohw"], "blind", "derived",
      "Dephasing-covariant operations with a readout in the incoherent basis see only the dephased state: no coherence witness fires, whatever the input.",
      "Dephasing-covariant operations L (D L = L D for the dephasing map D) and incoherent effects E = D(E): Tr(E L(rho)) = Tr(E L(D(rho))). This is the part of the v2.6 record 'CohW blind on Incoh' that holds.", ["dio"], ["P4"],
      ["Baumgratz, Cramer, Plenio, PRL 113, 140401 (2014)"])
hyper("HG3", "detect", ["s-wneg", "p-gaussU"], ["w-wig"], "fires", "theorem",
      "Wigner negativity can be detected with Gaussian measurements alone: homodyne tomography reconstructs the Wigner function, and the reconstruction of a single-photon state is negative at the origin.",
      "Continuous variables. The Wigner function is reconstructed from quadrature statistics; it is not measured by displaced parity (witness record of Parity: 'homodyne alone gives W only via tomography').", ["cv"], ["W8", "P10"],
      ["Lvovsky, Hansen, Aichele, Benson, Mlynek, Schiller, PRL 87, 050402 (2001)"])

# --- (2) unary detection records: the 'blind' lists of the witness records, lifted to edges -----
UNARY_SCOPE = {
    ("w-bell", "s-tts"): ["nondeg-H"], ("w-steer", "s-tts"): ["nondeg-H"], ("w-entw", "s-tts"): ["nondeg-H"], ("w-discw", "s-tts"): ["nondeg-H"],
    ("w-ncineq", "p-cov"): ["nondeg-H", "tts-readout"], ("w-sic", "p-cov"): ["nondeg-H", "tts-readout"], ("w-kcbs", "p-cov"): ["nondeg-H", "tts-readout"],
    ("w-kd", "p-cov"): ["nondeg-H", "tts-readout"], ("w-workq", "p-cov"): ["nondeg-H", "tts-readout"],
    ("w-cohw", "p-cov"): ["nondeg-H", "tts-readout", "energy-basis"],
    ("w-wig", "s-gauss"): ["cv"], ("w-wig", "s-stab"): ["odd-d"],
    ("w-kd", "s-tts"): ["energy-basis"], ("w-cohw", "s-tts"): ["energy-basis"], ("w-cohw", "p-projE"): ["energy-basis"],
    ("w-magicw", "p-cov"): ["stab-eigenbasis", "tts-readout"], ("w-magicw", "s-tts"): ["stab-eigenbasis"],
}
RETYPED_UNARY = {("w-kcbs", "s-stab"), ("w-wig", "p-gaussU"), ("w-magicw", "p-clifford"), ("w-cohw", "p-incoh")}
N1REF = ["N1 (this network)", "Lostaglio, PRL 120, 040602 (2018)"]
TPMREF = ["Perarnau-Llobet et al., PRL 118, 070601 (2017)", "Lostaglio, PRL 120, 040602 (2018)"]
UNARY_REFS = {   # (witness, cluster) -> (status, references); entries not listed: status theorem, no reference beyond the note
    ("w-bell", "s-tts"): ("derived", ["R1 (this network)"]), ("w-steer", "s-tts"): ("derived", ["R1 (this network)"]),
    ("w-entw", "s-tts"): ("derived", ["R1 (this network)"]), ("w-discw", "s-tts"): ("derived", ["R1 (this network)"]),
    ("w-magicw", "s-tts"): ("derived", ["U4 (this network)"]), ("w-magicw", "p-cov"): ("derived", ["U5 (this network)"]),
    ("w-cohw", "s-tts"): ("definition", []), ("w-kd", "s-tts"): ("derived", []), ("w-sorkin", "m-quantum"): ("theorem", refs_of("E9")),
    ("w-workq", "s-tts"): ("theorem", refs_of("W11")),
    ("w-cohw", "p-cov"): ("derived", ["N1 (this network)", "Marvian, Spekkens, Nat. Commun. 5, 3821 (2014)"]),
    ("w-ncineq", "p-cov"): ("derived", N1REF), ("w-sic", "p-cov"): ("derived", N1REF), ("w-kcbs", "p-cov"): ("derived", N1REF),
    ("w-kd", "p-cov"): ("derived", N1REF), ("w-workq", "p-cov"): ("derived", N1REF),
}
UNARY_GUARD = {("w-cohw", "p-cov"): "With TTS effects the statistics depend only on the dephased state (N1); covariant operations cannot increase energy coherence (P2).",
               ("w-kd", "s-tts"): "Kirkwood-Dirac distribution whose first basis is the energy eigenbasis: if [rho, P_a] = 0 then Q(a, b) = Tr(P_b P_a rho) = Tr(P_b P_a rho P_a) >= 0, a genuine joint probability (elementary).",
               ("w-sorkin", "m-quantum"): "I3 = 0 identically in quantum theory, in Sorkin's setting (orthogonal path subspaces, blocking by projection; scope note of R6). The estimator fires only in density-cube-type theories."}
for w, rec in net["witnesses"].items():
    for cid, cnote in rec["blind"]:
        if (w, cid) in RETYPED_UNARY:
            continue
        side = NODE[cid]["type"]
        what = {"state": "No state of the cluster '%s' fires the witness '%s', whatever the process.",
                "process": "No arrangement inside the process cluster '%s' fires the witness '%s', whatever the state.",
                "model": "Inside the model '%s' the witness '%s' never fires."}[side] % (NODE[cid]["label"], NODE[w]["label"])
        st, rf = UNARY_REFS.get((w, cid), ("theorem", TPMREF if cid == "p-projE" else []))
        hyper("B." + short(w) + "." + short(cid), "unary", [cid], [w], "blind", st, what, UNARY_GUARD.get((w, cid), cnote),
              UNARY_SCOPE.get((w, cid), []), ["witness record " + short(w)], rf)

# --- (3) requirement arcs: one witness -> the clusters it needs (joint necessity) ---------------
def req(wid, heads, reading, frm, guard="", scope=()):
    hyper("REQ." + short(wid), "require", [wid], heads, "requires", "theorem", reading, guard, scope, frm, refs_of(*[f for f in frm if f in EDGE]))
req("w-bell", ["s-ent", "p-incompset"], "A Bell-inequality violation needs an entangled state and incompatible measurements on each wing.", ["B1", "B1b", "B7"])
req("w-steer", ["s-ent", "p-incompset"], "A steering-inequality violation needs an entangled state and an incompatible measurement set on the steering side.", ["B1b", "B6"])
req("w-incomp", ["p-incompset"], "The joint-measurability test fails only for an incompatible measurement set.", ["W3"])
req("w-entw", ["s-ent"], "An entanglement witness is nonnegative on every separable state: it fires only on entangled states.", ["W4"])
req("w-wig", ["s-wneg"], "The Wigner estimator returns a negative value only for a Wigner-negative state.", ["W8"])
req("w-magicw", ["s-magic"], "A magic witness is bounded on the stabilizer polytope: it fires only on magic states.", ["W12"])
req("w-cohw", ["s-coh"], "A coherence witness fires only on states that are coherent in the named basis.", ["W13"])
req("w-discw", ["s-discord"], "The local-broadcasting test fails only for discordant states.", ["W14", "G7"])
req("w-workq", ["s-cohE"], "A negative work quasiprobability needs an initial state that does not commute with the Hamiltonian.", ["W11", "G4"], "Witness record of WorkQ.")
req("w-kd", ["s-coh"], "Kirkwood-Dirac nonpositivity needs a state that is coherent with respect to the two bases of the distribution.", ["R5", "W9"], "Coherence with respect to the Kirkwood-Dirac bases; noncommutation alone is not sufficient (R5).")

# --- (4) order records: definitional complements, and R2 as an exclusion of process clusters ----
def excl(id, a, b, reading, status="definition", scope=(), frm=(), guard=""):
    hyper(id, "order", [a], [b], "excludes" if status == "definition" else "forbids", status, reading, guard, scope, frm, refs_of(*[f for f in frm if f in EDGE]))
excl("X1", "s-sep", "s-ent", "A state is entangled exactly when it is not separable.")
excl("X2", "s-stab", "s-magic", "A state is a magic state exactly when it lies outside the stabilizer polytope.")
excl("X3", "s-tts", "s-cohE", "A state is energy-coherent exactly when it does not commute with the Hamiltonian.")
excl("X4", "s-zerodisc", "s-discord", "A state is discordant exactly when it is not classical-classical.", guard="Discord on at least one side.")
excl("X5", "s-thermal", "s-athermal", "A state is athermal exactly when it is not the Gibbs state.")
excl("X6", "p-cov", "p-incompset", "Energy-compatible measurements are jointly measurable: the covariant cluster with TTS effects contains no incompatible measurement set.",
     "derived", ["nondeg-H", "tts-readout"], ["R2"], "Nondegenerate H: every TTS POVM is a post-processing of the energy measurement (Lemma R2).")

# --- (5) transformation hyperedges: input state x process -> output state ----------------------
hyper("T1", "transform", ["s-tts", "p-cov"], ["s-cohE"], "cannot_create", "theorem",
      "Covariant operations cannot create energy coherence from a time-translation-symmetric state.", "Asymmetry monotones do not increase (P2).", [], ["P2"], refs_of("P2"))
hyper("T2", "transform", ["s-sep", "p-locc"], ["s-ent"], "cannot_create", "theorem",
      "Local operations and classical communication cannot create entanglement from a separable state.", "Entanglement monotones do not increase (P3). This is the content of the former row K16.", [], ["P3", "K16"], refs_of("P3"))
hyper("T3", "transform", ["s-gauss", "p-gaussU"], ["s-wneg"], "cannot_create", "theorem",
      "Gaussian operations cannot create Wigner negativity from a Gaussian state.", "Continuous variables; holds for every Wigner-positive input (P10).", ["cv"], ["P10"], refs_of("P10"))
hyper("T4", "transform", ["s-stab", "p-clifford"], ["s-magic"], "cannot_create", "theorem",
      "Clifford operations cannot create magic from a stabilizer state.", "Stabilizer operations map the stabilizer polytope into itself (resource theory of stabilizer computation).", [], ["W12", "P6"],
      ["Veitch, Mousavian, Gottesman, Emerson, NJP 16, 013009 (2014)"])
hyper("T5", "transform", ["s-gauss", "p-nongauss"], ["s-wneg"], "can_create", "theorem",
      "A non-Gaussian operation can turn a Gaussian state into a Wigner-negative state.", "Continuous variables; cubic or higher generators, photon counting (P11).", ["cv"], ["P11", "GN5"], refs_of("P11"))
hyper("T6", "transform", ["s-coh", "p-incoh"], ["s-ent"], "can_create", "theorem",
      "An incoherent operation can turn a coherent state into an entangled state.", "Bipartite incoherent operation on the state and an incoherent ancilla; the entanglement created is bounded by the input coherence (D1).", [], ["D1"], refs_of("D1"))
hyper("T7", "transform", ["s-stab", "p-thermalops"], ["s-magic"], "can_create", "theorem",
      "A thermal operation can turn a stabilizer state into a magic state.", "Qubit; conditions in de Oliveira Junior et al. For energy-diagonal inputs with H along a stabilizer axis no magic is created (U5b).", [], ["U5b", "U5"], refs_of("U5b"))

# --- (6) task hyperedges: state x process -> task ------------------------------------------------
hyper("Q1", "task", ["s-stab", "p-clifford"], ["t-mbqc"], "cannot_achieve", "theorem",
      "Stabilizer states with Clifford operations and Pauli measurements can be simulated efficiently on a classical computer: no universal quantum computation.", "Gottesman-Knill (P6).", [], ["P6"], refs_of("P6"))
hyper("Q2", "task", ["s-magic", "p-clifford"], ["t-mbqc"], "achieves", "theorem",
      "Magic states injected into Clifford circuits give universal quantum computation.", "State injection with distillable magic states (C4).", [], ["C4"], refs_of("C4"))
hyper("Q3", "task", ["s-gauss", "p-gaussU"], ["t-mbqc"], "cannot_achieve", "theorem",
      "Gaussian states with Gaussian operations and homodyne detection can be simulated efficiently: no quantum speed-up.", "Continuous variables; all components have nonnegative Wigner functions (C3).", ["cv"], ["C3"], ["Mari, Eisert, PRL 109, 230503 (2012)"])
hyper("Q4", "task", ["s-thermal", "p-thermalops"], ["t-secondlaws"], "cannot_achieve", "theorem",
      "Thermal operations leave the Gibbs state invariant: no resource state, hence no work, is obtained from it. Athermality is the necessary resource.", "Bath at the temperature of the Gibbs state (G1, P1).", [], ["G1", "P1"], refs_of("G1"))

# --- (7) multi-premise genesis and logical hyperedges ---------------------------------------------
hyper("L1", "logic", ["e-bell", "ax-nosig"], ["t-di"], "jointly_enable", "theorem",
      "A Bell-inequality violation together with no-signalling certifies randomness and secret key without trusting the devices.", "Witness record of CHSH: no-signalling is needed for the device-independent reading (B12).", [], ["B12"], refs_of("B12"))
hyper("L2", "logic", ["ax-symplectic", "ax-epirestrict"], ["m-spekkens", "m-gaussian", "m-stab-odd"], "jointly_generate", "theorem",
      "A classical phase space (Poisson structure) together with an epistemic restriction generates the noncontextual shell: Spekkens' toy theory, Gaussian quantum mechanics and the odd-dimensional stabilizer subtheory.", "Epistricted theories (GN1, GN2a-c).", [], ["GN1", "GN2a", "GN2b", "GN2c"], refs_of("GN2a", "GN2b", "GN2c"))
hyper("L3", "logic", ["ax-symplectic", "ax-moyal", "ax-complex", "ax-hbar"], ["m-quantum"], "jointly_generate", "theorem",
      "Quantum mechanics in phase space is the deformation of the Poisson algebra by the Moyal bracket; the Poisson structure, the lift, the complex unit and the scale hbar enter one formula, [f, g]_star = i hbar {f, g}_Moyal.", "Deformation quantization (GN4); i makes the commutator of observables an observable (GN7); hbar -> 0 returns the Poisson bracket (GN10).", [], ["GN4", "GN7", "GN10"], refs_of("GN4", "GN7"))
hyper("L4", "logic", ["m-quantum", "ax-nosig"], ["e-pr"], "jointly_exclude", "theorem",
      "Locally quantum systems composed under no-signalling cannot show superquantum (PR-box) correlations.", "E8.", [], ["E8"], refs_of("E8"))
hyper("L5", "logic", ["ax-nosig", "ax-norestrict"], ["m-boxworld"], "jointly_generate", "theorem",
      "No-signalling together with the no-restriction hypothesis gives boxworld as the maximal theory.", "E12.", [], ["E12"], refs_of("E12"))
hyper("L6", "logic", ["ax-purif", "ax-loctom"], ["m-quantum"], "jointly_generate", "theorem",
      "Purification together with local tomography and four further informational axioms singles out quantum theory.", "The four further axioms - causality, perfect distinguishability, ideal compression, atomicity of composition - are not nodes of the network (E6).", [], ["E6"], refs_of("E6"))
hyper("L7", "logic", ["e-incomp", "m-quantum"], ["e-ctx"], "jointly_imply", "partial",
      "When all quantum states are available as preparations, an incompatible measurement set always gives a contextual scenario.", "All quantum states available (A11). Without that premise incompatibility does not imply contextuality (A10): the second tail node is what separates the two edges.", [], ["A11", "A10"], refs_of("A11"))

# ----------------------------------------------------------------------------- records retyped with respect to v2.6 / v2b
RETYPED = [
    {"record": "K16  (Entangled states x LOCC -> EW: hidden)", "found": "closure conflict",
     "why": "K14 (bound entangled x LOCC -> EW fires) transferred along S10 (bound entangled is a sub-cluster of entangled) gives 'fires' on the same tuple. The note of K16 asserts that LOCC cannot increase entanglement, which is a statement about the output state, not about detection.",
     "now": "T2 (Separable states + LOCC cannot create Entangled states) and K27 (every entangled state fires EW under LOCC)."},
    {"record": "MagicW blind on Clifford operations (witness record)", "found": "closure conflict",
     "why": "K10 records 'fires' for Magic states x Clifford operations on the same witness. The note of the entry ('free operations: monotones non-increasing') is a statement about the output state.",
     "now": "T4 (Stabilizer states + Clifford operations cannot create Magic states); detection stays with K7 (blind) and K10-fires."},
    {"record": "Parity blind on Gaussian operations (witness record)", "found": "reading of the note",
     "why": "The note is P10, 'Gaussian processing cannot create negativity': a statement about the output state. As a detection verdict for every input it fails, because homodyne tomography reconstructs a negative Wigner function.",
     "now": "T3 (Gaussian states + Gaussian operations cannot create Wigner-negative states) and HG3 (Wigner-negative states x Gaussian operations -> fires by tomography); the blindness for Gaussian inputs is K5-blind."},
    {"record": "CohW blind on Incoherent / dephasing-covariant ops (witness record)", "found": "reading of the note",
     "why": "The note is P4, 'free operations cannot create coherence'. As a detection verdict it holds for dephasing-covariant operations and fails for general incoherent operations, which can read coherence out.",
     "now": "HG2b (blind, dephasing-covariant operations) and HG2 (fires, general incoherent operations): a split tuple, which marks the node as a union of two clusters."},
    {"record": "KCBS blind on Stabilizer states (witness record)", "found": "reading of the note",
     "why": "The note restricts the claim to stabilizer noncontextuality inequalities in odd dimension, i.e. to stabilizer measurements: a second tail node. For general KS ray sets a stabilizer state violates KCBS.",
     "now": "K7 (Stabilizer states x Clifford operations -> blind) already carries the claim; HG1 records the firing with non-stabilizer rays."},
    {"record": "K10  (Magic states x Clifford operations -> Parity: blind)", "found": "reading of the note",
     "why": "The note speaks of bound-magic states only: some magic states do not fire the negativity witness. The universal reading is false (Wigner-negative magic states exist).",
     "now": "K10-not (not_always)."},
    {"record": "K11  (Entangled states x Incompatible sets -> CHSH: blind)", "found": "reading of the note",
     "why": "The note speaks of Werner-type states only (status counterexample). Pure entangled states violate a Bell inequality with incompatible measurements (B2, B7).",
     "now": "K11-not (not_always) next to K20 (fires): a mixed tuple, the cluster-level form of hidden nonlocality."},
]
QUANTIFIER_NOTES = "Rows K4, K8, K10-fires, K11-fires, K15 are marked fires_all because their v2.6/v2b notes or the cited theorems state the result for every state of the cluster (N2; Mermin square; faithfulness of the robustness of magic; completeness of entanglement witnesses; local broadcasting iff classical-classical)."

# binary edges whose content a hyperedge states with its premises explicit (not followed by the forward-chaining tool)
SUPERSEDES = {"T1": ["P2"], "T2": ["P3"], "T3": ["P10"], "T5": ["P11"], "T6": ["D1"], "T7": ["U5b"], "Q1": ["P6"], "L1": ["B12"],
              "L2": ["GN2a", "GN2b", "GN2c"], "L3": ["GN4", "GN7"], "L4": ["E8"], "L5": ["E12"], "L7": ["A11"], "K12": ["P7"], "K3": ["P9"],
              "K2": ["P8"], "K19": ["B6"], "K21": ["R3"], "K22": ["U6"], "K23": ["U7"], "K24": ["C1"], "K25": ["U1"]}
for h in H:
    h["supersedes"] = SUPERSEDES.get(h["id"], [])
    for i in h["supersedes"]:
        assert i in EDGE, i
assert set(SUPERSEDES) <= {h["id"] for h in H}

# ----------------------------------------------------------------------------- engine inputs
INCL_S = [  # state-cluster inclusions recorded as binary edges (id of the edge, scope under which it is a set inclusion)
    {"id": "S3", "sub": "s-thermal", "sup": "s-tts", "scope": []},
    {"id": "S4", "sub": "s-cohE", "sup": "s-coh", "scope": ["energy-basis"]},
    {"id": "S7", "sub": "s-zerodisc", "sup": "s-sep", "scope": []},
    {"id": "S10", "sub": "s-bound", "sup": "s-ent", "scope": []},
    {"id": "S2", "sub": "s-ent", "sup": "s-discord", "scope": []},
    {"id": "S1", "sub": "s-ent", "sup": "s-coh", "scope": ["product-basis"]},
    {"id": "S5", "sub": "s-wneg", "sup": "s-magic", "scope": ["odd-d"]},
]
INCL_P = [
    {"id": "P1", "sub": "p-thermalops", "sup": "p-cov", "scope": []},
    {"id": "P5", "sub": "p-clifford", "sup": "p-unitary", "scope": []},
]
for a in INCL_S + INCL_P:
    e = EDGE[a["id"]]
    assert e["source"] == a["sub"] and e["target"] == a["sup"], a
incl_s = hc.inclusion_paths(STATES, INCL_S, SC)
incl_p = hc.inclusion_paths(PROCS, INCL_P, SC)
incl_t = {(t, t): [((), frozenset())] for t in [n["id"] for n in net["nodes"] if n["type"] == "task"]}

EXCL = [{"id": h["id"], "a": h["tail"][0], "b": h["head"][0], "scope": h["scope"]} for h in H if h["sig"] == "order"]
for eid, sc in (("S6", ["cv"]), ("S8", []), ("S9", ["odd-d"]), ("R1", ["nondeg-H"]), ("U4", ["stab-eigenbasis"])):
    e = EDGE[eid]; assert e["kind"] == "forbids"
    EXCL.append({"id": eid, "a": e["source"], "b": e["target"], "scope": sc})

REQS = []
for h in H:
    if h["sig"] == "require":
        for c in h["head"]:
            REQS.append({"id": h["id"], "witness": h["tail"][0], "cluster": c, "side": "S" if NODE[c]["type"] == "state" else "P", "scope": h["scope"]})
req_s = [r for r in REQS if r["side"] == "S"]; req_p = [r for r in REQS if r["side"] == "P"]
excl_s = [x for x in EXCL if NODE[x["a"]]["type"] == "state"]; excl_p = [x for x in EXCL if NODE[x["a"]]["type"] == "process"]
SYN = hc.requirement_records(req_s, excl_s, incl_s, SC) + hc.requirement_records(req_p, excl_p, incl_p, SC)

def det_records(hs):
    out = []
    for h in hs:
        if h["sig"] not in ("detect", "unary"):
            continue
        S = next((t for t in h["tail"] if NODE[t]["type"] == "state"), None)
        P = next((t for t in h["tail"] if NODE[t]["type"] == "process"), None)
        out.append({"id": h["id"], "S": S, "P": P, "heads": h["head"], "mod": h["mod"], "scope": h["scope"]})
    return out
DET = det_records(H)
N_TUPLES = len(STATES) * len(PROCS) * len(WITS)

# (a) the v2.6 rule on the v2.6 records - must reproduce the released census
def v26_rule(data):
    known = 0
    for w, rec in data["witnesses"].items():
        for s in STATES:
            for p in PROCS:
                c = next((c for c in data["combos"] if c["state"] == s and c["process"] == p), None)
                if c and w in c["verdict"]:
                    known += 1
                elif any(b[0] in (s, p) for b in rec["blind"]):
                    known += 1
    return known
V26_SETTLED = v26_rule(net)

# (b) raw mode: the v2.6 + v2b records taken literally (blind/hidden universal, fires existential)
K11X = {"id": "K11", "state": "s-ent", "process": "p-incompset", "verdict": {"w-bell": "blind", "w-entw": "fires"}}
K18X = {"id": "K18", "state": "s-ent", "process": "p-cov", "verdict": {"w-entw": "blind", "w-steer": "blind", "w-bell": "blind"}}
raw = []
for c in [c for c in net["combos"] if c["id"] != "K11"] + [K11X, K18X]:
    by = defaultdict(list)
    for w, v in c["verdict"].items():
        by[v].append(w)
    for v, ws in by.items():
        raw.append({"id": c["id"], "S": c["state"], "P": c["process"], "heads": ws, "mod": v, "scope": []})
for w, rec in net["witnesses"].items():
    for cid, _ in rec["blind"]:
        t = NODE[cid]["type"]
        raw.append({"id": "blind(%s|%s)" % (short(w), short(cid)), "S": cid if t == "state" else None, "P": cid if t == "process" else None,
                    "heads": [w], "mod": "blind", "scope": []})
incl_s0 = hc.inclusion_paths(STATES, [dict(a, scope=[]) for a in INCL_S], hc.Scopes())
incl_p0 = hc.inclusion_paths(PROCS, [dict(a, scope=[]) for a in INCL_P], hc.Scopes())
raw_table = hc.detection_table(STATES, PROCS, WITS, raw, incl_s0, incl_p0, hc.Scopes())
RAW_CONFLICTS = []
for w, row in raw_table.items():
    for (s, p), cell in row.items():
        if cell["cls"] == "conflict":
            RAW_CONFLICTS.append({"s": s, "p": p, "w": w,
                                  "pos": sorted({(d["by"][0], tuple(d["via"])) for d in cell["derivs"] if d["mod"] in hc.POS}),
                                  "neg": sorted({(d["by"][0], tuple(d["via"])) for d in cell["derivs"] if d["mod"] in hc.NEG_ALL})})

# (c) v3: stored records only, then with transfer and the requirement rule
T_STORED = hc.detection_table(STATES, PROCS, WITS, DET, incl_s, incl_p, SC, stored_only=True)
T_FULL = hc.detection_table(STATES, PROCS, WITS, DET + SYN, incl_s, incl_p, SC)
C_STORED = hc.census(T_STORED, N_TUPLES)
C_FULL = hc.census(T_FULL, N_TUPLES)

# (d) which stored unary state-side blind records are re-derived by the requirement rule
REDERIVED, PRIMITIVE = [], []
for h in H:
    if h["sig"] == "unary" and NODE[h["tail"][0]]["type"] == "state":
        sc = SC.close(h["scope"])
        hit = [r for r in SYN if r["S"] == h["tail"][0] and r["heads"] == h["head"] and SC.close(r["scope"]) <= sc]
        (REDERIVED if hit else PRIMITIVE).append((h["id"], [r["id"] for r in hit][:1]))

# (e) transformation and task signatures
TR = [{"id": h["id"], "A": h["tail"][0], "B": h["tail"][1], "C": h["head"][0], "mod": h["mod"], "scope": h["scope"]} for h in H if h["sig"] == "transform"]
TCL = hc.triple_closure(TR, "can_create", "cannot_create", incl_s, incl_p, incl_s, SC)
TCL = {k: v for k, v in TCL.items() if not (v[0]["mod"] == "can_create" and hc.leq(incl_s, k[0], k[2]))}   # drop a -> a (identity)
T_CONFLICTS = hc.triple_conflicts(TCL, "can_create", "cannot_create", SC)
TK = [{"id": h["id"], "A": h["tail"][0], "B": h["tail"][1], "C": h["head"][0], "mod": h["mod"], "scope": h["scope"]} for h in H if h["sig"] == "task"]
QCL = hc.triple_closure(TK, "achieves", "cannot_achieve", incl_s, incl_p, incl_t, SC, slots_c_monotone=False)
Q_CONFLICTS = hc.triple_conflicts(QCL, "achieves", "cannot_achieve", SC)

# (f) two-step pathways: (s1, p1) can create s2, and EVERY state of s2 fires w under p2
PATHS2 = []
for (a, b, c), ds in sorted(TCL.items()):
    for d in ds:
        if d["mod"] != "can_create" or not d["stored"]:
            continue
        for r in DET:
            if r["mod"] != "fires_all" or r["S"] is None:
                continue
            for via, sc_i in hc.leq(incl_s, c, r["S"]):
                sc = SC.close(set(d["scope"]) | set(r["scope"]) | sc_i)
                if SC.ok(sc):
                    for w in r["heads"]:
                        PATHS2.append({"s1": a, "p1": b, "s2": c, "p2": r["P"], "w": w, "by": [d["by"][0], r["id"]], "via": list(via), "scope": sorted(sc)})
# (g) created but unseen: p creates the cluster that w needs, and no arrangement inside P' >= p fires w
UNSEEN = []
for (a, b, c), ds in sorted(TCL.items()):
    for d in ds:
        if d["mod"] != "can_create":
            continue
        for h in H:
            if h["sig"] != "unary" or NODE[h["tail"][0]]["type"] != "process":
                continue
            w = h["head"][0]
            if not any(r["witness"] == w and r["cluster"] == c for r in REQS):
                continue
            for via, sc_i in hc.leq(incl_p, b, h["tail"][0]):
                sc = SC.close(set(d["scope"]) | set(h["scope"]) | sc_i)
                if SC.ok(sc):
                    UNSEEN.append({"s1": a, "p": b, "s2": c, "w": w, "by": d["by"] + d["via"] + [h["id"]] + list(via), "scope": sorted(sc)})

if __name__ == "__main__":
    lab = lambda i: NODE[i]["label"]
    print("nodes", len(net["nodes"]), "binary edges", len(net["edges"]), "hyperedge records", len(H))
    bysig = defaultdict(int)
    for h in H: bysig[h["sig"]] += 1
    print(" by signature:", dict(bysig))
    print("v2.6 rule on v2.6 records: settled", V26_SETTLED, "of", N_TUPLES)
    print("raw-mode conflicts (v2.6 + v2b records read literally):", len(RAW_CONFLICTS))
    for c in RAW_CONFLICTS: print("   ", short(c["s"]), "x", short(c["p"]), "->", short(c["w"]), "| pos", c["pos"], "| neg", c["neg"])
    print("v3 stored only :", C_STORED)
    print("v3 with transfer:", C_FULL)
    print("requirement rule re-derives", len(REDERIVED), "of", len(REDERIVED) + len(PRIMITIVE), "state-side blind records; primitive:", [p[0] for p in PRIMITIVE])
    print("transformation closure:", len(TCL), "tuples; stored", sum(1 for v in TCL.values() if any(d["stored"] for d in v)), "; conflicts", T_CONFLICTS)
    for k, v in sorted(TCL.items()):
        if not any(d["stored"] for d in v):
            print("    derived:", short(k[0]), "+", short(k[1]), v[0]["mod"], short(k[2]), "| by", v[0]["by"], "via", v[0]["via"], v[0]["scope"])
    print("task closure:", len(QCL), "tuples; conflicts", Q_CONFLICTS)
    for k, v in sorted(QCL.items()):
        if not any(d["stored"] for d in v):
            print("    derived:", short(k[0]), "+", short(k[1]), v[0]["mod"], k[2], "| by", v[0]["by"], "via", v[0]["via"], v[0]["scope"])
    print("two-step pathways:", len(PATHS2))
    for q in PATHS2: print("   ", short(q["s1"]), "+", short(q["p1"]), "->", short(q["s2"]), "+", short(q["p2"]), "->", short(q["w"]), q["by"], q["via"], q["scope"])
    print("created but unseen:", len(UNSEEN))
    for q in UNSEEN: print("   ", short(q["s1"]), "+", short(q["p"]), "->", short(q["s2"]), "| unseen by", short(q["w"]), q["by"], q["scope"])
    for cls in ("conflict", "split", "mixed"):
        print(cls, "tuples:")
        for w, row in T_FULL.items():
            for (s, p), cell in row.items():
                if cell["cls"] == cls:
                    print("   ", short(s), "x", short(p), "->", short(w), "|", sorted({(d["mod"], d["by"][0], tuple(d["scope"])) for d in cell["derivs"]}))


# ============================================================================= outputs
VERSION = "3.0 (2026-11-26)"
MOD_WORD = {
    "fires": "fires (some state)", "fires_all": "fires on every state", "blind": "blind", "hidden": "hidden (resource present)",
    "not_always": "does not always fire", "can_create": "can create", "cannot_create": "cannot create",
    "achieves": "achieves", "cannot_achieve": "cannot achieve", "jointly_enable": "jointly enable",
    "jointly_generate": "jointly generate", "jointly_imply": "jointly imply", "jointly_exclude": "jointly exclude",
    "requires": "requires", "excludes": "holds iff the other fails", "forbids": "rules out",
}
NEG_MODS = ["blind", "hidden", "not_always", "cannot_create", "cannot_achieve", "jointly_exclude", "excludes", "forbids"]
SIG_TITLE = {
    "detect": "Detection: state cluster + process cluster -> witness",
    "unary": "Unary detection records (the former blind lists): cluster -> witness",
    "require": "Requirement arcs: witness -> the clusters it needs",
    "order": "Order records: complements and exclusions between clusters",
    "transform": "Transformation: input state + process -> output state",
    "task": "Task: state cluster + process cluster -> task",
    "logic": "Genesis and logic: several axioms / models / effects -> conclusion",
}
SIG_ORDER = ["detect", "transform", "task", "logic", "require", "unary", "order"]


def best_derivs(ds, k=4):
    ds = sorted(ds, key=lambda d: (not d["stored"], len(d["scope"]), len(d["by"]), len(d["via"]), d["by"]))
    out, seen = [], set()
    for d in ds:                      # one of each modality first, so mixed / split tuples show both sides
        if d["mod"] not in seen:
            seen.add(d["mod"]); out.append(d)
    for d in ds:
        if len(out) >= k: break
        if d not in out: out.append(d)
    return [[d["mod"], d["by"], d["via"], d["scope"], 1 if d["stored"] else 0] for d in out[:k]]


def build_data():
    cells, per_w = {}, {}
    for w in WITS:
        row = {}
        cf, cs = defaultdict(int), defaultdict(int)
        for (s, p), cell in T_FULL[w].items():
            st = T_STORED[w].get((s, p))
            row[s + "|" + p] = [cell["cls"], st["cls"] if st else "", best_derivs(cell["derivs"])]
            cf[cell["cls"]] += 1
            if st: cs[st["cls"]] += 1
        cells[w] = row
        per_w[w] = {"full": dict(cf), "stored": dict(cs)}
    def tup(k, v):
        d = sorted(v, key=lambda d: (not d["stored"], len(d["scope"]), len(d["via"])))[0]
        return {"a": k[0], "b": k[1], "c": k[2], "mod": d["mod"], "by": d["by"], "via": d["via"], "scope": d["scope"], "stored": 1 if d["stored"] else 0}
    wit = {w: {"requires": r["requires"], **({"note": r["note"]} if r.get("note") else {})} for w, r in net["witnesses"].items()}
    meta = dict(net["meta"])
    meta["title"] = "Nonclassicality Network III - hypergraph form"
    meta["version"] = VERSION + ": hypergraph form of v2.6 (2026-11-01) with the pathway rows K11 (extended) and K18 of page v2b. Previous: " + net["meta"]["version"]
    meta["hypergraph"] = {
        "schema": "hyperedge = {id, sig, tail[], head[], mod, status, scope[], guard, reading, from[], refs[]}; a binary edge is the case |tail| = |head| = 1 and is kept in `edges` with its v2.6 record",
        "signatures": SIG_TITLE,
        "modalities": MOD_WORD,
        "negative_modalities": NEG_MODS,
        "scope_tokens": SCOPE_TOKENS,
        "scope_implied": IMPLIED,
        "scope_incompatible": INCOMPATIBLE,
        "inclusions": INCL_S + INCL_P,
        "transfer_rules": {
            "fires": "up in the state cluster, up in the process cluster",
            "fires_all": "down in the state cluster, up in the process cluster; implies fires",
            "blind / hidden": "down in both",
            "not_always": "up in the state cluster, down in the process cluster",
            "requires": "w requires c, x excludes c' and c is inside c'  =>  blind on x",
            "can_create / achieves": "up in every slot", "cannot_create / cannot_achieve": "down in every slot",
        },
        "quantifier_notes": QUANTIFIER_NOTES,
        "chain": {"note": "one-premise binary edges that the forward-chaining tool follows: an occurrence of the source entails or produces an occurrence of the target without a further premise",
                  "follow_kinds": ["subset", "pairs", "hosts", "generates", "enables"],
                  "follow_ids": ["B1", "B1b", "C10", "C14", "S1", "S2", "S5"],
                  "skip_ids": ["W1b", "P4"]},
    }
    counts = defaultdict(int)
    for h in H: counts[h["sig"]] += 1
    closure = {
        "tuples": N_TUPLES, "v26_rule_settled": V26_SETTLED,
        "stored": C_STORED, "full": C_FULL, "per_witness": per_w,
        "sorkin_cells": len(T_FULL["w-sorkin"]),
        "raw_conflicts": [{"s": c["s"], "p": c["p"], "w": c["w"], "pos": [list(map(list, [(a, list(b))])) [0] for a, b in c["pos"]], "neg": [[a, list(b)] for a, b in c["neg"]]} for c in RAW_CONFLICTS],
        "rederived": [r[0] for r in REDERIVED], "primitive": [r[0] for r in PRIMITIVE],
        "transform": [tup(k, v) for k, v in sorted(TCL.items())],
        "task": [tup(k, v) for k, v in sorted(QCL.items())],
        "paths2": PATHS2, "unseen": UNSEEN,
        "hyper_counts": dict(counts),
    }
    gaps = list(net["gaps"]) + [
        ["H1 · derived (v3)", "Transfer calculus on the hypergraph",
         "Verdicts move along recorded cluster inclusions: possibility upwards, impossibility downwards, and a requirement together with an exclusion gives blindness. Applied to the v3 records it settles %d further state x process x witness tuples without any new physics, re-derives %d of the %d state-side blindness records kept from v2.6 from pairings and exclusions, and reproduces U5 (covariant processes create magic that covariant probes cannot see) as a created-but-unseen pathway. Proof of soundness: catalog/hypergraph_v3_method.md." % (C_FULL["charted"] - C_STORED["charted"], len(REDERIVED), len(REDERIVED) + len(PRIMITIVE))],
        ["H2 · corrected (v3)", "Seven records retyped",
         "Read as detection verdicts with the transfer rules, the v2.6 + v2b records contain two contradictions (K16 against K14 with S10; 'MagicW blind on Clifford' against K10). Five further records state, in their own notes, either a non-generation claim or a claim about some states only. v3 records each with its premises explicit; the v2.6 and v2b pages are unchanged. Three rows close the cells this exposed: HG1 (a stabilizer state violates KCBS with non-stabilizer rays), HG2 / HG2b (incoherent operations can read coherence out, dephasing-covariant ones cannot), HG3 (homodyne tomography detects Wigner negativity)."],
        ["SG8 · open (structure)", "Clusters to refine, read off the mixed and split tuples",
         "A mixed tuple fires for some states of a cluster and provably not for others; a split tuple has opposite verdicts under incompatible hypotheses. Each names a missing node: Entangled states -> Bell-nonlocal / Bell-local (K20, K11-not); Magic states -> Wigner-negative (present) / bound magic (K9-not, K10-not); Discordant states -> contextual / noncontextual remote preparation (K21, K23; this is SG6); Incoherent operations -> general / dephasing-covariant (HG2, HG2b). The split tuple TTS x Covariant -> NC-LP is resolved by a hypothesis, not a node: nondegenerate against degenerate H (K1, K25; SG1 closed by U1)."],
        ["SG9 · open (automation hook)", "Uncharted tuples after transfer",
         "%d of %d state x process x witness tuples carry no verdict after transfer (v2.6 rule on v2.6 records: %d uncharted). The same census exists for the other signatures: state x process -> state has %d charted tuples of %d, state x process -> task %d of %d. Each uncharted tuple is a yes/no question in the sense of the method note; this supersedes the count in SG3." % (
             C_FULL["uncharted"], N_TUPLES, N_TUPLES - V26_SETTLED, len(TCL), len(STATES) * len(PROCS) * len(STATES), len(QCL), len(STATES) * len(PROCS) * 10)],
    ]
    return {"meta": meta, "nodes": net["nodes"], "edges": net["edges"], "hyper": H, "witnesses": wit,
            "plain": plain, "retyped": RETYPED, "closure": closure, "cells": cells, "gaps": gaps}


def dump_lines(data):
    """JSON with one record per line for the long arrays (diff-friendly, small)."""
    j = lambda x: json.dumps(x, ensure_ascii=False, separators=(",", ":"))
    parts = []
    for k, v in data.items():
        if k in ("nodes", "edges", "hyper", "retyped", "gaps"):
            parts.append(j(k) + ":[\n" + ",\n".join(j(r) for r in v) + "\n]")
        elif k in ("cells", "plain", "witnesses"):
            parts.append(j(k) + ":{\n" + ",\n".join(j(a) + ":" + j(b) for a, b in v.items()) + "\n}")
        else:
            parts.append(j(k) + ":" + j(v))
    return "{\n" + ",\n".join(parts) + "\n}\n"


def md_catalog(data):
    lab = lambda i: NODE[i]["label"]
    cs = lambda t: str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("|", "\\|")   # safe inside a markdown table cell
    L = []
    c = data["closure"]
    L.append("# Nonclassicality Network III: hyperedge catalog (v3.0, 2026-11-26)\n")
    L.append("Generated by `tools/build_v3.py` from `data/network_v2.6.json`; do not edit by hand. The definitions, the transfer rules and their proof are in `catalog/hypergraph_v3_method.md`.\n")
    L.append("## 1. Counts\n")
    L.append("- Nodes: %d (unchanged from v2.6). Binary edges: %d (unchanged). Hyperedge records beyond the binary edges: %d." % (len(net["nodes"]), len(net["edges"]), len(H)))
    L.append("- By signature: " + "; ".join("%s %d" % (k, c["hyper_counts"].get(k, 0)) for k in SIG_ORDER) + ".")
    L.append("- State x process x witness tuples: %d. Settled by the v2.6 rule on the v2.6 records: %d (reproduced)." % (c["tuples"], c["v26_rule_settled"]))
    L.append("- Settled by the v3 records alone: %d, of which %d are the single statement B.I3.QT (I3 = 0 in quantum theory)." % (c["stored"]["charted"], c["sorkin_cells"]))
    L.append("- Settled after transfer: %d (blind %d, hidden %d, fires on every state %d, fires %d, mixed %d, split %d, does not always fire %d); uncharted %d; conflicts %d." % (
        c["full"]["charted"], c["full"].get("blind", 0), c["full"].get("hidden", 0), c["full"].get("fires_all", 0), c["full"].get("fires", 0),
        c["full"].get("mixed", 0), c["full"].get("split", 0), c["full"].get("not_always", 0), c["full"]["uncharted"], c["full"].get("conflict", 0)))
    L.append("")
    L.append("## 2. Hyperedges\n")
    for sig in SIG_ORDER:
        hs = [h for h in H if h["sig"] == sig]
        L.append("### %s (%d)\n" % (SIG_TITLE[sig], len(hs)))
        L.append("| ID | Premises | Relation | Conclusions | Status | Reading. Conditions | From | References |")
        L.append("|---|---|---|---|---|---|---|---|")
        for h in hs:
            L.append("| %s | %s | %s | %s | %s | %s%s%s | %s | %s |" % (
                h["id"], " + ".join(lab(t) for t in h["tail"]), MOD_WORD[h["mod"]], "; ".join(lab(t) for t in h["head"]), h["status"],
                cs(h["reading"]), (" *Conditions:* " + cs(h["guard"])) if h["guard"] else "",
                (" *Scope:* " + ", ".join(h["scope"])) if h["scope"] else "",
                cs(", ".join(h["from"])), cs("; ".join(h["refs"]))))
        L.append("")
    L.append("## 3. Records of v2.6 / v2b retyped in v3\n")
    L.append("| Record | How found | Why | Now |")
    L.append("|---|---|---|---|")
    for r in RETYPED:
        L.append("| %s | %s | %s | %s |" % (cs(r["record"]), cs(r["found"]), cs(r["why"]), cs(r["now"])))
    L.append("")
    L.append(QUANTIFIER_NOTES + "\n")
    L.append("Mechanical check: reading the v2.6 + v2b records literally (blind and hidden universal, fires existential) and applying the transfer rules gives %d conflicting tuples:\n" % len(RAW_CONFLICTS))
    for x in RAW_CONFLICTS:
        L.append("- %s x %s -> %s: positive from %s; negative from %s." % (lab(x["s"]), lab(x["p"]), lab(x["w"]),
                 ", ".join(a + (" via " + "+".join(b) if b else "") for a, b in x["pos"]), ", ".join(a + (" via " + "+".join(b) if b else "") for a, b in x["neg"])))
    L.append("")
    L.append("## 4. Results of the transfer calculus\n")
    L.append("### 4.1 Tuples with two verdicts\n")
    for cls, txt in (("mixed", "Mixed (fires for some states of the cluster, provably not for others: the cluster is too coarse for this witness)"),
                     ("split", "Split (opposite verdicts under incompatible hypotheses)")):
        L.append("**%s**\n" % txt)
        for w, row in T_FULL.items():
            for (s, p), cell in row.items():
                if cell["cls"] == cls:
                    ds = sorted({(d["mod"], "+".join(d["by"]), "+".join(d["via"]), ", ".join(d["scope"])) for d in cell["derivs"]})
                    L.append("- %s x %s -> %s: " % (lab(s), lab(p), lab(w)) + "; ".join("%s by %s%s%s" % (m, b, (" via " + v) if v else "", (" [" + sc + "]") if sc else "") for m, b, v, sc in ds))
        L.append("")
    L.append("### 4.2 Transformation tuples (stored and derived)\n")
    L.append("| Input state | Process | Relation | Output state | By | Via | Scope |")
    L.append("|---|---|---|---|---|---|---|")
    for t in c["transform"]:
        L.append("| %s | %s | %s | %s | %s | %s | %s |" % (lab(t["a"]), lab(t["b"]), MOD_WORD[t["mod"]], lab(t["c"]), "+".join(t["by"]), "+".join(t["via"]) or "stored", ", ".join(t["scope"])))
    L.append("")
    L.append("### 4.3 Two-step pathways (creation, then detection on every created state)\n")
    L.append("| State | Process | Created state | Probe | Witness that fires | Records | Scope |")
    L.append("|---|---|---|---|---|---|---|")
    for q in PATHS2:
        L.append("| %s | %s | %s | %s | %s | %s | %s |" % (lab(q["s1"]), lab(q["p1"]), lab(q["s2"]), lab(q["p2"]), lab(q["w"]), " then ".join(q["by"]) + ((" via " + "+".join(q["via"])) if q["via"] else ""), ", ".join(q["scope"])))
    L.append("")
    L.append("### 4.4 Created but unseen (a process creates the cluster that a witness needs, and no arrangement inside the same process cluster fires the witness)\n")
    for q in UNSEEN:
        L.append("- %s + %s -> %s, unseen by %s. Records: %s. Scope: %s." % (lab(q["s1"]), lab(q["p"]), lab(q["s2"]), lab(q["w"]), ", ".join(q["by"]), ", ".join(q["scope"])))
    L.append("")
    L.append("### 4.5 State-side blind records re-derived by the requirement rule\n")
    L.append("Re-derived (%d): %s.\n" % (len(REDERIVED), ", ".join("%s (%s)" % (a, b[0]) for a, b in REDERIVED)))
    L.append("Primitive (%d), i.e. resting on their own note: %s.\n" % (len(PRIMITIVE), ", ".join(a for a, _ in PRIMITIVE)))
    L.append("### 4.6 Census per witness (charted tuples of %d)\n" % (len(STATES) * len(PROCS)))
    L.append("| Witness | v3 records | after transfer | classes after transfer |")
    L.append("|---|---|---|---|")
    for w in WITS:
        pw = c["per_witness"][w]
        L.append("| %s | %d | %d | %s |" % (lab(w), sum(pw["stored"].values()), sum(pw["full"].values()), ", ".join("%s %d" % kv for kv in sorted(pw["full"].items()))))
    L.append("")
    return "\n".join(L)


def emit():
    data = build_data()
    txt = dump_lines(data)
    json.loads(txt)
    open(os.path.join(ROOT, "data", "hypergraph_v3.json"), "w", encoding="utf-8").write(txt)
    open(os.path.join(ROOT, "catalog", "hyperedges_v3.md"), "w", encoding="utf-8").write(md_catalog(data))
    print("wrote data/hypergraph_v3.json (%d bytes), catalog/hyperedges_v3.md" % len(txt.encode("utf-8")))
    tpl_path = os.path.join(HERE, "v3_template.html")
    if os.path.exists(tpl_path):
        tpl = open(tpl_path, encoding="utf-8").read()
        assert tpl.count("<!--__DATA__-->") == 1 and tpl.count("<!--__HEAD__-->") == 1
        inline = '<script id="netdata" type="application/json">' + txt.replace("</", "<\\/") + "</script>"
        head = ('<!doctype html>\n<html lang="en">\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
                '<style>body{margin:0}</style>\n<p style="font-family:ui-monospace,monospace;font-size:12px;margin:10px 16px"><a href="./" style="color:inherit">&#8592; network overview</a></p>\n')
        open(os.path.join(ROOT, "v3.html"), "w", encoding="utf-8").write(tpl.replace("<!--__HEAD__-->", head).replace("<!--__DATA__-->", inline))
        art = os.path.join(ROOT, "tools", "_artifact")
        os.makedirs(art, exist_ok=True)
        open(os.path.join(art, "nonclassicality_hypergraph.html"), "w", encoding="utf-8").write(tpl.replace("<!--__HEAD__-->", "").replace("<!--__DATA__-->", ""))
        open(os.path.join(art, "hypergraph_v3.json"), "w", encoding="utf-8").write(txt)
        print("wrote v3.html and the artifact variant")


if __name__ == "__main__":
    emit()
