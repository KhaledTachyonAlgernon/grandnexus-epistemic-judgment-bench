"""H-Boucle (H109-H114) : choisir → vérifier → ancrer → réviser → rechoisir. Graines neuves 76-78, cache versionné."""
import json, os, random, sys, time
from cache import repertoire
from evaluer import _bootstrap
from monde import generer, Enonce
from meprise import Meprise
from test_selection import score_signaux

ANCRE, MONDES, GRAINES, B = "L'Ancre", ("mixte", "plausible"), (76, 77, 78), 10
POLITIQUES = ("contestee", "incertitude", "deux_files", "aleatoire")
CACHE = repertoire("boucle")
fin = time.time() + float(sys.argv[1] if len(sys.argv) > 1 else 170)


def entrainer(m, ancres):
    c = list(m.enonces)
    for cle in sorted(ancres):
        for t in range(m.n_epoques):
            c.append(Enonce(len(c), t, ANCRE, cle[0], cle[1], m.verite[cle][t], ""))
    o = Meprise(fixes={ANCRE: 0.99}); o.ingerer(c)
    return o


def etat(o, m):
    juste = {}
    for f in o.croyance:
        for t in range(m.n_epoques):
            post = o.croyance[f][t]
            juste[f"{f[0]}|{f[1]}|{t}"] = int(o.dom[f[1]][max(range(len(post)), key=post.__getitem__)] == m.verite[f][t])
    sc = score_signaux(o, m)
    conf = {f: sum(max(p) for p in o.croyance[f]) / m.n_epoques for f in o.croyance}
    return juste, {f: sc[f][0] for f in o.croyance}, conf


def choisir(pol, o, contest, conf, exclus, rng):
    faits = [f for f in sorted(o.croyance) if f not in exclus]
    file_c = sorted([f for f in faits if contest[f] >= 2], key=lambda f: (-contest[f], conf[f], f))
    file_u = sorted(faits, key=lambda f: (conf[f], f))
    if pol == "contestee":
        return file_c[:B]
    if pol == "incertitude":
        return file_u[:B]
    if pol == "aleatoire":
        return rng.sample(faits, B)
    pris = file_c[:B // 2]
    return pris + [f for f in file_u if f not in pris][:B - len(pris)]


def charge(w, g, pol):
    fic = f"{CACHE}/{w}_{g}_{pol}.json"
    if os.path.exists(fic):
        return json.load(open(fic))
    base_fic = f"{CACHE}/{w}_{g}_base.json"
    m = generer(w, g)
    if os.path.exists(base_fic):
        base = json.load(open(base_fic))
    else:
        if time.time() > fin:
            print(f"… à suivre ({w}, graine {g}, base)"); sys.exit(0)
        o0 = entrainer(m, set())
        j0, c0, f0 = etat(o0, m)
        base = {"juste": j0, "contest": {f"{k[0]}|{k[1]}": v for k, v in c0.items()},
                "conf": {f"{k[0]}|{k[1]}": v for k, v in f0.items()}}
        json.dump(base, open(base_fic, "w"))
    if time.time() > fin:
        print(f"… à suivre ({w}, graine {g}, {pol})"); sys.exit(0)
    rng = random.Random(f"boucle|{w}|{g}|{pol}")
    cle = lambda s: tuple(s.split("|"))
    o_ref = type("E", (), {})()
    o_ref.croyance = {cle(k): None for k in base["conf"]}
    contest = {cle(k): v for k, v in base["contest"].items()}
    conf = {cle(k): v for k, v in base["conf"].items()}
    tours, ancres = [], set()
    for tour in (1, 2):
        sel = choisir(pol, o_ref, contest, conf, ancres, rng)
        ancres |= set(sel)
        o = entrainer(m, ancres)
        juste, c, f_ = etat(o, m)
        tours.append({"selection": [f"{a}|{b}" for a, b in sel], "juste": juste})
        o_ref, contest, conf = o, c, f_
        if time.time() > fin and tour == 1:
            pass
    res = {"tours": tours}
    json.dump(res, open(fic, "w"))
    return res


def par_fait(base_j, apres_j, verifies):
    out = {}
    for k, j0 in base_j.items():
        f = k.rsplit("|", 1)[0]
        d = out.setdefault(f, [0, 0])
        d[0] += apres_j[k] - j0
        if f not in verifies and j0 == 1 and apres_j[k] == 0:
            d[1] += 1
    return out


if __name__ == "__main__":
    for w in MONDES:
        for g in GRAINES:
            for pol in POLITIQUES:
                charge(w, g, pol)
    print(f"BILAN — H-Boucle, graines 76-78, 2 tours × {B} faits — cache {CACHE}\n")
    for w in MONDES:
        print(f"── {w}")
        D, n_verif, T2 = {}, {}, {}
        for pol in POLITIQUES:
            vals, nv, t2 = [], 0, []
            for g in GRAINES:
                base = json.load(open(f"{CACHE}/{w}_{g}_base.json"))
                r = charge(w, g, pol)
                verifies = set(r["tours"][0]["selection"]) | set(r["tours"][1]["selection"])
                nv += len(verifies)
                pf = par_fait(base["juste"], r["tours"][1]["juste"], verifies)
                p1 = par_fait(base["juste"], r["tours"][0]["juste"], set(r["tours"][0]["selection"]))
                vals += [[f"{g}|{f}", v[0], v[1], p1.get(f, [0, 0])[0]] for f, v in sorted(pf.items())]
            D[pol], n_verif[pol] = vals, nv
            net = sum(x[1] for x in vals) / max(1, nv)
            deg = sum(x[2] for x in vals) / max(1, nv)
            t2 = (sum(x[1] for x in vals) - sum(x[3] for x in vals)) / max(1, nv)
            print(f"   {pol:<12} vérifications {nv:>3}  nettes/vérif {net:+.2f}  dégâts/vérif {deg:.2f}  apport du tour 2 /vérif {t2:+.2f}")
        for a, b in (("contestee", "aleatoire"), ("contestee", "incertitude"), ("deux_files", "incertitude")):
            A_, Bv = D[a], D[b]
            assert [x[0] for x in A_] == [x[0] for x in Bv]
            # comparaison par vérification : chaque bras normalisé par ses propres vérifications
            m_, h, k = _bootstrap([x[1] / max(1, n_verif[a]) - y[1] / max(1, n_verif[b]) for x, y in zip(A_, Bv)],
                                  [x[0] for x in A_], tirages=1000)
            print(f"   {a} − {b} : {m_ * len(A_):+.2f} ± {h * len(A_):.2f} corrections nettes par vérification")
        if w == "mixte":
            v = D["contestee"]
            m_, h, k = _bootstrap([x[1] - x[3] for x in v], [x[0] for x in v], tirages=1000)
            print(f"   H114 apport du tour 2 (contestée) : {m_ * len(v):+.1f} ± {h * len(v):.1f} corrections nettes au total")
