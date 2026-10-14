"""H-Collatéral (H81-H84) : d'où vient la perte hors cibles des ancres ? Greffe de paramètres, cache versionné."""
import json, os, sys, time
from cache import repertoire
from monde import generer
from meprise import Meprise
from mecanisme_ancres import corpus, greffe, ANCRE

GRAINES = (56, 57, 58, 59, 60)
CACHE = repertoire("collateral")
fin = time.time() + float(sys.argv[1] if len(sys.argv) > 1 else 160)
GREFFES = (("f",), ("parent",), ("q",), ("f", "parent"), ("tout",))


def justes(o, m, faits):
    return {(f, t): int(o.resoudre(f[0], f[1], t)[0] == m.verite[f][t]) for f in faits for t in range(m.n_epoques)}


def charge(g):
    fic = f"{CACHE}/{g}.json"
    if os.path.exists(fic):
        return json.load(open(fic))
    if time.time() > fin:
        print(f"… à suivre (graine {g})"); sys.exit(0)
    m = generer("complice", g)
    nom = m.menteur[0]
    c0, _, cibles = corpus(m, g, 0.0)
    c5, _, _ = corpus(m, g, 0.5)
    o0 = Meprise(fixes={ANCRE: 0.99}); o0.ingerer(c0)
    o5 = Meprise(fixes={ANCRE: 0.99}); o5.ingerer(c5)
    hors = sorted(k for k in m.verite if k not in cibles and k in o0.croyance)
    J0, J5 = justes(o0, m, hors), justes(o5, m, hors)
    res = {"n": len(J0), "base": sum(J0.values()), "ancre": sum(J5.values())}
    for q in GREFFES:
        res["+".join(q)] = sum(justes(greffe(o0, o5, q), m, hors).values())
    bascules = [k for k in J0 if J0[k] == 1 and J5[k] == 0]
    complices = [s for s in m.coalition if s != nom]
    escomptes = 0
    for (f, t) in bascules:                                   # un complice dit-il ce que le Notable venait de dire ?
        escomptes += any(src in complices and o5._dernier(nom, f, ep) == ob
                         for ep, src, ob in o5.obs[f])
    res["bascules"], res["bascules_avec_copie_escomptee"] = len(bascules), escomptes
    res["parents5"] = {k: [p, round(c, 2)] for k, (p, c) in o5.parent.items()}
    json.dump(res, open(fic, "w"))
    return res


R = {g: charge(g) for g in GRAINES}
n = sum(R[g]["n"] for g in GRAINES)
acc = lambda k: sum(R[g][k] for g in GRAINES) / n
perte = acc("ancre") - acc("base")
print(f"BILAN — H-Collatéral, graines 56-60 — cache {CACHE}\n")
print(f"Faits non ciblés × époques : {n} ; sans ancre {acc('base'):.3%} ; avec ancres {acc('ancre'):.3%} ; perte {perte:+.3%}")
for q in GREFFES:
    k = "+".join(q)
    print(f"   greffe {k:<10} {acc(k):.3%}   écart à la base {acc(k) - acc('base'):+.3%}   part de la perte {(acc(k) - acc('base')) / perte:+.0%}")
b = sum(R[g]["bascules"] for g in GRAINES)
e = sum(R[g]["bascules_avec_copie_escomptee"] for g in GRAINES)
print(f"\nBascules juste → faux : {b} ; dont avec un énoncé de complice escompté comme copie : {e} ({e / max(1, b):.0%})")
for g in GRAINES:
    print(f"   g{g} filiations avec ancres : {R[g]['parents5'] or 'aucune'}")
