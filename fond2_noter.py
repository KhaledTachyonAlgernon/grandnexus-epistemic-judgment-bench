"""H-FondRéplication : GrandNexus sur deux mondes neufs, puis notation. Usage : python fond2_noter.py gn <monde> <t> | bilan"""
import glob, json, os, random, sys
from monde import generer, Question
from meprise import Meprise

V = json.load(open("fond2_verite.json"))
bas = lambda v: " ".join(str(v).split()).lower()
os.makedirs("fond2_db", exist_ok=True)


def gn(w, t):
    fic = f"fond2_db/gn_{w}_{t}.json"
    if os.path.exists(fic):
        return json.load(open(fic))
    m = generer(w, V[w]["graine"], **V[w]["kw"])
    o = Meprise(); o.ingerer([e for e in m.enonces if e.epoque <= t])
    out = []
    for x in V[w]["points"][str(t)]:
        q = Question(x["id"], x["type"], x["sujet"], tuple(x["chaine"]), x["epoque"], x["texte"], x["attendu"])
        try:
            r, c = o.repondre(q)
        except (KeyError, IndexError):
            r, c = None, 0.0
        out.append({"id": x["id"], "rep": r, "conf": c})
    json.dump(out, open(fic, "w"), ensure_ascii=False)
    return out


if __name__ == "__main__" and sys.argv[1] == "gn":
    gn(sys.argv[2], int(sys.argv[3])); print("jugé", sys.argv[2], sys.argv[3])


def lignes_monde(w):
    arms = {"GrandNexus": {}, "Opus-fenêtre": {}, "Opus-recherche": {}}
    bad = 0
    for col, nom in (("fenetre", "Opus-fenêtre"), ("recherche", "Opus-recherche")):
        for f in glob.glob(f"fond2_db/page/{col}/{w}_*.json"):
            d = json.load(open(f)); bad += bool(d.get("tronque")) + (d.get("reponses") is None)
            for r in d.get("reponses") or []:
                v = r.get("reponse")
                arms[nom][(d["t"], int(r["id"]))] = (None if v is None or bas(v) in ("inconnu", "") else " ".join(str(v).split()), float(r.get("confiance", 0) or 0))
    for t in (3, 7, 11):
        for x in gn(w, t):
            arms["GrandNexus"][(t, x["id"])] = (x["rep"], x["conf"])
    L = {}
    for nom, A in arms.items():
        for t in (3, 7, 11):
            for q in V[w]["points"][str(t)]:
                r, c = A.get((t, q["id"]), (None, 0.0)); att = q["attendu"]
                j = (r is None) if att is None else (r is not None and bas(r) == bas(att))
                b = None if att is None else ((c if r is not None else 0.0) - (r is not None and bas(r) == bas(att))) ** 2
                L.setdefault((nom, t), []).append((q["type"], int(j), b))
    return L, bad


def ic(d, rng):
    s = sorted(sum(d[rng.randrange(len(d))] for _ in d) / len(d) for _ in range(5000))
    return sum(d) / len(d), s[125], s[4874]


if __name__ == "__main__" and sys.argv[1] == "bilan":
    rng = random.Random(9); sortie = []
    P = lambda *a: (print(*a), sortie.append(" ".join(str(x) for x in a)))
    tous = {}
    for w in ("complice", "plausible"):
        L, bad = lignes_monde(w)
        P(f"\n== {w} (graine {V[w]['graine']}) — lots tronqués ou illisibles : {bad}")
        for t in (3, 7, 11):
            P("   t=%-2d " % t + "   ".join(f"{n} {sum(j for _, j, _ in L[(n, t)]) / len(L[(n, t)]):.0%} (Brier {sum(b for *_, b in L[(n, t)] if b is not None) / sum(1 for *_, b in L[(n, t)] if b is not None):.3f})" for n in ("GrandNexus", "Opus-fenêtre", "Opus-recherche")))
        g = L[("GrandNexus", 11)]
        hist = {n: sum(j for ty, j, _ in L[(n, 11)] if ty == "historique") / 30 for n in ("GrandNexus", "Opus-fenêtre", "Opus-recherche")}
        P("   t=11 historique : " + " ; ".join(f"{n} {v:.0%}" for n, v in hist.items()))
        verdict = []
        for adv in ("Opus-fenêtre", "Opus-recherche"):
            m_, lo, hi = ic([x[1] - y[1] for x, y in zip(g, L[(adv, 11)])], rng)
            P(f"   t=11 GrandNexus − {adv} : {m_:+.1%} [{lo:+.1%} ; {hi:+.1%}]")
            verdict.append((lo > 0, hi < 0))
            tous.setdefault(adv, []).extend(x[1] - y[1] for x, y in zip(g, L[(adv, 11)]))
        v = "APTE" if verdict[0][0] and verdict[1][0] else ("INAPTE sur l'exactitude" if verdict[1][1] else ("AVANTAGE LIMITÉ" if verdict[0][0] else "INDÉTERMINÉ"))
        P(f"   VERDICT ({w}) : {v}")
    sys.path.insert(0, ".")
    import fond_noter
    L83 = fond_noter.bilan.__globals__  # réutilise la notation de H-Fond
    import io, contextlib
    with contextlib.redirect_stdout(io.StringIO()):
        L0 = fond_noter.bilan()
    d83 = [x[1] - y[1] for x, y in zip(L0[("GrandNexus", 11)], L0[("Opus-recherche", 11)])]
    m_, lo, hi = ic(d83 + tous["Opus-recherche"], rng)
    P(f"\nTrois graines réunies (83, 84, 85), t=11, GrandNexus − Opus-recherche : {m_:+.1%} [{lo:+.1%} ; {hi:+.1%}]  (n = {len(d83) + len(tous['Opus-recherche'])})")
    open("fond2_db/bilan.txt", "w").write("\n".join(sortie))
