"""Test pré-enregistré H-Litige (H58-H62), graines neuves 36-38, cache versionné.
Un seul entraînement par (monde, graine) : on compare les réponses de la Méprise (croyances tranchées)
et de la Méprise + Litige (croyances après litige) — appariement parfait."""
import json, os, sys, time
from cache import repertoire
from evaluer import _bootstrap
from monde import generer
from litige import Litige

GRAINES = (36, 37, 38)
MONDES = ("complice", "facile", "hostile", "echo", "menteur", "plausible", "echo_menteur")
CACHE = repertoire("litige")
fin = time.time() + float(sys.argv[1] if len(sys.argv) > 1 else 230)


def questions(o, m, g, croyance):
    o.croyance = croyance
    out = []
    for q in m.questions:
        rep, conf = o.repondre(q)
        juste = (rep is None) if q.attendu is None else (rep == q.attendu)
        out.append([int(juste), (conf if rep is not None else 0.0) if q.attendu is not None else None,
                    "|".join(map(str, (g,) + tuple(q.grappe)))])
    return out


def charge(w, g):
    f = f"{CACHE}/{w}_{g}.json"
    if os.path.exists(f):
        return json.load(open(f))
    if time.time() > fin:
        print(f"… à suivre ({w}, graine {g})"); sys.exit(0)
    t0 = time.time()
    m = generer(w, g)
    o = Litige(); o.ingerer(m.enonces)
    apres = o.croyance
    res = {"meprise": questions(o, m, g, o.croyance_tranchee), "litige": questions(o, m, g, apres),
           "n_litiges": len(o.litiges), "s": 0}
    if m.menteur:
        cibles = m.menteur[2]
        res["n_litiges_cibles"] = sum(1 for c in o.litiges if c in cibles)
        res["n_cibles"] = len(cibles)
        for nom, cr in (("meprise", o.croyance_tranchee), ("litige", apres)):
            pts = []
            for cle in sorted(cibles):
                if cle not in cr:
                    continue
                for t in range(m.n_epoques):
                    post = cr[cle][t]
                    i = max(range(len(post)), key=post.__getitem__)
                    ok = o.dom[cle[1]][i] == m.verite[cle][t]
                    pts.append([int(ok), int(post[i] >= 0.8 and not ok), f"{g}|{cle[0]}|{cle[1]}"])
            res["cibles_" + nom] = pts
    res["s"] = round(time.time() - t0)
    json.dump(res, open(f, "w"))
    return res


R = {(w, g): charge(w, g) for w in MONDES for g in GRAINES}
print(f"BILAN — H-Litige, graines 36-38 — cache {CACHE}\n")


def diff(vals_a, vals_b, gr):
    m_, h, k = _bootstrap([a - b for a, b in zip(vals_a, vals_b)], gr, tirages=1000)
    return f"{m_:+.2%} ± {h:.2%} [{m_ - h:+.2%} ; {m_ + h:+.2%}]"


for w in MONDES:
    L = [x for g in GRAINES for x in R[(w, g)]["litige"]]
    M = [x for g in GRAINES for x in R[(w, g)]["meprise"]]
    gr = [x[2] for x in L]
    ib = [i for i, x in enumerate(L) if x[1] is not None]
    bL = [(L[i][1] - L[i][0]) ** 2 for i in ib]
    bM = [(M[i][1] - M[i][0]) ** 2 for i in ib]
    nl = [R[(w, g)]["n_litiges"] for g in GRAINES]
    print(f"── {w} : litiges par graine {nl}"
          + (f" (dont ciblés {[R[(w, g)]['n_litiges_cibles'] for g in GRAINES]} / {[R[(w, g)]['n_cibles'] for g in GRAINES]})" if "n_cibles" in R[(w, GRAINES[0])] else ""))
    print(f"     exactitude  méprise {sum(x[0] for x in M)/len(M):.2%}  litige {sum(x[0] for x in L)/len(L):.2%}   Δ {diff([x[0] for x in L], [x[0] for x in M], gr)}")
    print(f"     Brier       méprise {sum(bM)/len(bM):.4f}  litige {sum(bL)/len(bL):.4f}   Δ {diff(bL, bM, [gr[i] for i in ib]).replace('%','')} (×100)")
    if "cibles_litige" in R[(w, GRAINES[0])]:
        CL = [x for g in GRAINES for x in R[(w, g)]["cibles_litige"]]
        CM = [x for g in GRAINES for x in R[(w, g)]["cibles_meprise"]]
        grc = [x[2] for x in CL]
        print(f"     faits ciblés — exactitude {sum(x[0] for x in CM)/len(CM):.1%} → {sum(x[0] for x in CL)/len(CL):.1%}"
              f"  Δ {diff([x[0] for x in CL], [x[0] for x in CM], grc)}")
        print(f"     faits ciblés — sûr-et-faux {sum(x[1] for x in CM)/len(CM):.1%} → {sum(x[1] for x in CL)/len(CL):.1%}"
              f"  Δ {diff([x[1] for x in CL], [x[1] for x in CM], grc)}")
