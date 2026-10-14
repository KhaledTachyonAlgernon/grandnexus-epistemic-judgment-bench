"""
temoins.py — les systèmes que tout organe GrandNexus doit battre.

Interface commune : ingerer(enonces), puis repondre(question) -> (reponse | None, confiance).
None signifie « je ne sais pas ». La confiance est la probabilité estimée d'avoir raison.

Règle du banc : aucun organe n'est ajouté s'il ne bat pas ces témoins sur au moins
une métrique, sans régresser nettement sur les autres.
"""
import re
import math
from collections import Counter, defaultdict


class Systeme:
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


class DernierGagne(Systeme):
    """Témoin 1 — la dernière affirmation datée l'emporte. Aveugle à la fiabilité."""
    nom = "dernier gagne"

    def ingerer(self, enonces):
        self.idx = defaultdict(list)
        for e in enonces:
            self.idx[(e.sujet, e.relation)].append((e.epoque, e.id, e.objet))

    def resoudre(self, s, r, t):
        c = [x for x in self.idx.get((s, r), []) if x[0] <= t]
        return (max(c)[2], 1.0) if c else (None, 0.0)


class Majorite(Systeme):
    """Témoin 2 — vote majoritaire sur tout ce qui a été dit jusqu'à t. Aveugle au temps."""
    nom = "majorité"

    def ingerer(self, enonces):
        self.idx = defaultdict(list)
        for e in enonces:
            self.idx[(e.sujet, e.relation)].append((e.epoque, e.objet))

    def resoudre(self, s, r, t):
        votes = Counter(o for ep, o in self.idx.get((s, r), []) if ep <= t)
        if not votes:
            return None, 0.0
        o, n = votes.most_common(1)[0]
        return o, n / sum(votes.values())


_VERBE = {"habite": "habite", "travaille": "travaille", "dirige": "dirigée", "naissance": "né"}
_tok = lambda s: set(re.findall(r"\w+", s.lower()))


class MotsCles(Systeme):
    """Témoin 3 — recherche par recouvrement de mots, comme un RAG naïf.
    Lit le texte, pas la structure ; ne comprend ni synonymes ni temps."""
    nom = "mots-clés"

    def ingerer(self, enonces):
        self.docs = [(_tok(e.texte), e) for e in enonces]

    def resoudre(self, s, r, t):
        nom_tok = _tok(s)
        req = nom_tok | {_VERBE[r], "époque", str(t)}
        best, score = None, -1
        for toks, e in self.docs:
            if not nom_tok <= toks:              # le sujet doit apparaître
                continue
            sc = len(req & toks)
            if sc > score:
                best, score = e, sc
        return (best.objet, 1.0) if best else (None, 0.0)


class Plafond(Systeme):
    """PAS un témoin — le plafond atteignable.
    Filtre bayésien avant-arrière sur la chaîne temporelle de chaque fait, avec les VRAIS
    paramètres du monde (fiabilité et retard des sources, taux de changement, domaines),
    qu'aucun vrai système ne connaît. Par construction, rien ne fait mieux en moyenne.
    S'il échoue lui-même, le monde est trop bruité : c'est l'instrument qui est faux."""
    nom = "plafond (triche)"

    def __init__(self, monde):
        self.src = {s.nom: s for s in monde.sources}
        self.dom, self.taux, self.E = monde.domaines, monde.taux, monde.n_epoques
        self.sosie, self.p_sosie = monde.sosie or {}, monde.p_sosie
        self.menteur = monde.menteur[:2] if monde.menteur else None   # (nom, part ciblée) — pas les cibles
        self.coalition = set(monde.coalition) if monde.coalition else None
        self.cache = {}

    def ingerer(self, enonces):
        self.idx = defaultdict(list)
        hist = defaultdict(list)                 # (source, sujet, relation) -> [(époque, objet)]
        for e in enonces:
            hist[(e.source, e.sujet, e.relation)].append((e.epoque, e.objet))
        for e in enonces:
            src = self.src[e.source]
            orig = None                          # ce que l'origine avait affirmé en dernier
            if src.copie:
                avant = [x for x in hist[(src.copie, e.sujet, e.relation)] if x[0] <= e.epoque]
                orig = max(avant)[1] if avant else None
            self.idx[(e.sujet, e.relation)].append(
                (max(0, e.epoque - src.retard), src.f(e.relation), e.objet,
                 src.taux_copie if orig is not None else 0.0, orig, e.source))

    def _avant_arriere(self, r, obs):
        """Filtre avant-arrière exact. Renvoie (croyance par époque, log-vraisemblance des énoncés)."""
        D, p = self.dom[r], self.taux[r]
        K = len(D)
        pos = {v: i for i, v in enumerate(D)}
        em = [[1.0] * K for _ in range(self.E)]
        logL = 0.0
        for eff, f, o, c, orig, _ in obs:
            j = pos[o]
            if self.p_sosie:                     # P(o | v) quand on se trompe vers le sosie de v
                ss, ps = self.sosie[r], self.p_sosie
                vr = [f if i == j else (1 - f) * (ps if ss[D[i]] == o else (1 - ps) / (K - 2))
                      for i in range(K)]
            else:
                autre = (1 - f) / (K - 1)
                vr = [f if i == j else autre for i in range(K)]
            base = c if o == orig else 0.0       # vraisemblance de mélange : copie ou témoignage
            ligne = [x * (base + (1 - c) * y) for x, y in zip(em[eff], vr)]
            mx = max(ligne)
            em[eff] = [x / mx for x in ligne]
            logL += math.log(mx)

        def transite(a):
            tot = sum(a)
            return [x * (1 - p) + (tot - x) * p / (K - 1) for x in a]

        a0 = [em[0][i] / K for i in range(K)]
        z = sum(a0); logL += math.log(z)
        fw = [[x / z for x in a0]]
        for t in range(1, self.E):
            a = [x * y for x, y in zip(transite(fw[-1]), em[t])]
            z = sum(a); logL += math.log(z)
            fw.append([x / z for x in a])
        bw = [[1.0] * K for _ in range(self.E)]
        for t in range(self.E - 2, -1, -1):
            b = transite([x * y for x, y in zip(bw[t + 1], em[t + 1])])
            zb = sum(b)
            bw[t] = [x / zb for x in b]
        post = []
        for t in range(self.E):
            q = [x * y for x, y in zip(fw[t], bw[t])]
            zq = sum(q)
            post.append([x / zq for x in q])
        return post, logL

    def _posterieur(self, s, r):
        D, obs = self.dom[r], self.idx[(s, r)]
        post, logL = self._avant_arriere(r, obs)
        if self.menteur and r in ("habite", "travaille", "dirige"):
            nom, q = self.menteur
            coal = self.coalition or {nom}       # ceux qui mentent ensemble sur les cibles
            dits = {x[2] for x in obs if x[5] in coal}
            if len(dits) == 1:                   # un mensonge constant reste possible
                sans, logL0 = self._avant_arriere(r, [x for x in obs if x[5] not in coal])
                logL0 += math.log(1.0 / (len(D) - 1))  # la valeur mentie, tirée une fois
                lA, lB = math.log(1 - q) + logL, math.log(q) + logL0
                m = max(lA, lB)
                wA, wB = math.exp(lA - m), math.exp(lB - m)
                wA, wB = wA / (wA + wB), wB / (wA + wB)
                post = [[wA * x + wB * y for x, y in zip(pa, pb)] for pa, pb in zip(post, sans)]
        return D, post

    def _croyance(self, s, r, t):
        if (s, r) not in self.cache:
            self.cache[(s, r)] = self._posterieur(s, r)
        D, post = self.cache[(s, r)]
        return D, post[t]

    def resoudre(self, s, r, t):
        if not self.idx.get((s, r)):
            return None, 0.0
        D, p = self._croyance(s, r, t)
        i = max(range(len(D)), key=lambda k: p[k])
        return D[i], p[i]

    def repondre(self, q):
        """Chaînes : on somme sur toutes les valeurs intermédiaires (optimal), au lieu de
        choisir la plus probable puis de continuer (optimal saut par saut seulement)."""
        if len(q.chaine) != 2:
            return super().repondre(q)
        r1, r2 = q.chaine
        if not self.idx.get((q.sujet, r1)):
            return None, 0.0
        D1, p1 = self._croyance(q.sujet, r1, q.epoque)
        final = defaultdict(float)
        for x, px in zip(D1, p1):
            if px < 1e-6:
                continue
            D2, p2 = self._croyance(x, r2, q.epoque)        # sans énoncé : croyance uniforme
            for y, py in zip(D2, p2):
                final[y] += px * py
        y = max(final, key=final.get)
        return y, final[y]
