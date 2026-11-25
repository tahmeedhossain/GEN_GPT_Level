#!/usr/bin/env python3
"""Checks of tools/hyperclosure.py on hand-computed cases, and of the built data.  Run: python3 tools/test_hyperclosure.py"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import hyperclosure as hc

SC = hc.Scopes({"strong": ["weak"]}, [("x", "y"), ("weak", "anti")])
ST = ["a", "b", "c", "d"]          # a <= b <= c ;  d unrelated ; a <= d under scope x
PR = ["p", "q", "r"]               # p <= q ; r unrelated
incl_s = hc.inclusion_paths(ST, [{"id": "I1", "sub": "a", "sup": "b", "scope": []}, {"id": "I2", "sub": "b", "sup": "c", "scope": []},
                                 {"id": "I3", "sub": "a", "sup": "d", "scope": ["x"]}], SC)
incl_p = hc.inclusion_paths(PR, [{"id": "J1", "sub": "p", "sup": "q", "scope": []}], SC)

def cls(records, s, p, w="w"):
    return hc.classify(hc.cell_derivations(s, p, w, records, incl_s, incl_p, SC), SC)

def test_scopes():
    assert SC.close({"strong"}) == frozenset({"strong", "weak"})
    assert not SC.ok({"x", "y"}) and SC.ok({"x"}) and not SC.ok({"strong", "anti"})

def test_inclusions():
    assert hc.leq(incl_s, "a", "c")[0][0] == ("I1", "I2")
    assert hc.leq(incl_s, "c", "a") == []
    assert hc.leq(incl_s, "a", "d")[0][1] == frozenset({"x"})

def test_fires_goes_up():
    R = [{"id": "F", "S": "b", "P": "p", "heads": ["w"], "mod": "fires", "scope": []}]
    assert cls(R, "b", "p") == "fires" and cls(R, "c", "q") == "fires" and cls(R, "c", "p") == "fires"
    assert cls(R, "a", "p") == "uncharted" and cls(R, "b", "r") == "uncharted" and cls(R, "d", "p") == "uncharted"

def test_blind_goes_down():
    R = [{"id": "B", "S": "b", "P": "q", "heads": ["w"], "mod": "blind", "scope": []}]
    assert cls(R, "b", "q") == "blind" and cls(R, "a", "p") == "blind" and cls(R, "a", "q") == "blind"
    assert cls(R, "c", "q") == "uncharted" and cls(R, "b", "r") == "uncharted"

def test_fires_all_down_in_state_up_in_process():
    R = [{"id": "A", "S": "b", "P": "p", "heads": ["w"], "mod": "fires_all", "scope": []}]
    assert cls(R, "a", "q") == "fires_all" and cls(R, "b", "p") == "fires_all"
    assert cls(R, "c", "p") == "fires"            # only some state of the larger cluster is known to fire
    assert cls(R, "d", "p") == "uncharted"

def test_not_always_up_in_state_down_in_process():
    R = [{"id": "N", "S": "b", "P": "q", "heads": ["w"], "mod": "not_always", "scope": []}]
    assert cls(R, "c", "p") == "not_always" and cls(R, "a", "q") == "uncharted" and cls(R, "b", "r") == "uncharted"

def test_unary_records():
    R = [{"id": "U", "S": "b", "P": None, "heads": ["w"], "mod": "blind", "scope": []},
         {"id": "V", "S": None, "P": "q", "heads": ["v"], "mod": "blind", "scope": []}]
    assert all(cls(R, "a", p) == "blind" for p in PR) and cls(R, "c", "p") == "uncharted"
    assert all(cls(R, s, "p", "v") == "blind" for s in ST) and cls(R, "a", "r", "v") == "uncharted"

def test_mixed_split_conflict():
    F = {"id": "F", "S": "a", "P": "p", "heads": ["w"], "mod": "fires", "scope": []}
    N = {"id": "N", "S": "a", "P": "q", "heads": ["w"], "mod": "not_always", "scope": []}
    B = {"id": "B", "S": "c", "P": "q", "heads": ["w"], "mod": "blind", "scope": []}
    Bx = dict(B, scope=["x"]); Fy = dict(F, scope=["y"])
    assert cls([F, N], "a", "p") == "mixed"
    assert cls([F, B], "a", "p") == "conflict" and cls([F, B], "b", "q") == "conflict"
    assert cls([Fy, Bx], "a", "p") == "split"
    A = {"id": "A", "S": "c", "P": "p", "heads": ["w"], "mod": "fires_all", "scope": []}
    assert cls([A, N], "a", "p") == "conflict"     # every state of c fires inside p, yet some state of a never fires inside q >= p

def test_scope_blocks_transfer():
    R = [{"id": "B", "S": "d", "P": None, "heads": ["w"], "mod": "blind", "scope": ["y"]}]
    assert cls(R, "d", "p") == "blind" and cls(R, "a", "p") == "uncharted"   # a <= d only under x, incompatible with y

def test_requirement_rule():
    inc = hc.inclusion_paths(ST + ["e"], [{"id": "I1", "sub": "a", "sup": "b", "scope": []}], SC)
    syn = hc.requirement_records([{"id": "REQ", "witness": "w", "cluster": "a", "side": "S", "scope": []}],
                                 [{"id": "X", "a": "e", "b": "b", "scope": []}], inc, SC)      # w needs a, a <= b, e excludes b
    assert [(r["S"], r["mod"], r["by"]) for r in syn] == [("e", "blind", ["REQ", "X", "I1"])]
    assert hc.classify(hc.cell_derivations("e", "r", "w", syn, inc, incl_p, SC), SC) == "blind"
    assert hc.cell_derivations("a", "p", "w", syn, inc, incl_p, SC) == []

def test_triple_closure():
    T = [{"id": "C", "A": "a", "B": "p", "C": "b", "mod": "can", "scope": []}, {"id": "D", "A": "c", "B": "q", "C": "d", "mod": "cannot", "scope": []}]
    cl = hc.triple_closure(T, "can", "cannot", incl_s, incl_p, incl_s, SC)
    assert ("b", "q", "c") in cl and cl[("a", "p", "b")][0]["stored"]
    assert ("a", "p", "d") in cl and cl[("a", "p", "d")][0]["mod"] == "cannot"
    assert hc.triple_conflicts(cl, "can", "cannot", SC) == []
    T2 = T + [{"id": "E", "A": "a", "B": "p", "C": "d", "mod": "can", "scope": []}]
    assert ("a", "p", "d") in hc.triple_conflicts(hc.triple_closure(T2, "can", "cannot", incl_s, incl_p, incl_s, SC), "can", "cannot", SC)

def test_b_closure():
    E = [{"id": "h1", "tail": ["a", "b"], "head": ["c"]}, {"id": "h2", "tail": ["c"], "head": ["d"]}, {"id": "h3", "tail": ["c", "z"], "head": ["e"]}]
    reached, blocked = hc.b_closure(["a", "b"], E)
    assert set(reached) == {"a", "b", "c", "d"} and reached["d"] == (2, "h2") and blocked == [("h3", ["z"])]
    assert set(hc.b_closure(["a"], E)[0]) == {"a"}

def test_built_data():
    root = os.path.dirname(HERE)
    d = json.load(open(os.path.join(root, "data", "hypergraph_v3.json"), encoding="utf-8"))
    v26 = json.load(open(os.path.join(root, "data", "network_v2.6.json"), encoding="utf-8"))
    assert d["nodes"] == v26["nodes"] and d["edges"] == v26["edges"]            # the binary layer is v2.6, unchanged
    ids = {n["id"] for n in d["nodes"]}; eids = {e["id"] for e in d["edges"]}
    hid = [h["id"] for h in d["hyper"]]
    assert len(hid) == len(set(hid)) and not (set(hid) & eids)
    for h in d["hyper"]:
        assert set(h["tail"]) | set(h["head"]) <= ids and not (set(h["tail"]) & set(h["head"])) and h["reading"]
        assert set(h["scope"]) <= set(d["meta"]["hypergraph"]["scope_tokens"]) and set(h.get("supersedes", [])) <= eids
    c = d["closure"]
    assert c["v26_rule_settled"] == 469 and c["full"].get("conflict", 0) == 0 and c["stored"].get("conflict", 0) == 0
    assert c["full"]["charted"] + c["full"]["uncharted"] == c["tuples"] == 14 * 13 * 17
    n = sum(len(v) for v in d["cells"].values())
    assert n == c["full"]["charted"]
    assert sum(1 for v in d["cells"].values() for x in v.values() if x[1]) == c["stored"]["charted"]
    assert all(e["id"] in d["plain"] for e in d["edges"])                      # every binary edge has a plain reading
    assert d["cells"]["w-ncineq"]["s-tts|p-cov"][0] == "split" and d["cells"]["w-bell"]["s-ent|p-incompset"][0] == "mixed"
    assert d["cells"]["w-entw"]["s-ent|p-locc"][0] == "fires_all" and d["cells"]["w-entw"]["s-zerodisc|p-unitary"][0] == "blind"

if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t(); print("ok ", t.__name__)
    print(len(tests), "checks passed")
