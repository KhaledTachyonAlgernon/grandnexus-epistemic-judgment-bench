"""Évaluation des lecteurs de paragraphes au niveau du fait. Usage : python eval_paragraphes.py dev | test"""
import json, sys
from monde import generer
from accueil_paragraphes import LecteurParagraphes

S = {s["id"]: s for s in json.load(open("structurel_verite.json"))}
LECT = {}
for w in ("complice", "plausible"):
    m = generer(w, 81, n_personnes=40, n_orgs=8)
    LECT[w] = LecteurParagraphes(sorted({s for (s, r) in m.verite if r == "habite"}),
                                 sorted({s for (s, r) in m.verite if r == "dirige"}), sorted(m.domaines["habite"]))


def noter(items, lecture, montrer=False):
    """lecture(item) -> liste de (s, r, o, confiance). Renvoie un enregistrement par fait lu ou attendu."""
    lignes, pieges, pieges_lus = [], 0, 0
    for x in items:
        sc = S[x["id"]]
        vrais = {tuple(f) for f in sc["faits"]}
        lus = lecture(x)
        lus_set = {(a, b, str(c)) for a, b, c, *_ in lus}
        for a, b, c, *reste in lus:
            lignes.append({"id": x["id"], "lu": 1, "juste": int((a, b, str(c)) in vrais), "conf": reste[0] if reste else None,
                           "inconnu": bool(sc["inconnu"] and sc["inconnu"] in (a, c))})
        for f in vrais:
            if f not in lus_set:
                lignes.append({"id": x["id"], "lu": 0, "juste": 0, "conf": None, "inconnu": bool(sc["inconnu"] and sc["inconnu"] in (f[0], f[2]))})
        if sc["piege"]:
            pieges += 1
            pieges_lus += tuple(sc["piege"]) in lus_set
        if montrer and lus_set != vrais:
            print(f"   #{x['id']} {sc['procedes']} « {x['texte']} »\n      manquants {sorted(vrais - lus_set)}\n      en trop  {sorted(lus_set - vrais)}")
    return lignes, pieges, pieges_lus


def resume(lignes, pieges, pieges_lus, titre):
    lus = [l for l in lignes if l["lu"]]
    tp = sum(l["juste"] for l in lus)
    attendus = sum(1 for l in lignes if l["juste"] or not l["lu"])
    p, r = tp / max(1, len(lus)), tp / max(1, attendus)
    print(f"{titre} : précision {p:.0%} ; rappel {r:.0%} ; F1 {2 * p * r / max(1e-9, p + r):.0%} ; pièges de correction lus "
          f"{pieges_lus}/{pieges}")
    att_conn = [l for l in lignes if (l["juste"] or not l["lu"]) and not l["inconnu"]]
    print(f"   rappel hors personnes inconnues : {sum(l['juste'] for l in att_conn) / max(1, len(att_conn)):.0%}")
    for lo, hi in ((0.95, 1.01), (0.75, 0.95), (0.0, 0.75)):
        E = [l for l in lus if l["conf"] is not None and lo <= l["conf"] < hi]
        if E:
            print(f"   confiance {lo:.2f}-{min(hi, 1):.2f} : n = {len(E):>3}, justes {sum(l['juste'] for l in E) / len(E):.0%}")
    return p, r


def lecture_regles(x):
    return [(s, r, o, c) for s, r, o, c, d in LECT[S[x["id"]]["monde"]].lire(x["texte"])]


if __name__ == "__main__":
    if sys.argv[1] == "dev":
        items = [y for i in range(4) for y in json.load(open(f"structurel_dev/structurel/lot_{i}.json"))["items"]]
        resume(*noter(items, lecture_regles, montrer=len(sys.argv) > 2), "DÉVELOPPEMENT — lecteur à règles")


def norm(v):
    return " ".join(str(v).split()).lower()


if __name__ == "__main__" and sys.argv[1] == "test":
    items = [y for i in range(4, 8) for y in json.load(open(f"structurel_test/structurel/lot_{i}.json"))["items"]]
    LLM = {}
    for i in range(4, 8):
        d = json.load(open(f"structurel_test/lecture/lot_{i}.json"))
        assert not d.get("tronque") and d["lectures"], i
        for p in d["lectures"]:
            LLM[int(p["id"])] = [(f.get("sujet", ""), f.get("relation", ""), f.get("objet", ""), float(f.get("confiance", 0) or 0))
                                 for f in p.get("faits", [])]
    print(f"{len(items)} paragraphes de test ; lectures LLM pour {len(LLM)} paragraphes\n")
    # normalisation identique pour les deux lecteurs
    S_norm = {k: dict(v, faits=[[norm(x) for x in f] for f in v["faits"]], piege=[norm(x) for x in v["piege"]] if v["piege"] else None,
                      inconnu=norm(v["inconnu"]) if v["inconnu"] else None) for k, v in S.items()}
    S.clear(); S.update(S_norm)
    regles = lambda x: [(norm(s), r, norm(o), c) for s, r, o, c, d in LECT[S[x["id"]]["monde"]].lire(x["texte"])]
    llm = lambda x: [(norm(s), norm(r), norm(o), c) for s, r, o, c in LLM.get(x["id"], [])]
    R1 = noter(items, regles); p1, r1 = resume(*R1, "TEST — lecteur à règles")
    print()
    R2 = noter(items, llm); p2, r2 = resume(*R2, "TEST — lecteur LLM")
    # complémentarité : faits vrais trouvés par l'un et pas par l'autre
    vrais_par = {x["id"]: {tuple(f) for f in S[x["id"]]["faits"]} for x in items}
    lus1 = {x["id"]: {(a, b, c) for a, b, c, _ in regles(x)} for x in items}
    lus2 = {x["id"]: {(a, b, c) for a, b, c, _ in llm(x)} for x in items}
    seul1 = sum(len((vrais_par[i] & lus1[i]) - lus2[i]) for i in vrais_par)
    seul2 = sum(len((vrais_par[i] & lus2[i]) - lus1[i]) for i in vrais_par)
    deux = sum(len(vrais_par[i] & lus1[i] & lus2[i]) for i in vrais_par)
    aucun = sum(len(vrais_par[i] - lus1[i] - lus2[i]) for i in vrais_par)
    print(f"\nFaits vrais : trouvés par les deux {deux} ; par les règles seules {seul1} ; par le LLM seul {seul2} ; par aucun {aucun}")
    faux2 = [(i, f) for i in vrais_par for f in lus2[i] - vrais_par[i]]
    print(f"Faits en trop du LLM ({len(faux2)}) :")
    for i, f in faux2[:12]:
        print(f"   #{i} {f}   (vrais : {sorted(vrais_par[i])})")
