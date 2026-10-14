"""Test pré-enregistré H-Ancres-confirmation (H78-H80), graines neuves 56-60, cache versionné."""
import json, os, random, sys, time
from cache import repertoire
from evaluer import _bootstrap
from monde import generer, Enonce
from meprise import Meprise

GRAINES, NIVEAUX, ANCRE = (56, 57, 58, 59, 60), (0.0, 0.50), "L'Ancre"
CACHE = repertoire("ancres_confirmation")
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
print(f"BILAN — H-Ancres-confirmation, graines 56-60 — cache {CACHE}\n")


def apparie(cat_fn):
    A = [x for g in GRAINES for x in R[(g, 0.5)]["pts"] if cat_fn(g, x)]
    Bl = [x for g in GRAINES for x in R[(g, 0.0)]["pts"] if cat_fn(g, x)]
    assert [x[1] for x in A] == [x[1] for x in Bl]
    m_, h, k = _bootstrap([a[2] - b[2] for a, b in zip(A, Bl)], [a[1] for a in A], tirages=4000)
    return m_, h, k


anc = [x for g in GRAINES for x in R[(g, 0.5)]["pts"] if x[0] == "ancré"]
print(f"H80 faits ancrés : {sum(x[2] for x in anc) / len(anc):.1%}  (ancre soupçonnée : "
      f"{[R[(g, 0.5)]['suspects_ancre'] for g in GRAINES]})")
d, h, k = apparie(lambda g, x: x[0] in ("ciblé", "ancré") and x[1] not in R[(g, 0.5)]["ancres"])
print(f"H78 ciblés non ancrés : {d:+.1%} ± {h:.1%}  (borne basse {d - h:+.1%} ; {k} faits)")
d2, h2, k2 = apparie(lambda g, x: x[0] == "non ciblé")
print(f"H79 non ciblés : {d2:+.2%} ± {h2:.2%}  (borne basse {d2 - h2:+.2%} ; marge −0,50 % ; {k2} faits)")
