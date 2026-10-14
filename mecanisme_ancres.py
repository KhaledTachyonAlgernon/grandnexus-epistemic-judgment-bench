"""H-Mécanisme-ancres (H73-H77) : décomposition par greffe de paramètres, cache versionné."""
import copy, json, os, random, sys, time
from cache import repertoire
from evaluer import _bootstrap
from monde import generer, Enonce
from meprise import Meprise

ANCRE, EXPLIQUER, REPLIQUER = "L'Ancre", (50, 51, 52), (53, 54, 55)
CACHE = repertoire("mecanisme_ancres")
fin = time.time() + float(sys.argv[1] if len(sys.argv) > 1 and __name__ == "__main__" else 160)


def corpus(m, g, part):
    nom, _, cibles = m.menteur
    ordre = sorted(cibles)
    random.Random(f"ancres|{g}").shuffle(ordre)                # même ordre que test_ancres.py
    ancres = set(ordre[:round(part * len(ordre))])
    c = list(m.enonces)
    for cle in sorted(ancres):
        for t in range(m.n_epoques):
            c.append(Enonce(len(c), t, ANCRE, cle[0], cle[1], m.verite[cle][t], ""))
    return c, ancres, cibles


def exact(o, m, faits):
    return [[f"{f[0]}|{f[1]}", int(o.resoudre(f[0], f[1], t)[0] == m.verite[f][t])]
            for f in sorted(faits) if f in o.croyance for t in range(m.n_epoques)]


def greffe(o0, o5, quoi):
    o = copy.deepcopy(o0)
    if "f" in quoi:
        o.f = {s: o5.f[s] for s in o0.f}
    if "q" in quoi:
        o.q = {s: o5.q[s] for s in o0.q}
    if "parent" in quoi:
        o.parent = {k: v for k, v in o5.parent.items() if k in o0.f}
    if "tout" in quoi:
        o.f = {s: o5.f[s] for s in o0.f}; o.q = {s: o5.q[s] for s in o0.q}
        o.parent = {k: v for k, v in o5.parent.items() if k in o0.f}
        o.L = {s: o5.L[s] for s in o0.L}; o.p = dict(o5.p)
        o.lam, o.N, o.Nv = dict(o5.lam), o5.N, o5.Nv
    o._col = {}
    o.croyance, _ = o._etape_e()
    return o


def charge(g):
    f = f"{CACHE}/{g}.json"
    if os.path.exists(f):
        return json.load(open(f))
    if time.time() > fin:
        print(f"… à suivre (graine {g})"); sys.exit(0)
    m = generer("complice", g)
    c0, _, cibles = corpus(m, g, 0.0)
    c5, ancres, _ = corpus(m, g, 0.5)
    o0 = Meprise(fixes={ANCRE: 0.99}); o0.ingerer(c0)
    o5 = Meprise(fixes={ANCRE: 0.99}); o5.ingerer(c5)
    U = set(cibles) - ancres                                    # faits ciblés NON ancrés
    hors = {k for k in m.verite if k not in cibles and k in o0.croyance}
    res = {"base": exact(o0, m, U), "ancre50": exact(o5, m, U),
           "parents50": {k: [p, round(c, 2)] for k, (p, c) in o5.parent.items()},
           "parents0": {k: [p, round(c, 2)] for k, (p, c) in o0.parent.items()}}
    if g in EXPLIQUER:
        for q in (("f",), ("q",), ("parent",), ("tout",)):
            o = greffe(o0, o5, q)
            res["greffe_" + "+".join(q)] = exact(o, m, U)
            if q == ("f",):
                res["hors_base"], res["hors_greffe_f"] = exact(o0, m, hors), exact(o, m, hors)
                res["hors_ancre50"] = exact(o5, m, hors)
    json.dump(res, open(f, "w"))
    return res


if __name__ == "__main__":
    R = {g: charge(g) for g in EXPLIQUER + REPLIQUER}
    acc = lambda L: sum(x[1] for x in L) / len(L)
    print(f"BILAN — H-Mécanisme-ancres — cache {CACHE}\n")
    B = [x for g in EXPLIQUER for x in R[g]["base"]]
    A = [x for g in EXPLIQUER for x in R[g]["ancre50"]]
    gain = acc(A) - acc(B)
    print(f"Faits ciblés non ancrés (graines 50-52) : sans ancre {acc(B):.1%} ; avec 50 % d'ancres {acc(A):.1%} ; gain {gain:+.1%}")
    for k in ("greffe_f", "greffe_q", "greffe_parent", "greffe_tout"):
        G = [x for g in EXPLIQUER for x in R[g][k]]
        print(f"   {k:<15} {acc(G):.1%}   part du gain récupérée : {(acc(G) - acc(B)) / gain:+.0%}")
    print("\nFiliations détectées (modèle 0 % → modèle 50 %) :")
    for g in EXPLIQUER + REPLIQUER:
        print(f"   g{g} : {R[g]['parents0'] or 'aucune'}  →  {R[g]['parents50'] or 'aucune'}")
    H0 = [x for g in EXPLIQUER for x in R[g]["hors_base"]]
    HF = [x for g in EXPLIQUER for x in R[g]["hors_greffe_f"]]
    H5 = [x for g in EXPLIQUER for x in R[g]["hors_ancre50"]]
    print(f"\nHors cibles (descriptif) : base {acc(H0):.2%} ; greffe des fiabilités seules {acc(HF):.2%} ; modèle ancré {acc(H5):.2%}")
    Br = [x for g in REPLIQUER for x in R[g]["base"]]
    Ar = [x for g in REPLIQUER for x in R[g]["ancre50"]]
    d, h, k = _bootstrap([a[1] - b[1] for a, b in zip(Ar, Br)], [a[0] for a in Ar], tirages=2000)
    print(f"\nH77 réplication (graines 53-55) : {acc(Br):.1%} → {acc(Ar):.1%} ; gain {d:+.1%} ± {h:.1%} ({k} faits)")
