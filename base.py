"""base.py — ce dont le moteur de jugement a besoin, et rien d'autre (extrait de monde.py, temoins.py, test_fidelite.py)."""
import math
from collections import namedtuple
from dataclasses import dataclass

@dataclass(frozen=True)
class Enonce:
    id: int
    epoque: int
    source: str
    sujet: str
    relation: str
    objet: str
    texte: str



@dataclass(frozen=True)
class Question:
    id: int
    type: str           # actuel | historique | deux_sauts | sans_reponse
    sujet: str
    chaine: tuple       # relations à suivre depuis le sujet
    epoque: int
    texte: str
    attendu: object     # None = la bonne réponse est « inconnu »
    grappe: tuple = ()  # le fait qui décide de la réponse : unité de preuve statistique




class Systeme:
    """Base de tout juge. repondre() COMPOSE les sauts : c'est ici que le graphe est parcouru."""
    nom = "?"

    def ingerer(self, enonces):
        raise NotImplementedError

    def resoudre(self, sujet, relation, epoque):
        raise NotImplementedError

    def repondre(self, q):
        x, conf = q.sujet, 1.0
        for r in q.chaine:                       # les sauts se composent
            x, c = self.resoudre(x, r, q.epoque)
            if x is None:
                return None, 0.0
            conf *= c
        return x, conf


def contributions(o, cle, t, a, b):
    """Part de chaque énoncé dans la préférence de la valeur a sur la valeur b (pour la justification)."""
    r = cle[1]
    K, p = len(o.dom[r]), o.p[r]
    out = []
    for i, (ep, src, ob) in enumerate(o.obs[cle]):
        v = o._vraisemblance(cle, ep, src, ob, K, o.pos[r][ob])
        eff = max(0, ep - o.L[src])
        c = (math.log(max(v[a], 1e-12)) - math.log(max(v[b], 1e-12))) * (1 - p) ** abs(eff - t)
        out.append((c, i))
    return out
