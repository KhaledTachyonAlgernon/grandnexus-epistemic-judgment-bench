"""Même données que reel_collecte.py (instantané au 1er de chaque mois), obtenues par l'historique des révisions. Reprise par article."""
import json, os, sys, time, urllib.request, urllib.parse
from concurrent.futures import ThreadPoolExecutor
from reel_collecte import extraire, CLES, MOIS, UA

FIC = "reel_pages.json"


def api(lang, params):
    url = f"https://{lang}.wikipedia.org/w/api.php?" + urllib.parse.urlencode(dict(params, action="query", prop="revisions", format="json", formatversion=2, rvslots="main", rvsection=0))
    for essai in range(4):
        try:
            return json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read())
        except Exception:
            time.sleep(3 + 4 * essai)
    return None


def page(qid, lang, titre):
    revs = []
    r = api(lang, {"titles": titre, "rvlimit": 1, "rvstart": "2019-07-01T00:00:00Z", "rvdir": "older", "rvprop": "timestamp|content"})
    if r is None:
        return None
    p = r["query"]["pages"][0]
    revs += [(x["timestamp"], extraire(x["slots"]["main"].get("content", ""), lang)) for x in p.get("revisions", [])]
    cont = {}
    while True:
        r = api(lang, dict({"titles": titre, "rvlimit": 50, "rvstart": "2019-07-01T00:00:00Z", "rvend": "2021-06-01T00:00:00Z",
                            "rvdir": "newer", "rvprop": "timestamp|content"}, **cont))
        if r is None:
            return None
        revs += [(x["timestamp"], extraire(x["slots"]["main"].get("content", ""), lang)) for x in r["query"]["pages"][0].get("revisions", [])]
        if "continue" not in r:
            break
        cont = {"rvcontinue": r["continue"]["rvcontinue"]}
    revs.sort()
    snap = []
    for m in MOIS:
        avant = [v for ts, v in revs if ts < m + "T00:00:00Z"]
        snap.append(avant[-1] if avant else None)
    return {"qid": qid, "lang": lang, "n_revisions": len(revs), "mensuel": snap}


if __name__ == "__main__":
    budget = time.time() + float(sys.argv[1] if len(sys.argv) > 1 else 240)
    C = json.load(open("reel_communes.json"))
    fait = json.load(open(FIC)) if os.path.exists(FIC) else []
    vus = {(x["qid"], x["lang"]) for x in fait}
    taches = [(c["qid"], l, c["titres"][l]) for c in C for l in CLES if l in c["titres"] and (c["qid"], l) not in vus]
    print("articles à faire :", len(taches))
    with ThreadPoolExecutor(6) as ex:
        for k in range(0, len(taches), 24):
            if time.time() > budget:
                break
            fait += [x for x in ex.map(lambda t: page(*t), taches[k:k + 24]) if x]
            json.dump(fait, open(FIC, "w"), ensure_ascii=False)
    print("articles collectés :", len(fait), "/", sum(len([l for l in CLES if l in c["titres"]]) for c in C))
