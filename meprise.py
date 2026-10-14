"""
meprise.py — quatrième organe : apprendre COMMENT le monde se trompe.

Ce qu'il fait à l'information : une erreur plausible (on confond Kali avec Kalo) n'est plus lue comme
une voix pour Kalo, mais comme du bruit attendu autour de Kali — et même comme un indice pour Kali.

Spécification (registre H-Méprise, écrite avant le code) :
- par relation : P(o | v, erreur) = λ·S[v][o] + (1 − λ)/(K − 1),
  S[v][o] = (N[v][o] + α/(K−1)) / (N_v + α), α = 1 ;
- N : erreurs attendues d'après les croyances complètes, pondérées par (non-copie) × (non-compromission) ;
- λ : part des erreurs qui suivent une forme, apprise sur la vraisemblance « un contre tous » — chaque
  erreur est jugée contre les comptes calculés SANS elle, pour ne pas voir de motifs dans le bruit ;
- désatténuation généralisée : f = (A − Γ)/(S − Γ).
Bâtie sur le Soupçon. Risque déclaré : l'apophénie.
"""
from collections import defaultdict

from soupcon import Soupcon


class Meprise(Soupcon):

    def __init__(self, alpha=1.0, **kw):
        super().__init__(**kw)
        self.nom = "méprise"
        self.alpha = alpha

    def ingerer(self, enonces):
        self.lam, self.N, self.Nv, self._col = {}, {}, {}, {}
        super().ingerer(enonces)

    # — la forme des erreurs —
    def _sp(self, r, v, o, K):
        return (self.N[r].get(v, {}).get(o, 0.0) + self.alpha / (K - 1)) / (self.Nv[r].get(v, 0.0) + self.alpha)

    def _erreur(self, r, o, K, j):
        lam = self.lam.get(r, 0.0)
        if lam <= 0.0:
            return None
        if (r, o) not in self._col:
            u = (1 - lam) / (K - 1)
            self._col[(r, o)] = [0.0 if v == o else lam * self._sp(r, v, o, K) + u for v in self.dom[r]]
        return self._col[(r, o)]

    def _apprendre(self, croyance):
        N = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
        erreurs = defaultdict(list)
        for src, liste in self.par_src.items():
            for cle, ep, o in liste:
                r = cle[1]
                pi = croyance[cle][max(0, ep - self.L[src])]
                w = self._poids(cle, ep, src, o, pi[self.pos[r][o]])
                for i, v in enumerate(self.dom[r]):
                    if v != o and pi[i] > 1e-4:
                        N[r][v][o] += w * pi[i]
                        erreurs[r].append((v, o, w * pi[i]))
        self.N = {r: {v: dict(d) for v, d in row.items()} for r, row in N.items()}
        self.Nv = {r: {v: sum(d.values()) for v, d in row.items()} for r, row in self.N.items()}
        for r, E in erreurs.items():
            K, lam = len(self.dom[r]), 0.5
            if K < 3:
                self.lam[r] = 0.0
                continue
            for _ in range(50):                              # EM sur λ, chaque erreur jugée sans elle
                num = den = 0.0
                for v, o, w in E:
                    p_f = (self.N[r][v][o] - w + self.alpha / (K - 1)) / (self.Nv[r][v] - w + self.alpha)
                    p_u = 1.0 / (K - 1)
                    num += w * lam * p_f / (lam * p_f + (1 - lam) * p_u)
                    den += w
                lam = num / max(den, 1e-9)
            self.lam[r] = lam
        self._col = {}

    def _etape_m(self, croyance, sejour):
        super()._etape_m(croyance, sejour)
        self._apprendre(croyance)

    # — désatténuation généralisée : l'accord par erreur n'est plus uniforme —
    def _fiabilite(self, croyance, src, L):
        A = S = G = n = 0.0
        for cle, ep, o in self.par_src[src]:
            r = cle[1]
            K = len(self.dom[r])
            pi = croyance[cle][max(0, ep - L)]
            w = self._poids(cle, ep, src, o, pi[self.pos[r][o]])
            A += w * pi[self.pos[r][o]]
            S += w * sum(x * x for x in pi)
            lam, g = self.lam.get(r, 0.0), 0.0
            for i, v in enumerate(self.dom[r]):
                if pi[i] < 1e-4 or K < 2:
                    continue
                reste = 1 - pi[i]
                forme = 0.0
                if lam > 0:
                    nv = self.Nv[r].get(v, 0.0)
                    acc = sum(c * pi[self.pos[r][x]] for x, c in self.N[r].get(v, {}).items() if x != v)
                    forme = (acc + self.alpha / (K - 1) * reste) / (nv + self.alpha)
                g += pi[i] * (lam * forme + (1 - lam) * reste / (K - 1))
            G += w * g
            n += w
        n = max(n, 1e-9)
        A, S, G = A / n, S / n, G / n
        den = S - G
        return A if den < 0.05 else (A - G) / den

    def rapport(self):
        r = super().rapport()
        r["lambda"] = {k: round(v, 2) for k, v in sorted(self.lam.items())}
        return r
