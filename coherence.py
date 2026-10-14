"""
coherence3.py — Cohérence v3 : la règle de v2 (auto-contradiction, désaveu par les sources propres) généralisée à trois familles.
  C1  « o dirigée par p »   et « p travaille pour x ≠ o »                       (même source, époques voisines)
  C2  « o dirigée par p »   et « p habite h », h ≠ siège établi de o
  C3  « a habite h1 »       et « b habite h2 ≠ h1 », a et b conjoints établis
Pour chaque auto-contradiction, on écarte le côté que les sources PROPRES (sans contradiction sur la même paire de faits) désavouent,
seulement si la décision est NETTE : au moins N_PROPRES_MIN témoignages propres de chaque côté, écart d'accord ≥ ECART_MIN.
"""
from meprise import Meprise

SEUIL_ETABLI = 0.9
N_PROPRES_MIN, ECART_MIN = 1, 0            # resserrement essayé en développement (2, 1/3) : gain divisé par deux, perte honnête inchangée → retiré


class Coherence3(Meprise):
    nom = "Cohérence v3"

    def __init__(self, *a, contraintes=("C1", "C2", "C3"), **k):
        super().__init__(*a, **k)
        self.contraintes = tuple(contraintes)

    def _etabli(self, cle, t):
        if cle not in self.croyance:
            return None
        u = self.croyance[cle][t]; i = max(range(len(u)), key=u.__getitem__)
        return self.dom[cle[1]][i] if u[i] >= SEUIL_ETABLI else None

    def ingerer(self, enonces):
        super().ingerer(enonces)
        self.croyance_meprise = {cle: [list(v) for v in serie] for cle, serie in self.croyance.items()}
        self.dom_meprise = {r: list(d) for r, d in self.dom.items()}
        self.ecartes = []
        if not self.contraintes:
            return
        par = {}                                   # (source, sujet, relation) -> [(t, valeur, id)]
        par_fait = {}                              # (sujet, relation) -> [(source, t, valeur)]
        for e in enonces:
            if e.source not in self.L:
                continue
            t = min(max(0, e.epoque - self.L[e.source]), self.E - 1)
            par.setdefault((e.source, e.sujet, e.relation), []).append((t, e.objet, e.id))
            par_fait.setdefault((e.sujet, e.relation), []).append((e.source, t, e.objet))
        sources = {k[0] for k in par}
        contradictions = []                        # (source, cle_paire, (faitA, valA, tA), (faitB, valB, tB))
        for src in sources:
            for (s0, s, r), L in par.items():
                if s0 != src:
                    continue
                if r == "dirige":
                    o = s
                    for t1, p, _ in L:
                        if "C1" in self.contraintes:
                            for t2, x, _ in par.get((src, p, "travaille"), []):
                                if abs(t1 - t2) <= 1 and x != o:
                                    contradictions.append((src, ("C1", o, p), ((o, "dirige"), p, t1), ((p, "travaille"), x, t2)))
                        if "C2" in self.contraintes:
                            for t2, h, _ in par.get((src, p, "habite"), []):
                                k = self._etabli((o, "siege"), t1)
                                if abs(t1 - t2) <= 1 and k is not None and h != k:
                                    contradictions.append((src, ("C2", o, p), ((o, "dirige"), p, t1), ((p, "habite"), h, t2)))
                if r == "habite" and "C3" in self.contraintes:
                    a = s
                    for t1, h1, _ in L:
                        b = self._etabli((a, "conjoint"), t1)
                        if b is None or not a < b:
                            continue
                        for t2, h2, _ in par.get((src, b, "habite"), []):
                            if abs(t1 - t2) <= 1 and h1 != h2:
                                contradictions.append((src, ("C3", a, b), ((a, "habite"), h1, t1), ((b, "habite"), h2, t2)))
        contradicteurs = {}
        for src, k, _, _ in contradictions:
            contradicteurs.setdefault(k, set()).add(src)
        suspects = set()
        for src, k, (fA, vA, tA), (fB, vB, tB) in contradictions:
            fen = (tA, tB)
            def accord(f, v):
                L = [x == v for s3, t3, x in par_fait.get(f, []) if s3 != src and s3 not in contradicteurs[k] and min(abs(t3 - u) for u in fen) <= 1]
                return sum(L) / len(L) if len(L) >= N_PROPRES_MIN else None
            aA, aB = accord(fA, vA), accord(fB, vB)
            if aA is None or aB is None:
                continue
            if abs(aA - aB) < ECART_MIN:
                continue
            if aA < aB:
                suspects.add((src, fA, vA))
            elif aB < aA:
                suspects.add((src, fB, vB))
        ids = {i for (src, f, v) in suspects for _, x, i in par.get((src, f[0], f[1]), []) if x == v}
        self.ecartes = sorted(suspects)
        if ids:
            super().ingerer([e for e in enonces if e.id not in ids])


class Coherence2(Coherence3):
    """Compatibilité : la contrainte C1 seule (version adoptée le 14 octobre 2026 ; v3 lui est identique sur C1)."""
    def __init__(self, *a, contraintes=("C1",), **k):
        super().__init__(*a, contraintes=contraintes, **k)
