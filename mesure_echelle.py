"""Mesure pré-enregistrée H-Échelle (H63-H67), graines neuves 45-49, cache versionné."""
import json, os, random, sys, time
from cache import repertoire
from echelle import generer_monde, verifier_verite, tirer_cibles, menteur_coherent, expose_naif, B

GRAINES = (45, 46, 47, 48, 49)
CACHE = repertoire("echelle")
fin = time.time() + float(sys.argv[1] if len(sys.argv) > 1 else 230)


def charge(g):
    f = f"{CACHE}/{g}.json"
    if os.path.exists(f):
        return json.load(open(f))
    if time.time() > fin:
        print(f"… à suivre (graine {g})"); sys.exit(0)
    m = generer_monde(g)
    verifier_verite(m)
    res = []
    for c in tirer_cibles(m, g):
        lig = {"cible": f"{g}|{c[0]}|{c[1]}", "K": [], "intenables": [], "E": []}
        for d in range(4):
            tot, ep, v = menteur_coherent(m, c, d)
            lig["K"].append(tot)
            lig["intenables"].append(sum(x > B for x in ep))
            lig["E"].append(sum(expose_naif(m, c, d, g)))
        assert all(lig["K"][i] <= lig["K"][i + 1] for i in range(3)), ("théorème violé", c, lig["K"])
        res.append(lig)
    json.dump(res, open(f, "w"))
    return res


R = [x for g in GRAINES for x in charge(g)]
n = len(R)


def boot(f, tirages=4000, graine=99):
    rng = random.Random(graine)
    m = f(R)
    s = sorted(f([R[rng.randrange(n)] for _ in range(n)]) for _ in range(tirages))
    return m, s[int(0.025 * tirages)], s[int(0.975 * tirages) - 1]


F = lambda d: (lambda X: sum(x["K"][d] == 0 for x in X) / len(X))
K = lambda d: (lambda X: sum(x["K"][d] for x in X) / len(X))
E = lambda d: (lambda X: sum(x["E"][d] for x in X) / (12 * len(X)))
print(f"BILAN — H-Échelle, graines 45-49 — {n} cibles — cache {CACHE}\n")
print(f"{'':<4}{'E(d) naïf exposé':>22}{'F(d) gratuits':>22}{'K(d) faits×époques':>26}")
for d in range(4):
    e, f_, k = boot(E(d)), boot(F(d)), boot(K(d))
    print(f"d{d}  {e[0]:>8.1%} [{e[1]:.1%};{e[2]:.1%}]  {f_[0]:>8.1%} [{f_[1]:.1%};{f_[2]:.1%}]  {k[0]:>8.2f} [{k[1]:.2f};{k[2]:.2f}]")
dF13 = boot(lambda X: F(1)(X) - F(3)(X))
dK12 = boot(lambda X: K(2)(X) - K(1)(X))
dK23 = boot(lambda X: K(3)(X) - K(2)(X))
intenables = sum(x["intenables"][3] for x in R) / (12 * n)
print(f"\nH63 F(d1) − F(d3) = {dF13[0]:+.1%} [{dF13[1]:+.1%} ; {dF13[2]:+.1%}]")
print(f"H64 F(d3) = {F(3)(R):.1%}")
print(f"H65 K(d2) − K(d1) = {dK12[0]:+.2f} [{dK12[1]:+.2f} ; {dK12[2]:+.2f}] ;  K(d3) − K(d2) = {dK23[0]:+.2f} [{dK23[1]:+.2f} ; {dK23[2]:+.2f}]")
print(f"H66 E(d3) = {E(3)(R):.1%}")
print(f"H67 époques intenables à d3 = {intenables:.1%}")
par_rel = {}
for x in R:
    r = x["cible"].split("|")[2]
    par_rel.setdefault(r, []).append(x)
print("\nPar relation (descriptif) :")
for r, X in sorted(par_rel.items()):
    print(f"   {r:<10} n={len(X):<3} F : " + " → ".join(f"{F(d)(X):.0%}" for d in range(4))
          + "   K : " + " → ".join(f"{K(d)(X):.1f}" for d in range(4)))
