"""H-Fragilité (H95-H99) : quels signaux internes repèrent les erreurs ? Graines neuves 67-69, cache versionné."""
import json, os, random, sys, time
from cache import repertoire
from monde import generer
from meprise import Meprise
from test_fidelite import reponse, contributions
from test_selection import score_signaux

MONDES, GRAINES, N_REP, RS = ("facile", "echo", "menteur", "plausible", "complice"), (67, 68, 69), 300, (1, 2, 3, 5, 8)
CACHE = repertoire("fragilite")
fin = time.time() + float(sys.argv[1] if len(sys.argv) > 1 else 170)


def charge(w, g):
    fic = f"{CACHE}/{w}_{g}.json"
    if os.path.exists(fic):
        return json.load(open(fic))
    if time.time() > fin:
        print(f"… à suivre ({w}, graine {g})"); sys.exit(0)
    m = generer(w, g)
    o = Meprise(); o.ingerer(m.enonces)
    contest = score_signaux(o, m)
    rng = random.Random(f"fragilite|{w}|{g}")
    paires = rng.sample([(f, t) for f in sorted(o.croyance) for t in range(m.n_epoques)], N_REP)
    out = []
    for cle, t in paires:
        post = o.croyance[cle][t]
        ordre = sorted(range(len(post)), key=lambda i: -post[i])
        a, b = ordre[0], ordre[1]
        tous = list(o.obs[cle])
        pos = sorted([x for x in contributions(o, cle, t, a, b) if x[0] > 0], key=lambda x: -x[0])
        R = 9
        for k in RS:
            if k > len(pos):
                break
            retire = {i for _, i in pos[:k]}
            if reponse(o, cle, t, [s for i, s in enumerate(tous) if i not in retire]) != a:
                R = k
                break
        out.append({"fait": f"{g}|{cle[0]}|{cle[1]}", "faux": int(o.dom[cle[1]][a] != m.verite[cle][t]),
                    "incertitude": 1 - post[a], "fragilite": -R, "contestation": contest[cle][0]})
    json.dump(out, open(fic, "w"))
    return out


def auc(L, cle):
    P = [x[cle] for x in L if x["faux"]]
    N = [x[cle] for x in L if not x["faux"]]
    if not P or not N:
        return float("nan")
    s = 0.0
    for p in P:
        for n in N:
            s += 1.0 if p > n else 0.5 if p == n else 0.0
    return s / (len(P) * len(N))


def boot_diff(L, c1, c2, tirages=600, graine=7):
    faits = sorted({x["fait"] for x in L})
    par = {}
    for x in L:
        par.setdefault(x["fait"], []).append(x)
    rng = random.Random(graine)
    d = []
    for _ in range(tirages):
        E = [x for f in (rng.choice(faits) for _ in faits) for x in par[f]]
        d.append((auc(E, c1) if c1 != "0.5" else 0.5) - (auc(E, c2) if c2 != "0.5" else 0.5))
    d = sorted(v for v in d if v == v)
    return d[int(0.025 * len(d))], d[int(0.975 * len(d)) - 1]


def capture(L, cle, part=0.10, graine=3):
    rng = random.Random(graine)
    ordre = sorted(L, key=lambda x: (-x[cle], rng.random()))
    pris = ordre[:round(part * len(L))]
    return sum(x["faux"] for x in pris) / max(1, sum(x["faux"] for x in L))


if __name__ == "__main__":
    R = {(w, g): charge(w, g) for w in MONDES for g in GRAINES}
    print(f"BILAN — H-Fragilité, graines 67-69 — cache {CACHE}\n")
    print(f"{'monde':<10}{'erreurs':>9}{'AUC incert.':>13}{'AUC fragil.':>13}{'AUC contest.':>14}   capture à 10 % (incert. / fragil. / contest.)")
    for w in MONDES:
        L = [x for g in GRAINES for x in R[(w, g)]]
        e = sum(x["faux"] for x in L)
        print(f"{w:<10}{e:>5}/{len(L):<4}{auc(L, 'incertitude'):>11.2f}{auc(L, 'fragilite'):>13.2f}{auc(L, 'contestation'):>14.2f}"
              f"   {capture(L, 'incertitude'):.0%} / {capture(L, 'fragilite'):.0%} / {capture(L, 'contestation'):.0%}")
    print()
    for w in ("facile", "echo", "menteur", "plausible"):
        L = [x for g in GRAINES for x in R[(w, g)]]
        lo, hi = boot_diff(L, "fragilite", "0.5")
        lo2, hi2 = boot_diff(L, "fragilite", "incertitude")
        print(f"H95/H98 {w:<10} AUC(fragilité) − 0,5 : [{lo:+.2f} ; {hi:+.2f}]   fragilité − incertitude : [{lo2:+.2f} ; {hi2:+.2f}]")
    L = [x for g in GRAINES for x in R[("complice", g)]]
    for c in ("fragilite", "incertitude"):
        lo, hi = boot_diff(L, "contestation", c)
        print(f"H96/H97 complice : contestation − {c} : [{lo:+.2f} ; {hi:+.2f}]")
