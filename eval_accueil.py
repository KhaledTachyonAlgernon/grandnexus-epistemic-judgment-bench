"""Évaluation de l'Accueil à règles. Usage : python eval_accueil.py dev   (le test n'est lu que par l'argument test)."""
import json, sys
from monde import generer
from accueil_regles import LecteurRegles

V = {x["id"]: x for x in json.load(open("desordre_verite.json"))}
LECTEURS = {}
for w in ("complice", "plausible"):
    m = generer(w, 80, n_personnes=40, n_orgs=8)
    pers = sorted({s for (s, r) in m.verite if r == "habite"})
    orgs = sorted({s for (s, r) in m.verite if r == "dirige"})
    LECTEURS[w] = LecteurRegles(pers, orgs, sorted(m.domaines["habite"]))


def evaluer(items, montrer_erreurs=False):
    res = []
    for x in items:
        v = V[x["id"]]
        lu, raisons = LECTEURS[v["monde"]].lire(x["texte"])
        vrai = (v["sujet"], v["relation"], str(v["objet"]))
        juste = lu is not None and lu[:3] == vrai
        res.append({"id": x["id"], "lu": lu is not None, "juste": juste, "conf": lu[3] if lu else 0.0,
                    "relation": v["relation"], "style": x.get("style", "?")})
        if montrer_erreurs and not juste:
            print(f"   ✗ [{v['relation']}] {x['texte']}\n       lu {lu} | raisons {raisons}")
    return res


def resume(res, titre):
    n = len(res)
    lus = [r for r in res if r["lu"]]
    print(f"{titre} : {n} phrases ; lues {len(lus) / n:.0%} ; justes {sum(r['juste'] for r in res) / n:.0%} ; "
          f"précision des lectures {sum(r['juste'] for r in lus) / max(1, len(lus)):.0%}")
    for lo, hi in ((0.95, 1.01), (0.6, 0.95), (0.0, 0.6)):
        E = [r for r in lus if lo <= r["conf"] < hi]
        if E:
            print(f"   confiance {lo:.2f}-{min(hi, 1):.2f} : n = {len(E):>3}, justes {sum(r['juste'] for r in E) / len(E):.0%}")


if __name__ == "__main__":
    if sys.argv[1] == "dev":
        items = [y for i in range(4) for y in json.load(open(f"desordre_dev/desordre/lot_{i}.json"))["items"]]
        resume(evaluer(items, montrer_erreurs=True), "DÉVELOPPEMENT")


if __name__ == "__main__" and sys.argv[1] == "test":
    items = [y for i in range(4, 8) for y in json.load(open(f"desordre_test/desordre/lot_{i}.json"))["items"]]
    res = evaluer(items, montrer_erreurs=False)
    resume(res, "TEST")
    print("par relation :", {r: f"{sum(x['juste'] for x in res if x['relation'] == r) / sum(1 for x in res if x['relation'] == r):.0%}"
                             for r in ("habite", "travaille", "dirige", "naissance")})
    json.dump(res, open("accueil_regles_test.json", "w"))
