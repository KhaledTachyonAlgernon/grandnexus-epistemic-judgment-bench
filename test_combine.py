"""H-Combiné (H100-H103) : un signal de doute combiné, lisible, bon dans tous les mondes ? Graines neuves 70-72."""
import json, os, random, sys, time
from cache import repertoire
from monde import generer
from meprise import Meprise
from test_selection import score_signaux

MONDES, GRAINES = ("facile", "echo", "menteur", "plausible", "complice"), (70, 71, 72)
CACHE = repertoire("combine")
fin = time.time() + float(sys.argv[1] if len(sys.argv) > 1 else 170)


def charge(w, g):
    fic = f"{CACHE}/{w}_{g}.json"
    if os.path.exists(fic):
        return json.load(open(fic))
    if time.time() > fin:
        print(f"… à suivre ({w}, graine {g})"); sys.exit(0)
    m = generer(w, g)
    o = Meprise(); o.ingerer(m.enonces)
    sc = score_signaux(o, m)
    out = []
    for cle in sorted(o.croyance):
        for t in range(m.n_epoques):
            post = o.croyance[cle][t]
            a = max(range(len(post)), key=post.__getitem__)
            u, c = 1 - post[a], sc[cle][0]
            out.append({"fait": f"{g}|{cle[0]}|{cle[1]}", "faux": int(o.dom[cle[1]][a] != m.verite[cle][t]),
                        "incertitude": u, "contestation": c, "combine": (1.0 if c >= 2 else 0.0) + u})
    json.dump(out, open(fic, "w"))
    return out


def rangs(v):
    ordre = sorted(range(len(v)), key=lambda i: v[i])
    r = [0.0] * len(v)
    i = 0
    while i < len(ordre):
        j = i
        while j + 1 < len(ordre) and v[ordre[j + 1]] == v[ordre[i]]:
            j += 1
        for k in range(i, j + 1):
            r[ordre[k]] = (i + j) / 2 + 1
        i = j + 1
    return r


def auc(L, cle):
    r = rangs([x[cle] for x in L])
    P = sum(1 for x in L if x["faux"])
    N = len(L) - P
    if not P or not N:
        return float("nan")
    return (sum(ri for ri, x in zip(r, L) if x["faux"]) - P * (P + 1) / 2) / (P * N)


def boot(L, f, tirages=400, graine=11):
    par = {}
    for x in L:
        par.setdefault(x["fait"], []).append(x)
    faits = sorted(par)
    rng = random.Random(graine)
    d = []
    for _ in range(tirages):
        E = [x for k in (rng.choice(faits) for _ in faits) for x in par[k]]
        v = f(E)
        if v == v:
            d.append(v)
    d.sort()
    return d[int(0.025 * len(d))], d[int(0.975 * len(d)) - 1]


def capture(L, cle, part=0.10, graine=3):
    rng = random.Random(graine)
    pris = sorted(L, key=lambda x: (-x[cle], rng.random()))[:round(part * len(L))]
    return sum(x["faux"] for x in pris) / max(1, sum(x["faux"] for x in L))


if __name__ == "__main__":
    R = {(w, g): charge(w, g) for w in MONDES for g in GRAINES}
    print(f"BILAN — H-Combiné, graines 70-72 — cache {CACHE}\n")
    for L in R.values():                                     # descriptif : max des rangs-centiles, par monde-graine
        ru, rc = rangs([x["incertitude"] for x in L]), rangs([x["contestation"] for x in L])
        for x, a, b in zip(L, ru, rc):
            x["max_rangs"] = max(a, b) / len(L)
    sig = ("incertitude", "contestation", "combine", "max_rangs")
    A, C = {}, {}
    print(f"{'monde':<10}{'erreurs':>12}" + "".join(f"{s:>14}" for s in sig) + "    capture 10 % (inc. / cont. / comb.)")
    for w in MONDES:
        L = [x for g in GRAINES for x in R[(w, g)]]
        A[w] = {s: auc(L, s) for s in sig}
        C[w] = {s: capture(L, s) for s in sig}
        print(f"{w:<10}{sum(x['faux'] for x in L):>5}/{len(L):<6}" + "".join(f"{A[w][s]:>14.3f}" for s in sig)
              + f"    {C[w]['incertitude']:.0%} / {C[w]['contestation']:.0%} / {C[w]['combine']:.0%}")
    print(f"\nH100 pire monde : incertitude {min(A[w]['incertitude'] for w in MONDES):.3f} ; contestation "
          f"{min(A[w]['contestation'] for w in MONDES):.3f} ; combiné {min(A[w]['combine'] for w in MONDES):.3f}")
    Lc = [x for g in GRAINES for x in R[("complice", g)]]
    lo, hi = boot(Lc, lambda E: auc(E, "combine") - auc(E, "incertitude"))
    print(f"H101 complice : combiné − incertitude : [{lo:+.3f} ; {hi:+.3f}]")
    for w in ("facile", "echo", "menteur", "plausible"):
        L = [x for g in GRAINES for x in R[(w, g)]]
        lo, hi = boot(L, lambda E: auc(E, "combine") - auc(E, "incertitude"))
        print(f"H102 {w:<10} combiné − incertitude : [{lo:+.3f} ; {hi:+.3f}]  (marge −0,02)")
    print(f"H103 capture moyenne à 10 % : combiné {sum(C[w]['combine'] for w in MONDES) / 5:.0%} ; "
          f"incertitude {sum(C[w]['incertitude'] for w in MONDES) / 5:.0%}")
