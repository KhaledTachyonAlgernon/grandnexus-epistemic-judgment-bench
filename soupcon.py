"""
soupcon.py — troisième organe : « fiable en général, mais pas ici ».

Ce qu'il fait à l'information : pour chaque fait, il se demande si UNE source y est compromise —
si sa valeur, toujours la même, est un mensonge tiré une fois puis répété. Si oui, ses énoncés
sur ce fait cessent de compter, et cessent aussi de ternir la réputation de ceux qui la contredisent.

Spécification (écrite avant le code, registre H-Soupçon) :
- candidats : sources dont tous les énoncés sur ce fait affirment la même valeur (au moins 2) ;
- hypothèses : « personne n'est compromis » ou « exactement la source s l'est » ;
- si s est compromise : ses énoncés valent 1/(K−1) et n'informent pas sur la vérité ;
- a priori q_s appris par EM (départ 0,02) ;
- fiabilité de s estimée sur ses énoncés pondérés par (1 − P(compromise)).
Bâti sur la Filiation v3. Risque déclaré : soupçonner les fidèles (faits stables) et les lents (retard).
"""
import math

from filiation import Filiation


class Soupcon(Filiation):

    def __init__(self, q0=0.02, **kw):
        super().__init__(desattenuer=True, **kw)
        self.nom = "soupçon"
        self.q0 = q0

    def ingerer(self, enonces):
        self.q, self.susp = {}, {}                       # a priori par source ; P(compromise) par fait
        self.q = {e.source: self.q0 for e in enonces}
        super().ingerer(enonces)

    def _candidats(self, cle, exclus):
        vals = {}
        for ep, src, o in self.obs[cle]:
            if src not in exclus:
                vals.setdefault(src, []).append(o)
        return [s for s, v in vals.items() if len(v) >= 2 and len(set(v)) == 1 and s not in self.fixes]

    def _avant_arriere(self, cle, exclure=None):
        exclus = exclure if isinstance(exclure, (set, frozenset)) else ({exclure} if exclure else set())
        post, sej, n, L = super()._avant_arriere(cle, exclus)
        K = len(self.dom[cle[1]])
        cands = self._candidats(cle, exclus) if K >= 3 else []
        if not cands:
            if not exclus:
                self.susp[cle] = {}
            return post, sej, n, L
        q_tot = min(0.9, sum(self.q[s] for s in cands))
        hyp = [(math.log(1 - q_tot) + L, None, post, sej)]
        for s in cands:                                  # « s ment ici » : on la fait taire
            p_s, sej_s, _, L_s = super()._avant_arriere(cle, exclus | {s})
            hyp.append((math.log(self.q[s]) + L_s + math.log(1.0 / (K - 1)), s, p_s, sej_s))
        m = max(h[0] for h in hyp)
        w = [math.exp(h[0] - m) for h in hyp]
        z = sum(w)
        w = [x / z for x in w]
        E = len(post)
        melange = [[sum(wi * h[2][t][i] for wi, h in zip(w, hyp)) for i in range(len(post[t]))]
                   for t in range(E)]
        sejour = sum(wi * h[3] for wi, h in zip(w, hyp))
        if not exclus:                                   # on ne retient le soupçon que du jugement complet
            self.susp[cle] = {h[1]: wi for wi, h in zip(w, hyp) if h[1] is not None}
        return melange, sejour, n, L

    def _poids(self, cle, ep, src, o, p_o):
        return super()._poids(cle, ep, src, o, p_o) * (1 - self.susp.get(cle, {}).get(src, 0.0))

    def _etape_m(self, croyance, sejour):
        super()._etape_m(croyance, sejour)
        for src in self.q:                               # propension de chaque source à mentir
            faits = {cle for cle, _, _ in self.par_src[src]}
            tot = sum(self.susp.get(cle, {}).get(src, 0.0) for cle in faits)
            self.q[src] = min(0.3, max(0.001, tot / max(1, len(faits))))

    def rapport(self):
        r = super().rapport()
        r["propension_au_mensonge"] = {s: round(q, 3) for s, q in sorted(self.q.items())}
        return r
