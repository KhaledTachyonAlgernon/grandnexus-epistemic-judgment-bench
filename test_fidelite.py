"""H-Fidélité (H91-H94) : une justification courte est-elle la vraie raison ? Graines neuves 64-66, cache versionné.
Fidélité LOCALE : paramètres appris fixés ; on recalcule exactement la décision sur le fait, énoncés retirés ou gardés."""
import json, math, os, random, sys, time
from cache import repertoire
from monde import generer
from meprise import Meprise

MONDES, GRAINES, N_REP, KS = ("facile", "echo", "menteur", "plausible", "complice"), (64, 65, 66), 60, (1, 3, 5)
CACHE = repertoire("fidelite")
fin = time.time() + float(sys.argv[1] if len(sys.argv) > 1 else 170)


def reponse(o, cle, t, obs):
    """Décision exacte de l'organe sur ce fait, avec une liste d'énoncés donnée (paramètres fixés)."""
    sauve_obs, sauve_susp = o.obs[cle], o.susp.get(cle)
    o.obs[cle] = obs
    try:
        post = o._avant_arriere(cle)[0][t]
    finally:
        o.obs[cle] = sauve_obs
        if sauve_susp is None:
            o.susp.pop(cle, None)
        else:
            o.susp[cle] = sauve_susp
    return max(range(len(post)), key=post.__getitem__)


def contributions(o, cle, t, a, b):
    r = cle[1]
    K, p = len(o.dom[r]), o.p[r]
    out = []
    for i, (ep, src, ob) in enumerate(o.obs[cle]):
        v = o._vraisemblance(cle, ep, src, ob, K, o.pos[r][ob])
        eff = max(0, ep - o.L[src])
        c = (math.log(max(v[a], 1e-12)) - math.log(max(v[b], 1e-12))) * (1 - p) ** abs(eff - t)
        out.append((c, i))
    return out


def charge(w, g):
    fic = f"{CACHE}/{w}_{g}.json"
    if os.path.exists(fic):
        return json.load(open(fic))
    if time.time() > fin:
        print(f"… à suivre ({w}, graine {g})"); sys.exit(0)
    m = generer(w, g)
    o = Meprise(); o.ingerer(m.enonces)
    rng = random.Random(f"fidelite|{w}|{g}")
    paires = rng.sample([(f, t) for f in sorted(o.croyance) for t in range(m.n_epoques)], N_REP)
    lignes = []
    for cle, t in paires:
        post = o.croyance[cle][t]
        ordre = sorted(range(len(post)), key=lambda i: -post[i])
        a, b = ordre[0], ordre[1]
        tous = list(o.obs[cle])
        contrib = contributions(o, cle, t, a, b)
        pos = sorted([x for x in contrib if x[0] > 0], key=lambda x: -x[0])
        lig = {"fait": f"{cle[0]}|{cle[1]}", "t": t, "juste": int(o.dom[cle[1]][a] == m.verite[cle][t]),
               "n_pos": len(pos), "n": len(tous)}
        for k in KS:
            kk = min(k, len(pos))
            cites = {i for _, i in pos[:kk]}
            hasard = set(rng.sample([i for _, i in pos], kk)) if kk else set()
            for nom, S in (("cite", cites), ("hasard", hasard)):
                garde = [s for i, s in enumerate(tous) if i in S]
                retire = [s for i, s in enumerate(tous) if i not in S]
                lig[f"suff_{nom}_{k}"] = int(reponse(o, cle, t, garde) == a)
                lig[f"nec_{nom}_{k}"] = int(reponse(o, cle, t, retire) != a)
        lignes.append(lig)
    json.dump(lignes, open(fic, "w"))
    return lignes


if __name__ == "__main__":
    R = {(w, g): charge(w, g) for w in MONDES for g in GRAINES}
    print(f"BILAN — H-Fidélité, graines 64-66, {N_REP} réponses par monde et graine — cache {CACHE}\n")
    taux = lambda L, k: sum(x[k] for x in L) / len(L)
    moy = {"suff": [], "nec": []}
    print(f"{'monde':<10}{'n':>5}{'suff. citée':>14}{'suff. hasard':>14}{'néc. citée':>13}{'néc. hasard':>13}   (k = 3)")
    for w in MONDES:
        L = [x for g in GRAINES for x in R[(w, g)]]
        s_c, s_h, n_c, n_h = (taux(L, f"{a}_{b}_3") for a, b in (("suff", "cite"), ("suff", "hasard"), ("nec", "cite"), ("nec", "hasard")))
        moy["suff"].append(s_c); moy["nec"].append(n_c)
        print(f"{w:<10}{len(L):>5}{s_c:>13.0%}{s_h:>14.0%}{n_c:>13.0%}{n_h:>13.0%}")
    print(f"\nmoyenne sur les mondes : suffisance citée {sum(moy['suff'])/5:.0%} ; nécessité citée {sum(moy['nec'])/5:.0%}")
    TOUT = [x for v in R.values() for x in v]
    print("\nDescriptif, tous mondes :")
    for k in KS:
        print(f"   k = {k} : suff. citée {taux(TOUT, f'suff_cite_{k}'):.0%} / hasard {taux(TOUT, f'suff_hasard_{k}'):.0%} ; "
              f"néc. citée {taux(TOUT, f'nec_cite_{k}'):.0%} / hasard {taux(TOUT, f'nec_hasard_{k}'):.0%}")
    F = [x for x in TOUT if not x["juste"]]
    print(f"   réponses FAUSSES (n = {len(F)}) : suff. citée(3) {taux(F, 'suff_cite_3'):.0%} ; néc. citée(3) {taux(F, 'nec_cite_3'):.0%}")
    print(f"   énoncés par réponse : médiane {sorted(x['n'] for x in TOUT)[len(TOUT)//2]} ; positifs médiane {sorted(x['n_pos'] for x in TOUT)[len(TOUT)//2]}")
