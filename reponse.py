"""
reponse.py — l'objet-réponse de GrandNexus : une valeur, deux doutes séparés, leurs motifs, et leurs raisons.

Aucun score fusionné. Le lecteur reçoit :
- la valeur et la confiance ;
- le doute « preuves » (motif « peu de preuves » si confiance < 0,9) ;
- le doute « contestation » (motif « contestée » si ≥ 2 voix effectives contredisent la réponse), avec les
  contradicteurs et les fusions de sources appliquées ;
- une justification courte (3 énoncés de plus forte contribution, fidèle à 99 % en suffisance, H-Fidélité) ;
- les hypothèses structurelles appliquées à ce fait (copies, soupçons).
"""
from base import contributions

SEUIL_PREUVES = 0.9


def objet_reponse(o, cle, t):
    post = o.croyance[cle][t]
    ordre = sorted(range(len(post)), key=lambda i: -post[i])
    a, b = ordre[0], ordre[1]
    valeur = o.dom[cle[1]][a]
    groupe = {}
    for s in o.f:                                          # fusion des copieurs avec leur source
        r, vus = s, set()
        while r in o.parent and r not in vus:
            vus.add(r); r = o.parent[r][0]
        groupe[s] = r
    par = {}
    for ep, src, ob in o.obs[cle]:
        rep_t = o.dom[cle[1]][max(range(len(o.croyance[cle][max(0, ep - o.L[src])])),
                                  key=o.croyance[cle][max(0, ep - o.L[src])].__getitem__)]
        par.setdefault(src, []).append(ob != rep_t)
    contre = sorted(s for s, v in par.items() if sum(v) / len(v) > 0.5)
    voix = sorted({groupe[s] for s in contre})
    fusions = [f"{s} compté avec {groupe[s]} (copie estimée {o.parent[s][1]:.2f})"
               for s in contre if groupe[s] != s and s in o.parent]
    contrib = sorted(contributions(o, cle, t, a, b), reverse=True)[:3]
    tous = o.obs[cle]
    motifs = []
    if len(voix) >= 2:
        motifs.append(f"contestée par {len(voix)} voix indépendantes : {', '.join(voix)}")
    if post[a] < SEUIL_PREUVES:
        motifs.append(f"peu de preuves (confiance {post[a]:.2f})")
    return {
        "fait": f"{cle[0]} — {cle[1]}", "epoque": t, "valeur": valeur, "confiance": round(post[a], 3),
        "doute_preuves": round(1 - post[a], 3), "doute_contestation": len(voix),
        "contradicteurs": contre, "voix_effectives": voix, "fusions": fusions,
        "justification": [f"{tous[i][1]} (époque {tous[i][0]}) : {tous[i][2]}" for c, i in contrib if c > 0],
        "soupcons": {s: round(p, 2) for s, p in o.susp.get(cle, {}).items() if p > 0.1},
        "motifs": motifs,
    }


def en_clair(obj):
    lignes = [f"{obj['fait']}, époque {obj['epoque']} : {obj['valeur']} (confiance {obj['confiance']:.2f})"]
    lignes += [f"  ⚠ {m}" for m in obj["motifs"]] or ["  aucun motif de doute"]
    if obj["fusions"]:
        lignes += [f"  fusion appliquée : {f}" for f in obj["fusions"]]
    if obj["soupcons"]:
        lignes.append(f"  soupçons sur ce fait : {obj['soupcons']}")
    lignes.append("  pourquoi : " + " ; ".join(obj["justification"]))
    return "\n".join(lignes)
