"""Test pré-enregistré H-Méprise (H42-H45), graines neuves 24-26. Relancer jusqu'au BILAN."""
import json, os, sys, time
from evaluer import evaluer, apparier
from monde import generer
from temoins import Plafond
from soupcon import Soupcon
from meprise import Meprise

GRAINES, MONDES = (24, 25, 26), ("plausible", "facile", "hostile", "echo", "menteur")
CACHE = "/tmp/cache_meprise"
os.makedirs(CACHE, exist_ok=True)
SYS = {"soupcon": lambda m: Soupcon(), "meprise": lambda m: Meprise(), "plafond": lambda m: Plafond(m)}
fin = time.time() + float(sys.argv[1] if len(sys.argv) > 1 else 240)


def charge(w, g, nom):
    f = f"{CACHE}/{w}_{g}_{nom}.json"
    if os.path.exists(f):
        return json.load(open(f))
    if time.time() > fin:
        print(f"… à suivre ({w}, graine {g}, {nom})"); sys.exit(0)
    t0 = time.time()
    m = generer(w, g)
    o = SYS[nom](m)
    vec = [(j, [g] + list(fait)) for j, fait in evaluer(o, m)["_vecteur"]]
    b = {"s": round(time.time() - t0)}
    if isinstance(o, Meprise):
        b["lambda"] = {k: round(v, 2) for k, v in o.lam.items()}
    json.dump({"vec": vec, "boite": b}, open(f, "w"))
    return json.load(open(f))


R = {(w, g, n): charge(w, g, n) for w in MONDES for g in GRAINES for n in SYS}
vec = lambda w, n: [(j, tuple(map(str, f))) for g in GRAINES for j, f in R[(w, g, n)]["vec"]]
print("BILAN — H-Méprise, graines neuves 24-26\n")
for w in MONDES:
    print(f"── {w} : " + "  ".join(f"{n} {sum(j for j, _ in vec(w, n)) / len(vec(w, n)):.1%}" for n in SYS))
    for a, b_ in [("meprise", "soupcon"), ("plafond", "meprise")]:
        d, h, _ = apparier(vec(w, a), vec(w, b_))
        print(f"     {a} − {b_} : {d:+.2%} ± {h:.2%}   (borne haute {d + h:+.2%})")
    for g in GRAINES:
        print(f"     g{g} λ : {R[(w, g, 'meprise')]['boite']['lambda']}   ({R[(w, g, 'meprise')]['boite']['s']} s)")
