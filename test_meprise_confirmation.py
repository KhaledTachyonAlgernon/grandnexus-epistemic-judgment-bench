"""Test pré-enregistré H-Méprise-confirmation (H46-H47), graines neuves 27-29. Relancer jusqu au BILAN."""
import json, os, sys, time
from evaluer import evaluer, apparier
from monde import generer
from temoins import Plafond
from soupcon import Soupcon
from meprise import Meprise

GRAINES, MONDES = (27, 28, 29), ("plausible", "facile", "hostile", "echo", "menteur")
CACHE = "/tmp/cache_meprise_conf"
os.makedirs(CACHE, exist_ok=True)
SYS = {"soupcon": lambda m: Soupcon(), "meprise": lambda m: Meprise()}
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
print("BILAN — H-Méprise-confirmation, graines neuves 27-29\n")
for w in MONDES:
    print(f"── {w} : " + "  ".join(f"{n} {sum(j for j, _ in vec(w, n)) / len(vec(w, n)):.1%}" for n in SYS))
    for a, b_ in [("meprise", "soupcon")]:
        d, h, _ = apparier(vec(w, a), vec(w, b_))
        print(f"     {a} − {b_} : {d:+.2%} ± {h:.2%}   (borne basse {d - h:+.2%}, borne haute {d + h:+.2%})")
    for g in GRAINES:
        print(f"     g{g} λ : {R[(w, g, 'meprise')]['boite']['lambda']}   ({R[(w, g, 'meprise')]['boite']['s']} s)")
