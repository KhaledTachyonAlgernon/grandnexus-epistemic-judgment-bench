"""H-Fond : GrandNexus aux trois points de contrôle, puis notation des trois concurrents. Usage : python fond_noter.py gn <t> | bilan"""
import glob, json, os, random, sys
from monde import generer, Question
from meprise import Meprise

M = generer("complice", 83)
P = {int(t): qs for t, qs in json.load(open("fond_verite.json"))["points"].items()}
bas = lambda v: " ".join(str(v).split()).lower()


def gn(t):
    fic = f"fond_db/gn_{t}.json"
    os.makedirs("fond_db", exist_ok=True)
    if os.path.exists(fic):
        return json.load(open(fic))
    o = Meprise(); o.ingerer([e for e in M.enonces if e.epoque <= t])
    out = []
    for x in P[t]:
        q = Question(x["id"], x["type"], x["sujet"], tuple(x["chaine"]), x["epoque"], x["texte"], x["attendu"])
        try:
            r, c = o.repondre(q)
        except (KeyError, IndexError):
            r, c = None, 0.0
        out.append({"id": x["id"], "rep": r, "conf": c})
    json.dump(out, open(fic, "w"), ensure_ascii=False)
    return out


if __name__ == "__main__" and sys.argv[1] == "gn":
    gn(int(sys.argv[2])); print("GrandNexus jugé au point", sys.argv[2])


def bilan():
    arms = {"GrandNexus": {}, "Opus-fenêtre": {}, "Opus-recherche": {}}
    integ = []
    for col, nom in (("fenetre", "Opus-fenêtre"), ("recherche", "Opus-recherche")):
        for f in glob.glob(f"fond_db/page/{col}/*.json"):
            d = json.load(open(f))
            integ.append((col, os.path.basename(f), bool(d.get("tronque")), d.get("reponses") is None, d.get("niveau")))
            for r in d.get("reponses") or []:
                v = r.get("reponse")
                arms[nom][(d["t"], int(r["id"]))] = (None if v is None or bas(v) in ("inconnu", "") else " ".join(str(v).split()), float(r.get("confiance", 0) or 0))
    print("Intégrité : tronqués", sum(x[2] for x in integ), "; illisibles", sum(x[3] for x in integ), "; niveaux", {x[4] for x in integ})
    for t in (3, 7, 11):
        for x in gn(t):
            arms["GrandNexus"][(t, x["id"])] = (x["rep"], x["conf"])
    L = {}
    for nom, A in arms.items():
        for t in (3, 7, 11):
            for q in P[t]:
                r, c = A.get((t, q["id"]), (None, 0.0))
                att = q["attendu"]
                j = (r is None) if att is None else (r is not None and bas(r) == bas(att))
                b = None if att is None else ((c if r is not None else 0.0) - (r is not None and bas(r) == bas(att))) ** 2
                L.setdefault((nom, t), []).append((q["type"], int(j), b, q["id"]))
    print(f"\n{'':<16}{'point':>6}{'exactitude':>12}{'actuel':>8}{'hist.':>7}{'2 sauts':>9}{'sans rép.':>11}{'Brier':>8}")
    for t in (3, 7, 11):
        for nom in arms:
            E = L[(nom, t)]
            par = lambda ty: sum(j for tt, j, _, _ in E if tt == ty) / max(1, sum(1 for tt, *_ in E if tt == ty))
            B = [b for _, _, b, _ in E if b is not None]
            print(f"{nom:<16}{t:>6}{sum(j for _, j, _, _ in E) / len(E):>11.0%}{par('actuel'):>8.0%}{par('historique'):>7.0%}{par('deux_sauts'):>9.0%}{par('sans_reponse'):>11.0%}{sum(B) / len(B):>8.3f}")
        print()
    rng = random.Random(7)
    def ic(d):
        s = sorted(sum(d[rng.randrange(len(d))] for _ in d) / len(d) for _ in range(5000))
        return sum(d) / len(d), s[125], s[4874]
    g = L[("GrandNexus", 11)]
    for adv in ("Opus-fenêtre", "Opus-recherche"):
        a = L[(adv, 11)]
        m_, lo, hi = ic([x[1] - y[1] for x, y in zip(g, a)])
        mb, lob, hib = ic([x[2] - y[2] for x, y in zip(g, a) if x[2] is not None])
        print(f"t = 11 : GrandNexus − {adv:<15} exactitude {m_:+.1%} [{lo:+.1%} ; {hi:+.1%}]   Brier {mb:+.3f} [{lob:+.3f} ; {hib:+.3f}]")
    return L


if __name__ == "__main__" and sys.argv[1] == "bilan":
    bilan()
