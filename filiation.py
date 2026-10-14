"""
filiation.py — deuxième organe : reconnaître qui recopie qui.

Ce qu'il fait à l'information : il retire aux énoncés recopiés la force de témoignage
qu'ils n'ont pas. Un énoncé recopié n'est pas une voix de plus, c'est un écho.

Signal : les ERREURS partagées. Deux sources indépendantes disent souvent la même vérité
(il n'y en a qu'une), mais partagent rarement la même erreur (il y en a beaucoup).
Pour chaque paire (X, Y) : à quelle fréquence X reprend-il la valeur de Y quand cette
valeur est probablement fausse, comparé à ce que le hasard donnerait ?

Un énoncé de X dont le parent présumé Y avait dit la même chose est jugé par une
vraisemblance de mélange : copie (probabilité c, n'apprend rien sur la vérité)
ou témoignage indépendant (1 − c).

Hérite de la Pesée D (fiabilité, retard, un contre tous).
Risque déclaré : circularité — on juge les erreurs avec des croyances que les copieurs ont façonnées.
"""
from bisect import bisect_right
from collections import defaultdict

from pesee import Pesee


class Filiation(Pesee):

    def __init__(self, seuil=0.3, estimateur="vraisemblance", desattenuer=False, **kw):
        super().__init__(True, True, un_contre_tous=True, desattenuer=desattenuer, **kw)
        self.estimateur = estimateur          # "erreurs" = v1 (rejetée), "vraisemblance" = v2/v3
        self.nom = ("filiation v3" if desattenuer else "filiation v2") if estimateur == "vraisemblance" \
            else "filiation v1"
        self.seuil = seuil

    def ingerer(self, enonces):
        self.parent = {}                                    # source -> (parent, taux de copie)
        dit, par_src = defaultdict(list), defaultdict(list)
        for e in enonces:
            dit[(e.source, e.sujet, e.relation)].append((e.epoque, e.objet))
            par_src[e.source].append(((e.sujet, e.relation), e.epoque, e.objet))
        self.dit = {k: sorted(v) for k, v in dit.items()}
        self.epq = {k: [x[0] for x in v] for k, v in self.dit.items()}
        self.par_src = par_src
        super().ingerer(enonces)

    def _dernier(self, src, cle, ep):
        """Ce que src avait affirmé en dernier sur ce fait, à l'époque ep incluse."""
        k = (src,) + cle
        if k not in self.dit:
            return None
        i = bisect_right(self.epq[k], ep)
        return self.dit[k][i - 1][1] if i else None

    # — un écho n'informe pas : vraisemblance de mélange —
    def _vraisemblance(self, cle, ep, src, o, K, j):
        v = super()._vraisemblance(cle, ep, src, o, K, j)
        if src in self.parent:
            par, c = self.parent[src]
            if self._dernier(par, cle, ep) == o:
                return [c + (1 - c) * x for x in v]
        return v

    # — une source est jugée sur ses témoignages, pas sur ses échos —
    def _poids(self, cle, ep, src, o, p_o):
        par = self.parent.get(src)
        if par and self._dernier(par[0], cle, ep) == o:
            fs, K = self.f[src], len(self.dom[cle[1]])
            indep = p_o * fs + (1 - p_o) * (1 - fs) / max(1, K - 1)
            return 1 - par[1] / (par[1] + (1 - par[1]) * indep)
        return 1.0

    def _etape_m(self, croyance, sejour):
        super()._etape_m(croyance, sejour)
        self._filiation()

    def _filiation(self):
        sources, taux = sorted(x for x in self.f if x not in self.fixes), {}   # une ancre ne copie ni n'est copiée
        for X in sources:
            croy, fX = self._juge[X], self.f[X]              # croyances SANS X
            for Y in sources:
                if Y == X:
                    continue
                if self.estimateur == "erreurs":
                    c = self._taux_erreurs(X, Y, croy, fX)
                else:
                    c = self._taux_vraisemblance(X, Y, croy, fX)
                if c is not None:
                    taux[(X, Y)] = c
        self.parent = {}
        for X in sources:                                    # on garde le sens le plus fort
            cands = [(c, Y) for (A, Y), c in taux.items()
                     if A == X and c >= self.seuil and c > taux.get((Y, A), 0.0)]
            if cands:
                c, Y = max(cands)
                self.parent[X] = (Y, min(0.95, c))
        self.taux = taux

    def _taux_erreurs(self, X, Y, croy, fX):
        """v1 (rejetée) : erreurs partagées pondérées par le doute — biaisée quand les erreurs sont rares."""
        poids = partage = hasard = 0.0
        for cle, ep, o in self.par_src[X]:
            K = len(self.dom[cle[1]])
            oy = self._dernier(Y, cle, ep)
            if K < 2 or oy is None:
                continue
            faux = 1 - croy[cle][max(0, ep - self.L[Y])][self.pos[cle[1]][oy]]
            poids += faux
            partage += faux * (o == oy)
            hasard += faux * (1 - fX) / (K - 1)
        if poids < 3:
            return None
        r_obs, r_ind = partage / poids, hasard / poids
        return max(0.0, (r_obs - r_ind) / (1 - r_ind))

    def _taux_vraisemblance(self, X, Y, croy, fX, tours=30):
        """v2 : maximum de vraisemblance de P(o) = c·[o = dernier de Y] + (1-c)·P_indép(o).
        P_indép est calculé à l'époque effective de X : un accord sur une valeur
        probablement vraie s'explique très bien sans copie, et ne l'accuse donc pas."""
        donnees = []
        for cle, ep, o in self.par_src[X]:
            K = len(self.dom[cle[1]])
            oy = self._dernier(Y, cle, ep)
            if K < 2 or oy is None:
                continue
            p_o = croy[cle][max(0, ep - self.L[X])][self.pos[cle[1]][o]]
            donnees.append((o == oy, p_o * fX + (1 - p_o) * (1 - fX) / (K - 1)))
        if len(donnees) < 20:
            return None
        c = 0.5
        for _ in range(tours):                               # EM sur c : log-vraisemblance concave
            c = sum(c / (c + (1 - c) * q) if d else 0.0 for d, q in donnees) / len(donnees)
        return c

    def rapport(self):
        r = super().rapport()
        r["parent"] = {s: (p, round(c, 2)) for s, (p, c) in sorted(self.parent.items())}
        return r
