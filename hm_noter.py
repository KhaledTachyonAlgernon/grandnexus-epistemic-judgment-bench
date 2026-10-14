"""H-HorsModèle : GrandNexus scellé, puis notation contre Opus-recherche. Usage : python hm_noter.py gn | bilan"""
import glob, json, os, random, sys
from hors_modele import generer_hm
from monde import Question
from meprise import Meprise

V = json.load(open("hm_verite.json"))["hors_modele"]
bas = lambda v: " ".join(str(v).split()).lower()
os.makedirs("hm_db", exist_ok=True)
M = generer_hm(86)


def gn(t):
    fic = f"hm_db/gn_{t}.json"
    if os.path.exists(fic):
        return json.load(open(fic))
    o = Meprise(); o.ingerer([e for e in M.enonces if e.epoque <= t])
    out = []
    for x in V["points"][str(t)]:
        q = Question(x["id"], x["type"], x["sujet"], tuple(x["chaine"]), x["epoque"], x["texte"], x["attendu"])
        try:
            r, c = o.repondre(q)
        except (KeyError, IndexError):
            r, c = None, 0.0
        out.append({"id": x["id"], "rep": r, "conf": c})
    json.dump(out, open(fic, "w"), ensure_ascii=False)
    return out


if __name__ == "__main__" and sys.argv[1] == "gn":
    for t in (3, 7, 11):
        gn(t)
    print("GrandNexus scellé aux trois points")

if __name__ == "__main__" and sys.argv[1] == "bilan":
    opus, bad = {}, 0
    for f in glob.glob("hm_db/page/recherche/*.json"):
        d = json.load(open(f)); bad += bool(d.get("tronque")) + (d.get("reponses") is None)
        for r in d.get("reponses") or []:
            v = r.get("reponse")
            opus[(d["t"], int(r["id"]))] = (None if v is None or bas(v) in ("inconnu", "") else " ".join(str(v).split()), float(r.get("confiance", 0) or 0))
    print("lots tronqués ou illisibles :", bad)
    rng = random.Random(11)
    for t in (3, 7, 11):
        G, O = [], []
        for x, q in zip(gn(t), V["points"][str(t)]):
            att = q["attendu"]
            for L, (r, c) in ((G, (x["rep"], x["conf"])), (O, opus.get((t, q["id"]), (None, 0.0)))):
                j = (r is None) if att is None else (r is not None and bas(r) == bas(att))
                b = None if att is None else ((c if r is not None else 0.0) - (r is not None and bas(r) == bas(att))) ** 2
                L.append((q["type"], int(j), b))
        bg = [b for *_, b in G if b is not None]; bo = [b for *_, b in O if b is not None]
        par = lambda L, ty: sum(j for tt, j, _ in L if tt == ty) / max(1, sum(1 for tt, *_ in L if tt == ty))
        print(f"t={t:<2} GrandNexus {sum(j for _, j, _ in G) / len(G):.0%} (Brier {sum(bg) / len(bg):.3f})   Opus-recherche {sum(j for _, j, _ in O) / len(O):.0%} (Brier {sum(bo) / len(bo):.3f})"
              + "   par type GN/Opus : " + " ".join(f"{ty[:5]} {par(G, ty):.0%}/{par(O, ty):.0%}" for ty in ("actuel", "historique", "deux_sauts", "sans_reponse")))
        if t == 11:
            d = [g[1] - o[1] for g, o in zip(G, O)]
            s = sorted(sum(d[rng.randrange(len(d))] for _ in d) / len(d) for _ in range(5000))
            m_, lo, hi = sum(d) / len(d), s[125], s[4874]
            v = "ROBUSTE HORS MODÈLE" if lo > 0 else ("BATTU HORS MODÈLE" if hi < 0 else "AVANTAGE DÉPENDANT DU MODÈLE")
            print(f"t=11 GrandNexus − Opus-recherche : {m_:+.1%} [{lo:+.1%} ; {hi:+.1%}]  →  VERDICT : {v}")
