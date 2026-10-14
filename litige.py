"""
litige.py — cinquième organe : savoir qu'on ne peut pas trancher.

Ce qu'il fait à l'information : quand un bloc de sources figées s'oppose à des dissidents, et que rien
ne permet de savoir quel camp ment, il ne choisit pas. Il rend la croyance au mélange à parts égales
des deux lectures — « le bloc ment » et « les dissidents mentent » — et l'expose.

Spécification (registre H-Litige, figée avant le code) :
- bloc : ≥ 2 sources EFFECTIVES (un copieur dont la source est dans le groupe ne compte pas), figées
  (≥ 80 % de leurs énoncés, au moins 2 chacune) sur une valeur v ;
- dissidents : ≥ 2 sources effectives, ≥ 1 énoncé chacune, majoritairement ≠ v, ≥ 3 énoncés au total ;
- n'accuse personne, ne touche ni aux réputations ni à l'apprentissage : s'applique après la Méprise.
Un menteur isolé relève du Soupçon ; le Litige ne traite que les blocs.
"""
from collections import Counter, defaultdict

from meprise import Meprise


class Litige(Meprise):

    def __init__(self, persistance=0.8, **kw):
        super().__init__(**kw)
        self.nom = "litige"
        self.persistance = persistance

    def ingerer(self, enonces):
        super().ingerer(enonces)
        self.croyance_tranchee = dict(self.croyance)       # ce que la Méprise aurait répondu
        self.litiges = {}
        for cle in list(self.croyance):
            camps = self._camps(cle)
            if not camps:
                continue
            bloc, diss, v = camps
            lectures = [self._avant_arriere(cle, frozenset(bloc))[0],
                        self._avant_arriere(cle, frozenset(diss))[0]]
            self.croyance[cle] = [[(a + b) / 2 for a, b in zip(lectures[0][t], lectures[1][t])]
                                  for t in range(len(lectures[0]))]
            self.litiges[cle] = {"valeur_du_bloc": v, "bloc": sorted(bloc), "dissidents": sorted(diss)}

    def _effectif(self, groupe):
        """Une voix répétée reste une voix : un copieur dont la source est dans le groupe ne compte pas."""
        return {s for s in groupe if not (s in self.parent and self.parent[s][0] in groupe)}

    def _camps(self, cle):
        par = defaultdict(list)
        for ep, src, o in self.obs[cle]:
            par[src].append(o)
        figes = defaultdict(set)
        for src, vals in par.items():
            if len(vals) >= 2:
                v, n = Counter(vals).most_common(1)[0]
                if n / len(vals) >= self.persistance:
                    figes[v].add(src)
        for v, bloc in sorted(figes.items(), key=lambda x: (-len(x[1]), str(x[0]))):
            if len(self._effectif(bloc)) < 2:
                continue
            diss = {s for s, vals in par.items() if s not in bloc
                    and sum(x != v for x in vals) / len(vals) > 0.5}
            if len(self._effectif(diss)) >= 2 and sum(len(par[s]) for s in diss) >= 3:
                return bloc, diss, v
        return None

    def rapport(self):
        r = super().rapport()
        r["litiges"] = len(self.litiges)
        return r
