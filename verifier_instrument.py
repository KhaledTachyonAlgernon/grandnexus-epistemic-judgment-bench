"""Critère I1 : le plafond domine-t-il tout le monde, à un intervalle EN GRAPPES près ?
Les évaluations sont mises en cache (une machine à un cœur : on avance par tranches)."""
import json, os, sys, time
from evaluer import evaluer, apparier
from monde import generer
from temoins import DernierGagne, Majorite, MotsCles, Plafond
from pesee import Pesee
from filiation import Filiation

CACHE = "/tmp/cache_banc"
os.makedirs(CACHE, exist_ok=True)
SYS = {"dernier gagne": lambda m: DernierGagne(), "majorité": lambda m: Majorite(),
       "mots-clés": lambda m: MotsCles(), "pesée D": lambda m: Pesee(True, True, un_contre_tous=True),
       "filiation v2": lambda m: Filiation(), "plafond": lambda m: Plafond(m)}


def vecteur(monde, g, nom, budget_fin):
    f = f"{CACHE}/{monde}_{g}_{nom.replace(' ', '_')}.json"
    if os.path.exists(f):
        return json.load(open(f))
    if time.time() > budget_fin:
        return None
    m = generer(monde, g)
    v = [(j, [g] + list(fait)) for j, fait in evaluer(SYS[nom](m), m)["_vecteur"]]
    json.dump(v, open(f, "w"))
    return v


if __name__ == "__main__":
    monde, graines = sys.argv[1], [int(x) for x in sys.argv[2].split(",")]
    fin = time.time() + float(sys.argv[3]) if len(sys.argv) > 3 else 1e18
    vec, types = {}, []
    for g in graines:
        for nom in SYS:
            v = vecteur(monde, g, nom, fin)
            if v is None:
                print(f"… pas fini ({monde}, graine {g}, {nom}) — relancer")
                sys.exit(0)
            vec.setdefault(nom, []).extend((j, tuple(map(str, f))) for j, f in v)
        types += [q.type for q in generer(monde, g).questions]
    ds = [i for i, t in enumerate(types) if t == "deux_sauts"]
    print(f"\n══ « {monde} », graines {graines} — plafond moins système (apparié, IC 95 % en grappes)")
    print(f"{'système':<15}{'global':>18}{'deux sauts':>20}   I1")
    n_f = len({f for _, f in vec["plafond"]})
    n_ds = len({vec["plafond"][i][1] for i in ds})
    print(f"{'faits distincts':<15}{n_f:>18}{n_ds:>20}")
    for nom in SYS:
        if nom == "plafond":
            continue
        g_m, g_h, _ = apparier(vec["plafond"], vec[nom])
        d_m, d_h, _ = apparier([vec["plafond"][i] for i in ds], [vec[nom][i] for i in ds])
        ok = g_m + g_h >= 0 and d_m + d_h >= 0
        print(f"{nom:<15}{g_m:>+10.1%} ±{g_h:.1%}{d_m:>+12.1%} ±{d_h:.1%}   {'✓' if ok else '✗'}")
