"""
evaluer.py — passe chaque système dans chaque monde et mesure.

  python evaluer.py                  # tableau complet, 3 graines par monde
  python evaluer.py --exporter-llm   # écrit les invites pour le témoin LLM

Métriques :
  exactitude par type de question ;
  sans_reponse : correct seulement si le système dit « je ne sais pas » ;
  Brier : (confiance - avait_raison)², sur les questions qui ont une réponse.
          0 = parfaitement calibré et juste, 1 = sûr de lui et faux. Plus bas = mieux.
"""
import json
import math
import random
import sys
from collections import defaultdict

from monde import generer
from temoins import DernierGagne, Majorite, MotsCles, Plafond
from pesee import Pesee

TYPES = ["actuel", "historique", "deux_sauts", "sans_reponse"]


def evaluer(systeme, monde):
    """Renvoie les scores ET le vecteur question par question (pour les comparaisons appariées)."""
    systeme.ingerer(monde.enonces)
    ok, n, brier, vecteur = defaultdict(int), defaultdict(int), [], []
    for q in monde.questions:
        rep, conf = systeme.repondre(q)
        juste = (rep is None) if q.attendu is None else (rep == q.attendu)
        ok[q.type] += juste
        n[q.type] += 1
        vecteur.append((int(juste), q.grappe))
        if q.attendu is not None:
            brier.append(((conf if rep is not None else 0.0) - (rep == q.attendu)) ** 2)
    res = {t: ok[t] / n[t] for t in TYPES}
    res["global"] = sum(ok.values()) / sum(n.values())
    res["brier"] = sum(brier) / len(brier)
    res["_vecteur"] = vecteur        # [(juste, fait décisif)] : l'unité de preuve est le fait
    return res


def _bootstrap(valeurs, grappes, tirages=1000, graine=12345):
    """IC à 95 % d'une moyenne par bootstrap EN GRAPPES : on rééchantillonne des faits, pas des
    questions — des questions qui reposent sur le même fait ne sont pas des preuves indépendantes."""
    somme, nb = defaultdict(float), defaultdict(int)
    for v, g in zip(valeurs, grappes):
        somme[g] += v
        nb[g] += 1
    cles = list(somme)
    S, N = [somme[c] for c in cles], [nb[c] for c in cles]
    moy = sum(S) / sum(N)
    rng, k, stats = random.Random(graine), len(cles), []
    for _ in range(tirages):
        idx = [rng.randrange(k) for _ in range(k)]
        stats.append(sum(S[i] for i in idx) / sum(N[i] for i in idx))
    stats.sort()
    bas, haut = stats[int(0.025 * tirages)], stats[int(0.975 * tirages) - 1]
    return moy, max(moy - bas, haut - moy), k


def ic95(vecteur):
    return _bootstrap([v for v, _ in vecteur], [g for _, g in vecteur])[1]


TEMOINS = [lambda m: DernierGagne(), lambda m: Majorite(), lambda m: MotsCles()]
ORGANES = [lambda m: Pesee(False, False), lambda m: Pesee(True, False), lambda m: Pesee(True, True),
           lambda m: Pesee(True, True, un_contre_tous=True)]
PLAFOND = [lambda m: Plafond(m)]


def tableau(graines=(0, 1, 2), systemes=TEMOINS + ORGANES + PLAFOND,
            presets=("facile", "realiste", "hostile", "echo")):
    resultats = {}
    for preset in presets:
        mondes = [generer(preset, g) for g in graines]
        m0 = mondes[0]
        jetons = sum(len(e.texte) for e in m0.enonces) // 4
        print(f"\n══ monde « {preset} » — {len(m0.enonces)} énoncés (~{jetons:,} jetons), "
              f"{len(m0.questions)} questions × {len(graines)} graines")
        print(f"{'système':<18}" + "".join(f"{t:>13}" for t in TYPES) + f"{'global':>14}{'brier':>8}")
        for fabrique in systemes:
            rs = []
            for m in mondes:
                s = fabrique(m)
                rs.append(evaluer(s, m))
            moy = {k: sum(r[k] for r in rs) / len(rs) for k in rs[0] if k != "_vecteur"}
            vec = [x for r in rs for x in r["_vecteur"]]
            resultats[(preset, s.nom)] = (moy, vec)
            print(f"{s.nom:<18}" + "".join(f"{moy[t]:>12.1%} " for t in TYPES)
                  + f"{moy['global']:>8.1%} ±{ic95(vec):.1%} {moy['brier']:>6.3f}")
    return resultats


def apparier(vec_a, vec_b):
    """Différence appariée A − B (mêmes questions), IC à 95 % en grappes de faits.
    Renvoie (moyenne, demi-largeur, nombre de faits distincts)."""
    return _bootstrap([a - b for (a, _), (b, _) in zip(vec_a, vec_b)], [g for _, g in vec_a])


def exporter_llm(preset="realiste", graine=0, chemin="invites_llm.jsonl"):
    """Témoin 4 (non exécuté ici) : un LLM avec tout le corpus en contexte.
    Écrit une invite par question ; les réponses se notent ensuite avec noter_llm()."""
    m = generer(preset, graine)
    corpus = "\n".join(e.texte for e in sorted(m.enonces, key=lambda e: e.id))
    consigne = ("Voici des informations datées provenant de sources diverses, parfois "
                "contradictoires, parfois périmées. Réponds à la question par la seule valeur "
                "demandée, ou par INCONNU si l'information est absente. Puis, sur une seconde "
                "ligne, ta confiance entre 0 et 1.\n\n")
    with open(chemin, "w", encoding="utf-8") as f:
        for q in m.questions:
            f.write(json.dumps({"id": q.id, "invite": consigne + corpus + "\n\nQuestion : " + q.texte},
                               ensure_ascii=False) + "\n")
    print(f"{len(m.questions)} invites écrites dans {chemin}")


def noter_llm(preset, graine, reponses):
    """reponses : {id_question: (texte_reponse | 'INCONNU', confiance)}"""
    m = generer(preset, graine)

    class Rejoue:
        nom = "LLM"
        def ingerer(self, _): pass
        def repondre(self, q):
            r, c = reponses[q.id]
            return (None, 0.0) if r.strip().upper() == "INCONNU" else (r.strip(), float(c))

    return evaluer(Rejoue(), m)


if __name__ == "__main__":
    if "--exporter-llm" in sys.argv:
        exporter_llm()
    else:
        tableau()
        for variante, kw in [("C", {}), ("D", {"un_contre_tous": True})]:
            for g in (0, 1, 2):
                m = generer("hostile", g)
                o = Pesee(True, True, **kw)
                o.ingerer(m.enonces)
                if g == 0:
                    print(f"\n── boîte de verre, variante {variante} (monde hostile)")
                    print(f"{'source':<16}{'fiabilité apprise':>19}{'vraie':>8}{'retard appris':>15}{'vrai':>6}")
                    for s in m.sources:
                        print(f"{s.nom:<16}{o.f[s.nom]:>19.2f}{s.fiabilite:>8.2f}{o.L[s.nom]:>15}{s.retard:>6}")
                alm = o.L["L'Almanach"]
                print(f"   graine {g} : retard appris de L'Almanach = {alm}")
