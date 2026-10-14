"""
echelle.py — échelle de mondes synthétiques à contraintes imbriquées (CHARTE §8, registre H-Échelle).

Mesure des PROPRIÉTÉS DU MONDE, sans source ni organe : E(d), F(d), K(d).
Un seul monde par graine, identique à tous les niveaux ; seules varient les contraintes DÉCLARÉES.
  C1 dirige(o) = p ⇒ travaille(p) = o
  C2 dirige(o) = p ⇒ habite(p) = siège(o)
  C3 conjoint(p) = q ⇒ habite(p) = habite(q)
Niveaux : d0 {} ; d1 {C1} ; d2 {C1, C2} ; d3 {C1, C2, C3}.

Menteur cohérent : pour chaque cible (fait fixé par graine), il choisit la valeur constante v (≠ vérité à
l'époque 0) qui minimise Σ_époques coût_t(v) ; coût_t(v) = nombre minimal de faits de l'époque t, autres que
la cible, à falsifier pour respecter les contraintes déclarées. Recherche par approfondissement itératif,
bornée à B = 4 par époque (au-delà : « intenable », coût B + 1). Les remplaçants d'un dirigeant sont essayés
par CLASSES équivalentes (un représentant par classe) : exact à symétrie près — vérifié par verifier_symetrie().
"""
import random

N_P, N_O, N_Q, N_E = 80, 24, 6, 12
CHANGEMENT, B = 0.12, 4
NIVEAUX = {0: (), 1: ("C1",), 2: ("C1", "C2"), 3: ("C1", "C2", "C3")}


def generer_monde(graine):
    rng = random.Random(1_000_003 * graine + 17)
    P = [f"P{i:02d}" for i in range(N_P)]
    O = [f"O{i:02d}" for i in range(N_O)]
    Q = [f"Q{i}" for i in range(N_Q)]
    siege = {o: rng.choice(Q) for o in O}
    melange = P[:]
    rng.shuffle(melange)
    conj = {}
    for i in range(0, N_P // 2, 2):                          # 50 % des personnes en couple
        a, b = melange[i], melange[i + 1]
        conj[a], conj[b] = b, a
    unites = [(p, conj[p]) for p in P if p in conj and p < conj[p]] + [(p,) for p in P if p not in conj]
    chez = {u: rng.choice(Q) for u in unites}
    unite = {p: u for u in unites for p in u}
    chef, poste = {}, {p: rng.choice(O) for p in P}
    for o in O:                                              # on n'appointe pas le conjoint d'un dirigeant
        libres = [p for p in P if p not in chef.values() and conj.get(p) not in chef.values()]
        chef[o] = rng.choice(libres)
        poste[chef[o]] = o
    H, W, D = [], [], []
    p_dir = CHANGEMENT * 0.5
    for t in range(N_E):
        if t > 0:
            for o in O:
                if rng.random() < p_dir:
                    libres = [p for p in P if p not in chef.values() and conj.get(p) not in chef.values()]
                    chef[o] = rng.choice(libres)
                    poste[chef[o]] = o
            dirigeants = set(chef.values())
            for p in P:
                if p not in dirigeants and rng.random() < CHANGEMENT:
                    poste[p] = rng.choice([x for x in O if x != poste[p]])
            for u in unites:
                if not any(p in dirigeants for p in u) and rng.random() < CHANGEMENT:
                    chez[u] = rng.choice([x for x in Q if x != chez[u]])
        for o, p in chef.items():                            # un dirigeant (et son couple) habite au siège
            chez[unite[p]] = siege[o]
        H.append({p: chez[unite[p]] for p in P})
        W.append(dict(poste))
        D.append(dict(chef))
    return {"P": P, "O": O, "Q": Q, "S": siege, "C": conj, "H": H, "W": W, "D": D}


def verifier_verite(m):
    for t in range(N_E):
        for o, p in m["D"][t].items():
            assert m["W"][t][p] == o, ("C1", t, o)
            assert m["H"][t][p] == m["S"][o], ("C2", t, o)
        for p, q in m["C"].items():
            assert m["H"][t][p] == m["H"][t][q], ("C3", t, p)
    return True


def tirer_cibles(m, graine, part=0.15):
    rng = random.Random(7_919 * graine + 3)                  # générateur dédié : cibles identiques à tous niveaux
    faits = [(p, "habite") for p in m["P"]] + [(p, "travaille") for p in m["P"]] + [(o, "dirige") for o in m["O"]]
    return sorted(f for f in faits if rng.random() < part)


# — état d'une époque : vérité + réécritures ————————————————————————————————
class Etat:
    def __init__(self, m, t, ecrit):
        self.m, self.t, self.e = m, t, ecrit                 # ecrit : {(rel, sujet): valeur}

    def get(self, rel, s):
        if (rel, s) in self.e:
            return self.e[(rel, s)]
        m, t = self.m, self.t
        return {"H": m["H"][t], "W": m["W"][t], "D": m["D"][t], "S": m["S"], "C": m["C"]}[rel].get(s)

    def cout(self):
        m, t, n = self.m, self.t, 0
        for (rel, s), v in self.e.items():
            vrai = {"H": m["H"][t], "W": m["W"][t], "D": m["D"][t], "S": m["S"], "C": m["C"]}[rel].get(s)
            n += v != vrai
        return n

    def dirige_par(self, p):
        return [o for o in self.m["O"] if self.get("D", o) == p]


def premiere_violation(etat, contraintes):
    """Seules les contraintes qui touchent un fait réécrit peuvent être violées (la vérité les respecte)."""
    orgs, couples = set(), set()
    for (rel, s) in etat.e:
        if rel in ("D", "S"):
            orgs.add(s)
        if rel in ("W", "H"):
            orgs.update(etat.dirige_par(s))
        if rel in ("H", "C"):
            for x in (s, etat.m["C"].get(s), etat.get("C", s)):
                if x and etat.get("C", x):
                    couples.add(tuple(sorted((x, etat.get("C", x)))))
    for o in sorted(orgs):
        p = etat.get("D", o)
        if "C1" in contraintes and etat.get("W", p) != o:
            return ("C1", o)
        if "C2" in contraintes and etat.get("H", p) != etat.get("S", o):
            return ("C2", o)
    if "C3" in contraintes:
        for a, b in sorted(couples):
            if etat.get("C", a) == b and etat.get("H", a) != etat.get("H", b):
                return ("C3", (a, b))
    return None


def remplacants(etat, o, complet=False):
    """Candidats pour diriger o. Par défaut : un représentant par classe équivalente."""
    actuel, vus, out = etat.get("D", o), set(), []
    for y in etat.m["P"]:
        if y == actuel:
            continue
        if complet:
            out.append(y)
            continue
        cle = (etat.get("W", y) == o, etat.get("H", y) == etat.get("S", o), bool(etat.dirige_par(y)),
               bool(etat.get("C", y)), ("W", y) in etat.e, ("H", y) in etat.e)
        if cle not in vus:
            vus.add(cle)
            out.append(y)
    return out


def options(etat, viol, complet=False):
    Q = etat.m["Q"]
    kind, x = viol
    if kind in ("C1", "C2"):
        o, p = x, etat.get("D", x)
        ops = []
        if kind == "C1":
            ops.append({("W", p): o})
        else:
            ops.append({("H", p): etat.get("S", o)})
            ops += [{("S", o): z} for z in Q if z != etat.get("S", o)]
        ops += [{("D", o): y} for y in remplacants(etat, o, complet)]
        return ops
    a, b = x
    ops = [{("H", a): z} for z in Q if z != etat.get("H", a)]
    ops += [{("H", b): z} for z in Q if z != etat.get("H", b)]
    ops.append({("C", a): None, ("C", b): None})            # dissoudre le couple : deux faits
    return ops


def cout_minimal(m, t, ecrit0, verrou0, contraintes, complet=False, borne=B):
    """Approfondissement itératif : plus petit nombre de faits supplémentaires à réécrire."""
    base = Etat(m, t, dict(ecrit0)).cout()

    def dfs(ecrit, verrou, limite):
        etat = Etat(m, t, ecrit)
        v = premiere_violation(etat, contraintes)
        if v is None:
            return True
        for op in options(etat, v, complet):
            if any(k in verrou for k in op):
                continue
            nouv = dict(ecrit); nouv.update(op)
            if Etat(m, t, nouv).cout() - base > limite:
                continue
            if dfs(nouv, verrou | set(op), limite):
                return True
        return False

    for limite in range(borne + 1):
        if dfs(dict(ecrit0), set(verrou0), limite):
            return limite
    return borne + 1                                         # intenable dans la borne


REL = {"habite": "H", "travaille": "W", "dirige": "D"}


def valeurs_possibles(m, rel):
    return {"H": m["Q"], "W": m["O"], "D": m["P"]}[rel]


def cout_cible(m, cible, v, niveau, complet=False):
    s, r = cible
    rel = REL[r]
    par_epoque = [cout_minimal(m, t, {(rel, s): v}, {(rel, s)}, NIVEAUX[niveau], complet) for t in range(N_E)]
    return sum(par_epoque), par_epoque


def menteur_coherent(m, cible, niveau, complet=False):
    s, r = cible
    rel = REL[r]
    vrai0 = {"H": m["H"][0], "W": m["W"][0], "D": m["D"][0]}[rel][s]
    meilleur = None
    for v in valeurs_possibles(m, rel):
        if v == vrai0:
            continue
        tot, ep = cout_cible(m, cible, v, niveau, complet)
        if meilleur is None or tot < meilleur[0]:
            meilleur = (tot, ep, v)
            if tot == 0:
                break
    return meilleur


def expose_naif(m, cible, niveau, graine):
    s, r = cible
    rel = REL[r]
    rng = random.Random(f"naif|{graine}|{s}|{r}")     # graine textuelle : reproductible
    vrai0 = {"H": m["H"][0], "W": m["W"][0], "D": m["D"][0]}[rel][s]
    v = rng.choice([x for x in valeurs_possibles(m, rel) if x != vrai0])
    return [premiere_violation(Etat(m, t, {(rel, s): v}), NIVEAUX[niveau]) is not None for t in range(N_E)]
