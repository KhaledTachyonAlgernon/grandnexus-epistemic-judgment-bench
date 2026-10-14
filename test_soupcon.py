"""Test pré-enregistré H-Soupçon (H37-H41), graines neuves 21-23. Relancer jusqu'au BILAN."""
import json, os, sys, time
from evaluer import evaluer, apparier
from monde import generer
from temoins import Plafond
from filiation import Filiation
from soupcon import Soupcon

GRAINES, MONDES = (21, 22, 23), ("menteur", "facile", "hostile", "echo")
from cache import repertoire
CACHE = repertoire("soupcon")          # versionné : empreinte du code source
SYS = {"filiation v3": lambda m: Filiation(desattenuer=True), "soupçon": lambda m: Soupcon(),
       "plafond": lambda m: Plafond(m)}
fin = time.time() + float(sys.argv[1] if len(sys.argv) > 1 else 240)


def charge(w, g, nom):
    f = f"{CACHE}/{w}_{g}_{nom.replace(' ', '_').replace('ç', 'c')}.json"
    if os.path.exists(f):
        return json.load(open(f))
    if time.time() > fin:
        print(f"… à suivre ({w}, graine {g}, {nom})"); sys.exit(0)
    t0 = time.time()
    m = generer(w, g)
    o = SYS[nom](m)
    vec = [(j, [g] + list(fait)) for j, fait in evaluer(o, m)["_vecteur"]]
    b = {"secondes": round(time.time() - t0)}
    if m.menteur:                                        # exactitude sur faits ciblés (faits × époques)
        nomM, _, cibles = m.menteur
        ok = n = 0
        for cle in cibles:
            if cle in getattr(o, "obs", {cle: 1}) or isinstance(o, Plafond):
                for t in range(m.n_epoques):
                    ok += o.resoudre(cle[0], cle[1], t)[0] == m.verite[cle][t]; n += 1
        b["cibles"] = [ok, n]
    if hasattr(o, "f"):
        honn = [s for s in m.sources if not s.cibles]
        b["err_f_honnetes"] = sum(abs(o.f[s.nom] - s.f("habite")) for s in honn) / len(honn)
        b["f"] = {s.nom: [round(o.f[s.nom], 3), s.fiabilite] for s in m.sources}
    if isinstance(o, Soupcon):
        b["q"] = {k: round(v, 3) for k, v in o.q.items()}
        couples = [(cle, s, p) for cle, d in o.susp.items() for s, p in d.items()]
        b["candidats"] = len(couples)
        b["marques"] = sum(p > 0.5 for _, _, p in couples)
        if m.menteur:                                    # métrique sur les COUPLES (source, fait)
            nomM, _, cibles = m.menteur
            assert all(sum(p > 0.5 for p in d.values()) <= 1 for d in o.susp.values()), \
                "invariant rompu : plusieurs sources marquées sur un même fait"
            marques = {(s, cle) for cle, s, p in couples if p > 0.5}
            vrais = {(nomM, cle) for cle in cibles}
            candidats = {(nomM, cle) for cle in cibles if nomM in o.susp.get(cle, {})}
            tp = len(marques & vrais)
            b["precision"] = tp / max(1, len(marques))
            b["rappel"] = tp / max(1, len(vrais))
            b["rappel_candidats"] = tp / max(1, len(candidats))
    json.dump({"vec": vec, "boite": b}, open(f, "w"))
    return json.load(open(f))


R = {(w, g, n): charge(w, g, n) for w in MONDES for g in GRAINES for n in SYS}
print(f"BILAN — H-Soupçon, graines 21-23 — cache {CACHE}\n")
vec = lambda w, n: [(j, tuple(map(str, f))) for g in GRAINES for j, f in R[(w, g, n)]["vec"]]
for w in MONDES:
    print(f"── {w} : " + "  ".join(f"{n} {sum(j for j, _ in vec(w, n)) / len(vec(w, n)):.1%}" for n in SYS))
    for a, b_ in [("soupçon", "filiation v3"), ("plafond", "soupçon")]:
        d, h, _ = apparier(vec(w, a), vec(w, b_))
        print(f"     {a} − {b_} : {d:+.1%} ± {h:.1%}")
    for g in GRAINES:
        b = R[(w, g, "soupçon")]["boite"]
        extra = (f"  précision {b['precision']:.0%} rappel {b['rappel']:.0%} rappel/candidats {b['rappel_candidats']:.0%}"
                 if "precision" in b else "")
        print(f"     g{g} marqués {b['marques']}/{b['candidats']} candidats{extra}   err f honnêtes : "
              f"soupçon {b['err_f_honnetes']:.3f} / v3 {R[(w, g, 'filiation v3')]['boite']['err_f_honnetes']:.3f}"
              f"   ({b['secondes']} s)")
    if w == "menteur":
        for n in SYS:
            ok = sum(R[(w, g, n)]["boite"]["cibles"][0] for g in GRAINES)
            nn = sum(R[(w, g, n)]["boite"]["cibles"][1] for g in GRAINES)
            print(f"     faits ciblés — {n}: {ok / nn:.1%}")
        print("     propension apprise (g21) :", R[(w, 21, "soupçon")]["boite"]["q"])
        print("     fiabilités (g21) :", R[(w, 21, "soupçon")]["boite"]["f"])
