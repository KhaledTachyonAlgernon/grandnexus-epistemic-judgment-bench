"""Tests de robustesse (phase 2) : un monde qui casse UNE hypothèse des organes.
Usage : python test_robustesse.py <monde> <graines, ex. 9,10,11> [budget_s]. Relancer jusqu'au BILAN."""
import json, os, sys, time
from evaluer import evaluer, apparier
from monde import generer
from temoins import Majorite, Plafond
from pesee import Pesee
from filiation import Filiation

MONDE, GRAINES = sys.argv[1], tuple(int(x) for x in sys.argv[2].split(","))
CACHE = f"/tmp/cache_rob_{MONDE}"
os.makedirs(CACHE, exist_ok=True)
SYS = {"majorité": lambda m: Majorite(), "pesée D": lambda m: Pesee(True, True, un_contre_tous=True),
       "pesée E": lambda m: Pesee(True, True, un_contre_tous=True, desattenuer=True),
       "filiation v3": lambda m: Filiation(desattenuer=True), "plafond": lambda m: Plafond(m)}
fin = time.time() + float(sys.argv[3] if len(sys.argv) > 3 else 240)


def charge(g, nom):
    f = f"{CACHE}/{g}_{nom.replace(' ', '_')}.json"
    if os.path.exists(f):
        return json.load(open(f))
    if time.time() > fin:
        print(f"… à suivre (graine {g}, {nom})"); sys.exit(0)
    m = generer(MONDE, g)
    o = SYS[nom](m)
    vec = [(j, [g] + list(fait)) for j, fait in evaluer(o, m)["_vecteur"]]
    boite = {}
    if hasattr(o, "f"):
        boite = {"err_f": sum(abs(o.f[s.nom] - s.fiabilite) for s in m.sources) / len(m.sources),
                 "f": {s.nom: [round(o.f[s.nom], 3), s.fiabilite] for s in m.sources},
                 "parent": {k: [p, round(c, 2)] for k, (p, c) in getattr(o, "parent", {}).items()}}
    json.dump({"vec": vec, "boite": boite}, open(f, "w"))
    return json.load(open(f))


R = {(g, n): charge(g, n) for g in GRAINES for n in SYS}
vec = lambda n: [(j, tuple(map(str, f))) for g in GRAINES for j, f in R[(g, n)]["vec"]]
print(f"BILAN — monde « {MONDE} », graines {GRAINES}\n")
print("Global :", "  ".join(f"{n} {sum(j for j, _ in vec(n)) / len(vec(n)):.1%}" for n in SYS))
print("\nDifférences appariées (IC 95 % en grappes) :")
for a, b in [("plafond", "filiation v3"), ("filiation v3", "pesée E"), ("pesée E", "pesée D"), ("filiation v3", "majorité")]:
    d, h, k = apparier(vec(a), vec(b))
    print(f"   {a:>13} − {b:<13} {d:+.1%} ± {h:.1%}")
print("\nBoîte de verre :")
for g in GRAINES:
    for n in ("pesée E", "filiation v3"):
        b = R[(g, n)]["boite"]
        print(f"   g{g} {n:<13} erreur f {b['err_f']:.3f}   parents : {b['parent'] or 'aucun'}")
    print(f"        f appris/vrai (v3) : " + ", ".join(f"{k} {v[0]:.2f}/{v[1]:.2f}" for k, v in R[(g, 'filiation v3')]['boite']['f'].items()))
