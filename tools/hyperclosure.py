#!/usr/bin/env python3
"""hyperclosure.py - transfer calculus on an epistemic hypergraph (reference implementation).

The engine is independent of the physics. It takes

  * clusters ordered by recorded inclusions  (a "sub" is contained in a "sup"),
  * recorded exclusions between clusters      (two clusters share no member),
  * joint-premise records  T -> h  with a modality,
  * requirement records    w => c  ("w fires only on members of c"),

and returns, for every tuple of a signature, the verdicts that follow from the records by
monotone transfer, each with its derivation, plus the tuples on which two records disagree.

Modalities of a detection record (S, P) -> w   (S a state cluster, P a process cluster):

  fires       some state of S fires w under some arrangement inside P          (existential, positive)
  fires_all   every state of S fires w under some arrangement inside P         (universal in the state)
  blind       no state of S fires w under any arrangement inside P             (universal, negative)
  hidden      as blind, and the states of S carry the resource that w detects
  not_always  some state of S fires w under no arrangement inside P            (existential, negative)

Transfer rules (s <= S means "s is a sub-cluster of S"); soundness is proved in catalog/hypergraph_v3.md:

  fires(S,P)       =>  fires(s,p)       for S <= s, P <= p
  fires_all(S,P)   =>  fires_all(s,p)   for s <= S, P <= p     and  fires(S,P)
  blind(S,P)       =>  blind(s,p)       for s <= S, p <= P     (same for hidden)
  not_always(S,P)  =>  not_always(s,p)  for S <= s, p <= P
  requires(w; c), x and c' exclusive, c <= c'   =>  blind(x, any)   (or blind(any, x) for a process cluster)

Every record carries a scope: a set of tokens naming the standing hypotheses under which it holds
(e.g. "odd-d", "cv", "nondeg-H").  A derivation is discarded when the union of the scopes it uses
contains an incompatible pair; two opposite verdicts on one tuple are a *conflict* only when their
scopes are compatible, and a *split* (the tuple depends on the hypothesis) otherwise.
"""
from collections import defaultdict

POS = ("fires", "fires_all")
NEG_ALL = ("blind", "hidden")


# ----------------------------------------------------------------------------- scopes
class Scopes:
    def __init__(self, implied=None, incompatible=None):
        self.implied = implied or {}
        self.incompatible = [tuple(p) for p in (incompatible or [])]

    def close(self, tokens):
        out = set(tokens)
        changed = True
        while changed:
            changed = False
            for t in list(out):
                for u in self.implied.get(t, ()):
                    if u not in out:
                        out.add(u)
                        changed = True
        return frozenset(out)

    def ok(self, tokens):
        t = self.close(tokens)
        return not any(a in t and b in t for a, b in self.incompatible)


# ----------------------------------------------------------------------------- inclusion order
def inclusion_paths(nodes, arcs, scopes, maxlen=5):
    """arcs: [{id, sub, sup, scope}].  Returns {(a, b): [(via_ids, scope), ...]} for a <= b,
    keeping for each pair the derivations whose scope is minimal under set inclusion."""
    adj = defaultdict(list)
    for a in arcs:
        adj[a["sub"]].append(a)
    out = defaultdict(list)
    for n in nodes:
        out[(n, n)].append(((), frozenset()))
        stack = [(n, (), frozenset(), frozenset([n]))]
        while stack:
            cur, via, sc, seen = stack.pop()
            for a in adj[cur]:
                if a["sup"] in seen:
                    continue
                sc2 = scopes.close(sc | set(a.get("scope", ())))
                if not scopes.ok(sc2):
                    continue
                via2 = via + (a["id"],)
                out[(n, a["sup"])].append((via2, sc2))
                if len(via2) < maxlen:
                    stack.append((a["sup"], via2, sc2, seen | {a["sup"]}))
    pruned = {}
    for k, lst in out.items():
        keep = []
        for via, sc in sorted(lst, key=lambda x: (len(x[1]), len(x[0]), x[0])):
            if not any(s2 <= sc for _, s2 in keep):
                keep.append((via, sc))
        pruned[k] = keep
    return pruned


def leq(incl, a, b):
    """Derivations of a <= b (empty list if not derivable)."""
    return incl.get((a, b), [])


# ----------------------------------------------------------------------------- requirement rule
def requirement_records(requires, exclusions, incl, scopes):
    """requires: [{id, witness, cluster, side ('S'|'P'), scope}]
    exclusions: [{id, a, b, scope}]  (a and b share no member)
    Returns synthetic unary blind records: every cluster x <= a with c <= b (or the mirror image)."""
    out = []
    for r in requires:
        c = r["cluster"]
        for x in exclusions:
            for a, b in ((x["a"], x["b"]), (x["b"], x["a"])):
                for via_c, sc_c in leq(incl, c, b):
                    sc = scopes.close(set(r.get("scope", ())) | set(x.get("scope", ())) | sc_c)
                    if not scopes.ok(sc):
                        continue
                    out.append({
                        "id": r["id"] + "+" + x["id"],
                        "S": a if r["side"] == "S" else None,
                        "P": a if r["side"] == "P" else None,
                        "heads": [r["witness"]],
                        "mod": "blind",
                        "scope": sorted(sc),
                        "by": [r["id"], x["id"]] + list(via_c),
                        "origin": "requirement",
                    })
    return out


# ----------------------------------------------------------------------------- detection signature
def _down(incl, x, X):
    """x <= X, or X is None (the record does not restrict this slot)."""
    return [((), frozenset())] if X is None else leq(incl, x, X)


def _up(incl, x, X):
    """X <= x; a record that leaves the slot open cannot be transferred upwards."""
    return [] if X is None else leq(incl, X, x)


def cell_derivations(s, p, w, records, incl_s, incl_p, scopes):
    """All derivations of a verdict for the tuple (s, p; w)."""
    out = []

    def add(mod, r, ds, dp):
        for via_s, sc_s in ds:
            for via_p, sc_p in dp:
                sc = scopes.close(set(r.get("scope", ())) | sc_s | sc_p)
                if not scopes.ok(sc):
                    continue
                via = list(via_s) + list(via_p)
                out.append({
                    "mod": mod,
                    "by": list(r.get("by", [r["id"]])),
                    "via": via,
                    "scope": sorted(sc),
                    "stored": (not via) and r.get("origin", "stored") == "stored",
                })

    for r in records:
        if w not in r["heads"]:
            continue
        S, P, mod = r.get("S"), r.get("P"), r["mod"]
        if mod in NEG_ALL:
            add(mod, r, _down(incl_s, s, S), _down(incl_p, p, P))
        elif mod == "fires":
            add("fires", r, _up(incl_s, s, S), _up(incl_p, p, P))
        elif mod == "fires_all":
            add("fires_all", r, _down(incl_s, s, S) if S is not None else [], _up(incl_p, p, P))
            if s != S:
                add("fires", r, _up(incl_s, s, S), _up(incl_p, p, P))
        elif mod == "not_always":
            add("not_always", r, _up(incl_s, s, S), _down(incl_p, p, P) if P is not None else [])
        else:
            raise ValueError("unknown modality " + mod)
    # de-duplicate
    seen, uniq = set(), []
    for d in out:
        k = (d["mod"], tuple(d["by"]), tuple(d["via"]), tuple(d["scope"]))
        if k not in seen:
            seen.add(k)
            uniq.append(d)
    return uniq


def classify(derivs, scopes):
    """Verdict class of a tuple from its derivations."""
    if not derivs:
        return "uncharted"
    pos = [d for d in derivs if d["mod"] in POS]
    pall = [d for d in derivs if d["mod"] == "fires_all"]
    neg = [d for d in derivs if d["mod"] in NEG_ALL]
    nal = [d for d in derivs if d["mod"] == "not_always"]
    clash = [(a, b) for a in pos for b in neg] + [(a, b) for a in pall for b in nal]
    if any(scopes.ok(set(a["scope"]) | set(b["scope"])) for a, b in clash):
        return "conflict"
    if pos and neg:
        return "split"
    if neg:
        return "hidden" if any(d["mod"] == "hidden" for d in neg) else "blind"
    if pos and nal:
        return "mixed"
    if pall:
        return "fires_all"
    if pos:
        return "fires"
    return "not_always"


def detection_table(states, procs, witnesses, records, incl_s, incl_p, scopes, stored_only=False):
    """{w: {(s, p): {"cls": class, "derivs": [...]}}} for every charted tuple."""
    table = {}
    for w in witnesses:
        row = {}
        for s in states:
            for p in procs:
                ds = cell_derivations(s, p, w, records, incl_s, incl_p, scopes)
                if stored_only:
                    ds = [d for d in ds if d["stored"]]
                if ds:
                    row[(s, p)] = {"cls": classify(ds, scopes), "derivs": ds}
        table[w] = row
    return table


def census(table, n_tuples):
    c = defaultdict(int)
    for row in table.values():
        for cell in row.values():
            c[cell["cls"]] += 1
    charted = sum(c.values())
    c["uncharted"] = n_tuples - charted
    c["charted"] = charted
    c["total"] = n_tuples
    return dict(c)


# ----------------------------------------------------------------------------- three-slot signatures
def triple_closure(records, pos_mod, neg_mod, incl_a, incl_b, incl_c, scopes, slots_c_monotone=True):
    """Records (A, B) -> C with a positive existential modality `pos_mod` and a negative universal
    modality `neg_mod`.  Positive records transfer up in A and B (and up in C when the head is a
    cluster: a member of C is a member of every super-cluster); negative records transfer down in
    A, B (and C).  Returns {(a, b, c): [derivations]}."""
    out = defaultdict(list)
    for r in records:
        A, B, C, mod = r["A"], r["B"], r["C"], r["mod"]
        if mod == pos_mod:
            ca = [(a, d) for (x, a), ds in incl_a.items() if x == A for d in ds]
            cb = [(b, d) for (x, b), ds in incl_b.items() if x == B for d in ds]
            cc = [(c, d) for (x, c), ds in incl_c.items() if x == C for d in ds] if slots_c_monotone else [(C, ((), frozenset()))]
        elif mod == neg_mod:
            ca = [(a, d) for (a, x), ds in incl_a.items() if x == A for d in ds]
            cb = [(b, d) for (b, x), ds in incl_b.items() if x == B for d in ds]
            cc = [(c, d) for (c, x), ds in incl_c.items() if x == C for d in ds] if slots_c_monotone else [(C, ((), frozenset()))]
        else:
            raise ValueError("unknown modality " + mod)
        for a, (va, sa) in ca:
            for b, (vb, sb) in cb:
                for c, (vc, sc_) in cc:
                    sc = scopes.close(set(r.get("scope", ())) | sa | sb | sc_)
                    if not scopes.ok(sc):
                        continue
                    via = list(va) + list(vb) + list(vc)
                    out[(a, b, c)].append({"mod": mod, "by": [r["id"]], "via": via, "scope": sorted(sc), "stored": not via})
    return out


def triple_conflicts(closure, pos_mod, neg_mod, scopes):
    bad = []
    for k, ds in closure.items():
        pos = [d for d in ds if d["mod"] == pos_mod]
        neg = [d for d in ds if d["mod"] == neg_mod]
        if any(scopes.ok(set(a["scope"]) | set(b["scope"])) for a in pos for b in neg):
            bad.append(k)
    return bad


# ----------------------------------------------------------------------------- structural hyperpaths
def b_closure(start, hyperedges):
    """Forward chaining (B-connection of Gallo et al. 1993): a hyperedge is traversed when ALL its
    tail nodes have been reached.  hyperedges: [{id, tail, head}] (positive ones only).
    Returns (reached {node: (round, edge id or None)}, blocked [(edge id, missing tail nodes)])."""
    reached = {n: (0, None) for n in start}
    rnd = 0
    changed = True
    while changed:
        changed = False
        rnd += 1
        new = {}
        for e in hyperedges:
            if all(t in reached for t in e["tail"]):
                for h in e["head"]:
                    if h not in reached and h not in new:
                        new[h] = (rnd, e["id"])
        if new:
            reached.update(new)
            changed = True
    blocked = []
    for e in hyperedges:
        have = [t for t in e["tail"] if t in reached]
        miss = [t for t in e["tail"] if t not in reached]
        if have and miss:
            blocked.append((e["id"], miss))
    return reached, blocked
