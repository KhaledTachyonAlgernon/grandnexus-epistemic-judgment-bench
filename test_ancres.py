"""Test pré-enregistré H-Ancres (H68-H72), graines neuves 50-52, cache versionné."""
import json, os, random, sys, time
from cache import repertoire
from evaluer import _bootstrap
from monde import generer, Enonce
from meprise import Meprise

GRAINES, NIVEAUX, ANCRE = (50, 51, 52), (0.0, 0.10, 0.25, 0.50), "L'Ancre"
CACHE = repertoire("ancres")
fin = time.time() + float(sys.argv[1] if len(sys.argv) > 1 else 200)


def charge(g, part):
    f = f"{CACHE}/{g}_{int(part * 100)}.json"
    if os.path.exists(f):
        return json.load(open(f))
    if time.time() > fin:
        print(f"… à suivre (graine {g}, {int(part * 100)} %)"); sys.exit(0)
    m = generer("complice", g)
    nom, _, cibles = m.menteur
    ordre = sorted(cibles)
    random.Random(f"ancres|{g}").shuffle(ordre)              # ordre tiré une fois : niveaux emboîtés
    ancres = set(ordre[:round(part * len(ordre))])
    corpus = list(m.enonces)
    for cle in sorted(ancres):
        for t in range(m.n_epoques):
            corpus.append(Enonce(len(corpus), t, ANCRE, cle[0], cle[1], m.verite[cle][t], ""))
    o = Meprise(fixes={ANCRE: 0.99})
    o.ingerer(corpus)
    pts = []
    for cle, serie in m.verite.items():
        if cle not in o.croyance:
            continue
        cat = ("ancré" if cle in ancres else "ciblé") if cle in cibles else "non ciblé"
        for t in range(m.n_epoques):
            pts.append([cat, f"{g}|{cle[0]}|{cle[1]}", int(o.resoudre(cle[0], cle[1], t)[0] == serie[t])])
    res = {"pts": pts, "f": {s.nom: o.f[s.nom] for s in m.sources}, "vrai": {s.nom: s.fiabilite for s in m.sources},
           "coalition": list(m.coalition), "n_cibles": len(ordre), "n_ancres": len(ancres),
           "ancres": sorted(f"{g}|{c[0]}|{c[1]}" for c in ancres),
           "suspects_ancre": sum(1 for d in o.susp.values() if d.get(ANCRE, 0) > 0.5)}
    json.dump(res, open(f, "w"))
    return res


R = {(g, p): charge(g, p) for g in GRAINES for p in NIVEAUX}
print(f"BILAN — H-Ancres, graines 50-52 — cache {CACHE}\n")
print(f"{'ancrage':<9}{'ancres':>8}{'faits ancrés':>15}{'ciblés non ancrés':>20}{'non ciblés':>13}   fiabilité coalition / honnêtes")
for p in NIVEAUX:
    pts = [x for g in GRAINES for x in R[(g, p)]["pts"]]
    acc = lambda c: (lambda L: f"{sum(x[2] for x in L) / len(L):.1%}" if L else "—")([x for x in pts if x[0] == c])
    coal = sum(R[(g, p)]["f"][s] for g in GRAINES for s in R[(g, p)]["coalition"]) / (3 * len(GRAINES))
    hon = sum(R[(g, p)]["f"][s] for g in GRAINES for s in ("Le Registre", "La Gazette")) / (2 * len(GRAINES))
    print(f"{int(p * 100):>5} %  {sum(R[(g, p)]['n_ancres'] for g in GRAINES):>6}  {acc('ancré'):>13}  {acc('ciblé'):>18}  {acc('non ciblé'):>11}   {coal:.3f} / {hon:.3f}")


def apparie(cat_fn, p_a, p_b):
    A = [x for g in GRAINES for x in R[(g, p_a)]["pts"] if cat_fn(g, x)]
    Bv = {(x[1], i): x[2] for g in GRAINES for i, x in enumerate(R[(g, p_b)]["pts"])}
    Bl = [x for g in GRAINES for x in R[(g, p_b)]["pts"] if cat_fn(g, x)]
    assert [x[1] for x in A] == [x[1] for x in Bl]
    m_, h, k = _bootstrap([a[2] - b[2] for a, b in zip(A, Bl)], [a[1] for a in A], tirages=2000)
    return m_, h, k


non_ancre_50 = lambda g, x: x[0] == "ciblé" and x[1] not in R[(g, 0.5)]["ancres"] or \
    (x[0] == "ciblé" and False)
cibles_restants = lambda g, x: x[0] in ("ciblé", "ancré") and x[1] not in R[(g, 0.5)]["ancres"]
d, h, k = apparie(cibles_restants, 0.5, 0.0)
print(f"\nH69 faits ciblés NON ancrés à 50 % : exactitude(50 %) − exactitude(0 %) = {d:+.1%} ± {h:.1%}  ({k} faits)")
d2, h2, k2 = apparie(lambda g, x: x[0] == "non ciblé", 0.5, 0.0)
print(f"H72 faits non ciblés : exactitude(50 %) − exactitude(0 %) = {d2:+.2%} ± {h2:.2%}  ({k2} faits)")
for g in GRAINES:
    c0 = sum(R[(g, 0.0)]["f"][s] for s in R[(g, 0.0)]["coalition"]) / 3
    c5 = sum(R[(g, 0.5)]["f"][s] for s in R[(g, 0.5)]["coalition"]) / 3
    e = lambda p: sum(abs(R[(g, p)]["f"][s] - R[(g, p)]["vrai"][s]) for s in ("Le Registre", "La Gazette")) / 2
    print(f"g{g} : coalition {c0:.3f} → {c5:.3f}   erreur honnêtes {e(0.0):.3f} → {e(0.5):.3f}   "
          f"ancre soupçonnée : {[R[(g, p)]['suspects_ancre'] for p in NIVEAUX]}")
