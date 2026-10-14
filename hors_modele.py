"""
hors_modele.py — un monde où CHAQUE hypothèse des organes de GrandNexus est fausse, en même temps, sans coalition.

Hypothèses des organes                → ce que fait ce monde
- changements sans mémoire (Markov)   → on revient souvent à son ancienne adresse
- changements indépendants            → les emplois changent par vagues (restructurations aux époques 4 et 8)
- retard fixe par source              → Le Registre a un retard variable, de 0 à 2 époques, énoncé par énoncé
- fiabilité constante                 → La Gazette se dégrade à mi-parcours (0,90 puis 0,55)
- erreurs uniformes ou par sosie      → Radio Quartier se trompe vers deux valeurs « fétiches » par relation
- copie de la dernière valeur         → Le Forum recopie Radio Quartier avec un délai de 0 à 2 époques
Aucun organe n'est modifié pour ce monde : c'est le but.
"""
import random

from monde import Enonce, GABARITS, _SYLL


class MondeHM:
    pass


def generer_hm(graine, n_p=80, n_o=24, n_q=6, E=12):
    rng = random.Random(f"hors_modele|{graine}")
    pris = set()

    def frais(k):
        while True:
            x = "".join(rng.choice(_SYLL) for _ in range(k)).capitalize()
            if x not in pris:
                pris.add(x)
                return x
    P = [f"{frais(2)} {frais(3)}" for _ in range(n_p)]
    O = [f"Maison {frais(3)}" for _ in range(n_o)]
    Q = [frais(2) for _ in range(n_q)]
    A = [str(a) for a in range(1950, 2006)]
    dom = {"habite": Q, "travaille": O, "dirige": P, "naissance": A}
    V = {}
    for p in P:                                   # domicile : on revient souvent à l'adresse précédente
        h, prec = [rng.choice(Q)], None
        for t in range(1, E):
            cur = h[-1]
            if rng.random() < 0.12:
                nouv = prec if (prec and rng.random() < 0.5) else rng.choice([x for x in Q if x != cur])
                prec = cur
                h.append(nouv)
            else:
                h.append(cur)
        V[(p, "habite")] = h
        V[(p, "naissance")] = [rng.choice(A)] * E
    poste = {p: rng.choice(O) for p in P}       # emploi : faible dérive + vagues de restructuration
    W = {p: [] for p in P}
    for t in range(E):
        if t > 0:
            for p in P:
                if rng.random() < 0.05:
                    poste[p] = rng.choice([x for x in O if x != poste[p]])
            if t in (4, 8):
                o = rng.choice(O)
                for p in P:
                    if poste[p] == o and rng.random() < 0.4:
                        poste[p] = rng.choice([x for x in O if x != o])
        for p in P:
            W[p].append(poste[p])
    for p in P:
        V[(p, "travaille")] = W[p]
    for o in O:
        d = [rng.choice(P)]
        for t in range(1, E):
            d.append(rng.choice(P) if rng.random() < 0.06 else d[-1])
        V[(o, "dirige")] = d
    discretes = set(rng.sample(P, n_p // 6))
    fetiches = {r: rng.sample(dom[r], 2) for r in dom}
    COUV = {"Le Registre": 0.25, "La Gazette": 0.30, "Radio Quartier": 0.30, "Le Forum": 0.35}
    enonces, radio = [], {}

    def faux(r, vrai):
        return rng.choice([x for x in dom[r] if x != vrai])
    for t in range(E):
        for src in ("Le Registre", "La Gazette", "Radio Quartier", "Le Forum"):
            for (s, r), serie in V.items():
                if rng.random() >= COUV[src] or (r == "habite" and s in discretes):
                    continue
                if src == "Le Registre":
                    vrai = serie[max(0, t - rng.randint(0, 2))]
                    o = vrai if rng.random() < 0.92 else faux(r, vrai)
                elif src == "La Gazette":
                    f = 0.90 if t <= 5 else 0.55
                    o = serie[t] if rng.random() < f else faux(r, serie[t])
                elif src == "Radio Quartier":
                    if rng.random() < 0.75:
                        o = serie[t]
                    else:
                        cand = [x for x in fetiches[r] if x != serie[t]]
                        o = rng.choice(cand) if cand else faux(r, serie[t])
                    radio.setdefault((s, r), []).append((t, o))
                else:
                    d = rng.randint(0, 2)
                    anciens = [o_ for (tt, o_) in radio.get((s, r), []) if tt <= t - d]
                    if anciens and rng.random() < 0.6:
                        o = anciens[-1]
                    else:
                        o = serie[t] if rng.random() < 0.6 else faux(r, serie[t])
                texte = f"[époque {t} · {src}] " + rng.choice(GABARITS[r]).format(s=s, o=o)
                enonces.append(Enonce(len(enonces), t, src, s, r, o, texte))
    m = MondeHM()
    m.enonces, m.verite, m.n_epoques, m.domaines = enonces, V, E, dom
    return m
