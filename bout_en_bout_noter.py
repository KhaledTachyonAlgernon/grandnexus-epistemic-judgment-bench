"""H-BoutEnBout (H132-H137) : notation des cinq montages. Usage : python bout_en_bout_noter.py <montage> | bilan"""
import glob, json, os, random, sys
from monde import generer, Enonce
from meprise import Meprise

V = json.load(open("bout_en_bout_verite.json"))
DEP = {d["id"]: d for d in V["depeches"]}
M = generer("complice", 82, n_personnes=30, n_orgs=6, n_questions=60)
RELS = {"habite", "travaille", "dirige", "naissance"}
esp = lambda v: " ".join(str(v).split())
bas = lambda v: esp(v).lower()


def lectures(col):
    out = {}
    for f in glob.glob(f"bout_db/{col}/*.json"):
        for p in json.load(open(f))["lectures"] or []:
            out[int(p["id"])] = [(esp(x.get("sujet", "")), bas(x.get("relation", "")), esp(x.get("objet", "")))
                                 for x in p.get("faits", []) if bas(x.get("relation", "")) in RELS]
    return out


def corpus(montage):
    if montage == "D":
        return list(M.enonces)
    LC, LR = lectures("lecture_complete"), lectures("lecture_rapide")
    out = []
    for i, d in sorted(DEP.items()):
        if montage == "B":
            faits, src = LC.get(i, []), d["source"]
        elif montage == "C":
            faits, src = LR.get(i, []), d["source"]
        else:
            canal = d["canal_E"]
            faits = (LC if canal == "complet" else LR).get(i, [])
            src = f"{d['source']} · {canal}"
        for s, r, o in faits:
            out.append(Enonce(len(out), d["epoque"], src, s, r, o, ""))
    return out


def juger(montage):
    fic = f"bout_db/gn_{montage}.json"
    if os.path.exists(fic):
        return json.load(open(fic))
    o = Meprise(); o.ingerer(corpus(montage))
    rep = []
    for q in M.questions:
        try:
            r, c = o.repondre(q)
        except KeyError:
            r, c = None, 0.0
        rep.append({"id": q.id, "rep": r, "conf": c})
    res = {"rep": rep, "f": o.f}
    json.dump(res, open(fic, "w"), ensure_ascii=False)
    return res


def perception(col):
    L = lectures(col)
    tp = fp = fn = pieges = lus = 0
    for i, d in DEP.items():
        vrais = {(bas(s), r, bas(o)) for s, r, o in d["faits"]}
        lu = {(bas(s), r, bas(o)) for s, r, o in L.get(i, [])}
        tp += len(vrais & lu); fp += len(lu - vrais); fn += len(vrais - lu)
        if d["piege"]:
            pieges += 1; s, r, o = d["piege"]; lus += (bas(s), r, bas(o)) in lu
    return tp / max(1, tp + fp), tp / max(1, tp + fn), lus, pieges


if __name__ == "__main__":
    if sys.argv[1] != "bilan":
        juger(sys.argv[1]); print("montage", sys.argv[1], "jugé"); sys.exit(0)
    temoin = {}
    for f in glob.glob("bout_db/temoin/*.json"):
        for r in json.load(open(f))["reponses"]:
            temoin[int(r["id"])] = (None if bas(r.get("reponse", "")) in ("inconnu", "") else esp(r["reponse"]), float(r.get("confiance", 0) or 0))
    arms = {"A Opus seul": {q: temoin.get(q, (None, 0.0)) for q in range(len(M.questions))}}
    for k, nom in (("B", "B Opus lit, GN juge"), ("C", "C petit lit, GN juge"), ("D", "D GN, faits parfaits"), ("E", "E hybride à canaux")):
        arms[nom] = {x["id"]: (x["rep"], x["conf"]) for x in juger(k)["rep"]}
    lignes = {}
    print(f"{'montage':<24}{'exactitude':>11}{'actuel':>8}{'hist.':>7}{'2 sauts':>9}{'sans rép.':>11}{'Brier':>8}")
    for nom, A in arms.items():
        L = []
        for q in M.questions:
            r, c = A.get(q.id, (None, 0.0))
            att = q.attendu
            j = (r is None) if att is None else (r is not None and bas(r) == bas(att))
            b = None if att is None else ((c if r is not None else 0.0) - (r is not None and bas(r) == bas(att))) ** 2
            L.append((q.type, int(j), b))
        lignes[nom] = L
        par = lambda t: sum(j for ty, j, _ in L if ty == t) / max(1, sum(1 for ty, _, _ in L if ty == t))
        B_ = [b for _, _, b in L if b is not None]
        print(f"{nom:<24}{sum(j for _, j, _ in L) / len(L):>10.0%}{par('actuel'):>8.0%}{par('historique'):>7.0%}{par('deux_sauts'):>9.0%}"
              f"{par('sans_reponse'):>11.0%}{sum(B_) / len(B_):>8.3f}")
    rng = random.Random(1)
    a, b = lignes["A Opus seul"], lignes["B Opus lit, GN juge"]
    d = [y[1] - x[1] for x, y in zip(a, b)]
    s = sorted(sum(d[rng.randrange(len(d))] for _ in d) / len(d) for _ in range(4000))
    print(f"\nB − A exactitude : {sum(d) / len(d):+.0%} [{s[100]:+.0%} ; {s[3899]:+.0%}]")
    db_ = [y[2] - x[2] for x, y in zip(a, b) if x[2] is not None]
    s = sorted(sum(db_[rng.randrange(len(db_))] for _ in db_) / len(db_) for _ in range(4000))
    print(f"B − A Brier : {sum(db_) / len(db_):+.3f} [{s[100]:+.3f} ; {s[3899]:+.3f}]")
    for col, nom in (("lecture_complete", "B lecteur par défaut"), ("lecture_rapide", "C petit modèle")):
        p, r, l, n = perception(col)
        print(f"Perception {nom:<22} précision {p:.1%} ; rappel {r:.1%} ; pièges lus {l}/{n}")
    f = juger("E")["f"]
    print("\nE — fiabilité apprise par canal :")
    for s in sorted({d["source"] for d in DEP.values()}):
        fc, fr = f.get(f"{s} · complet"), f.get(f"{s} · rapide")
        print(f"   {s:<15} lu par Opus {fc:.3f} ; lu par le petit modèle {fr:.3f} ; {'petit < Opus' if fr < fc else 'petit ≥ Opus'}")
