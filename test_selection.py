"""H-Sélection (H85-H90) : où vérifier sous budget ? Graines neuves 61-63, cache versionné, par tranches."""
import json, os, random, sys, time
from cache import repertoire
from evaluer import _bootstrap
from monde import generer, Enonce
from meprise import Meprise

ANCRE, GRAINES, MONDES, BUDGET = "L'Ancre", (61, 62, 63), ("complice", "menteur", "plausible"), 10
BRAS = ("aleatoire", "signaux", "oracle")
CACHE = repertoire("selection")
fin = time.time() + float(sys.argv[1] if len(sys.argv) > 1 else 170)


def suite(cle):
    return f"{cle[0]}|{cle[1]}"


def reponses(o, m):
    out = {}
    for f in o.croyance:
        for t in range(m.n_epoques):
            post = o.croyance[f][t]
            i = max(range(len(post)), key=post.__getitem__)
            out[f"{suite(f)}|{t}"] = [int(o.dom[f[1]][i] == m.verite[f][t]), post[i]]
    return out


def groupes(o):
    """Fusion des copieurs avec leur source (par transitivité) : une voix répétée reste une voix."""
    racine = {}
    def r(s):
        while s in o.parent:
            s = o.parent[s][0]
            if s in racine:
                break
        return s
    return {s: r(s) for s in o.f}


def score_signaux(o, m):
    grp = groupes(o)
    rep = {f: [o.dom[f[1]][max(range(len(o.croyance[f][t])), key=o.croyance[f][t].__getitem__)]
               for t in range(m.n_epoques)] for f in o.croyance}
    scores = {}
    for f in o.croyance:
        par = {}
        for ep, src, ob in o.obs[f]:
            t = max(0, ep - o.L[src])
            par.setdefault(src, []).append(ob != rep[f][t])
        contre = sorted(s for s, v in par.items() if sum(v) / len(v) > 0.5)
        effectifs = sorted({grp[s] for s in contre})
        incert = sum(1 - max(p) for p in o.croyance[f]) / m.n_epoques
        scores[f] = (len(effectifs), incert, contre, effectifs)
    return scores


def charge_base(w, g):
    fic = f"{CACHE}/{w}_{g}_base.json"
    if os.path.exists(fic):
        return json.load(open(fic))
    if time.time() > fin:
        print(f"… à suivre ({w}, graine {g}, base)"); sys.exit(0)
    m = generer(w, g)
    o = Meprise(fixes={ANCRE: 0.99}); o.ingerer(m.enonces)
    rep = reponses(o, m)
    faits = sorted(o.croyance)
    sel = {"aleatoire": random.Random(f"aleatoire|{w}|{g}").sample(faits, BUDGET)}
    sc = score_signaux(o, m)
    sel["signaux"] = sorted(faits, key=lambda f: (-sc[f][0], -sc[f][1], suite(f)))[:BUDGET]
    faux = {f: sum(1 - rep[f"{suite(f)}|{t}"][0] for t in range(m.n_epoques)) for f in faits}
    sel["oracle"] = sorted(faits, key=lambda f: (-faux[f], suite(f)))[:BUDGET]
    sel["incertitude"] = sorted(faits, key=lambda f: (-sc[f][1], suite(f)))[:BUDGET]
    res = {"rep": rep, "sel": {k: [list(f) for f in v] for k, v in sel.items()},
           "purete": {k: sum(faux[f] for f in v) / (BUDGET * m.n_epoques) for k, v in sel.items()},
           "justif": [{"fait": suite(f), "contredit_par": sc[f][2], "voix_effectives": sc[f][3],
                       "incertitude": round(sc[f][1], 3)} for f in sel["signaux"]]}
    json.dump(res, open(fic, "w"))
    return res


def charge_bras(w, g, bras):
    fic = f"{CACHE}/{w}_{g}_{bras}.json"
    if os.path.exists(fic):
        return json.load(open(fic))
    base = charge_base(w, g)
    if time.time() > fin:
        print(f"… à suivre ({w}, graine {g}, {bras})"); sys.exit(0)
    m = generer(w, g)
    c = list(m.enonces)
    for f in base["sel"][bras]:
        cle = tuple(f)
        for t in range(m.n_epoques):
            c.append(Enonce(len(c), t, ANCRE, cle[0], cle[1], m.verite[cle][t], ""))
    o = Meprise(fixes={ANCRE: 0.99}); o.ingerer(c)
    res = {"rep": reponses(o, m)}
    json.dump(res, open(fic, "w"))
    return res


if __name__ == "__main__":
    B = {(w, g): charge_base(w, g) for w in MONDES for g in GRAINES}
    A = {(w, g, b): charge_bras(w, g, b) for w in MONDES for g in GRAINES for b in BRAS}
    print(f"BILAN — H-Sélection, graines 61-63, budget {BUDGET} faits par graine — cache {CACHE}\n")


    def deltas(w, b):
        """Par fait : changement net d'époques justes, et dégâts (juste → faux) si le fait n'est pas vérifié."""
        out = []
        for g in GRAINES:
            base, arm = B[(w, g)]["rep"], A[(w, g, b)]["rep"]
            verif = {suite(tuple(f)) for f in B[(w, g)]["sel"][b]}
            par = {}
            for k, (j0, _) in base.items():
                fait = k.rsplit("|", 1)[0]
                j1 = arm[k][0]
                d = par.setdefault(fait, [0, 0, fait in verif])
                d[0] += j1 - j0
                if not d[2] and j0 == 1 and j1 == 0:
                    d[1] += 1
            out += [[f"{g}|{f}", v[0], v[1], v[2]] for f, v in par.items()]
        return out


    norm = BUDGET * len(GRAINES)
    for w in MONDES:
        print(f"── {w}")
        D = {b: deltas(w, b) for b in BRAS}
        for b in BRAS:
            net = sum(x[1] for x in D[b]) / norm
            direct = sum(x[1] for x in D[b] if x[3]) / norm
            degats = sum(x[2] for x in D[b]) / norm
            pur = sum(B[(w, g)]["purete"][b] for g in GRAINES) / len(GRAINES)
            print(f"   {b:<10} nettes/vérif {net:+.2f}  (directes {direct:+.2f}, indirectes {net - direct:+.2f})"
                  f"   dégâts/vérif {degats:.2f}   pureté {pur:.0%}")
        pu = sum(B[(w, g)]["purete"]["incertitude"] for g in GRAINES) / len(GRAINES)
        print(f"   incertitude seule (descriptif) : pureté {pu:.0%}")
        n = len(D["signaux"])
        for a, b in (("signaux", "aleatoire"), ("oracle", "signaux")):
            m_, h, k = _bootstrap([x[1] - y[1] for x, y in zip(D[a], D[b])], [x[0] for x in D[a]], tirages=2000)
            print(f"   {a} − {b} : {m_ * n / norm:+.2f} ± {h * n / norm:.2f} corrections nettes par vérification")
    print("\nExemple de justification enregistrée au moment du choix (complice, graine 61, premier fait SIGNAUX) :")
    print("  ", B[("complice", 61)]["justif"][0])
