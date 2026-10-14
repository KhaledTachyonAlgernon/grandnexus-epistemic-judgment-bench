"""Test pré-enregistré H-Désatténuation (H17-H20), graines neuves 6-8. Relancer jusqu'à « BILAN »."""
import json, os, sys, time
from evaluer import evaluer, apparier
from monde import generer
from temoins import Majorite, Plafond
from pesee import Pesee
from filiation import Filiation

CACHE, GRAINES, MONDES = "/tmp/cache_desatt", (6, 7, 8), ("facile", "realiste", "hostile", "echo")
os.makedirs(CACHE, exist_ok=True)
SYS = {"majorité": lambda m: Majorite(), "pesée D": lambda m: Pesee(True, True, un_contre_tous=True),
       "pesée E": lambda m: Pesee(True, True, un_contre_tous=True, desattenuer=True),
       "filiation v2": lambda m: Filiation(), "filiation v3": lambda m: Filiation(desattenuer=True),
       "plafond": lambda m: Plafond(m)}
fin = time.time() + float(sys.argv[1] if len(sys.argv) > 1 else 240)


def charge(w, g, nom):
    f = f"{CACHE}/{w}_{g}_{nom.replace(' ', '_')}.json"
    if os.path.exists(f):
        return json.load(open(f))
    if time.time() > fin:
        print(f"… à suivre ({w}, graine {g}, {nom})"); sys.exit(0)
    m = generer(w, g)
    o = SYS[nom](m)
    vec = [(j, [g] + list(fait)) for j, fait in evaluer(o, m)["_vecteur"]]
    boite = {}
    if hasattr(o, "f"):
        boite["err_f"] = sum(abs(o.f[s.nom] - s.fiabilite) for s in m.sources) / len(m.sources)
        boite["parent"] = getattr(o, "parent", {})
    json.dump({"vec": vec, "boite": boite}, open(f, "w"))
    return json.load(open(f))


R = {(w, g, n): charge(w, g, n) for w in MONDES for g in GRAINES for n in SYS}
print("BILAN — graines neuves 6, 7, 8\n")
print("H17 erreur moyenne |f appris − f vrai|")
for w in MONDES:
    print(f"   {w:<9}" + "".join(f"{n}: {sum(R[(w, g, n)]['boite']['err_f'] for g in GRAINES) / 3:.3f}   "
                             for n in ("pesée D", "pesée E", "filiation v2", "filiation v3")))
print("\nH18/H19 filiations détectées (filiation v3 | v2)")
for w in MONDES:
    for g in GRAINES:
        print(f"   {w:<9} g{g}  v3 : {R[(w, g, 'filiation v3')]['boite']['parent'] or 'aucune'}")
        print(f"   {'':<9}     v2 : {R[(w, g, 'filiation v2')]['boite']['parent'] or 'aucune'}")
vec = lambda w, n: [(j, tuple(map(str, f))) for g in GRAINES for j, f in R[(w, g, n)]["vec"]]
print("\nH20 global, différences appariées (IC 95 % en grappes)")
for w in MONDES:
    lig = f"   {w:<9}"
    for a, b in [("filiation v3", "pesée D"), ("filiation v3", "filiation v2"), ("pesée E", "pesée D"), ("plafond", "filiation v3")]:
        d, h, _ = apparier(vec(w, a), vec(w, b))
        lig += f"{a[:5]}{a[-2:]}−{b[:5]}{b[-2:]} {d:+.1%}±{h:.1%}   "
    print(lig)
print("\nAbsolu (global) :")
for w in MONDES:
    print(f"   {w:<9}" + "".join(f"{n}: {sum(j for j, _ in vec(w, n)) / len(vec(w, n)):.1%}  " for n in SYS))
