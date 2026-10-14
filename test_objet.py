"""H-ObjetRéponse (H105-H108), graines neuves 73-75, cache versionné."""
import json, os, random, sys, time
from cache import repertoire
from monde import generer
from meprise import Meprise
from reponse import objet_reponse, en_clair, SEUIL_PREUVES

MONDES, GRAINES = ("mixte", "complice", "plausible"), (73, 74, 75)
CACHE = repertoire("objet")
fin = time.time() + float(sys.argv[1] if len(sys.argv) > 1 else 170)


def charge(w, g):
    fic = f"{CACHE}/{w}_{g}.json"
    if os.path.exists(fic):
        return json.load(open(fic))
    if time.time() > fin:
        print(f"… à suivre ({w}, graine {g})"); sys.exit(0)
    m = generer(w, g)
    o = Meprise(); o.ingerer(m.enonces)
    cibles = m.menteur[2] if m.menteur else set()
    out, exemple = [], None
    for cle in sorted(o.croyance):
        for t in range(m.n_epoques):
            ob = objet_reponse(o, cle, t)
            faux = int(ob["valeur"] != m.verite[cle][t])
            out.append({"fait": f"{g}|{cle[0]}|{cle[1]}", "faux": faux, "type": "coordination" if cle in cibles else "bruit",
                        "conf": ob["confiance"], "contest": ob["doute_contestation"]})
            if exemple is None and faux and cle in cibles and ob["motifs"]:
                exemple = en_clair(ob)
    json.dump({"rep": out, "exemple": exemple}, open(fic, "w"))
    return {"rep": out, "exemple": exemple}


def boot(L, f, tirages=500, graine=5):
    par = {}
    for x in L:
        par.setdefault(x["fait"], []).append(x)
    faits, rng, d = sorted(par), random.Random(graine), []
    for _ in range(tirages):
        v = f([x for k in (rng.choice(faits) for _ in faits) for x in par[k]])
        if v == v:
            d.append(v)
    d.sort()
    return d[int(0.025 * len(d))], d[int(0.975 * len(d)) - 1]


def part(E, cond, typ):
    S = [x for x in E if x["faux"] and cond(x)]
    T = [x for x in E if x["faux"]]
    if not S or not T:
        return float("nan")
    return sum(x["type"] == typ for x in S) / len(S) - sum(x["type"] == typ for x in T) / len(T)


def capture(L, politique, budget=0.10, graine=3):
    n, rng = round(budget * len(L)), random.Random(graine)
    if politique == "incertitude":
        pris = sorted(L, key=lambda x: (x["conf"], rng.random()))[:n]
    else:                                                  # moitié file contestée, moitié file peu sûre
        file_c = sorted([x for x in L if x["contest"] >= 2], key=lambda x: (-x["contest"], x["conf"], rng.random()))
        pris = file_c[:n // 2]
        deja = {id(x) for x in pris}
        reste = sorted([x for x in L if id(x) not in deja], key=lambda x: (x["conf"], rng.random()))
        pris += reste[:n - len(pris)]
    return sum(x["faux"] for x in pris) / max(1, sum(x["faux"] for x in L))


if __name__ == "__main__":
    R = {(w, g): charge(w, g) for w in MONDES for g in GRAINES}
    print(f"BILAN — H-ObjetRéponse, graines 73-75 — cache {CACHE}\n")
    contestee = lambda x: x["contest"] >= 2
    peu_seul = lambda x: x["contest"] < 2 and x["conf"] < SEUIL_PREUVES
    for w in MONDES:
        L = [x for g in GRAINES for x in R[(w, g)]["rep"]]
        F = [x for x in L if x["faux"]]
        nc = sum(x["type"] == "coordination" for x in F)
        motif = sum(1 for x in F if contestee(x) or x["conf"] < SEUIL_PREUVES)
        print(f"── {w} : {len(F)} erreurs ({nc} de coordination, {len(F) - nc} de bruit) ; portant au moins un motif : {motif / len(F):.0%}")
        Fc, Fp = [x for x in F if contestee(x)], [x for x in F if peu_seul(x)]
        if Fc:
            print(f"     motif « contestée » : {len(Fc)} erreurs, dont coordination {sum(x['type'] == 'coordination' for x in Fc) / len(Fc):.0%} (base {nc / len(F):.0%})")
        if Fp:
            print(f"     motif « peu de preuves » seul : {len(Fp)} erreurs, dont bruit {sum(x['type'] == 'bruit' for x in Fp) / len(Fp):.0%} (base {(len(F) - nc) / len(F):.0%})")
        print(f"     capture à 10 % : incertitude seule {capture(L, 'incertitude'):.0%} ; objet (deux files) {capture(L, 'objet'):.0%}")
        if w == "mixte":
            lo, hi = boot(L, lambda E: part(E, contestee, "coordination"))
            print(f"     H105 excès de coordination sous « contestée » : [{lo:+.0%} ; {hi:+.0%}]")
            lo, hi = boot(L, lambda E: part(E, peu_seul, "bruit"))
            print(f"     H106 excès de bruit sous « peu de preuves » seul : [{lo:+.0%} ; {hi:+.0%}]")
    print("\nExemple d'objet-réponse (mixte, graine 73, une erreur de coordination signalée) :")
    print(R[("mixte", 73)]["exemple"])
