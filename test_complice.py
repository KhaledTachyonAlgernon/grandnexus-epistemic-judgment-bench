"""Test pré-enregistré H-Complices (H53-H57), graines neuves 33-35, cache versionné."""
import json, os, sys, time
from cache import repertoire
from evaluer import evaluer, apparier, _bootstrap
from monde import generer
from temoins import Majorite, Plafond
from meprise import Meprise

GRAINES, MONDE = (33, 34, 35), "complice"
CACHE = repertoire("complice")
SYS = {"majorité": lambda m: Majorite(), "référence": lambda m: Meprise(), "plafond": lambda m: Plafond(m)}
fin = time.time() + float(sys.argv[1] if len(sys.argv) > 1 else 240)


def charge(g, nom):
    f = f"{CACHE}/{g}_{nom.replace('é', 'e')}.json"
    if os.path.exists(f):
        return json.load(open(f))
    if time.time() > fin:
        print(f"… à suivre (graine {g}, {nom})"); sys.exit(0)
    t0 = time.time()
    m = generer(MONDE, g)
    nomM, _, cibles = m.menteur
    o = SYS[nom](m)
    vec = [(j, [g] + list(fait)) for j, fait in evaluer(o, m)["_vecteur"]]
    b = {"s": 0, "cibles": []}                         # [(fait, juste)] sur faits ciblés × époques
    for cle in sorted(cibles):
        for t in range(m.n_epoques):
            b["cibles"].append([f"{g}|{cle[0]}|{cle[1]}", int(o.resoudre(cle[0], cle[1], t)[0] == m.verite[cle][t])])
    if isinstance(o, Meprise):
        b["parents"] = {k: [p, round(c, 2)] for k, (p, c) in o.parent.items()}
        b["q"] = {k: round(v, 3) for k, v in o.q.items()}
        b["f"] = {s.nom: [round(o.f[s.nom], 3), s.fiabilite] for s in m.sources}
        assert all(sum(p > 0.5 for p in d.values()) <= 1 for d in o.susp.values())
        marques = {(s, cle) for cle, d in o.susp.items() for s, p in d.items() if p > 0.5}
        vrais = {(nomM, cle) for cle in cibles}
        tp = len(marques & vrais)
        b["precision"], b["rappel"] = tp / max(1, len(marques)), tp / max(1, len(vrais))
        b["marques_autres"] = sorted({s for s, _ in marques if s != nomM})
    b["s"] = round(time.time() - t0)
    json.dump({"vec": vec, "boite": b}, open(f, "w"))
    return json.load(open(f))


R = {(g, n): charge(g, n) for g in GRAINES for n in SYS}
vec = lambda n: [(j, tuple(map(str, f))) for g in GRAINES for j, f in R[(g, n)]["vec"]]
print(f"BILAN — H-Complices, graines 33-35 — cache {CACHE}\n")
print("Global : " + "  ".join(f"{n} {sum(j for j, _ in vec(n)) / len(vec(n)):.1%}" for n in SYS))
for a, b_ in [("plafond", "référence"), ("référence", "majorité")]:
    d, h, _ = apparier(vec(a), vec(b_))
    print(f"   {a} − {b_} : {d:+.1%} ± {h:.1%}  (borne basse {d - h:+.1%})")
cib = lambda n: [(j, f) for g in GRAINES for f, j in R[(g, n)]["boite"]["cibles"]]
for n in SYS:
    print(f"Faits ciblés × époques — {n} : {sum(j for j, _ in cib(n)) / len(cib(n)):.1%}")
P, Rf = cib("plafond"), cib("référence")
m_, h_, k_ = _bootstrap([a - b for (a, _), (b, _) in zip(P, Rf)], [f for _, f in P])
print(f"   plafond − référence sur faits ciblés : {m_:+.1%} ± {h_:.1%}  (borne basse {m_ - h_:+.1%}, {k_} faits)")
for g in GRAINES:
    b = R[(g, "référence")]["boite"]
    print(f"g{g} : parents {b['parents'] or 'aucun'}  | Notable précision {b['precision']:.0%} rappel {b['rappel']:.0%}"
          f"  | autres marqués {b['marques_autres'] or 'aucun'}  ({b['s']} s)")
    print(f"      propension {b['q']}")
    print(f"      fiabilités {b['f']}")
