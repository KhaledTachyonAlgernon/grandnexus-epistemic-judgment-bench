"""
pesee.py — premier organe : juger sans savoir à qui se fier.

Ce qu'il fait à l'information : à chaque fait, il attache une croyance par époque,
qui dépend de QUI l'a dit, QUAND, et de ce que disent les autres.

Il ne connaît ni la fiabilité des sources, ni leur retard, ni la vitesse à laquelle
le monde change. Il les estime à partir des seuls accords et désaccords, par
espérance-maximisation (dans l'esprit de Dawid & Skene, 1979) :
  E — pour chaque fait, filtre avant-arrière le long du temps → croyance par époque
  M — chaque source est réévaluée contre ces croyances ; le taux de changement aussi
Chaque fait ne parle qu'à ses époques voisines : des règles locales, sous un objectif.

Hypothèse déclarée : au moins une source est à jour (le plus petit retard vaut 0).
Biais connu (variantes A-C) : une source est jugée contre des croyances qu'elle a influencées.
La variante D (un_contre_tous) juge chaque source contre les croyances des autres seulement.
"""
import math
from collections import defaultdict

from base import Systeme


class Pesee(Systeme):

    def __init__(self, fiabilite=True, retard=True, iterations=12,
                 f0=0.7, p0=0.1, retard_max=4, un_contre_tous=False, desattenuer=False, fixes=None):
        self.app_f, self.app_l, self.loo, self.desatt = fiabilite, retard, un_contre_tous, desattenuer
        self.fixes = dict(fixes or {})                    # sources à fiabilité FIXÉE (ancres) : jamais réapprises
        self.iterations, self.f0, self.p0, self.retard_max = iterations, f0, p0, retard_max
        self.nom = "pesée " + {(False, False): "A datation",
                               (True, False): "B +fiabilité",
                               (True, True): "C +retard"}.get((fiabilite, retard), "?")
        if un_contre_tous:
            self.nom = "pesée E désatt." if desattenuer else "pesée D un/tous"

    # — accueil des énoncés, puis apprentissage —
    def ingerer(self, enonces):
        self.E = max(e.epoque for e in enonces) + 1
        self.obs = defaultdict(list)                       # (sujet, relation) -> [(époque, source, objet)]
        valeurs = defaultdict(set)
        self.par_src = defaultdict(list)                   # source -> [((sujet, relation), époque, objet)]
        for e in enonces:
            self.obs[(e.sujet, e.relation)].append((e.epoque, e.source, e.objet))
            self.par_src[e.source].append(((e.sujet, e.relation), e.epoque, e.objet))
            valeurs[e.relation].add(e.objet)
        self.dom = {r: sorted(v) for r, v in valeurs.items()}   # domaine OBSERVÉ, pas le vrai
        self.pos = {r: {v: i for i, v in enumerate(d)} for r, d in self.dom.items()}
        sources = {e.source for e in enonces}
        self.f = {s: self.fixes.get(s, self.f0) for s in sources}
        self.L = {s: 0 for s in sources}
        self.p = {r: self.p0 for r in self.dom}
        for _ in range(self.iterations):
            self._etape_m(*self._etape_e())
        self.croyance, _ = self._etape_e()

    def _etape_e(self, exclure=None):
        croyance, sejour = {}, defaultdict(lambda: [0.0, 0])
        for cle in self.obs:
            post, s, n, _ = self._avant_arriere(cle, exclure)
            croyance[cle] = post
            sejour[cle[1]][0] += s
            sejour[cle[1]][1] += n
        return croyance, sejour

    def _avant_arriere(self, cle, exclure=None):
        r = cle[1]
        K, E, p = len(self.dom[r]), self.E, self.p[r]
        if K < 2:
            return [[1.0] for _ in range(E)], E - 1, E - 1, 0.0
        exclus = exclure if isinstance(exclure, (set, frozenset)) else ({exclure} if exclure else set())
        pos = self.pos[r]
        em = [[1.0] * K for _ in range(E)]
        logL = 0.0                                         # log-vraisemblance des énoncés retenus
        for ep, src, o in self.obs[cle]:
            if src in exclus:                              # un contre tous : on se tait
                continue
            t = max(0, ep - self.L[src])
            v = self._vraisemblance(cle, ep, src, o, K, pos[o])
            ligne = [x * y for x, y in zip(em[t], v)]
            m = max(ligne)
            em[t] = [x / m for x in ligne]
            logL += math.log(m)

        def transite(a):                                   # garder (1-p) ou changer vers un autre
            tot = sum(a)
            return [x * (1 - p) + (tot - x) * p / (K - 1) for x in a]

        def norm(a):
            z = sum(a)
            return [x / z for x in a]

        z0 = sum(em[0])
        logL += math.log(z0 / K)
        av = [[x / z0 for x in em[0]]]
        for t in range(1, E):
            a = [x * y for x, y in zip(transite(av[-1]), em[t])]
            z = sum(a)
            logL += math.log(z)
            av.append([x / z for x in a])
        ar = [[1.0] * K for _ in range(E)]
        for t in range(E - 2, -1, -1):
            ar[t] = norm(transite([a * b for a, b in zip(em[t + 1], ar[t + 1])]))
        post = [norm([a * b for a, b in zip(av[t], ar[t])]) for t in range(E)]

        sejour = 0.0                                       # espérance du nombre de non-changements
        for t in range(E - 1):
            g = [a * b for a, b in zip(em[t + 1], ar[t + 1])]
            z = sum(a * b for a, b in zip(av[t], transite(g)))
            sejour += sum(a * (1 - p) * b for a, b in zip(av[t], g)) / z
        return post, sejour, E - 1, logL

    def _vraisemblance(self, cle, ep, src, o, K, j):
        """P(la source dit o | la vraie valeur est v), pour chaque v. Erreurs indépendantes."""
        f = self.f[src]
        e = self._erreur(cle[1], o, K, j)
        if e is None:                                      # erreurs uniformes
            autre = (1 - f) / (K - 1)
            return [f if i == j else autre for i in range(K)]
        return [f if i == j else (1 - f) * e[i] for i in range(K)]

    def _erreur(self, r, o, K, j):
        """P(dire o | vérité v, erreur) pour chaque v ; None = uniforme (organes de base)."""
        return None

    def _poids(self, cle, ep, src, o, p_o):
        """Poids d'un énoncé dans le jugement de sa source (1 = témoignage plein)."""
        return 1.0

    def _stats(self, croyance, src, L, complet=False):
        """A = accord moyen ; S = netteté moyenne des croyances (Σπ²) ; u = moyenne de 1/(K-1)."""
        A = S = U = n = 0.0
        for cle, ep, o in self.par_src[src]:
            r = cle[1]
            pi = croyance[cle][max(0, ep - L)]
            p_o = pi[self.pos[r][o]]
            w = self._poids(cle, ep, src, o, p_o)
            A += w * p_o
            n += w
            if complet:
                K = len(self.dom[r])
                S += w * (sum(x * x for x in pi) if K >= 2 else 1.0)
                U += w / (K - 1) if K >= 2 else 0.0
        n = max(n, 1e-9)
        return A / n, S / n, U / n

    def _accord(self, croyance, src, L):
        return self._stats(croyance, src, L)[0]

    def _fiabilite(self, croyance, src, L):
        """Sans désatténuation : f = A. Avec : on inverse A = f·S + (1-f)(1-S)·u
        (un accord avec des croyances non certaines sous-estime toujours l'exactitude)."""
        if not self.desatt:
            return self._accord(croyance, src, L)
        A, S, u = self._stats(croyance, src, L, complet=True)
        den = S - (1 - S) * u
        return A if den < 0.05 else (A - (1 - S) * u) / den

    def _etape_m(self, croyance, sejour):
        for r, (s, n) in sejour.items():
            self.p[r] = min(0.5, max(0.001, 1 - s / max(1, n)))
        # chaque source est jugée contre les croyances des AUTRES (si un_contre_tous)
        juge = {src: (self._etape_e(exclure=src)[0] if self.loo else croyance)
                for src in self.f if src not in self.fixes}
        self._juge = juge
        if self.app_l:
            for src in self.L:
                if src in self.fixes:
                    continue
                self.L[src] = max(range(self.retard_max + 1),
                                  key=lambda L: self._accord(juge[src], src, L))
            m = min(self.L.values())
            self.L = {s: L - m for s, L in self.L.items()}
        if self.app_f:
            for src in self.f:
                if src in self.fixes:
                    continue
                self.f[src] = min(0.99, max(0.02, self._fiabilite(juge[src], src, self.L[src])))

    # — répondre —
    def resoudre(self, s, r, t):
        cle = (s, r)
        if cle not in self.croyance:
            return None, 0.0
        post, dom = self.croyance[cle][min(t, self.E - 1)], self.dom[r]
        i = max(range(len(dom)), key=post.__getitem__)
        return dom[i], post[i]

    # — boîte de verre : ce que l'organe croit de ses sources —
    def rapport(self):
        return {"fiabilite": {s: round(f, 2) for s, f in sorted(self.f.items())},
                "retard": dict(sorted(self.L.items())),
                "changement": {r: round(p, 3) for r, p in sorted(self.p.items())}}
